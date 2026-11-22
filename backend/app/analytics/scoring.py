"""
PATHWAY AI - Multi-Dimensional Career Analytics, Scoring & Ranking Engine
Evaluates assessment sessions across:
1. 15 Universal Module Dimensions (M01 to M15)
2. Domain Technical and Profession-Specific Knowledge
3. Multi-Dimensional Career Compatibility Profiles (All 30 Careers)
4. Evidence Confidence Classification (high_confidence, moderate, more_evidence_needed)
5. 3-Part Indian Academic & Regulatory Eligibility Analysis
"""

import json
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from backend.app.models.entities import (
    AssessmentSession, StudentAnswer, Question, QuestionOption,
    Career, CareerSkill, Skill, AssessmentResult, CareerRecommendation,
    EducationDetail, CareerRequirement, AssessmentModule
)
from backend.app.analytics.career_mapping import CAREER_MAPPING_PROFILES, MODULE_DEFINITIONS

# Map module codes to their primary dimension key
MODULE_CODE_TO_DIMENSION = {m["code"]: m["primary_dimension"] for m in MODULE_DEFINITIONS}
DIMENSION_TO_MODULE_NAME = {m["primary_dimension"]: m["name"] for m in MODULE_DEFINITIONS}


def evaluate_assessment_session(db: Session, session_id: int) -> AssessmentResult:
    session = db.query(AssessmentSession).filter(AssessmentSession.id == session_id).first()
    if not session:
        raise ValueError(f"Assessment session {session_id} not found")

    answers = db.query(StudentAnswer).filter(StudentAnswer.session_id == session_id).all()

    # Dimension score buckets for all 15 dimensions
    dimension_scores: Dict[str, List[float]] = {
        m["primary_dimension"]: [] for m in MODULE_DEFINITIONS
    }
    
    # Specific skill scores
    skill_scores: Dict[str, List[float]] = {}
    
    # Track questions answered per career (for evidence verification)
    career_questions_answered: Dict[int, List[float]] = {}

    for ans in answers:
        q: Question = ans.question
        opt: QuestionOption = ans.selected_option
        if not q or not opt:
            continue

        # Compute question score (0 to 100)
        score = 0.0
        if q.scoring_type == "accuracy":
            score = 100.0 if opt.is_correct else 0.0
        elif q.scoring_type == "likert":
            # Likert 1 to 5 mapped to 20% to 100%
            score = min(100.0, max(20.0, opt.score_value * 20.0))
        elif q.scoring_type == "weighted":
            # Situational judgment weighted (0.0 to 1.0) -> (0 to 100)
            score = min(100.0, max(0.0, opt.score_value * 100.0))
        else:
            score = 100.0 if opt.is_correct else (opt.score_value * 100.0)

        # 1. Attribute to 15-module dimensions
        dim_key = None
        if q.module and q.module.primary_dimension:
            dim_key = q.module.primary_dimension
        elif q.module_id:
            mod = db.query(AssessmentModule).filter(AssessmentModule.id == q.module_id).first()
            if mod:
                dim_key = mod.primary_dimension

        # Fallback mapping based on category/skill if module not explicitly linked
        if not dim_key:
            cat_dim_map = {
                "aptitude": "numerical_aptitude",
                "logical": "logical_reasoning",
                "verbal": "verbal_ability",
                "critical": "critical_thinking",
                "spatial": "spatial_abstract",
                "creativity": "creativity",
                "science": "science_tech",
                "commerce": "commerce_finance",
                "technical": "computational_thinking",
                "interest": "interest_discovery",
                "personality": "work_preferences",
                "communication": "communication",
                "situational": "situational_judgement",
                "learning": "learning_style",
                "career_interest": "career_exploration"
            }
            dim_key = cat_dim_map.get(q.category, "numerical_aptitude")

        if dim_key in dimension_scores:
            dimension_scores[dim_key].append(score)

        # 2. Attribute to specific skill name
        skill_name = q.skill_name or "Analytical Reasoning"
        if skill_name not in skill_scores:
            skill_scores[skill_name] = []
        skill_scores[skill_name].append(score)

        # 3. Track career-specific question performance
        if q.career_id:
            if q.career_id not in career_questions_answered:
                career_questions_answered[q.career_id] = []
            career_questions_answered[q.career_id].append(score)

    def calculate_average(lst: List[float], default: float = 65.0) -> float:
        return round(sum(lst) / len(lst), 1) if lst else default

    # Compute finalized dimension averages (0 - 100)
    dimensions_summary = {}
    for m in MODULE_DEFINITIONS:
        dim = m["primary_dimension"]
        dim_name = m["name"]
        avg_val = calculate_average(dimension_scores.get(dim, []), default=68.0)
        dimensions_summary[dim] = {
            "name": dim_name,
            "module_number": m["module_number"],
            "score": avg_val,
            "questions_count": len(dimension_scores.get(dim, []))
        }

    # Aggregate high-level category scores
    aptitude_avg = calculate_average(
        dimension_scores["numerical_aptitude"] +
        dimension_scores["logical_reasoning"] +
        dimension_scores["spatial_abstract"] +
        dimension_scores["critical_thinking"],
        default=70.0
    )
    interest_avg = calculate_average(
        dimension_scores["interest_discovery"] +
        dimension_scores["career_exploration"],
        default=75.0
    )
    technical_avg = calculate_average(
        dimension_scores["science_tech"] +
        dimension_scores["commerce_finance"] +
        dimension_scores["computational_thinking"],
        default=68.0
    )
    soft_skills_avg = calculate_average(
        dimension_scores["communication"] +
        dimension_scores["situational_judgement"] +
        dimension_scores["work_preferences"] +
        dimension_scores["learning_style"] +
        dimension_scores["creativity"],
        default=72.0
    )
    overall_avg = round(
        (aptitude_avg * 0.35 + interest_avg * 0.25 + technical_avg * 0.25 + soft_skills_avg * 0.15),
        1
    )

    # Skill breakdown
    skill_breakdown = {sk: calculate_average(scores) for sk, scores in skill_scores.items()}
    if not skill_breakdown:
        skill_breakdown = {
            "Numerical Reasoning": dimensions_summary["numerical_aptitude"]["score"],
            "Logical Deduction": dimensions_summary["logical_reasoning"]["score"],
            "Critical Evaluation": dimensions_summary["critical_thinking"]["score"],
            "Verbal Articulation": dimensions_summary["verbal_ability"]["score"],
            "Problem Solving": technical_avg,
            "Interpersonal Communication": dimensions_summary["communication"]["score"]
        }

    # Identify strengths and growth areas
    sorted_skills = sorted(skill_breakdown.items(), key=lambda x: x[1], reverse=True)
    top_strengths = [s[0] for s in sorted_skills[:3]]
    growth_areas = [s[0] for s in sorted_skills[-3:] if s[1] < 72]

    # Generate transparent explanations and insights
    insights = []
    insights.append(
        f"Demonstrated strongest competencies in {', '.join(top_strengths)} based on empirical assessment responses."
    )
    if growth_areas:
        insights.append(
            f"Focused growth opportunities identified in {', '.join(growth_areas)} to enhance competitive readiness."
        )
    else:
        insights.append("Well-rounded and balanced performance across cognitive, analytical, and domain benchmarks.")

    if dimensions_summary["computational_thinking"]["score"] >= 75:
        insights.append("Strong algorithmic mindset with high aptitude for systematic problem decomposition.")
    if dimensions_summary["situational_judgement"]["score"] >= 75:
        insights.append("High situational maturity and ethical decision-making alignment observed in workplace scenarios.")

    recommended_actions = [
        f"Focus next 4 weeks on strengthening {growth_areas[0] if growth_areas else 'domain-specific applications'} with standard curriculum resources.",
        "Review official Indian entrance exam syllabi and minimum percentage prerequisites for targeted courses.",
        "Complete 1 structured hands-on project or internship simulation to build tangible portfolio evidence."
    ]

    # 4. Multi-Dimensional Compatibility Across All 30 Careers
    all_careers = db.query(Career).filter(Career.is_active == True).all()
    career_by_slug = {c.slug: c for c in all_careers}
    career_by_id = {c.id: c for c in all_careers}

    # Determine selected careers based on assessment mode
    selected_career_ids = set()
    if session.mode == "fixed" and session.target_career_id:
        selected_career_ids.add(session.target_career_id)
    elif session.mode == "clarity" and session.clarity_career_ids_json:
        if isinstance(session.clarity_career_ids_json, list):
            selected_career_ids.update(session.clarity_career_ids_json)

    career_evaluations = []
    evidence_status_map = {}

    for c in all_careers:
        profile = CAREER_MAPPING_PROFILES.get(c.slug)
        if not profile:
            # Fallback uniform weights
            dim_weights = {m["primary_dimension"]: 1.0 for m in MODULE_DEFINITIONS}
            critical_skills = ["Problem Solving", "Logical Reasoning"]
            min_thresh = 60.0
            evidence_reqs = ["logical_reasoning", "numerical_aptitude"]
        else:
            dim_weights = profile["dimension_weights"]
            critical_skills = profile.get("critical_skills", [])
            min_thresh = profile.get("min_proficiency_threshold", 60.0)
            evidence_reqs = profile.get("evidence_requirements", [])

        # Weighted dot product between student's dimension scores and career dimension weights
        weighted_score_sum = 0.0
        total_weight = 0.0
        for dim, w in dim_weights.items():
            s_val = dimensions_summary.get(dim, {}).get("score", 65.0)
            weighted_score_sum += s_val * w
            total_weight += w

        raw_compat = weighted_score_sum / (total_weight or 1.0)

        # Factor in career-specific technical questions if answered
        if c.id in career_questions_answered:
            career_q_scores = career_questions_answered[c.id]
            cq_avg = sum(career_q_scores) / len(career_q_scores)
            # Blend 60% general multi-dimension + 40% dedicated profession questions
            compat_score = round(raw_compat * 0.60 + cq_avg * 0.40, 1)
        else:
            compat_score = round(raw_compat, 1)

        # Clamp compatibility between 25.0 and 99.0
        compat_score = min(99.0, max(25.0, compat_score))

        # Evidence Confidence Assessment
        # high_confidence: dedicated career questions answered OR all evidence_req dimensions have >= 2 questions answered and score >= 65%
        evidence_status = "moderate"
        if c.id in career_questions_answered and len(career_questions_answered[c.id]) >= 5:
            evidence_status = "high_confidence"
        else:
            # Check universal evidence dimensions
            satisfied_reqs = 0
            for req_dim in evidence_reqs:
                dim_info = dimensions_summary.get(req_dim, {})
                if dim_info.get("questions_count", 0) >= 2 and dim_info.get("score", 0) >= min_thresh - 5:
                    satisfied_reqs += 1
            if satisfied_reqs == len(evidence_reqs) and len(evidence_reqs) > 0:
                evidence_status = "high_confidence"
            elif satisfied_reqs == 0 and len(evidence_reqs) > 1 and session.mode != "fixed":
                evidence_status = "more_evidence_needed"
            else:
                evidence_status = "moderate"

        evidence_status_map[str(c.id)] = evidence_status

        # Alignment categorization
        if compat_score >= 78.0:
            alignment = "Strong alignment"
        elif compat_score >= 65.0:
            alignment = "Promising alignment"
        elif compat_score >= 50.0:
            alignment = "Developing alignment"
        else:
            alignment = "More exploration recommended"

        is_selected = (c.id in selected_career_ids)

        career_evaluations.append({
            "career_id": c.id,
            "title": c.title,
            "slug": c.slug,
            "category_name": c.category.name if c.category else "",
            "compatibility_score": compat_score,
            "alignment_category": alignment,
            "evidence_status": evidence_status,
            "is_selected_choice": is_selected,
            "critical_skills": critical_skills,
            "explanation": (
                f"{alignment} based on your {top_strengths[0]} strengths and multi-dimensional profile match. "
                f"Empirical match of {compat_score}%."
            )
        })

    # Sort all careers descending by compatibility score
    career_evaluations.sort(key=lambda x: x["compatibility_score"], reverse=True)

    # Separate selected vs alternative recommendations
    selected_evals = [e for e in career_evaluations if e["is_selected_choice"]]
    alternative_evals = [e for e in career_evaluations if not e["is_selected_choice"]]

    # Save or update AssessmentResult in database
    result = db.query(AssessmentResult).filter(AssessmentResult.session_id == session_id).first()
    if not result:
        result = AssessmentResult(
            session_id=session_id,
            student_id=session.student_id
        )
        db.add(result)
        db.flush()

    result.aptitude_score = aptitude_avg
    result.interest_score = interest_avg
    result.technical_score = technical_avg
    result.soft_skills_score = soft_skills_avg
    result.overall_score = overall_avg
    result.dimensions_breakdown_json = dimensions_summary
    result.skill_breakdown_json = skill_breakdown
    result.evidence_status_json = evidence_status_map
    result.alternative_recommendations_json = alternative_evals[:6]
    result.insights_json = insights
    result.recommended_actions_json = recommended_actions
    db.commit()
    db.refresh(result)

    # Clear prior recommendations for this result
    db.query(CareerRecommendation).filter(CareerRecommendation.result_id == result.id).delete()

    # Insert top recommendations
    # If selected careers exist (Fixed or Clarity), put them at the top of recommendations table
    final_recs_to_insert = []
    if selected_evals:
        for idx, sel in enumerate(selected_evals, start=1):
            sel["rank_order"] = idx
            final_recs_to_insert.append(sel)
        # Followed by top 10 alternative recommendations
        for idx, alt in enumerate(alternative_evals[:10], start=len(selected_evals) + 1):
            alt["rank_order"] = idx
            final_recs_to_insert.append(alt)
    else:
        # Not Fixed mode: top 10 overall ranked
        for idx, cand in enumerate(career_evaluations[:10], start=1):
            cand["rank_order"] = idx
            final_recs_to_insert.append(cand)

    for item in final_recs_to_insert:
        rec = CareerRecommendation(
            result_id=result.id,
            career_id=item["career_id"],
            compatibility_score=item["compatibility_score"],
            alignment_category=item["alignment_category"],
            evidence_status=item["evidence_status"],
            is_selected_choice=item["is_selected_choice"],
            explanation=item["explanation"],
            rank_order=item["rank_order"]
        )
        db.add(rec)

    db.commit()
    db.refresh(result)
    return result


