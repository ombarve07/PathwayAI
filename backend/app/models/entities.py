import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from backend.app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(150), nullable=False)
    mobile = Column(String(20), nullable=True)
    dob = Column(String(20), nullable=True)
    guardian_consent = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    profile = relationship("StudentProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    target_career_id = Column(Integer, ForeignKey("careers.id", ondelete="SET NULL"), nullable=True)
    current_journey_step = Column(String(50), default="registered")  # registered, education_set, career_chosen, assessed, report_unlocked
    preferred_mode = Column(String(50), default="fixed")  # fixed, not_fixed, clarity
    clarity_careers_json = Column(JSON, nullable=True)  # List of career ids for clarity mode
    bio = Column(Text, nullable=True)
    streak_days = Column(Integer, default=1)
    last_active_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="profile")
    target_career = relationship("Career", foreign_keys=[target_career_id])
    education_detail = relationship("EducationDetail", back_populates="profile", uselist=False, cascade="all, delete-orphan")
    assessment_sessions = relationship("AssessmentSession", back_populates="student")
    skill_progresses = relationship("StudentSkillProgress", back_populates="student")
    projects = relationship("StudentProject", back_populates="student")
    student_courses = relationship("StudentCourse", back_populates="student")


class EducationDetail(Base):
    __tablename__ = "education_details"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), unique=True, nullable=False)
    education_level = Column(String(50), nullable=False)  # school_8_10, school_11_12, diploma, college_grad
    current_class_year = Column(String(100), nullable=True)
    board_university = Column(String(150), nullable=True)
    stream = Column(String(100), nullable=True)  # Science (PCM/PCB), Commerce, Arts/Humanities
    subjects = Column(String(255), nullable=True)
    diploma_branch = Column(String(100), nullable=True)
    degree = Column(String(100), nullable=True)  # B.Tech, B.Sc, B.Com, BA, etc.
    semester = Column(String(50), nullable=True)
    academic_interests = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    profile = relationship("StudentProfile", back_populates="education_detail")


class CareerCategory(Base):
    __tablename__ = "career_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)  # Science and Technology, Commerce, Business, Arts and Humanities
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    careers = relationship("Career", back_populates="category")


class Career(Base):
    __tablename__ = "careers"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("career_categories.id"), nullable=False)
    title = Column(String(150), unique=True, nullable=False)
    slug = Column(String(150), unique=True, nullable=False)
    summary = Column(Text, nullable=False)
    what_they_do = Column(Text, nullable=False)
    min_education_level = Column(String(50), default="school_11_12")
    stream_flexibility = Column(Text, nullable=True)
    avg_salary_inr = Column(String(100), default="₹6,00,000 - ₹18,00,000 per annum")
    growth_rate = Column(String(50), default="High (+18% YoY)")
    official_source_url = Column(String(500), nullable=True)
    official_authority_name = Column(String(150), nullable=True)
    last_verified_date = Column(String(50), default="2026-01-15")
    icon_name = Column(String(50), default="briefcase")
    is_active = Column(Boolean, default=True)

    category = relationship("CareerCategory", back_populates="careers")
    requirements = relationship("CareerRequirement", back_populates="career", cascade="all, delete-orphan")
    career_skills = relationship("CareerSkill", back_populates="career", cascade="all, delete-orphan")
    roadmaps = relationship("CareerRoadmap", back_populates="career", cascade="all, delete-orphan")


class CareerRequirement(Base):
    __tablename__ = "career_requirements"

    id = Column(Integer, primary_key=True, index=True)
    career_id = Column(Integer, ForeignKey("careers.id", ondelete="CASCADE"), nullable=False)
    requirement_type = Column(String(50), nullable=False)  # academic, entrance_exam, certification, eligibility_rule
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    is_mandatory = Column(Boolean, default=True)
    official_link = Column(String(500), nullable=True)

    career = relationship("Career", back_populates="requirements")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(50), nullable=False)  # technical, analytical, creative, soft_skill, practical
    description = Column(Text, nullable=True)

    career_associations = relationship("CareerSkill", back_populates="skill")


