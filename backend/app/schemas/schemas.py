from typing import Optional, List, Dict, Any
from pydantic import BaseModel, field_validator
import re
import datetime

# --- AUTH SCHEMAS ---
class UserRegister(BaseModel):
    full_name: str
    email: str
    password: str
    mobile: Optional[str] = None
    dob: Optional[str] = None
    guardian_consent: Optional[bool] = False

    @field_validator("email")
    def validate_email(cls, v):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, v):
            raise ValueError("Invalid email format")
        return v.lower()

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    full_name: str
    email: str
    is_admin: bool

class PasswordForgot(BaseModel):
    email: str

class PasswordReset(BaseModel):
    token: str
    new_password: str

# --- EDUCATION DETAILS ---
class EducationDetailCreate(BaseModel):
    education_level: str  # school_8_10, school_11_12, diploma, college_grad
    current_class_year: Optional[str] = None
    board_university: Optional[str] = None
    stream: Optional[str] = None
    subjects: Optional[str] = None
    diploma_branch: Optional[str] = None
    degree: Optional[str] = None
    semester: Optional[str] = None
    academic_interests: Optional[str] = None

class EducationDetailResponse(EducationDetailCreate):
    id: int
    profile_id: int
    updated_at: datetime.datetime

    class Config:
        from_attributes = True

# --- STUDENT PROFILE ---
class StudentProfileResponse(BaseModel):
    id: int
    user_id: int
    full_name: str
    email: str
    mobile: Optional[str]
    dob: Optional[str]
    guardian_consent: bool
    current_journey_step: str
    preferred_mode: str
    target_career_id: Optional[int] = None
    target_career_title: Optional[str] = None
    clarity_careers_json: Optional[List[int]] = None
    streak_days: int
    education: Optional[EducationDetailResponse] = None

    class Config:
        from_attributes = True

class StudentProfileUpdate(BaseModel):
    preferred_mode: Optional[str] = None
    target_career_id: Optional[int] = None
    clarity_careers_json: Optional[List[int]] = None
    current_journey_step: Optional[str] = None
    bio: Optional[str] = None

# --- CAREERS ---
class CareerRequirementResponse(BaseModel):
    id: int
    requirement_type: str
    title: str
    description: str
    is_mandatory: bool
    official_link: Optional[str] = None

    class Config:
        from_attributes = True

class CareerSkillResponse(BaseModel):
    skill_id: int
    skill_name: str
    category: str
    importance_weight: float
    min_proficiency_needed: int

class CareerSimpleResponse(BaseModel):
    id: int
    category_id: int
    category_name: str
    title: str
    slug: str
    summary: str
    what_they_do: str
    min_education_level: str
    stream_flexibility: Optional[str] = None
    avg_salary_inr: str
    growth_rate: str
    official_source_url: Optional[str] = None
    official_authority_name: Optional[str] = None
    last_verified_date: Optional[str] = None
    icon_name: str

    class Config:
        from_attributes = True

class CareerDetailResponse(CareerSimpleResponse):
    requirements: List[CareerRequirementResponse] = []
    skills: List[CareerSkillResponse] = []

# --- QUESTIONS & ASSESSMENT ---
class QuestionOptionResponse(BaseModel):
    id: int
    option_key: str
    text: str

    class Config:
        from_attributes = True

class QuestionResponse(BaseModel):
    id: int
    category: str
    education_level: str
    difficulty: str
    skill_name: Optional[str] = None
    text: str
    scoring_type: str
    options: List[QuestionOptionResponse] = []

    class Config:
        from_attributes = True

class AssessmentStartRequest(BaseModel):
    mode: str = "fixed"  # fixed, not_fixed, clarity
    target_career_id: Optional[int] = None
    clarity_career_ids: Optional[List[int]] = None

class AssessmentAnswerSubmit(BaseModel):
    question_id: int
    selected_option_id: int
    response_time_seconds: Optional[int] = 10

class CareerRecommendationResponse(BaseModel):
    career_id: int
    title: str
    category_name: str
    slug: str
    compatibility_score: float
    alignment_category: str
    explanation: Optional[str] = None
    rank_order: int

class AssessmentResultResponse(BaseModel):
    id: int
    session_id: int
    overall_score: float
    aptitude_score: float
    interest_score: float
    technical_score: float
    soft_skills_score: float
    skill_breakdown: Dict[str, float]
    insights: List[str]
    recommended_actions: List[str]
    is_unlocked: bool
    unlocked_at: Optional[datetime.datetime] = None
    recommendations: List[CareerRecommendationResponse] = []
    target_career: Optional[CareerSimpleResponse] = None
    eligibility_analysis: Optional[Dict[str, Any]] = None

# --- ROADMAP & PROGRESS ---
class RoadmapStageResponse(BaseModel):
    id: int
    stage_number: int
    title: str
    objective: str
    recommended_subjects: Optional[str] = None
    entrance_exams: Optional[str] = None
    resources: Optional[str] = None
    practical_projects: Optional[str] = None
    expected_outcome: Optional[str] = None
    official_source_url: Optional[str] = None
    is_completed: bool = False

    class Config:
        from_attributes = True

class CareerRoadmapResponse(BaseModel):
    id: int
    career_id: int
    career_title: str
    title: str
    description: Optional[str] = None
    stages: List[RoadmapStageResponse] = []

class SkillProgressUpdate(BaseModel):
    skill_id: int
    proficiency_level: int
    evidence_note: Optional[str] = None

class RoadmapStageUpdate(BaseModel):
    stage_id: int
    is_completed: bool
    notes: Optional[str] = None

# --- COURSES ---
class CourseResponse(BaseModel):
    id: int
    provider_name: str
    title: str
    description: str
    category: str
    skills_taught: List[str]
    difficulty: str
    price_inr: float
    is_free: bool
    duration: str
    certificate_info: str
    course_url: str
    affiliate_url: Optional[str] = None
    why_recommended: Optional[str] = None

    class Config:
        from_attributes = True

# --- PAYMENTS ---
class RazorpayOrderCreate(BaseModel):
    session_id: Optional[int] = None
    item_type: str = "analytics_report"  # analytics_report or premium_sub

class RazorpayOrderResponse(BaseModel):
    order_id: str
    amount: float
    currency: str = "INR"
    key_id: str
    item_type: str
    reference_id: Optional[str] = None

class RazorpayVerifyRequest(BaseModel):
    order_id: str
    payment_id: str
    signature: str

# --- ADMIN & FEEDBACK ---
class FeedbackCreate(BaseModel):
    rating: int
    comment: str
    page_context: Optional[str] = None

class AdminStatsResponse(BaseModel):
    total_students: int
    total_assessments: int
    unlocked_reports: int
    total_revenue_inr: float
    education_distribution: Dict[str, int]
    popular_careers: List[Dict[str, Any]]
    recent_registrations: List[Dict[str, Any]]