def compute_eligibility_status(db: Session, career_id: int, student_education: Optional[EducationDetail]) -> Dict[str, Any]:
    """
    Computes Indian academic and regulatory eligibility breakdown:
    - Eligible now
    - Not yet eligible
    - Future eligibility
    """
    career = db.query(Career).filter(Career.id == career_id).first()
    if not career:
        return {"status": "Unknown", "eligible_now": [], "not_yet_eligible": [], "future_eligibility": []}

    level = student_education.education_level if student_education else "school_8_10"
    stream = (student_education.stream or "").lower() if student_education else ""

    eligible_now = []
    not_yet_eligible = []
    future_eligibility = []

    requirements = db.query(CareerRequirement).filter(CareerRequirement.career_id == career_id).all()

    # Rule-based logic tailored to Indian Education System
    if career.slug in ["doctor-mbbs", "dentist", "pharmacist", "physiotherapist", "biotechnologist"]:
        if level == "school_8_10":
            eligible_now.append("Eligible to choose Class 11th Science stream with Biology (PCB).")
            not_yet_eligible.append("Class 12th Board qualification with minimum 50% in Physics, Chemistry & Biology.")
            not_yet_eligible.append("NEET-UG qualification administered by National Testing Agency (NTA).")
            future_eligibility.append("Take PCB in 11th/12th, register for NEET-UG, secure qualifying cutoff rank for MBBS/BDS/B.Pharm admission.")
        elif level == "school_11_12":
            if "bio" in stream or "pcb" in stream or "science" in stream:
                eligible_now.append("Enrolled in required Science PCB stream.")
                not_yet_eligible.append("NEET-UG entrance examination score and state/all-India counseling.")
                future_eligibility.append("Focus on NEET-UG preparation and Class 12 board marksheet verification.")
            else:
                not_yet_eligible.append("Current stream lacks mandatory Biology (PCB) curriculum prescribed by NMC.")
                future_eligibility.append("Consider NIOS additional Biology certification or allied health management paths.")
        else:
            eligible_now.append("Basic higher secondary foundation verified.")
            not_yet_eligible.append("NEET-UG qualification if not previously attempted for clinical medicine.")
            future_eligibility.append("Explore specialized postgraduate biomedical, biotechnology or healthcare administration tracks.")

    elif career.slug in ["engineer", "software-developer", "data-scientist", "artificial-intelligence-engineer", "cybersecurity-analyst", "mechanical-engineer", "architect"]:
        if level == "school_8_10":
            eligible_now.append("Eligible for admission into Class 11 Science with Mathematics (PCM) or Polytechnic Diploma.")
            not_yet_eligible.append("Class 12th PCM or 3-year AICTE recognized Polytechnic Diploma.")
            not_yet_eligible.append("JEE Main / State Engineering CET / NATA (for Architecture).")
            future_eligibility.append("Score strong grades in 10th Math/Science, choose PCM or Diploma, prepare for JEE / CET.")
        elif level == "school_11_12":
            eligible_now.append("Eligible to appear for national engineering entrance tests (JEE Main, BITSAT, State CET).")
            not_yet_eligible.append("B.Tech / B.E. / B.Sc. CS or IT undergraduate degree.")
            future_eligibility.append("Appear for JEE Main / CET counseling and enter an accredited engineering institution.")
        elif level == "diploma":
            eligible_now.append("Eligible for Direct 2nd Year B.Tech Lateral Entry (LEET / DSE).")
            not_yet_eligible.append("B.Tech graduation completion.")
            future_eligibility.append("Complete lateral entry counseling and maintain high aggregate in core technical subjects.")
        else:
            eligible_now.append("Eligible for software developer / tech roles, campus hiring and off-campus placements.")
            not_yet_eligible.append("Industry technical project portfolio, GitHub repository verification, DSA proficiency.")
            future_eligibility.append("Target industry certifications (AWS, Azure, Full-Stack) and apply to tech associate programs.")

    elif career.slug in ["chartered-accountant-ca", "company-secretary-cs", "financial-analyst", "investment-banker"]:
        if level == "school_8_10":
            eligible_now.append("Eligible to register provisionally for ICAI CA Foundation after 10th Standard.")
            not_yet_eligible.append("Class 12th completion (any stream, Commerce with Math/Accounts recommended).")
            future_eligibility.append("Register with ICAI, complete 12th board exams, appear for CA Foundation examination.")
        elif level in ["school_11_12", "diploma"]:
            eligible_now.append("Eligible to appear for CA Foundation / CS EET exams.")
            not_yet_eligible.append("CA Intermediate, 2-year practical articleship training, and CA Final.")
            future_eligibility.append("Clear CA Foundation, register for Intermediate, complete mandatory ICITSS IT & Soft Skills training.")
        else:
            eligible_now.append("Graduates with 55%+ Commerce or 60%+ other streams are exempt from CA Foundation (Direct Entry to CA Intermediate).")
            not_yet_eligible.append("Articleship training under a practicing Chartered Accountant.")
            future_eligibility.append("Enroll via ICAI Direct Entry Route, begin articleship, clear CA Final.")

    elif career.slug in ["ias-officer", "ips-officer"]:
        if level in ["school_8_10", "school_11_12", "diploma"]:
            eligible_now.append("Eligible to build general studies foundation, NCERT readings and current affairs awareness.")
            not_yet_eligible.append("Recognized undergraduate degree from an Indian university (mandatory minimum for UPSC CSE).")
            not_yet_eligible.append("Minimum age of 21 years on 1st August of examination year.")
            future_eligibility.append("Complete any recognized 3 or 4-year graduation degree and prepare for UPSC CSE Prelims/Mains.")
        else:
            eligible_now.append("Academically eligible for UPSC Civil Services Examination (CSE) provided age criteria (21-32 years) is satisfied.")
            not_yet_eligible.append("UPSC CSE Prelims, Mains (9 papers) and Personality Test (Interview).")
            future_eligibility.append("Select optional subject, register for UPSC CSE notification via upsc.gov.in.")

    elif career.slug == "lawyer":
        if level == "school_8_10":
            eligible_now.append("Eligible to build English reading speed, critical thinking and constitutional awareness.")
            not_yet_eligible.append("Class 12th completion (any stream).")
            not_yet_eligible.append("CLAT (Common Law Admission Test) for 5-Year Integrated B.A. LL.B.")
            future_eligibility.append("Complete 12th, appear for CLAT / AILET, join a National Law University (NLU).")
        elif level == "school_11_12":
            eligible_now.append("Eligible to appear for CLAT-UG, AILET, SLAT, LSAT India.")
            not_yet_eligible.append("5-Year integrated LL.B. degree + Bar Council of India (BCI) enrollment.")
            future_eligibility.append("Secure NLU admission, complete 5-year curriculum, clear All India Bar Examination (AIBE).")
        else:
            eligible_now.append("Eligible for 3-Year LL.B. degree via DU LLB / CUET-PG / MH CET Law.")
            not_yet_eligible.append("3-Year LL.B. degree and BCI Advocate enrollment.")
            future_eligibility.append("Enroll in 3-year LL.B. program, complete court internships, pass AIBE.")

    elif career.slug == "pilot":
        if level == "school_8_10":
            eligible_now.append("Eligible to choose Class 11th Science with Physics and Mathematics.")
            not_yet_eligible.append("Class 12th with 50%+ in Physics & Mathematics (mandatory DGCA requirement).")
            not_yet_eligible.append("DGCA Class 1 Medical clearance and 200 flying hours.")
            future_eligibility.append("Pass 12th PCM, undergo DGCA Class 2 and Class 1 medicals, enroll in a DGCA-approved Flying Training Organisation (FTO).")
        elif level == "school_11_12":
            if "pcm" in stream or "math" in stream or "science" in stream:
                eligible_now.append("Satisfies 10+2 Physics & Mathematics requirement for DGCA CPL.")
                not_yet_eligible.append("DGCA Class 1 Medical Fitness Certificate & Pilot Aptitude Test (WOMBAT).")
                future_eligibility.append("Obtain DGCA Computer Number, clear Ground School theory papers (Air Nav, Met, Regs), complete 200 hours flight training.")
            else:
                not_yet_eligible.append("Missing mandatory Physics and Mathematics at 10+2 level.")
                future_eligibility.append("Clear Physics and Mathematics as single/additional subjects through NIOS (National Institute of Open Schooling).")
        else:
            eligible_now.append("Can directly apply to Flying Training Organisations (FTOs) or Airline Cadet Pilot Programs.")
            not_yet_eligible.append("DGCA Commercial Pilot License (CPL) and Multi-Engine Instrument Rating.")
            future_eligibility.append("Complete Cadet Pilot Assessment (IndiGo, Air India) or modular flying training.")

    else:
        if level in ["school_8_10", "school_11_12"]:
            eligible_now.append("Eligible to explore stream combinations without stream restriction.")
            not_yet_eligible.append("Undergraduate degree or professional design/management entrance (UCEED, NID-DAT, IPMAT).")
            future_eligibility.append("Build portfolio, prepare for entrance test, and complete relevant undergraduate program.")
        else:
            eligible_now.append("Eligible for entry-level roles, internships, or postgraduate entrance (CAT, CEED).")
            not_yet_eligible.append("Industry portfolio / case study demonstrations.")
            future_eligibility.append("Complete specialized certifications, build a public portfolio, and network for placements.")

    for r in requirements:
        if r.requirement_type == "entrance_exam":
            if r.title not in " ".join(not_yet_eligible + eligible_now):
                not_yet_eligible.append(f"Entrance Exam: {r.title} ({r.description})")

    return {
        "career_id": career_id,
        "career_title": career.title,
        "eligible_now": eligible_now,
        "not_yet_eligible": not_yet_eligible,
        "future_eligibility": future_eligibility,
        "official_authority": career.official_authority_name,
        "official_url": career.official_source_url,
        "last_verified_date": career.last_verified_date
    }