class CareerSkill(Base):
    __tablename__ = "career_skills"

    id = Column(Integer, primary_key=True, index=True)
    career_id = Column(Integer, ForeignKey("careers.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    importance_weight = Column(Float, default=1.0)  # Relative weight in suitability scoring (0.5 - 2.0)
    min_proficiency_needed = Column(Integer, default=60)  # Threshold 0-100

    career = relationship("Career", back_populates="career_skills")
    skill = relationship("Skill", back_populates="career_associations")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_code = Column(String(50), unique=True, index=True, nullable=True)
    module_id = Column(Integer, ForeignKey("assessment_modules.id", ondelete="SET NULL"), nullable=True)
    career_id = Column(Integer, ForeignKey("careers.id", ondelete="SET NULL"), nullable=True)  # NULL if universal
    category = Column(String(50), nullable=False)  # aptitude, logical, technical, domain, interest, personality, situational
    sub_topic = Column(String(100), nullable=True)
    education_level = Column(String(50), default="all")  # all, school_8_10, school_11_12, diploma, college_grad
    difficulty = Column(String(20), default="medium")  # easy, medium, hard
    skill_name = Column(String(100), nullable=True)
    text = Column(Text, nullable=False)
    question_type = Column(String(50), default="multiple_choice")  # multiple_choice, likert, scenario
    scoring_type = Column(String(30), default="accuracy")  # accuracy, likert, weighted
    explanation = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    module = relationship("AssessmentModule", back_populates="questions")
    career = relationship("Career")
    options = relationship("QuestionOption", back_populates="question", cascade="all, delete-orphan")


class AssessmentModule(Base):
    __tablename__ = "assessment_modules"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(150), nullable=False)
    module_number = Column(Integer, nullable=False)
    primary_dimension = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)

    questions = relationship("Question", back_populates="module")


class AssessmentConfiguration(Base):
    __tablename__ = "assessment_configurations"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    mode = Column(String(50), nullable=False)  # fixed, not_fixed, clarity
    career_id = Column(Integer, ForeignKey("careers.id", ondelete="SET NULL"), nullable=True)
    education_level = Column(String(50), default="all")
    description = Column(Text, nullable=True)
    modules_config_json = Column(JSON, nullable=True)
    target_questions_count = Column(Integer, default=25)
    time_limit_minutes = Column(Integer, default=30)
    is_active = Column(Boolean, default=True)

    career = relationship("Career")


class QuestionOption(Base):
    __tablename__ = "question_options"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    option_key = Column(String(10), nullable=False)  # A, B, C, D
    text = Column(Text, nullable=False)
    score_value = Column(Float, default=0.0)  # For accuracy: 1.0 or 0.0. For likert: 1 to 5.
    is_correct = Column(Boolean, default=False)
    skill_weights_json = Column(JSON, nullable=True)  # e.g., {"Problem-solving": 1.0}

    question = relationship("Question", back_populates="options")


class AssessmentSession(Base):
    __tablename__ = "assessment_sessions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    mode = Column(String(30), default="fixed")  # fixed, not_fixed, clarity
    target_career_id = Column(Integer, ForeignKey("careers.id", ondelete="SET NULL"), nullable=True)
    config_id = Column(Integer, ForeignKey("assessment_configurations.id", ondelete="SET NULL"), nullable=True)
    clarity_career_ids_json = Column(JSON, nullable=True)
    current_stage = Column(String(50), default="core")  # core, adaptive, completed
    adaptive_career_ids_json = Column(JSON, nullable=True)
    education_level = Column(String(50), nullable=False)
    status = Column(String(30), default="in_progress")  # in_progress, completed
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    student = relationship("StudentProfile", back_populates="assessment_sessions")
    target_career = relationship("Career", foreign_keys=[target_career_id])
    config = relationship("AssessmentConfiguration", foreign_keys=[config_id])
    answers = relationship("StudentAnswer", back_populates="session", cascade="all, delete-orphan")
    result = relationship("AssessmentResult", back_populates="session", uselist=False, cascade="all, delete-orphan")


class StudentAnswer(Base):
    __tablename__ = "student_answers"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("assessment_sessions.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    selected_option_id = Column(Integer, ForeignKey("question_options.id", ondelete="CASCADE"), nullable=True)
    answer_value = Column(Float, default=0.0)
    response_time_seconds = Column(Integer, default=15)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    session = relationship("AssessmentSession", back_populates="answers")
    question = relationship("Question")
    selected_option = relationship("QuestionOption")


class AssessmentResult(Base):
    __tablename__ = "assessment_results"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("assessment_sessions.id", ondelete="CASCADE"), unique=True, nullable=False)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    aptitude_score = Column(Float, default=0.0)
    interest_score = Column(Float, default=0.0)
    technical_score = Column(Float, default=0.0)
    soft_skills_score = Column(Float, default=0.0)
    overall_score = Column(Float, default=0.0)
    dimensions_breakdown_json = Column(JSON, nullable=True)  # 15 Module scores
    skill_breakdown_json = Column(JSON, nullable=True)  # {"Math": 85, "Logic": 90, ...}
    evidence_status_json = Column(JSON, nullable=True)  # {"career_id": "high_confidence"|"more_evidence_needed"}
    alternative_recommendations_json = Column(JSON, nullable=True)  # Top alternative careers outside selected
    insights_json = Column(JSON, nullable=True)  # List of string insights
    recommended_actions_json = Column(JSON, nullable=True)  # List of actionable next steps
    is_unlocked = Column(Boolean, default=False)  # Unlocked upon ₹99 payment
    unlocked_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    session = relationship("AssessmentSession", back_populates="result")
    recommendations = relationship("CareerRecommendation", back_populates="result", cascade="all, delete-orphan")


