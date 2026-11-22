import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.entities import (
    StudentProfile, EducationDetail, Career, Question, QuestionOption,
    AssessmentSession, StudentAnswer, AssessmentResult, CareerRecommendation,
    AssessmentModule, AssessmentConfiguration
)
from backend.app.schemas.schemas import (
    AssessmentStartRequest, AssessmentAnswerSubmit
)
from backend.app.core.deps import get_current_student
from backend.app.analytics.scoring import evaluate_assessment_session, compute_eligibility_status
from backend.app.analytics.career_mapping import MODULE_DEFINITIONS

router = APIRouter(prefix="/api/assessments", tags=["Assessments"])


@router.get("/configurations")
def get_assessment_configurations(
    db: Session = Depends(get_db)
):
    """
    Returns available assessment configurations for Fixed, Not Fixed, and Clarity modes.
    """
    configs = db.query(AssessmentConfiguration).filter(AssessmentConfiguration.is_active == True).all()
    res = []
    for c in configs:
        res.append({
            "id": c.id,
            "code": c.code,
            "name": c.name,
            "mode": c.mode,
            "career_id": c.career_id,
            "target_questions_count": c.target_questions_count,
            "time_limit_minutes": c.time_limit_minutes,
            "description": c.description
        })
    return res


@router.post("/start")
def start_assessment_session(
    req: AssessmentStartRequest,
    profile: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    edu = db.query(EducationDetail).filter(EducationDetail.profile_id == profile.id).first()
    edu_level = edu.education_level if edu else "school_8_10"

    # Update profile mode and career if provided
    profile.preferred_mode = req.mode
    if req.target_career_id:
        profile.target_career_id = req.target_career_id
    if req.clarity_career_ids:
        profile.clarity_careers_json = req.clarity_career_ids
    profile.current_journey_step = "assessing"
    db.commit()

    # Determine matched configuration
    matched_config = None
    if req.mode == "fixed" and req.target_career_id:
        matched_config = db.query(AssessmentConfiguration).filter(
            AssessmentConfiguration.mode == "fixed",
            AssessmentConfiguration.career_id == req.target_career_id
        ).first()
    elif req.mode == "clarity":
        matched_config = db.query(AssessmentConfiguration).filter(
            AssessmentConfiguration.mode == "clarity"
        ).first()
    elif req.mode == "not_fixed":
        matched_config = db.query(AssessmentConfiguration).filter(
            AssessmentConfiguration.mode == "not_fixed"
        ).first()

    # Create session
    session = AssessmentSession(
        student_id=profile.id,
        mode=req.mode,
        target_career_id=req.target_career_id,
        config_id=matched_config.id if matched_config else None,
        clarity_career_ids_json=req.clarity_career_ids if req.mode == "clarity" else None,
        current_stage="core",
        education_level=edu_level,
        status="in_progress",
        started_at=datetime.datetime.utcnow()
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return {
        "session_id": session.id,
        "mode": session.mode,
        "education_level": session.education_level,
        "target_career_id": session.target_career_id,
        "clarity_career_ids": session.clarity_career_ids_json,
        "config_code": matched_config.code if matched_config else None,
        "time_limit_minutes": matched_config.time_limit_minutes if matched_config else 35,
        "status": session.status,
        "started_at": session.started_at
    }


@router.get("/{session_id}/questions")
def get_session_questions(
    session_id: int,
    profile: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    session = db.query(AssessmentSession).filter(
        AssessmentSession.id == session_id,
        AssessmentSession.student_id == profile.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Assessment session not found.")

    student_level = session.education_level or "school_8_10"
    level_filters = ["all", student_level]

    selected_questions = []

    if session.mode == "fixed" and session.target_career_id:
        # 1. FIXED CAREER MODE:
        # Fetch up to 10 dedicated questions for this target career
        career_qs = db.query(Question).filter(
            Question.career_id == session.target_career_id,
            Question.is_active == True
        ).all()
        selected_questions.extend(career_qs[:10])

        # Fetch foundational universal questions (M01 Aptitude, M02 Logic, M04 Critical, M12 Comm, M13 Situational)
        core_module_codes = ["M01_GENERAL_APTITUDE", "M02_LOGICAL_REASONING", "M04_CRITICAL_THINKING", "M12_COMMUNICATION_SKILLS", "M13_SITUATIONAL_JUDGEMENT"]
        core_modules = db.query(AssessmentModule).filter(AssessmentModule.code.in_(core_module_codes)).all()
        core_mod_ids = [m.id for m in core_modules]

        uni_qs = db.query(Question).filter(
            Question.module_id.in_(core_mod_ids),
            Question.education_level.in_(level_filters),
            Question.is_active == True
        ).all()
        # Take 2 per core module
        mod_buckets = {}
        for q in uni_qs:
            mod_buckets.setdefault(q.module_id, []).append(q)
        for m_id, q_list in mod_buckets.items():
            selected_questions.extend(q_list[:2])

    elif session.mode == "clarity":
        # 2. CAREER CLARITY MODE:
        # Fetch dedicated questions for each of the selected clarity careers
        clarity_ids = session.clarity_career_ids_json or []
        for c_id in clarity_ids:
            c_qs = db.query(Question).filter(
                Question.career_id == c_id,
                Question.is_active == True
            ).all()
            selected_questions.extend(c_qs[:5])

        # Fetch foundational comparison modules (M01, M02, M04, M10 Interest, M11 Personality, M15 Career)
        comp_module_codes = ["M01_GENERAL_APTITUDE", "M02_LOGICAL_REASONING", "M04_CRITICAL_THINKING", "M10_INTEREST_DISCOVERY", "M11_WORK_PREFERENCES", "M15_CAREER_EXPLORATION"]
        comp_modules = db.query(AssessmentModule).filter(AssessmentModule.code.in_(comp_module_codes)).all()
        comp_mod_ids = [m.id for m in comp_modules]

        uni_qs = db.query(Question).filter(
            Question.module_id.in_(comp_mod_ids),
            Question.education_level.in_(level_filters),
            Question.is_active == True
        ).all()
        mod_buckets = {}
        for q in uni_qs:
            mod_buckets.setdefault(q.module_id, []).append(q)
        for m_id, q_list in mod_buckets.items():
            selected_questions.extend(q_list[:2])

    else:
        # 3. NOT FIXED (UNIVERSAL DISCOVERY) MODE:
        # Giant universal question bank across all 15 modules (2 questions per module = 30 questions)
        all_modules = db.query(AssessmentModule).order_by(AssessmentModule.module_number.asc()).all()
        for mod in all_modules:
            mod_qs = db.query(Question).filter(
                Question.module_id == mod.id,
                Question.education_level.in_(level_filters),
                Question.is_active == True
            ).all()
            if not mod_qs:
                # Fallback to any active question in this module
                mod_qs = db.query(Question).filter(
                    Question.module_id == mod.id,
                    Question.is_active == True
                ).all()
            selected_questions.extend(mod_qs[:2])

    # Fallback safety if database has fewer questions
    if not selected_questions:
        selected_questions = db.query(Question).filter(Question.is_active == True).limit(25).all()

    # Format question output with module metadata
    formatted_questions = []
    for q in selected_questions:
        mod = q.module
        career = q.career
        mod_name = mod.name if mod else (f"Domain: {career.title}" if career else "General Aptitude")
        mod_num = mod.module_number if mod else 1
        sec_title = f"Module {mod_num}: {mod_name}" if mod else (f"Technical Deep Dive: {career.title}" if career else "Assessment")

        formatted_questions.append({
            "id": q.id,
            "question_code": q.question_code or f"Q_{q.id}",
            "module_number": mod_num,
            "module_name": mod_name,
            "section_title": sec_title,
            "category": q.category,
            "sub_topic": q.sub_topic,
            "difficulty": q.difficulty,
            "skill_name": q.skill_name,
            "text": q.text,
            "question_type": q.question_type,
            "scoring_type": q.scoring_type,
            "options": [{
                "id": opt.id,
                "option_key": opt.option_key,
                "text": opt.text
            } for opt in q.options]
        })

    # Retrieve already answered questions for resume
    answered_map = {}
    answers = db.query(StudentAnswer).filter(StudentAnswer.session_id == session_id).all()
    for a in answers:
        answered_map[a.question_id] = a.selected_option_id

    return {
        "session_id": session_id,
        "mode": session.mode,
        "education_level": session.education_level,
        "total_questions": len(formatted_questions),
        "answered_count": len(answers),
        "answered_map": answered_map,
        "questions": formatted_questions
    }


@router.post("/{session_id}/answer")
def submit_answer(
    session_id: int,
    ans_in: AssessmentAnswerSubmit,
    profile: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    session = db.query(AssessmentSession).filter(
        AssessmentSession.id == session_id,
        AssessmentSession.student_id == profile.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Assessment session not found.")

    opt = db.query(QuestionOption).filter(QuestionOption.id == ans_in.selected_option_id).first()
    if not opt:
        raise HTTPException(status_code=400, detail="Invalid option selected.")

    # Upsert answer record
    ans = db.query(StudentAnswer).filter(
        StudentAnswer.session_id == session_id,
        StudentAnswer.question_id == ans_in.question_id
    ).first()

    if not ans:
        ans = StudentAnswer(
            session_id=session_id,
            question_id=ans_in.question_id
        )
        db.add(ans)

    ans.selected_option_id = ans_in.selected_option_id
    ans.answer_value = opt.score_value
    ans.response_time_seconds = ans_in.response_time_seconds
    ans.created_at = datetime.datetime.utcnow()

    db.commit()
    return {"message": "Answer recorded successfully.", "question_id": ans_in.question_id}


@router.post("/{session_id}/adaptive-next")
def get_adaptive_stage_questions(
    session_id: int,
    profile: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """
    Adaptive Assessment Engine:
    Triggers Stage 2 drill-down when the student demonstrates strong potential in 2-3 careers
    or when additional evidence is required to confirm recommendations.
    """
    session = db.query(AssessmentSession).filter(
        AssessmentSession.id == session_id,
        AssessmentSession.student_id == profile.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Assessment session not found.")

    # Preliminary evaluation to find top candidates
    res = evaluate_assessment_session(db, session_id)
    top_recs = db.query(CareerRecommendation).filter(
        CareerRecommendation.result_id == res.id
    ).order_by(CareerRecommendation.compatibility_score.desc()).limit(2).all()

    adaptive_career_ids = [r.career_id for r in top_recs]
    session.adaptive_career_ids_json = adaptive_career_ids
    session.current_stage = "adaptive"
    db.commit()

    # Fetch 4 specialized questions per top candidate career
    adaptive_qs = []
    for c_id in adaptive_career_ids:
        qs = db.query(Question).filter(
            Question.career_id == c_id,
            Question.is_active == True
        ).limit(4).all()
        for q in qs:
            career = q.career
            adaptive_qs.append({
                "id": q.id,
                "question_code": q.question_code or f"Q_ADAPTIVE_{q.id}",
                "section_title": f"Adaptive Deep-Dive: {career.title if career else 'Specialized'}",
                "category": q.category,
                "difficulty": "hard",
                "skill_name": q.skill_name,
                "text": q.text,
                "scoring_type": q.scoring_type,
                "options": [{
                    "id": opt.id,
                    "option_key": opt.option_key,
                    "text": opt.text
                } for opt in q.options]
            })

    return {
        "session_id": session_id,
        "stage": "adaptive",
        "top_candidate_careers": [r.career.title for r in top_recs if r.career],
        "adaptive_questions": adaptive_qs
    }


@router.post("/{session_id}/complete")
def complete_assessment(
    session_id: int,
    profile: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    session = db.query(AssessmentSession).filter(
        AssessmentSession.id == session_id,
        AssessmentSession.student_id == profile.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Assessment session not found.")

    session.status = "completed"
    session.completed_at = datetime.datetime.utcnow()
    profile.current_journey_step = "assessed"
    db.commit()

    # Run multi-dimensional scoring & recommendation engine
    result = evaluate_assessment_session(db, session_id)

    return {
        "message": "Assessment completed successfully.",
        "session_id": session_id,
        "overall_score": result.overall_score,
        "is_unlocked": result.is_unlocked
    }


@router.get("/{session_id}/results")
def get_assessment_results(
    session_id: int,
    profile: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    session = db.query(AssessmentSession).filter(
        AssessmentSession.id == session_id,
        AssessmentSession.student_id == profile.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Assessment session not found.")

    result = db.query(AssessmentResult).filter(AssessmentResult.session_id == session_id).first()
    if not result:
        result = evaluate_assessment_session(db, session_id)

    recs = db.query(CareerRecommendation).filter(
        CareerRecommendation.result_id == result.id
    ).order_by(CareerRecommendation.rank_order.asc()).all()

    # Separate selected choices vs alternatives
    selected_recs = []
    alternative_recs = []
    all_recommendations = []

    edu = db.query(EducationDetail).filter(EducationDetail.profile_id == profile.id).first()

    for r in recs:
        c = r.career
        c_data = {
            "career_id": r.career_id,
            "title": c.title if c else "",
            "category_name": c.category.name if c and c.category else "",
            "slug": c.slug if c else "",
            "compatibility_score": r.compatibility_score,
            "alignment_category": r.alignment_category,
            "evidence_status": r.evidence_status or "moderate",
            "is_selected_choice": r.is_selected_choice,
            "explanation": r.explanation,
            "rank_order": r.rank_order,
            "avg_salary_inr": c.avg_salary_inr if c else "₹6,00,000 - ₹18,00,000",
            "growth_rate": c.growth_rate if c else "High",
            "official_authority_name": c.official_authority_name if c else None,
            "official_source_url": c.official_source_url if c else None,
            "eligibility": compute_eligibility_status(db, r.career_id, edu) if c else None
        }
        all_recommendations.append(c_data)
        if r.is_selected_choice:
            selected_recs.append(c_data)
        else:
            alternative_recs.append(c_data)

    # Primary target career for header showcase
    primary_career = selected_recs[0] if selected_recs else (all_recommendations[0] if all_recommendations else None)

    return {
        "id": result.id,
        "session_id": session_id,
        "mode": session.mode,
        "education_level": session.education_level,
        "overall_score": result.overall_score,
        "aptitude_score": result.aptitude_score,
        "interest_score": result.interest_score,
        "technical_score": result.technical_score,
        "soft_skills_score": result.soft_skills_score,
        "dimensions_breakdown": result.dimensions_breakdown_json or {},
        "skill_breakdown": result.skill_breakdown_json or {},
        "evidence_status": result.evidence_status_json or {},
        "selected_careers": selected_recs,
        "alternative_recommendations": alternative_recs[:5],
        "all_recommendations": all_recommendations,
        "recommendations": all_recommendations,
        "target_career": primary_career,
        "primary_career": primary_career,
        "eligibility_analysis": primary_career["eligibility"] if primary_career else None,
        "insights": result.insights_json or [],
        "recommended_actions": result.recommended_actions_json or [],
        "is_unlocked": result.is_unlocked,
        "unlocked_at": result.unlocked_at
    }


@router.get("/history")
def get_assessment_history(
    profile: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    sessions = db.query(AssessmentSession).filter(
        AssessmentSession.student_id == profile.id
    ).order_by(AssessmentSession.started_at.desc()).all()

    history = []
    for s in sessions:
        r = s.result
        target_name = s.target_career.title if s.target_career else ("Career Clarity Choice" if s.mode == "clarity" else "Universal Discovery")
        history.append({
            "session_id": s.id,
            "mode": s.mode,
            "status": s.status,
            "target_career": target_name,
            "started_at": s.started_at,
            "completed_at": s.completed_at,
            "overall_score": r.overall_score if r else None,
            "is_unlocked": r.is_unlocked if r else False
        })
    return history
