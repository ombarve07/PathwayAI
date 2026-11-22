import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.entities import (
    StudentProfile, StudentSkillProgress, StudentRoadmapProgress,
    StudentProject, Skill, RoadmapStage
)
from backend.app.schemas.schemas import SkillProgressUpdate, RoadmapStageUpdate
from backend.app.core.deps import get_current_student

router = APIRouter(prefix="/api/progress", tags=["Progress & Journey"])

@router.get("")
def get_student_progress(
    profile: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    skills = db.query(Skill).all()
    user_skills = db.query(StudentSkillProgress).filter(
        StudentSkillProgress.student_id == profile.id
    ).all()
    user_skill_map = {us.skill_id: us for us in user_skills}

    skill_list = []
    for sk in skills:
        us = user_skill_map.get(sk.id)
        skill_list.append({
            "skill_id": sk.id,
            "name": sk.name,
            "category": sk.category,
            "proficiency_level": us.proficiency_level if us else 0,
            "is_verified": us.is_verified if us else False,
            "evidence_note": us.evidence_note if us else ""
        })

    # Roadmap progress
    stages_done = db.query(StudentRoadmapProgress).filter(
        StudentRoadmapProgress.student_id == profile.id,
        StudentRoadmapProgress.is_completed == True
    ).all()
    completed_stage_ids = [s.stage_id for s in stages_done]

    # Projects
    projects = db.query(StudentProject).filter(
        StudentProject.student_id == profile.id
    ).order_by(StudentProject.submitted_at.desc()).all()

    return {
        "streak_days": profile.streak_days,
        "skills_progress": skill_list,
        "completed_stage_ids": completed_stage_ids,
        "projects": [{
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "github_or_file_url": p.github_or_file_url,
            "skills_applied": p.skills_applied,
            "submitted_at": p.submitted_at
        } for p in projects]
    }

@router.post("/skills")
def update_skill_progress(
    data: SkillProgressUpdate,
    profile: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    sp = db.query(StudentSkillProgress).filter(
        StudentSkillProgress.student_id == profile.id,
        StudentSkillProgress.skill_id == data.skill_id
    ).first()

    if not sp:
        sp = StudentSkillProgress(
            student_id=profile.id,
            skill_id=data.skill_id
        )
        db.add(sp)

    sp.proficiency_level = min(100, max(0, data.proficiency_level))
    if data.evidence_note:
        sp.evidence_note = data.evidence_note
    sp.updated_at = datetime.datetime.utcnow()

    db.commit()
    return {"message": "Skill proficiency updated.", "skill_id": data.skill_id, "new_level": sp.proficiency_level}

@router.post("/roadmap")
def update_roadmap_stage(
    data: RoadmapStageUpdate,
    profile: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    stage_prog = db.query(StudentRoadmapProgress).filter(
        StudentRoadmapProgress.student_id == profile.id,
        StudentRoadmapProgress.stage_id == data.stage_id
    ).first()

    if not stage_prog:
        stage_prog = StudentRoadmapProgress(
            student_id=profile.id,
            stage_id=data.stage_id
        )
        db.add(stage_prog)

    stage_prog.is_completed = data.is_completed
    if data.notes:
        stage_prog.notes = data.notes
    if data.is_completed:
        stage_prog.completed_at = datetime.datetime.utcnow()

    db.commit()
    return {"message": "Roadmap stage progress updated.", "stage_id": data.stage_id, "is_completed": data.is_completed}

@router.post("/projects")
def submit_student_project(
    title: str,
    description: str,
    github_or_file_url: str,
    skills_applied: str,
    profile: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    project = StudentProject(
        student_id=profile.id,
        title=title,
        description=description,
        github_or_file_url=github_or_file_url,
        skills_applied=skills_applied,
        submitted_at=datetime.datetime.utcnow()
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return {"message": "Project evidence submitted successfully.", "project_id": project.id}