class CareerRecommendation(Base):
    __tablename__ = "career_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    result_id = Column(Integer, ForeignKey("assessment_results.id", ondelete="CASCADE"), nullable=False)
    career_id = Column(Integer, ForeignKey("careers.id", ondelete="CASCADE"), nullable=False)
    compatibility_score = Column(Float, default=0.0)  # 0-100%
    alignment_category = Column(String(50), default="Promising alignment")  # Strong alignment, Promising, Developing, Exploratory
    evidence_status = Column(String(50), default="high_confidence")  # high_confidence, moderate, more_evidence_needed
    is_selected_choice = Column(Boolean, default=False)  # True if selected by student in Fixed or Clarity
    explanation = Column(Text, nullable=True)
    rank_order = Column(Integer, default=1)

    result = relationship("AssessmentResult", back_populates="recommendations")
    career = relationship("Career")


class CareerRoadmap(Base):
    __tablename__ = "career_roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    career_id = Column(Integer, ForeignKey("careers.id", ondelete="CASCADE"), nullable=False)
    education_level = Column(String(50), default="all")  # school_8_10, school_11_12, higher_ed, all
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)

    career = relationship("Career", back_populates="roadmaps")
    stages = relationship("RoadmapStage", back_populates="roadmap", cascade="all, delete-orphan")


class RoadmapStage(Base):
    __tablename__ = "roadmap_stages"

    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("career_roadmaps.id", ondelete="CASCADE"), nullable=False)
    stage_number = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    objective = Column(Text, nullable=False)
    recommended_subjects = Column(String(255), nullable=True)
    entrance_exams = Column(String(255), nullable=True)
    resources = Column(Text, nullable=True)
    practical_projects = Column(Text, nullable=True)
    expected_outcome = Column(Text, nullable=True)
    official_source_url = Column(String(500), nullable=True)

    roadmap = relationship("CareerRoadmap", back_populates="stages")


class StudentRoadmapProgress(Base):
    __tablename__ = "student_roadmap_progress"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    stage_id = Column(Integer, ForeignKey("roadmap_stages.id", ondelete="CASCADE"), nullable=False)
    is_completed = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    completed_at = Column(DateTime, nullable=True)


class CourseProvider(Base):
    __tablename__ = "course_providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    website_url = Column(String(255), nullable=True)
    default_commission_rate = Column(Float, default=15.0)  # percentage

    courses = relationship("Course", back_populates="provider")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("course_providers.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), default="Technology")
    skills_taught_json = Column(JSON, nullable=False)  # ["Python", "Algorithms"]
    difficulty = Column(String(50), default="Beginner")
    suitable_education_levels_json = Column(JSON, nullable=True)
    price_inr = Column(Float, default=0.0)  # 0 = Free
    is_free = Column(Boolean, default=False)
    duration = Column(String(50), default="6 Weeks")
    certificate_info = Column(String(100), default="Certificate of Completion included")
    course_url = Column(String(500), nullable=False)
    affiliate_url = Column(String(500), nullable=True)
    commission_rate = Column(Float, default=10.0)
    is_active = Column(Boolean, default=True)

    provider = relationship("CourseProvider", back_populates="courses")


class StudentCourse(Base):
    __tablename__ = "student_courses"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="enrolled")  # enrolled, in_progress, completed
    progress_percent = Column(Integer, default=0)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    student = relationship("StudentProfile", back_populates="student_courses")
    course = relationship("Course")


class StudentSkillProgress(Base):
    __tablename__ = "student_skill_progress"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    proficiency_level = Column(Integer, default=20)  # 0 - 100
    is_verified = Column(Boolean, default=False)
    evidence_note = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    student = relationship("StudentProfile", back_populates="skill_progresses")
    skill = relationship("Skill")


class StudentProject(Base):
    __tablename__ = "student_projects"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    github_or_file_url = Column(String(500), nullable=True)
    skills_applied = Column(String(255), nullable=True)
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("StudentProfile", back_populates="projects")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    order_id = Column(String(100), unique=True, index=True, nullable=False)
    payment_id = Column(String(100), nullable=True)
    signature = Column(String(255), nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="INR")
    status = Column(String(50), default="created")  # created, success, failed
    item_type = Column(String(50), default="analytics_report")  # analytics_report, premium_sub
    reference_id = Column(String(100), nullable=True)  # session_id or plan_code
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="payments")


class PremiumPlan(Base):
    __tablename__ = "premium_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    price_inr = Column(Float, default=999.0)
    duration_days = Column(Integer, default=365)
    features_json = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=True)


class AffiliateClick(Base):
    __tablename__ = "affiliate_clicks"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    referral_code = Column(String(50), default="PATHWAY_AI_REF")
    ip_address = Column(String(50), nullable=True)
    clicked_at = Column(DateTime, default=datetime.datetime.utcnow)


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, default=5)
    comment = Column(Text, nullable=False)
    page_context = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="feedbacks")
