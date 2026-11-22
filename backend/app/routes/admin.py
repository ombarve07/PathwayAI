from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.database import get_db
from backend.app.config import settings
from backend.app.models.entities import (
    User, StudentProfile, EducationDetail, Career, CareerCategory,
    CareerRequirement, Question, QuestionOption, Course, CourseProvider,
    Payment, Feedback, AssessmentSession, AssessmentResult
)
from backend.app.core.deps import get_current_admin

router = APIRouter(prefix="/api/admin", tags=["Admin Portal"])

@router.get("/dashboard")
def get_admin_dashboard_stats(
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    total_students = db.query(User).filter(User.is_admin == False).count()
    total_assessments = db.query(AssessmentSession).count()
    completed_assessments = db.query(AssessmentSession).filter(AssessmentSession.status == "completed").count()
    unlocked_reports = db.query(AssessmentResult).filter(AssessmentResult.is_unlocked == True).count()

    # Revenue
    successful_payments = db.query(Payment).filter(Payment.status == "success").all()
    total_revenue = sum([p.amount for p in successful_payments])

    # Education Distribution
    edu_levels = db.query(
        EducationDetail.education_level, func.count(EducationDetail.id)
    ).group_by(EducationDetail.education_level).all()
    edu_dist = {lvl: count for lvl, count in edu_levels}

    # Popular Target Careers
    popular = db.query(
        Career.title, func.count(StudentProfile.id)
    ).join(StudentProfile, StudentProfile.target_career_id == Career.id)\
     .group_by(Career.title).order_by(func.count(StudentProfile.id).desc()).limit(5).all()

    popular_careers = [{"title": p[0], "count": p[1]} for p in popular]

    return {
        "total_students": total_students,
        "total_assessments": total_assessments,
        "completed_assessments": completed_assessments,
        "unlocked_reports": unlocked_reports,
        "total_revenue_inr": total_revenue,
        "education_distribution": edu_dist,
        "popular_careers": popular_careers,
        "pricing": {
            "report_price_inr": settings.REPORT_PRICE_INR,
            "premium_price_inr": settings.PREMIUM_PRICE_INR
        }
    }

@router.get("/students")
def list_admin_students(
    limit: int = 50,
    offset: int = 0,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    users = db.query(User).filter(User.is_admin == False).order_by(User.created_at.desc()).offset(offset).limit(limit).all()
    student_records = []
    for u in users:
        prof = u.profile
        edu = prof.education_detail if prof else None
        target = prof.target_career.title if prof and prof.target_career else "None"
        student_records.append({
            "user_id": u.id,
            "full_name": u.full_name,
            "email": u.email,
            "mobile": u.mobile,
            "education_level": edu.education_level if edu else "Unspecified",
            "target_career": target,
            "journey_step": prof.current_journey_step if prof else "registered",
            "created_at": u.created_at
        })
    return student_records

@router.post("/careers")
def create_career(
    data: Dict[str, Any],
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    slug = data.get("title", "").lower().replace(" ", "-").replace("(", "").replace(")", "")
    career = Career(
        category_id=data.get("category_id", 1),
        title=data.get("title"),
        slug=slug,
        summary=data.get("summary", ""),
        what_they_do=data.get("what_they_do", ""),
        min_education_level=data.get("min_education_level", "school_11_12"),
        stream_flexibility=data.get("stream_flexibility", ""),
        avg_salary_inr=data.get("avg_salary_inr", "₹6,00,000 per annum"),
        growth_rate=data.get("growth_rate", "High"),
        official_source_url=data.get("official_source_url"),
        official_authority_name=data.get("official_authority_name"),
        icon_name=data.get("icon_name", "briefcase")
    )
    db.add(career)
    db.commit()
    db.refresh(career)
    return {"message": "Career created successfully.", "career_id": career.id}

@router.post("/questions")
def add_question(
    data: Dict[str, Any],
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    q = Question(
        category=data.get("category", "aptitude"),
        education_level=data.get("education_level", "all"),
        difficulty=data.get("difficulty", "medium"),
        skill_name=data.get("skill_name"),
        text=data.get("text"),
        scoring_type=data.get("scoring_type", "accuracy"),
        explanation=data.get("explanation")
    )
    db.add(q)
    db.commit()
    db.refresh(q)

    options = data.get("options", [])
    for opt in options:
        qo = QuestionOption(
            question_id=q.id,
            option_key=opt.get("option_key", "A"),
            text=opt.get("text", ""),
            score_value=float(opt.get("score_value", 0.0)),
            is_correct=bool(opt.get("is_correct", False))
        )
        db.add(qo)
    db.commit()

    return {"message": "Question added to bank.", "question_id": q.id}

@router.get("/questions")
def list_questions(
    limit: int = 50,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    qs = db.query(Question).limit(limit).all()
    return [{
        "id": q.id,
        "category": q.category,
        "skill_name": q.skill_name,
        "text": q.text,
        "options_count": len(q.options)
    } for q in qs]

@router.get("/revenue")
def get_revenue_report(
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    payments = db.query(Payment).order_by(Payment.created_at.desc()).all()
    return [{
        "id": p.id,
        "order_id": p.order_id,
        "payment_id": p.payment_id,
        "amount": p.amount,
        "item_type": p.item_type,
        "status": p.status,
        "created_at": p.created_at
    } for p in payments]

@router.put("/pricing")
def update_pricing(
    report_price: float,
    premium_price: float,
    admin: User = Depends(get_current_admin)
):
    settings.REPORT_PRICE_INR = report_price
    settings.PREMIUM_PRICE_INR = premium_price
    return {
        "message": "Pricing parameters updated successfully.",
        "report_price_inr": settings.REPORT_PRICE_INR,
        "premium_price_inr": settings.PREMIUM_PRICE_INR
    }

@router.post("/feedback")
def submit_feedback(
    rating: int,
    comment: str,
    page_context: Optional[str] = None,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    fb = Feedback(
        user_id=admin.id,
        rating=rating,
        comment=comment,
        page_context=page_context
    )
    db.add(fb)
    db.commit()
    return {"message": "Feedback submitted successfully."}

@router.get("/feedback")
def list_feedback(
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    fbs = db.query(Feedback).order_by(Feedback.created_at.desc()).all()
    return [{
        "id": f.id,
        "user_email": f.user.email if f.user else "Anonymous",
        "rating": f.rating,
        "comment": f.comment,
        "page_context": f.page_context,
        "created_at": f.created_at
    } for f in fbs]
