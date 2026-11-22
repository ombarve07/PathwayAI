from typing import Optional
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.entities import (
    StudentProfile, AssessmentResult, CareerRecommendation, Course,
    AffiliateClick
)
from backend.app.core.deps import get_current_student

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

@router.get("/careers")
def get_recommended_careers(
    profile: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    latest_result = db.query(AssessmentResult).filter(
        AssessmentResult.student_id == profile.id
    ).order_by(AssessmentResult.created_at.desc()).first()

    if not latest_result:
        return []

    recs = db.query(CareerRecommendation).filter(
        CareerRecommendation.result_id == latest_result.id
    ).order_by(CareerRecommendation.rank_order.asc()).all()

    output = []
    for r in recs:
        c = r.career
        if c:
            output.append({
                "career_id": c.id,
                "title": c.title,
                "category_name": c.category.name if c.category else "",
                "slug": c.slug,
                "summary": c.summary,
                "compatibility_score": r.compatibility_score,
                "alignment_category": r.alignment_category,
                "explanation": r.explanation,
                "rank_order": r.rank_order,
                "avg_salary_inr": c.avg_salary_inr,
                "growth_rate": c.growth_rate,
                "icon_name": c.icon_name
            })
    return output

@router.get("/courses")
def get_recommended_courses(
    skill_gap: Optional[str] = None,
    profile: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    # Find student's growth skills from latest assessment
    latest_result = db.query(AssessmentResult).filter(
        AssessmentResult.student_id == profile.id
    ).order_by(AssessmentResult.created_at.desc()).first()

    growth_skills = []
    if latest_result and latest_result.skill_breakdown_json:
        # Find skills under 75%
        for sk, score in latest_result.skill_breakdown_json.items():
            if score < 75:
                growth_skills.append(sk)

    courses = db.query(Course).filter(Course.is_active == True).all()
    recommendations = []

    for c in courses:
        why = "Curated foundational course for holistic skill mastery."
        skills = c.skills_taught_json or []

        # Check if course covers a student's assessed skill gap
        matched_gaps = [g for g in growth_skills if g in skills]
        if skill_gap and skill_gap in skills:
            why = f"Specifically recommended to bridge your assessed gap in {skill_gap}."
        elif matched_gaps:
            why = f"Addresses your assessed growth area in {', '.join(matched_gaps)}."

        recommendations.append({
            "id": c.id,
            "provider_name": c.provider.name if c.provider else "Partner Institution",
            "title": c.title,
            "description": c.description,
            "category": c.category,
            "skills_taught": skills,
            "difficulty": c.difficulty,
            "price_inr": c.price_inr,
            "is_free": c.is_free,
            "duration": c.duration,
            "certificate_info": c.certificate_info,
            "course_url": c.course_url,
            "affiliate_url": c.affiliate_url,
            "why_recommended": why
        })

    return recommendations

@router.post("/affiliate-click")
def record_affiliate_click(
    course_id: int,
    request: Request,
    profile: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    ip = request.client.host if request.client else "unknown"
    click = AffiliateClick(
        student_id=profile.id,
        course_id=course_id,
        referral_code="PATHWAY_AI_REF",
        ip_address=ip
    )
    db.add(click)
    db.commit()
    return {"message": "Affiliate click recorded."}
