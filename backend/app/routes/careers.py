from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.entities import (
    Career, CareerCategory, CareerRequirement, CareerSkill,
    CareerRoadmap, RoadmapStage, EducationDetail, StudentProfile
)
from backend.app.core.deps import get_current_user, get_current_student
from backend.app.analytics.scoring import compute_eligibility_status

router = APIRouter(prefix="/api/careers", tags=["Careers"])

@router.get("")
def list_careers(
    category_slug: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Career).filter(Career.is_active == True)

    if category_slug:
        query = query.join(CareerCategory).filter(CareerCategory.slug == category_slug)

    if search:
        term = f"%{search.strip()}%"
        query = query.filter(Career.title.ilike(term) | Career.summary.ilike(term))

    careers = query.all()
    results = []
    for c in careers:
        results.append({
            "id": c.id,
            "category_id": c.category_id,
            "category_name": c.category.name if c.category else "",
            "title": c.title,
            "slug": c.slug,
            "summary": c.summary,
            "what_they_do": c.what_they_do,
            "min_education_level": c.min_education_level,
            "stream_flexibility": c.stream_flexibility,
            "avg_salary_inr": c.avg_salary_inr,
            "growth_rate": c.growth_rate,
            "official_source_url": c.official_source_url,
            "official_authority_name": c.official_authority_name,
            "last_verified_date": c.last_verified_date,
            "icon_name": c.icon_name
        })
    return results

@router.get("/categories")
def list_categories(db: Session = Depends(get_db)):
    cats = db.query(CareerCategory).all()
    return [{
        "id": c.id,
        "name": c.name,
        "slug": c.slug,
        "description": c.description,
        "careers_count": len(c.careers)
    } for c in cats]

@router.get("/{career_id_or_slug}")
def get_career_details(career_id_or_slug: str, db: Session = Depends(get_db)):
    if career_id_or_slug.isdigit():
        career = db.query(Career).filter(Career.id == int(career_id_or_slug)).first()
    else:
        career = db.query(Career).filter(Career.slug == career_id_or_slug).first()

    if not career:
        raise HTTPException(status_code=404, detail="Career not found in catalogue.")

    requirements = [{
        "id": r.id,
        "requirement_type": r.requirement_type,
        "title": r.title,
        "description": r.description,
        "is_mandatory": r.is_mandatory,
        "official_link": r.official_link
    } for r in career.requirements]

    skills = [{
        "skill_id": cs.skill.id,
        "skill_name": cs.skill.name,
        "category": cs.skill.category,
        "importance_weight": cs.importance_weight,
        "min_proficiency_needed": cs.min_proficiency_needed
    } for cs in career.career_skills if cs.skill]

    return {
        "id": career.id,
        "category_id": career.category_id,
        "category_name": career.category.name if career.category else "",
        "title": career.title,
        "slug": career.slug,
        "summary": career.summary,
        "what_they_do": career.what_they_do,
        "min_education_level": career.min_education_level,
        "stream_flexibility": career.stream_flexibility,
        "avg_salary_inr": career.avg_salary_inr,
        "growth_rate": career.growth_rate,
        "official_source_url": career.official_source_url,
        "official_authority_name": career.official_authority_name,
        "last_verified_date": career.last_verified_date,
        "icon_name": career.icon_name,
        "requirements": requirements,
        "skills": skills
    }

@router.get("/{career_id}/roadmap")
def get_career_roadmap(career_id: int, db: Session = Depends(get_db)):
    career = db.query(Career).filter(Career.id == career_id).first()
    if not career:
        raise HTTPException(status_code=404, detail="Career not found.")

    roadmap = db.query(CareerRoadmap).filter(CareerRoadmap.career_id == career_id).first()
    if not roadmap:
        return {"career_id": career_id, "career_title": career.title, "stages": []}

    stages = db.query(RoadmapStage).filter(RoadmapStage.roadmap_id == roadmap.id).order_by(RoadmapStage.stage_number.asc()).all()

    return {
        "id": roadmap.id,
        "career_id": career.id,
        "career_title": career.title,
        "title": roadmap.title,
        "description": roadmap.description,
        "stages": [{
            "id": s.id,
            "stage_number": s.stage_number,
            "title": s.title,
            "objective": s.objective,
            "recommended_subjects": s.recommended_subjects,
            "entrance_exams": s.entrance_exams,
            "resources": s.resources,
            "practical_projects": s.practical_projects,
            "expected_outcome": s.expected_outcome,
            "official_source_url": s.official_source_url
        } for s in stages]
    }

@router.get("/{career_id}/eligibility")
def get_career_eligibility(
    career_id: int,
    profile: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    edu = db.query(EducationDetail).filter(EducationDetail.profile_id == profile.id).first()
    eligibility_info = compute_eligibility_status(db, career_id, edu)
    return eligibility_info
