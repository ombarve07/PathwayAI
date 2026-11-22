import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.entities import User, StudentProfile, EducationDetail, Career, AssessmentResult
from backend.app.schemas.schemas import (
    StudentProfileResponse, StudentProfileUpdate,
    EducationDetailCreate, EducationDetailResponse
)
from backend.app.core.deps import get_current_user, get_current_student

router = APIRouter(prefix="/api/students", tags=["Students"])

@router.get("/profile")
def get_student_profile(
    current_user: User = Depends(get_current_user),
    profile: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    edu = db.query(EducationDetail).filter(EducationDetail.profile_id == profile.id).first()
    target_career_title = profile.target_career.title if profile.target_career else None

    edu_data = None
    if edu:
        edu_data = {
            "id": edu.id,
            "profile_id": edu.profile_id,
            "education_level": edu.education_level,
            "current_class_year": edu.current_class_year,
            "board_university": edu.board_university,
            "stream": edu.stream,
            "subjects": edu.subjects,
            "diploma_branch": edu.diploma_branch,
            "degree": edu.degree,
            "semester": edu.semester,
            "academic_interests": edu.academic_interests,
            "updated_at": edu.updated_at
        }

    return {
        "id": profile.id,
        "user_id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "mobile": current_user.mobile,
        "dob": current_user.dob,
        "guardian_consent": current_user.guardian_consent,
        "current_journey_step": profile.current_journey_step,
        "preferred_mode": profile.preferred_mode,
        "target_career_id": profile.target_career_id,
        "target_career_title": target_career_title,
        "clarity_careers_json": profile.clarity_careers_json,
        "streak_days": profile.streak_days,
        "education": edu_data
    }

@router.put("/profile")
def update_student_profile(
    update_data: StudentProfileUpdate,
    profile: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    if update_data.preferred_mode is not None:
        profile.preferred_mode = update_data.preferred_mode
    if update_data.target_career_id is not None:
        profile.target_career_id = update_data.target_career_id
    if update_data.clarity_careers_json is not None:
        profile.clarity_careers_json = update_data.clarity_careers_json
    if update_data.current_journey_step is not None:
        profile.current_journey_step = update_data.current_journey_step
    if update_data.bio is not None:
        profile.bio = update_data.bio

    profile.updated_at = datetime.datetime.utcnow()
    db.commit()
    db.refresh(profile)
    return {"message": "Profile updated successfully."}

@router.post("/education", response_model=EducationDetailResponse)
def save_education_details(
    edu_in: EducationDetailCreate,
    profile: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    edu = db.query(EducationDetail).filter(EducationDetail.profile_id == profile.id).first()
    if not edu:
        edu = EducationDetail(profile_id=profile.id, education_level=edu_in.education_level)
        db.add(edu)

    edu.education_level = edu_in.education_level
    edu.current_class_year = edu_in.current_class_year
    edu.board_university = edu_in.board_university
    edu.stream = edu_in.stream
    edu.subjects = edu_in.subjects
    edu.diploma_branch = edu_in.diploma_branch
    edu.degree = edu_in.degree
    edu.semester = edu_in.semester
    edu.academic_interests = edu_in.academic_interests
    edu.updated_at = datetime.datetime.utcnow()

    # Advance journey step if still at registered
    if profile.current_journey_step == "registered":
        profile.current_journey_step = "education_set"

    db.commit()
    db.refresh(edu)
    return edu

@router.get("/dashboard")
def get_student_dashboard_overview(
    profile: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    # Retrieve latest assessment result
    latest_result = db.query(AssessmentResult).filter(
        AssessmentResult.student_id == profile.id
    ).order_by(AssessmentResult.created_at.desc()).first()

    # Target Career
    target_career = None
    if profile.target_career_id:
        c = db.query(Career).filter(Career.id == profile.target_career_id).first()
        if c:
            target_career = {
                "id": c.id,
                "title": c.title,
                "slug": c.slug,
                "category_name": c.category.name if c.category else "General",
                "avg_salary_inr": c.avg_salary_inr,
                "growth_rate": c.growth_rate,
                "icon_name": c.icon_name
            }

    result_summary = None
    if latest_result:
        result_summary = {
            "session_id": latest_result.session_id,
            "overall_score": latest_result.overall_score,
            "aptitude_score": latest_result.aptitude_score,
            "interest_score": latest_result.interest_score,
            "technical_score": latest_result.technical_score,
            "soft_skills_score": latest_result.soft_skills_score,
            "skill_breakdown": latest_result.skill_breakdown_json or {},
            "insights": latest_result.insights_json or [],
            "recommended_actions": latest_result.recommended_actions_json or [],
            "is_unlocked": latest_result.is_unlocked,
            "created_at": latest_result.created_at
        }

    return {
        "student_id": profile.id,
        "journey_step": profile.current_journey_step,
        "preferred_mode": profile.preferred_mode,
        "streak_days": profile.streak_days,
        "target_career": target_career,
        "latest_result": result_summary
    }
