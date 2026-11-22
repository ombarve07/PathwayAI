import datetime
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal, engine, Base
from backend.app.core.security import get_password_hash
from backend.app.models.entities import (
    User, CareerCategory, Career, CareerRequirement, Skill, CareerSkill,
    Question, QuestionOption, CareerRoadmap, RoadmapStage, CourseProvider,
    Course, PremiumPlan, AssessmentModule, AssessmentConfiguration
)
from backend.app.analytics.career_mapping import MODULE_DEFINITIONS
from backend.app.data.assessment_configs import ASSESSMENT_CONFIGURATIONS
from backend.app.data.universal_question_bank import UNIVERSAL_QUESTIONS
from backend.app.data.profession_question_bank import PROFESSION_QUESTIONS

def seed_database():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        print("Starting comprehensive database seeding...")

        # 1. Admin User
        admin_user = db.query(User).filter(User.email == "admin@pathway.ai").first()
        if not admin_user:
            admin_user = User(
                email="admin@pathway.ai",
                password_hash=get_password_hash("Admin@12345"),
                full_name="PATHWAY Admin",
                is_admin=True,
                is_active=True
            )
            db.add(admin_user)
            db.commit()

        # 2. Categories
        cat_sci = db.query(CareerCategory).filter(CareerCategory.slug == "science-technology").first()
        if not cat_sci:
            cat_sci = CareerCategory(
                name="Science and Technology",
                slug="science-technology",
                description="STEM careers focused on engineering, medicine, software, artificial intelligence, biotechnology and scientific exploration."
            )
            db.add(cat_sci)

        cat_comm = db.query(CareerCategory).filter(CareerCategory.slug == "commerce-business-arts-humanities").first()
        if not cat_comm:
            cat_comm = CareerCategory(
                name="Commerce, Business, Arts and Humanities",
                slug="commerce-business-arts-humanities",
                description="Careers spanning financial leadership, civil services, legal advocacy, creative design, journalism, psychology and enterprise management."
            )
            db.add(cat_comm)
        db.commit()
        db.refresh(cat_sci)
        db.refresh(cat_comm)

        # 3. Core Skills
        skills_data = [
            ("Logical Reasoning", "analytical", "Ability to analyze sequences, deductive problems, and structured arguments."),
            ("Numerical Aptitude", "analytical", "Facility with mathematics, arithmetic computations, statistics, and financial modeling."),
            ("Verbal Reasoning", "analytical", "Reading comprehension, vocabulary nuances, and articulate written expression."),
            ("Algorithmic Thinking", "technical", "Step-by-step logic, complexity awareness, and systematic decomposition of problems."),
            ("Python & Programming", "technical", "Writing maintainable software code, debugging, and computational execution."),
            ("Data Interpretation", "technical", "Extracting meaningful insights from charts, graphs, tables, and large datasets."),
            ("Biology Fundamentals", "technical", "Physiology, genetics, anatomy, and understanding living biological systems."),
            ("Scientific Method", "technical", "Hypothesis testing, laboratory precision, and evidence-driven experimentation."),
            ("Spatial Reasoning", "analytical", "3D mental modeling, geometric visualization, and architectural drafting."),
            ("Financial Acumen", "practical", "Understanding balance sheets, taxation principles, risk profiling, and corporate audits."),
            ("Legal Argumentation", "analytical", "Statutory interpretation, case law analysis, and constitutional logic."),
            ("Visual Creativity", "creative", "Aesthetics, colour harmony, typography, composition, and visual communication."),
            ("Situational Judgement", "practical", "Ethical decision-making under public policy, organizational or patient stress."),
            ("Communication & Empathy", "soft_skill", "Active listening, patient counseling, and persuasive oral delivery."),
            ("Leadership & Teamwork", "soft_skill", "Delegation, collective goal attainment, and conflict resolution.")
        ]

        skill_map = {}
        for s_name, s_cat, s_desc in skills_data:
            sk = db.query(Skill).filter(Skill.name == s_name).first()
            if not sk:
                sk = Skill(name=s_name, category=s_cat, description=s_desc)
                db.add(sk)
                db.commit()
                db.refresh(sk)
            skill_map[s_name] = sk

        # 4. Define 30 Professions
        careers_def = [
            # CATEGORY 1: Science and Technology (15)
            {
                "category_id": cat_sci.id,
                "title": "Doctor (MBBS)",
                "slug": "doctor-mbbs",
                "summary": "Medical practitioners diagnosed to prevent, treat, and alleviate human diseases while safeguarding public health.",
                "what_they_do": "Doctors examine patients, order and interpret diagnostic laboratory tests, prescribe pharmacological regimens, perform medical procedures, and conduct life-saving emergency care.",
                "min_education_level": "school_11_12",
                "stream_flexibility": "Class 12th with mandatory Physics, Chemistry, and Biology (PCB) as mandated by NMC regulations.",
                "avg_salary_inr": "₹8,00,000 - ₹30,00,000+ per annum",
                "growth_rate": "Very High (+22% YoY)",
                "official_source_url": "https://www.nmc.org.in",
                "official_authority_name": "National Medical Commission (NMC)",
                "icon_name": "heart-pulse",
                "skills": [("Biology Fundamentals", 2.0), ("Communication & Empathy", 1.8), ("Situational Judgement", 1.7), ("Scientific Method", 1.5)],
                "requirements": [
                    ("academic", "10+2 with PCB", "Minimum 50% marks in Physics, Chemistry, Biology aggregate (40% for reserved categories).", True, "https://neet.nta.nic.in"),
                    ("entrance_exam", "NEET-UG", "National Eligibility cum Entrance Test conducted annually by the National Testing Agency (NTA).", True, "https://neet.nta.nic.in"),
                    ("certification", "NMC Compulsory Rotatory Internship", "Completion of 4.5 years MBBS degree followed by a mandatory 1-year clinical rotatory internship.", True, "https://www.nmc.org.in")
                ],
                "stages": [
                    (1, "Foundation Phase (Class 8th–10th)", "Master NCERT Science fundamentals, cellular biology, and analytical reasoning.", "Science, Mathematics", "Olympiads / NTSE", "NCERT Books, Khan Academy", "Human anatomy chart project, school science exhibition", "Clear conceptual understanding of biological sciences."),
                    (2, "Pre-Medical Preparation (Class 11th–12th)", "Extensive preparation in Physics, Chemistry, and Biology syllabus.", "Physics, Chemistry, Biology (PCB)", "NEET-UG", "NCERT Line-by-Line Biology, Standard NEET prep guides", "Mock tests, biology specimen dissection records", "Qualify NEET-UG with competitive All-India Rank."),
                    (3, "Undergraduate MBBS Degree (Years 1–4.5)", "Undergo preclinical, paraclinical, and clinical medical modules in a recognized medical college.", "Anatomy, Physiology, Pharmacology, Pathology, Surgery, Medicine", "NExT / University Proff Exams", "Marrow, Prepladder, Guyton Physiology", "Hospital clinical postings, bedside case presentations", "Clear professional exams with distinction."),
                    (4, "Compulsory Internship & Licensing (Year 5)", "Gain hands-on clinical rotational experience in medicine, surgery, obstetrics, and casualty.", "Emergency Medicine, Patient Triage", "NExT Step 2", "Hospital logbooks", "365 days rotatory clinical duties across departments", "Permanent Registration with State Medical Council / NMC."),
                    (5, "Postgraduate Specialization (MD / MS)", "Specialize in cardiology, neurosurgery, pediatrics, or radiology.", "Specialized Clinical Sciences", "NEET-PG / INI-CET", "Clinical Research journals", "Dissertation, thesis defense, surgical cases", "Attain Specialist or Consultant Doctor status.")
                ]
            },
            {
                "category_id": cat_sci.id,
                "title": "Engineer",
                "slug": "engineer",
                "summary": "Design, innovate, construct, and optimize complex technical systems, machinery, and infrastructure.",
                "what_they_do": "Engineers apply mathematics and scientific principles to solve industrial challenges, model structural stress, build sustainable energy mechanisms, and develop hardware devices.",
                "min_education_level": "school_11_12",
                "stream_flexibility": "Class 12th with PCM or 3-year AICTE recognized Polytechnic Diploma.",
                "avg_salary_inr": "₹5,00,000 - ₹20,00,000 per annum",
                "growth_rate": "High (+15% YoY)",
                "official_source_url": "https://www.aicte-india.org",
                "official_authority_name": "All India Council for Technical Education (AICTE)",
                "icon_name": "cpu",
                "skills": [("Logical Reasoning", 1.8), ("Numerical Aptitude", 1.8), ("Spatial Reasoning", 1.6), ("Algorithmic Thinking", 1.4)],
                "requirements": [
                    ("academic", "10+2 with PCM", "Physics, Chemistry, Mathematics with minimum 60% aggregate.", True, "https://jeemain.nta.nic.in"),
                    ("entrance_exam", "JEE Main / Advanced / State CET", "National and state-level engineering entrance exams.", True, "https://jeemain.nta.nic.in")
                ],
                "stages": [
                    (1, "School Phase (8th-10th)", "Strengthen physics concepts, algebra, geometry and numerical calculation.", "Science, Math", "NTSE, Math Olympiad", "NCERT, Foundation Science", "Robotics club projects, scientific fair models", "Solid analytical foundation."),
                    (2, "Higher Secondary (11th-12th)", "Rigorous practice of mechanics, calculus, thermodynamics and electrodynamics.", "Physics, Chemistry, Math (PCM)", "JEE Main, BITSAT, State CET", "HC Verma Physics, Cengage Math", "Solving JEE previous year question papers", "Admission to an AICTE / IIT / NIT engineering program."),
                    (3, "B.Tech / B.E. Core Studies (Years 1-4)", "Study core discipline subjects, lab simulations, CAD drafting, and embedded circuits.", "Discipline Specific Core", "Semester University Exams", "NPTEL, Coursera, MIT OpenCourseWare", "Final Year Capstone Design Project", "Accredited Engineering degree."),
                    (4, "Industry Internship & Placement", "Industrial training in core manufacturing or R&D firms.", "Industry Standards, QA", "GATE (optional for PSUs)", "IEEE Journals, Tech Workshops", "6-month industrial internship report", "Placement in leading engineering enterprises or PSUs.")
                ]
            },
            {
                "category_id": cat_sci.id,
                "title": "Data Scientist",
                "slug": "data-scientist",
                "summary": "Transforms complex raw datasets into predictive mathematical models and strategic organizational decisions.",
                "what_they_do": "Clean terabytes of unstructured data, design statistical experiments, train machine learning regressors and classifiers, and build automated enterprise intelligence pipelines.",
                "min_education_level": "college_grad",
                "stream_flexibility": "Open to graduates in Computer Science, Mathematics, Statistics, Economics, or Engineering.",
                "avg_salary_inr": "₹8,50,000 - ₹28,00,000 per annum",
                "growth_rate": "Exponential (+28% YoY)",
                "official_source_url": "https://nasscom.in",
                "official_authority_name": "NASSCOM FutureSkills",
                "icon_name": "database",
                "skills": [("Data Interpretation", 2.0), ("Python & Programming", 1.9), ("Numerical Aptitude", 1.8), ("Logical Reasoning", 1.6)],
                "requirements": [
                    ("academic", "Undergraduate Degree", "B.Tech, B.Sc. Statistics, BCA, or B.Sc. Math with strong quantitative foundation.", True, "https://nasscom.in"),
                    ("certification", "Data Science & Machine Learning Portfolio", "Demonstrated GitHub repositories, Kaggle competitions, and end-to-end data pipelines.", True, "https://kaggle.com")
                ],
                "stages": [
                    (1, "School Foundation (8th-10th)", "Learn logic, probability, spreadsheets, and intro programming.", "Math, Computer Science", "Coding Olympiads", "Scratch, Python Basics, Khan Academy Math", "Analyzing school survey data with spreadsheets", "Mathematical curiosity."),
                    (2, "Pre-University (11th-12th)", "Master calculus, linear equations, probability and statistics.", "PCM or Commerce with Math", "CUET, JEE Main", "NCERT Math, Introductory Python", "Predictive script for cricket match scores", "Enrolment in quantitative degree."),
                    (3, "Undergraduate Training (College)", "Deep dive into Linear Algebra, Multivariable Calculus, Pandas, Scikit-learn, SQL.", "Algorithms, Statistics, Machine Learning", "Kaggle Competitions", "StatQuest, Fast.ai, CS229", "End-to-end customer churn prediction pipeline", "Published portfolio of predictive models."),
                    (4, "Professional Career & Specialization", "Deploy ML pipelines into cloud production environments.", "MLOps, Docker, AWS/GCP, Big Data", "AWS Certified Machine Learning", "Research Papers (arXiv)", "Real-time fraud detection deployment", "Senior Data Scientist / Lead Data Architect.")
                ]
            },
            {
                "category_id": cat_sci.id,
                "title": "Software Developer",
                "slug": "software-developer",
                "summary": "Architects, engineers, and tests web, mobile, and cloud software applications powering the digital economy.",
                "what_they_do": "Write clean, modular code, implement data structures and algorithms, design microservices REST APIs, integrate databases, and collaborate using Git version control.",
                "min_education_level": "school_11_12",
                "stream_flexibility": "Flexible pathways: B.Tech, BCA, B.Sc. CS, or self-taught developers with strong GitHub portfolios.",
                "avg_salary_inr": "₹6,00,000 - ₹25,00,000+ per annum",
                "growth_rate": "Very High (+20% YoY)",
                "official_source_url": "https://nasscom.in",
                "official_authority_name": "NASSCOM IT-BPM Council",
                "icon_name": "code-slash",
                "skills": [("Algorithmic Thinking", 2.0), ("Python & Programming", 2.0), ("Logical Reasoning", 1.8), ("Leadership & Teamwork", 1.3)],
                "requirements": [
                    ("academic", "10+2 / Diploma / Degree", "Formal degree in CS/IT or validated coding competency.", True, "https://aicte-india.org"),
                    ("certification", "Full Stack / DSA Proficiency", "Mastery of Data Structures & Algorithms, REST APIs, Git, and relational databases.", True, "https://leetcode.com")
                ],
                "stages": [
                    (1, "Curiosity & Logic (8th-10th)", "Understand boolean logic, loops, conditional branching and build simple web pages.", "Mathematics, Computer Applications", "Bebras Computational Thinking Challenge", "freeCodeCamp, Code.org", "Personal portfolio website with HTML/CSS/JS", "Confidence in algorithmic thinking."),
                    (2, "Pre-College / Diploma (11th-12th)", "Learn object-oriented programming in Python, Java, or C++ and understand basic algorithms.", "Science (PCM) / Computer Science / Diploma", "JEE Main / CET / CUET", "LeetCode (Easy), HackerRank", "Console-based student management system in Python", "Seat in B.Tech / BCA / B.Sc. CS."),
                    (3, "Core Engineering & Full-Stack (College)", "Data Structures, System Design, SQL databases, FastAPI, React/Vue, Git workflows.", "Computer Science Core", "Campus Tech Drives", "GitHub, NeetCode, FullStackOpen", "Full-stack SaaS application with authentication and payment gateway", "High-paying tech placement."),
                    (4, "Scale & Architecture", "Build distributed cloud systems, optimize query latency, and maintain CI/CD pipelines.", "Microservices, Kubernetes, System Design", "System Design Interview Prep", "Martin Fowler Architecture, High Scalability", "Contribution to major open-source repository", "Senior Software Engineer / Tech Lead.")
                ]
            },
            {
                "category_id": cat_sci.id,
                "title": "Artificial Intelligence Engineer",
                "slug": "artificial-intelligence-engineer",
                "summary": "Builds and deploys neural networks, large language models, computer vision, and autonomous agent systems.",
                "what_they_do": "Train deep learning architectures using PyTorch/TensorFlow, optimize model weights, fine-tune open-source LLMs, implement RAG systems, and deploy inference microservices.",
                "min_education_level": "college_grad",
                "stream_flexibility": "Engineering, Mathematics, or Computer Science graduation background.",
                "avg_salary_inr": "₹10,000,000 - ₹35,00,000 per annum",
                "growth_rate": "Hyper Growth (+34% YoY)",
                "official_source_url": "https://indiaai.gov.in",
                "official_authority_name": "IndiaAI / MeitY",
                "icon_name": "sparkles",
                "skills": [("Python & Programming", 2.0), ("Algorithmic Thinking", 1.9), ("Numerical Aptitude", 1.8), ("Data Interpretation", 1.7)],
                "requirements": [
                    ("academic", "B.Tech / M.Tech in CS/AI/Data Science", "Rigorous training in mathematics, neural networks, and computer science.", True, "https://indiaai.gov.in"),
                    ("certification", "Deep Learning Specialization", "Demonstrated competence in Transformer architectures, PyTorch, and CUDA.", True, "https://deeplearning.ai")
                ],
                "stages": [
                    (1, "Foundations (8th-10th)", "Master coordinate geometry, probability, matrices, and introductory Python.", "Mathematics, Science", "Kaggle Micro-courses", "Khan Academy Multivariable, 3Blue1Brown", "Handwritten digit recognition script", "Intuition for mathematical patterns."),
                    (2, "Advanced Preparation (11th-12th)", "Study vector algebra, calculus, discrete math, and algorithms.", "Physics, Chemistry, Math (PCM)", "JEE Main / Advanced", "MIT OCW Linear Algebra, HuggingFace Docs", "Chatbot prototype using NLP APIs", "Strong mathematical foundation."),
                    (3, "Specialized Degree (College)", "Deep neural networks, CNNs, Transformers, Vector Databases, Retrieval Augmented Generation.", "AI, Machine Learning, Operating Systems", "NeurIPS / CVPR workshops", "Fast.ai, Andrej Karpathy Neural Networks", "Custom domain-specific fine-tuned LLM assistant", "AI Engineer job offer."),
                    (4, "Autonomous Agents & Frontier AI", "Scale distributed multi-node GPU model training clusters and real-time agentic workflows.", "GPU Optimization, Triton, LangGraph", "NVIDIA Deep Learning Institute", "arXiv Machine Learning Preprints", "Autonomous research agent production deployment", "Principal AI Scientist.")
                ]
            },
            {
                "category_id": cat_sci.id,
                "title": "Pharmacist",
                "slug": "pharmacist",
                "summary": "Healthcare specialists expert in drug compositions, therapeutic efficacy, dispensing safety, and pharmacology.",
                "what_they_do": "Dispense medications, advise patients on dosages and drug-drug interactions, compound sterile formulations, and conduct pharmaceutical clinical trials.",
                "min_education_level": "school_11_12",
                "stream_flexibility": "Class 12th with Physics, Chemistry, and Biology/Mathematics.",
                "avg_salary_inr": "₹3,50,000 - ₹10,00,000 per annum",
                "growth_rate": "Moderate (+12% YoY)",
                "official_source_url": "https://www.pci.nic.in",
                "official_authority_name": "Pharmacy Council of India (PCI)",
                "icon_name": "capsule",
                "skills": [("Biology Fundamentals", 1.8), ("Scientific Method", 1.7), ("Situational Judgement", 1.5), ("Communication & Empathy", 1.4)],
                "requirements": [
                    ("academic", "10+2 with PCB/PCM", "Pass in 12th with minimum 50% marks in science subjects.", True, "https://www.pci.nic.in"),
                    ("entrance_exam", "GPAT / State CET Pharmacy", "State-level CETs for B.Pharm and GPAT for M.Pharm admissions.", True, "https://gpat.nta.nic.in"),
                    ("certification", "State Pharmacy Council Registered Pharmacist", "Mandatory statutory license to dispense or manufacture medicines.", True, "https://www.pci.nic.in")
                ],
                "stages": [
                    (1, "School Prep (8th-10th)", "Focus on chemistry reactions, organic compounds, and human health.", "Science", "Science Olympiad", "NCERT Chemistry", "Herbal plant extraction exhibit", "Interest in chemical therapeutics."),
                    (2, "Higher Secondary (11th-12th)", "Concentrate on Organic Chemistry mechanisms, solutions, and biology.", "PCB / PCM", "State Pharmacy CET, BITSAT", "NCERT Chemistry & Biology", "Laboratory titrations and synthesis records", "Admission to PCI-approved B.Pharm college."),
                    (3, "B.Pharm Curriculum (Years 1-4)", "Pharmacology, Pharmaceutics, Medicinal Chemistry, Pharmacognosy, and Hospital Pharmacy.", "Pharmaceutical Sciences", "College Semester Exams", "Tripathi Pharmacology, Remington", "Hospital training and formulation lab project", "Registered Pharmacist statutory license."),
                    (4, "Clinical or Industrial Role", "Work in formulation research, regulatory affairs, quality assurance, or clinical pharmacy.", "GMP, Clinical Trials, Pharmacovigilance", "GPAT for M.Pharm", "IP/USP Pharmacopoeia", "Drug stability test report", "Production Manager / Clinical Trial Specialist.")
                ]
            },
            {
                "category_id": cat_sci.id,
                "title": "Architect",
                "slug": "architect",
                "summary": "Creates the design, spatial planning, and aesthetic blueprints for buildings, homes, and urban skylines.",
                "what_they_do": "Draft 2D and 3D architectural elevations, calculate structural load balances, select sustainable building materials, and supervise site construction compliance.",
                "min_education_level": "school_11_12",
                "stream_flexibility": "Class 12th with Physics, Chemistry, and Mathematics (PCM mandatory as per CoA).",
                "avg_salary_inr": "₹5,00,000 - ₹18,00,000 per annum",
                "growth_rate": "Steady (+14% YoY)",
                "official_source_url": "https://www.coa.gov.in",
                "official_authority_name": "Council of Architecture (CoA)",
                "icon_name": "building",
                "skills": [("Spatial Reasoning", 2.0), ("Visual Creativity", 1.9), ("Numerical Aptitude", 1.5), ("Logical Reasoning", 1.5)],
                "requirements": [
                    ("academic", "10+2 with PCM", "Minimum 50% marks in Physics, Chemistry, Mathematics and 50% overall aggregate.", True, "https://www.coa.gov.in"),
                    ("entrance_exam", "NATA / JEE Main Paper 2", "National Aptitude Test in Architecture (NATA) conducted by CoA.", True, "https://www.nata.in"),
                    ("certification", "CoA Registered Architect License", "Mandatory statutory registration to practice architecture in India.", True, "https://www.coa.gov.in")
                ],
                "stages": [
                    (1, "Visual Foundation (8th-10th)", "Develop freehand perspective sketching, geometry, and appreciation for historic buildings.", "Math, Fine Arts", "Drawing competitions", "Perspective drawing books", "Cardboard miniature house model", "Keen sense of 3D spatial proportion."),
                    (2, "NATA Preparation (11th-12th)", "Prepare for 2D/3D visual perception, architectural awareness, and PCM.", "PCM", "NATA, JEE Main Paper 2", "NATA Question Banks, CoA Guidelines", "Architectural sketch portfolio", "Admission to 5-year B.Arch program."),
                    (3, "B.Arch Degree (Years 1-5)", "Architectural design studio, building materials, structures, climatology, and urban planning.", "Architecture Design Studios", "CoA Internal Reviews", "Ching Architectural Graphics, ArchDaily", "Comprehensive Thesis Project (e.g. Sustainable Eco-Hospital)", "Degree completion and CoA Registration number."),
                    (4, "Studio Practice / Firm Leadership", "Execute commercial and residential commissions, interior spatial layouts, and LEED certifications.", "BIM, Revit, AutoCAD, Sustainable Design", "LEED Green Associate", "Architectural Digest, Indian Architect & Builder", "Execution of live public infrastructure project", "Chief Architect / Principal Partner.")
                ]
            },
            {
                "category_id": cat_sci.id,
                "title": "Pilot",
                "slug": "pilot",
                "summary": "Aviators certified to command commercial airliners, cargo aircraft, and executive aviation transports.",
                "what_they_do": "Calculate flight dispatch manifests, review meteorological weather charts, operate flight management computers, communicate with Air Traffic Control, and execute takeoffs and landings.",
                "min_education_level": "school_11_12",
                "stream_flexibility": "Class 12th with mandatory Physics and Mathematics (or NIOS equivalent).",
                "avg_salary_inr": "₹15,00,000 - ₹50,00,000+ per annum",
                "growth_rate": "Very High (+25% YoY with Indian aviation fleet expansion)",
                "official_source_url": "https://www.dgca.gov.in",
                "official_authority_name": "Directorate General of Civil Aviation (DGCA)",
                "icon_name": "airplane",
                "skills": [("Situational Judgement", 2.0), ("Spatial Reasoning", 1.8), ("Logical Reasoning", 1.6), ("Communication & Empathy", 1.5)],
                "requirements": [
                    ("academic", "10+2 with Physics & Math", "Minimum 50% in Physics and Mathematics from recognized board or NIOS.", True, "https://www.dgca.gov.in"),
                    ("certification", "DGCA Class 1 Medical Fitness", "Rigorous medical examination at an authorized Indian Air Force medical center.", True, "https://www.dgca.gov.in"),
                    ("certification", "Commercial Pilot License (CPL)", "200 hours of flight time + DGCA theory exams (Air Nav, Meteorology, Regulations, Technical).", True, "https://www.dgca.gov.in")
                ],
                "stages": [
                    (1, "Aviation Curiosity (8th-10th)", "Understand aerodynamics, principles of flight, coordinate navigation, and weather patterns.", "Science, Math, Geography", "Aero-modelling clubs", "FAA Pilot's Handbook of Aeronautical Knowledge", "Remote-controlled plane or flight simulation flights", "Strong spatial coordination and reflexes."),
                    (2, "Eligibility & Medicals (11th-12th)", "Score high in Physics and Math, clear DGCA Class 2 medicals followed by Class 1 medicals.", "PCM", "Flying School Entrance / Airline Cadet Assessment", "DGCA Computer Number Portal", "Clearance certificate from DGCA medical board", "DGCA Computer Number issued."),
                    (3, "Flying Training (18-24 Months)", "Complete 200 hours of logged flight time, solo cross-countries, night flying, and instrument flying.", "Aviation Ground School", "DGCA CPL Theory Papers", "Jeppesen Aviation Guides, Oxford Aviation", "200 logged flight hours in Cessna 172 / Diamond DA42", "Issue of Commercial Pilot License (CPL)."),
                    (4, "Type Rating & Airline Induction", "Get type rated on Airbus A320 or Boeing 737 aircraft and undergo airline line training.", "Multi-Crew Cooperation, Jet Orientation", "Airline Simulator Checks", "FCOM (Flight Crew Operating Manual)", "Line checks with senior flight instructor", "First Officer on Indian Scheduled Airline.")
                ]
            },
            {
                "category_id": cat_sci.id,
                "title": "Biotechnologist",
                "slug": "biotechnologist",
                "summary": "Combines biological mechanisms with engineering to engineer vaccines, gene therapies, and industrial enzymes.",
                "what_they_do": "Perform recombinant DNA cloning, culture bioreactor cell lines, sequence microbial genomes, develop biosensors, and conduct bio-fermentation.",
                "min_education_level": "school_11_12",
                "stream_flexibility": "Class 12th with PCB or PCMB.",
                "avg_salary_inr": "₹4,50,000 - ₹15,00,000 per annum",
                "growth_rate": "High (+17% YoY)",
                "official_source_url": "https://dbtindia.gov.in",
                "official_authority_name": "Department of Biotechnology (DBT), Govt. of India",
                "icon_name": "flask",
                "skills": [("Biology Fundamentals", 2.0), ("Scientific Method", 1.9), ("Logical Reasoning", 1.5), ("Data Interpretation", 1.5)],
                "requirements": [
                    ("academic", "10+2 with PCB/PCMB", "Minimum 55% in biology, chemistry and physics.", True, "https://dbtindia.gov.in"),
                    ("entrance_exam", "JEE Main / CUET-UG / GAT-B", "Entrance tests for B.Tech Biotechnology or B.Sc. Biotech programs.", True, "https://rcb.res.in")
                ],
                "stages": [
                    (1, "Biology & Chemistry Roots (8th-10th)", "Explore genetics, plant cells, microorganisms, and chemical solutions.", "Science", "National Science Olympiad", "NCERT, Scientific American", "Yeast fermentation observation experiment", "Curiosity about molecular biology."),
                    (2, "Pre-University (11th-12th)", "Understand biomolecules, DNA replication, photosynthesis, and immunology.", "PCB or PCMB", "CUET-UG, State CETs", "NCERT Biology, Lehninger Principles of Biochemistry", "Laboratory chromatography report", "Admission to B.Tech/B.Sc. Biotechnology."),
                    (3, "Degree & Laboratory Experience (College)", "Molecular biology, bioprocess engineering, bioinformatics, immunology, and tissue culture.", "Biotechnology Core", "Semester Lab Practicals", "NCBI GenBank, BLAST, PyMOL", "CRISPR gene expression lab project", "Published research report or internship with Biocon/Serum Institute."),
                    (4, "Biopharma R&D / Higher Studies", "Develop biosimilars, optimize fermentation yields, or pursue M.Tech/Ph.D.", "GLP, Fermentation, Genomics", "GAT-B / CSIR-NET", "Nature Biotechnology, Cell", "Scale-up of therapeutic monoclonal antibody in 50L bioreactor", "Lead Bioprocess Scientist.")
                ]
            },
            {
                "category_id": cat_sci.id,
                "title": "Research Scientist",
                "slug": "research-scientist",
                "summary": "Investigates uncharted physical, chemical, or planetary phenomena to generate peer-reviewed human knowledge.",
                "what_they_do": "Formulate mathematical hypotheses, design particle collision or spectroscopy experiments, publish research in international journals, and secure scientific grants.",
                "min_education_level": "college_grad",
                "stream_flexibility": "Pure Sciences (Physics, Chemistry, Math, Biology) or Applied Sciences.",
                "avg_salary_inr": "₹7,00,000 - ₹24,00,000 per annum",
                "growth_rate": "Steady (+12% YoY)",
                "official_source_url": "https://dst.gov.in",
                "official_authority_name": "Department of Science and Technology (DST) / CSIR",
                "icon_name": "microscope",
                "skills": [("Scientific Method", 2.0), ("Logical Reasoning", 1.9), ("Numerical Aptitude", 1.8), ("Data Interpretation", 1.7)],
                "requirements": [
                    ("academic", "M.Sc. / Integrated M.Sc. / Ph.D.", "Postgraduate degree in relevant fundamental scientific discipline.", True, "https://csirhrdg.res.in"),
                    ("entrance_exam", "CSIR-UGC NET / GATE / JEST", "National eligibility test for Junior Research Fellowship (JRF).", True, "https://csirnet.nta.nic.in")
                ],
                "stages": [
                    (1, "Scientific Inquiry (8th-10th)", "Question physical anomalies, read scientific biographies, master empirical measurement.", "Science, Math", "Kishore Vaigyanik Protsahan (KVPY) / NTSE", "Feynman Lectures, Cosmos", "Astronomy telescope observation journal", "Deep theoretical passion."),
                    (2, "Pure Science Pathway (11th-12th)", "Excel in theoretical physics, organic chemistry, or abstract mathematics.", "PCM / PCB", "NEST, IISER Aptitude Test (IAT)", "Irodov Physics, Morrison Boyd Chemistry", "Independent paper critique", "Enrolment at IISc, IISER, or NISER."),
                    (3, "BS-MS / Master's Program", "Quantum mechanics, thermodynamics, advanced crystallography, and computational modeling.", "Pure Sciences Core", "JEST / GATE / CSIR NET", "arXiv, Physical Review Letters", "Master's thesis defense with experimental validation", "Award of CSIR-JRF fellowship."),
                    (4, "Doctorate & Postdoctoral Tenure", "Complete doctoral dissertation, defend novel scientific contribution, lead institutional labs.", "Scientific Publishing, Grant Writing", "Ph.D. Defense Committee", "Leading peer-reviewed journal papers", "First-author paper in Nature / Science / Physical Review", "Principal Scientist at TIFR / BARC / CSIR Labs.")
                ]
            },
            {
                "category_id": cat_sci.id,
                "title": "Dentist",
                "slug": "dentist",
                "summary": "Oral healthcare doctors diagnosing diseases of the teeth, gums, jaw, and maxillofacial structures.",
                "what_they_do": "Perform root canal treatments, install dental crowns, conduct orthodontic corrections, perform tooth extractions, and educate patients on oral hygiene.",
                "min_education_level": "school_11_12",
                "stream_flexibility": "Class 12th with Physics, Chemistry, and Biology (PCB).",
                "avg_salary_inr": "₹4,50,000 - ₹18,00,000 per annum",
                "growth_rate": "Moderate (+14% YoY)",
                "official_source_url": "https://dciindia.gov.in",
                "official_authority_name": "Dental Council of India (DCI)",
                "icon_name": "tooth",
                "skills": [("Biology Fundamentals", 1.8), ("Spatial Reasoning", 1.7), ("Communication & Empathy", 1.6), ("Situational Judgement", 1.5)],
                "requirements": [
                    ("academic", "10+2 with PCB", "Minimum 50% aggregate in Physics, Chemistry, and Biology.", True, "https://neet.nta.nic.in"),
                    ("entrance_exam", "NEET-UG", "Qualifying score in National Eligibility cum Entrance Test.", True, "https://neet.nta.nic.in"),
                    ("certification", "DCI State Dental Council Registration", "Statutory license to practice clinical dentistry in India.", True, "https://dciindia.gov.in")
                ],
                "stages": [
                    (1, "School Science (8th-10th)", "Learn human skeletal system, dental anatomy, and fine hand dexterity.", "Science", "School Science Clubs", "NCERT Biology", "Plaster of Paris dental cast model", "Manual dexterity and artistic patience."),
                    (2, "NEET Qualification (11th-12th)", "Rigorous preparation of 11th and 12th PCB syllabus.", "PCB", "NEET-UG", "Standard NEET preparation materials", "Mock full-length NEET papers", "BDS seat allotment via counseling."),
                    (3, "BDS Degree (Years 1-4 + 1 Year Internship)", "Dental materials, oral pathology, conservative dentistry, prosthodontics, and oral surgery.", "Dental Clinical Sciences", "University BDS Exams", "Wheeler's Dental Anatomy, Carranza", "Treated over 100 clinical dental patients in hospital clinic", "Permanent State Dental Council Registration."),
                    (4, "Private Clinic / MDS Specialization", "Establish dental clinic or clear NEET-MDS for Orthodontics or Maxillofacial Surgery.", "Practice Management, Advanced Endodontics", "NEET-MDS", "Journal of Indian Prosthodontic Society", "Establishment of high-tech digital dentistry operatory", "Consultant Dental Specialist.")
                ]
            },
            {
                "category_id": cat_sci.id,
                "title": "Physiotherapist",
                "slug": "physiotherapist",
                "summary": "Rehabilitation specialists restoring physical movement, relieving musculoskeletal pain, and recovering post-stroke mobility.",
                "what_they_do": "Assess posture alignment, design kinetic rehabilitation workouts, administer electrotherapy, mobilize spinal joints, and train athletes for peak injury-free performance.",
                "min_education_level": "school_11_12",
                "stream_flexibility": "Class 12th with Physics, Chemistry, and Biology (PCB).",
                "avg_salary_inr": "₹3,50,000 - ₹12,00,000 per annum",
                "growth_rate": "High (+18% YoY with booming sports and geriatric care in India)",
                "official_source_url": "https://www.iapindia.org",
                "official_authority_name": "Indian Association of Physiotherapists (IAP)",
                "icon_name": "person-walking",
                "skills": [("Biology Fundamentals", 1.8), ("Communication & Empathy", 1.8), ("Situational Judgement", 1.5), ("Scientific Method", 1.4)],
                "requirements": [
                    ("academic", "10+2 with PCB", "Minimum 50% in Physics, Chemistry, Biology from recognized board.", True, "https://www.iapindia.org"),
                    ("entrance_exam", "NEET-UG / State CET Physiotherapy", "Admissions through state common entrance tests or NEET scores.", True, "https://cetcell.mahacet.org"),
                    ("certification", "Bachelor of Physiotherapy (BPT) + 6-month Internship", "Statutory 4.5 years course with clinical rotations.", True, "https://www.iapindia.org")
                ],
                "stages": [
                    (1, "School Foundations (8th-10th)", "Study muscles, joints, locomotion, and physics of levers.", "Science, Physical Education", "Sports & Athletic Competitions", "NCERT, Sports Science blogs", "First aid and sports taping demonstration", "Passion for physical therapy."),
                    (2, "Entrance Readiness (11th-12th)", "Prepare PCB syllabus with emphasis on human physiology.", "PCB", "NEET-UG / State CET", "NCERT, Objective Biology", "Clinical observation notes from local clinic", "Admission to BPT program."),
                    (3, "BPT Professional Degree (4.5 Years)", "Biomechanics, exercise therapy, electrotherapy, neurology, and sports medicine.", "Physiotherapy Sciences", "Clinical University Exams", "Kendall Muscles Testing, Kisner Therapeutic Exercise", "Six-month clinical rotatory hospital internship", "State Council / IAP Membership."),
                    (4, "Sports Teams / Specialized Clinic", "Specialize with MPT in Sports, Neuro, or Cardio-respiratory physiotherapy.", "Dry Needling, Kinesiology, Manual Therapy", "MPT Entrance Exams", "British Journal of Sports Medicine", "Lead physiotherapist for state sports academy", "Head Sports Rehabilitation Specialist.")
                ]
            },
            {
                "category_id": cat_sci.id,
                "title": "Cybersecurity Analyst",
                "slug": "cybersecurity-analyst",
                "summary": "Digital defenders protecting cloud infrastructures, banking protocols, and corporate networks against intrusions.",
                "what_they_do": "Conduct penetration tests, configure next-generation firewalls, investigate digital forensics incident reports, detect zero-day vulnerabilities, and ensure ISO 27001 compliance.",
                "min_education_level": "school_11_12",
                "stream_flexibility": "Flexible pathways: B.Tech, BCA, B.Sc. IT, or industry certified security analysts.",
                "avg_salary_inr": "₹7,00,000 - ₹24,00,000 per annum",
                "growth_rate": "Very High (+26% YoY)",
                "official_source_url": "https://www.cert-in.org.in",
                "official_authority_name": "CERT-In (Indian Computer Emergency Response Team)",
                "icon_name": "shield-check",
                "skills": [("Algorithmic Thinking", 1.9), ("Logical Reasoning", 1.8), ("Python & Programming", 1.7), ("Situational Judgement", 1.6)],
                "requirements": [
                    ("academic", "10+2 / Degree in CS/IT", "Knowledge of computer networks, Linux systems, and cryptographic protocols.", True, "https://www.cert-in.org.in"),
                    ("certification", "CEH / CompTIA Security+ / OSCP", "Industry recognized offensive or defensive security certifications.", True, "https://www.offensive-security.com")
                ],
                "stages": [
                    (1, "Computer Basics & Networks (8th-10th)", "Learn OSI layers, IP addressing, basic Linux bash commands, and ethical internet practices.", "Computer Science, Math", "Cyber Olympiads / Capture The Flag (CTF) Jr.", "OverTheWire (Bandit), Network Fundamentals", "Configuring home Wi-Fi firewall and router security", "Understanding of network protocols."),
                    (2, "Programming & Systems (11th-12th)", "Learn Python scripting, socket programming, assembly basics, and cryptography fundamentals.", "PCM or Computer Science", "JEE / CET / BCA Entrances", "TryHackMe, Wireshark Packet Analysis", "Python port scanner script with banner grabbing", "Admission to CS/IT or Cybersecurity degree."),
                    (3, "College & Offensive/Defensive Labs", "Penetration testing, reverse engineering, web application security (OWASP Top 10), and SIEM logs.", "Information Security Core", "HackTheBox, National CTF Competitions", "PortSwigger Web Security Academy", "Discovered verified vulnerability in bug bounty program", "Certified Ethical Hacker (CEH) / Junior Security Analyst job."),
                    (4, "SOC Leadership / Red Teaming", "Manage Security Operations Centers (SOC), execute adversary red team simulations, and handle incident responses.", "Threat Hunting, Cloud Security (AWS/Azure), OSCP", "OSCP / CISSP Certification", "SANS Reading Room, CVE Databases", "Neutralizing simulated ransomware attack in enterprise sandbox", "Chief Information Security Officer (CISO).")
                ]
            },
            {
                "category_id": cat_sci.id,
                "title": "Mechanical Engineer",
                "slug": "mechanical-engineer",
                "summary": "Engineers designing thermal systems, automotive propulsion, industrial robotics, and manufacturing assembly lines.",
                "what_they_do": "Simulate finite element stress, design gearboxes in SolidWorks/CATIA, optimize thermodynamic engine efficiency, and program CNC machining cells.",
                "min_education_level": "school_11_12",
                "stream_flexibility": "Class 12th with PCM or Polytechnic Diploma in Mechanical Engineering.",
                "avg_salary_inr": "₹5,00,000 - ₹17,00,000 per annum",
                "growth_rate": "Steady (+14% YoY with EV and automated manufacturing in India)",
                "official_source_url": "https://www.aicte-india.org",
                "official_authority_name": "AICTE / Bureau of Indian Standards (BIS)",
                "icon_name": "gear",
                "skills": [("Spatial Reasoning", 1.9), ("Numerical Aptitude", 1.8), ("Logical Reasoning", 1.6), ("Scientific Method", 1.5)],
                "requirements": [
                    ("academic", "10+2 with PCM or Diploma in Mechanical", "Physics, Chemistry, Math minimum 55% aggregate.", True, "https://jeemain.nta.nic.in"),
                    ("entrance_exam", "JEE Main / GATE / State CET", "Admissions to B.Tech Mechanical and PSUs through GATE.", True, "https://gate2026.iit.ac.in")
                ],
                "stages": [
                    (1, "Mechanical Curiosities (8th-10th)", "Understand simple machines, levers, pulley systems, engines, and kinetic energy.", "Science, Math", "Robotics Competitions", "NCERT Physics, How Things Work", "Building rubber-band powered car with gear ratios", "Intuitive physics understanding."),
                    (2, "Engineering Entrance (11th-12th)", "Master classical mechanics, rotational dynamics, thermodynamics, and calculus.", "PCM", "JEE Main / Advanced / State CET", "HC Verma Physics, IE Irodov Mechanics", "Working hydraulic arm model", "Admission to B.Tech Mechanical program."),
                    (3, "B.Tech Curriculum (Years 1-4)", "Strength of materials, fluid mechanics, CAD/CAM drafting, heat transfer, and machine design.", "Mechanical Engineering Core", "BAJA SAE / Formula Student India", "Shigley's Mechanical Engineering Design, ANSYS", "Designing chassis for college Formula Student race car", "B.Tech degree in Mechanical Engineering."),
                    (4, "Automotive / EV / Aerospace Design", "Work in electric vehicle battery cooling, aerospace structures, or heavy industrial automation.", "CFD, FEA, Additive Manufacturing", "GATE Mechanical for PSU (BHEL, IOCL, ISRO)", "ASME Technical Journals", "Production line optimization reducing cycle time by 20%", "Lead Automotive Powertrain Engineer.")
                ]
            },
            {
                "category_id": cat_sci.id,
                "title": "Statistician",
                "slug": "statistician",
                "summary": "Mathematical scientists developing stochastic algorithms, demographic surveys, clinical biostatistics, and actuarial projections.",
                "what_they_do": "Design sampling methodologies, formulate hypothesis tests, model time-series volatility in financial markets, and validate pharmacological clinical trials.",
                "min_education_level": "college_grad",
                "stream_flexibility": "Mathematics, Statistics, or Economics backgrounds.",
                "avg_salary_inr": "₹7,00,000 - ₹22,00,000 per annum",
                "growth_rate": "High (+19% YoY)",
                "official_source_url": "https://www.isical.ac.in",
                "official_authority_name": "Indian Statistical Institute (ISI) / MoSPI",
                "icon_name": "chart-pie",
                "skills": [("Numerical Aptitude", 2.0), ("Data Interpretation", 1.9), ("Logical Reasoning", 1.8), ("Python & Programming", 1.5)],
                "requirements": [
                    ("academic", "B.Stat / B.Sc. Statistics / M.Stat", "Undergraduate or postgraduate degree with core focus on statistical theory.", True, "https://www.isical.ac.in"),
                    ("entrance_exam", "ISI Admission Test / IIT-JAM / ISS", "Entrance to Indian Statistical Institute, IITs or Indian Statistical Service.", True, "https://www.isical.ac.in")
                ],
                "stages": [
                    (1, "Numbers & Logic (8th-10th)", "Master permutations, combinations, mean, median, standard deviation, and logic puzzles.", "Math", "Regional Mathematics Olympiad (RMO)", "NCERT Math, Arthur Engel Problem Solving", "Statistical analysis of school sports records", "Knack for quantitative precision."),
                    (2, "Higher Secondary Math (11th-12th)", "Excel in probability theory, calculus, binomial distribution, and linear algebra.", "PCM or Commerce with Math", "ISI Entrance Test / CMI / CUET", "NCERT, Hall & Knight Higher Algebra", "Probability simulator script in Python/R", "Admission to ISI B.Stat or premier statistics program."),
                    (3, "B.Stat / M.Sc. Rigor (College)", "Stochastic processes, Bayesian inference, regression analysis, multivariate statistics, and R programming.", "Theoretical Statistics", "ISS / IIT JAM", "Casella & Berger Statistical Inference", "Comprehensive biostatistical study on local health markers", "Accredited degree from ISI or leading university."),
                    (4, "Biostats / Financial Risk / ISS", "Serve as Indian Statistical Service (ISS) officer or Principal Biostatistician for global clinical research.", "SAS, R, Clinical Trial Protocols, Econometrics", "UPSC ISS Examination", "Journal of the American Statistical Association", "Formulating national economic sampling framework", "Chief Statistician / Director of Analytics.")
                ]
            },

            # CATEGORY 2: Commerce, Business, Arts and Humanities (15)
            {
                "category_id": cat_comm.id,
                "title": "Chartered Accountant (CA)",
                "slug": "chartered-accountant-ca",
                "summary": "India's premier statutory financial authorities authorized to audit company balance sheets, manage taxation, and advise boards.",
                "what_they_do": "Conduct statutory corporate audits, certify financial statements, optimize GST and direct tax filings, design corporate finance strategies, and ensure regulatory compliance.",
                "min_education_level": "school_11_12",
                "stream_flexibility": "Any 10+2 stream (Commerce recommended; Science and Arts students also eligible).",
                "avg_salary_inr": "₹9,00,000 - ₹30,00,000+ per annum",
                "growth_rate": "Very High (+20% YoY)",
                "official_source_url": "https://www.icai.org",
                "official_authority_name": "Institute of Chartered Accountants of India (ICAI)",
                "icon_name": "calculator",
                "skills": [("Financial Acumen", 2.0), ("Numerical Aptitude", 1.9), ("Logical Reasoning", 1.7), ("Situational Judgement", 1.6)],
                "requirements": [
                    ("academic", "10+2 (Any Stream)", "Qualify Class 12 board examination.", True, "https://www.icai.org"),
                    ("entrance_exam", "ICAI CA Foundation", "Four objective and descriptive papers conducted twice yearly by ICAI.", True, "https://www.icai.org"),
                    ("certification", "CA Final + 2-Year Articleship", "Clear CA Intermediate, complete 2-year practical training under a practicing CA, and clear CA Final.", True, "https://www.icai.org")
                ],
                "stages": [
                    (1, "Financial Curiosity (8th-10th)", "Understand basic money math, compound interest, personal budgeting, and current economic affairs.", "Mathematics, Social Studies", "Commerce Olympiads", "The Intelligent Investor, Economic Times", "Family budget analysis spreadsheet", "Interest in commerce and balance sheets."),
                    (2, "CA Foundation Entry (11th-12th)", "Study Accountancy, Business Economics, Mercantile Law, and register for ICAI Foundation.", "Commerce with Math / Any Stream", "CA Foundation Exam", "ICAI Study Material", "Solving previous ICAI foundation test papers", "Clear CA Foundation examination."),
                    (3, "CA Intermediate & Articleship", "Clear 6 papers of CA Intermediate, undergo mandatory ICITSS IT training, and join a CA firm for 2-year articleship.", "Corporate Laws, Auditing, Tax, Financial Management", "CA Intermediate Exams", "ICAI Modules, Bare Acts", "Auditing statutory balance sheets of manufacturing firms", "Completion of 2-year articleship."),
                    (4, "CA Final & ICAI Membership", "Clear Group 1 and Group 2 of CA Final and apply for ICAI membership to practice or lead corporate finance.", "Strategic Financial Management, Advanced Auditing", "CA Final Exam", "ICAI Standards on Auditing", "Passing CA Final on first attempt", "ICAI ACA Associate Member.")
                ]
            },
            {
                "category_id": cat_comm.id,
                "title": "Investment Banker",
                "slug": "investment-banker",
                "summary": "Financial powerbrokers orchestrating multi-million dollar corporate mergers, initial public offerings (IPOs), and capital debt raises.",
                "what_they_do": "Build discounted cash flow (DCF) valuation models, author pitchbooks for institutional investors, structure cross-border acquisitions, and underwrite securities.",
                "min_education_level": "college_grad",
                "stream_flexibility": "Commerce, Economics, Engineering, or Management graduates.",
                "avg_salary_inr": "₹15,00,000 - ₹50,00,000+ per annum",
                "growth_rate": "High (+18% YoY in expanding Indian capital markets)",
                "official_source_url": "https://www.sebi.gov.in",
                "official_authority_name": "SEBI / Indian Merchant Bankers Association",
                "icon_name": "cash-stack",
                "skills": [("Financial Acumen", 2.0), ("Numerical Aptitude", 1.8), ("Logical Reasoning", 1.7), ("Communication & Empathy", 1.6)],
                "requirements": [
                    ("academic", "B.Com / B.Tech / MBA Finance", "Top-tier undergraduate degree or premier MBA (IIMs / XLRI / ISB).", True, "https://iimcat.ac.in"),
                    ("entrance_exam", "CAT / GMAT / CFA", "Common Admission Test for IIMs or Chartered Financial Analyst (CFA) credential.", True, "https://www.cfainstitute.org")
                ],
                "stages": [
                    (1, "Market Curiosity (8th-10th)", "Learn how stocks trade on BSE/NSE, what companies do, and how revenue translates into profit.", "Mathematics, Economics", "Stock Market Virtual Simulators", "One Up On Wall Street by Peter Lynch", "Virtual portfolio tracking 10 Indian equities", "Fascination with capital markets."),
                    (2, "Commerce or Math Foundation (11th-12th)", "Build solid mastery of corporate accounting, microeconomics, and calculus.", "Commerce with Math or Science", "CUET-UG (SRCC/St. Stephen's) / IPMAT", "NCERT Economics, Zerodha Varsity", "Valuation analysis of an Indian consumer tech IPO", "Admission to premier undergraduate institution."),
                    (3, "College & Financial Modeling", "Excel, DCF valuation, LBO models, Bloomberg terminal data, and clearing CFA Level 1.", "Finance, Economics, Statistics", "CAT / GMAT", "Wall Street Prep, Damodaran Online", "Complete 3-statement financial model for an Indian FMCG major", "Summer Analyst internship at global investment bank."),
                    (4, "Top-Tier MBA / Associate Role", "IIM MBA or Direct Analyst promotion; executing live M&A transactions, debt syndications, and IPO filings.", "Mergers & Acquisitions, Private Equity", "SEBI Registered Merchant Banker Guidelines", "Financial Times, Mint", "Closing a ₹500 Cr cross-border equity buyout", "Vice President / Managing Director.")
                ]
            },
            {
                "category_id": cat_comm.id,
                "title": "Financial Analyst",
                "slug": "financial-analyst",
                "summary": "Evaluates macroeconomic trends, corporate earnings, and stock valuations to guide mutual funds, banks, and retail investors.",
                "what_they_do": "Forecast corporate EBITDA margins, track sector regulatory developments, write equity research initiation reports, and evaluate corporate debt creditworthiness.",
                "min_education_level": "college_grad",
                "stream_flexibility": "Commerce, Economics, Math, Statistics, or Engineering.",
                "avg_salary_inr": "₹6,00,000 - ₹20,00,000 per annum",
                "growth_rate": "High (+16% YoY)",
                "official_source_url": "https://www.sebi.gov.in",
                "official_authority_name": "SEBI Research Analyst Regulations (NISM)",
                "icon_name": "graph-up",
                "skills": [("Financial Acumen", 1.9), ("Data Interpretation", 1.9), ("Numerical Aptitude", 1.7), ("Verbal Reasoning", 1.5)],
                "requirements": [
                    ("academic", "Graduation in Commerce/Economics/Finance", "Recognized degree with quantitative finance courses.", True, "https://www.nism.ac.in"),
                    ("certification", "NISM Series XV / CFA Charter", "SEBI Research Analyst certification or CFA levels.", True, "https://www.nism.ac.in")
                ],
                "stages": [
                    (1, "Basics of Business (8th-10th)", "Understand how businesses earn revenues, costs of goods sold, and reading simple financial charts.", "Mathematics, Social Sciences", "School Business Quizzes", "Rich Dad Poor Dad, Moneycontrol", "Comparison of quarterly results of two retail companies", "Analytical curiosity."),
                    (2, "Commerce & Statistics Prep (11th-12th)", "Learn ledger accounting, financial statement ratios, and probability.", "Commerce with Math / Science", "CUET-UG / State University Entrances", "NCERT, Zerodha Varsity", "Ratio analysis of a Nifty 50 firm", "College admission in Finance/Economics."),
                    (3, "Degree & NISM / CFA Studies", "Financial econometrics, advanced Excel, Python for finance, and NISM Series XV exam.", "Corporate Finance, Portfolio Theory", "NISM Series XV Research Analyst Exam", "Investopedia, CFA Institute Curriculum", "Published equity research report on Indian EV ecosystem", "Junior Research Analyst placement."),
                    (4, "Sector Specialist / Portfolio Manager", "Cover entire sectors (IT, Pharma, Banking) and generate institutional buy/sell recommendations.", "Equity Research, Credit Ratings", "CFA Charter", "SEBI Research Analyst Guidelines", "Consistently outperforming benchmark index with stock picks", "Head of Equity Research.")
                ]
            },
            {
                "category_id": cat_comm.id,
                "title": "Business Manager",
                "slug": "business-manager",
                "summary": "Directs departmental operations, oversees budgets, optimizes productivity, and aligns teams with executive strategy.",
                "what_they_do": "Set quarterly OKRs, allocate departmental budgets, resolve supply chain bottlenecks, conduct performance reviews, and lead cross-functional delivery.",
                "min_education_level": "college_grad",
                "stream_flexibility": "Open to all academic backgrounds; MBA / BBA / B.Tech.",
                "avg_salary_inr": "₹8,00,000 - ₹26,00,000 per annum",
                "growth_rate": "Steady (+15% YoY)",
                "official_source_url": "https://www.aima.in",
                "official_authority_name": "All India Management Association (AIMA)",
                "icon_name": "briefcase",
                "skills": [("Leadership & Teamwork", 2.0), ("Communication & Empathy", 1.8), ("Situational Judgement", 1.7), ("Logical Reasoning", 1.5)],
                "requirements": [
                    ("academic", "Graduation (Any Discipline)", "Recognized undergraduate degree with minimum 50% marks.", True, "https://iimcat.ac.in"),
                    ("entrance_exam", "CAT / XAT / CMAT", "Common Admission Test for premier Indian B-schools.", True, "https://iimcat.ac.in")
                ],
                "stages": [
                    (1, "School Organizing & Leadership (8th-10th)", "Take on school council leadership, organize sports meets, and learn team delegation.", "All Subjects", "School Student Council", "Harvard Business Review for Youth", "Organizing inter-school charity fundraiser", "Natural leadership instinct."),
                    (2, "Higher Secondary Development (11th-12th)", "Build strong communication, critical problem solving, and public speaking.", "Any Stream", "IPMAT (IIM Indore/Rohtak 5-year Integrated)", "The Personal MBA by Josh Kaufman", "Leading school debate or cultural club", "College admission."),
                    (3, "Undergraduate & Management Entrance", "Complete graduation, lead college fests, maintain high GPA, and score 98%+ percentile in CAT.", "Any Discipline", "CAT, XAT, GMAT", "Arun Sharma CAT Prep, HBR Case Studies", "Internship managing product operations at startup", "Admission to premier IIM / XLRI MBA program."),
                    (4, "Executive Corporate Operations", "Manage business unit P&L, launch new geographical service territories, and scale revenues.", "P&L Management, Agile Operations", "Six Sigma Black Belt", "McKinsey Quarterly", "Scaling departmental revenue by 35% while cutting waste", "General Manager / Chief Operating Officer (COO).")
                ]
            },
            {
                "category_id": cat_comm.id,
                "title": "Entrepreneur",
                "slug": "entrepreneur",
                "summary": "Visionary company founders identifying market gaps, building breakthrough products, and raising venture capital.",
                "what_they_do": "Conduct customer discovery interviews, build minimum viable products (MVPs), pitch angel investors, recruit core founding talent, and steer company growth.",
                "min_education_level": "school_11_12",
                "stream_flexibility": "Completely open; skill and market validation matter far more than formal degrees.",
                "avg_salary_inr": "Variable (Equity Ownership & Profit Distributions)",
                "growth_rate": "High Potential (Startup India initiative)",
                "official_source_url": "https://www.startupindia.gov.in",
                "official_authority_name": "Startup India / DPIIT",
                "icon_name": "rocket",
                "skills": [("Leadership & Teamwork", 2.0), ("Visual Creativity", 1.8), ("Financial Acumen", 1.7), ("Situational Judgement", 1.7)],
                "requirements": [
                    ("academic", "No Mandatory Degree", "Enterprise capability, market obsession, and execution stamina.", True, "https://www.startupindia.gov.in"),
                    ("certification", "DPIIT Startup India Recognition", "Company incorporation (Pvt Ltd / LLP) and DPIIT tax exemption certification.", True, "https://www.startupindia.gov.in")
                ],
                "stages": [
                    (1, "Curiosity & Problem Spotting (8th-10th)", "Notice daily frictions, experiment with small selling ideas, build simple prototypes.", "Any Subjects", "Student Innovation Challenges", "Zero to One by Peter Thiel, How I Built This", "Creating and selling hand-crafted or digital design assets", "Bias toward action and resourcefulness."),
                    (2, "Skill Building & Networking (11th-12th)", "Learn coding, copywriting, graphic design, and basic economics.", "Any Stream", "TiE Young Entrepreneurs (TYE)", "The Lean Startup by Eric Ries", "Launching a local tutoring or digital services micro-business", "Customer-first mindset."),
                    (3, "MVP Build & Market Validation (College)", "Form a team, build a working prototype, acquire 100 organic paying customers, and pitch to incubators.", "Technology or Business Studies", "College E-Cell, Y Combinator Startup School", "Y Combinator Startup Library, Paul Graham Essays", "Working B2B or consumer app with active revenue", "Incorporation of Pvt Ltd company on MCA portal."),
                    (4, "Venture Scale & Capital Expansion", "Raise Seed / Series A funding from institutional venture capital and expand hiring across departments.", "Fundraising, Cap Table, Culture Building", "Startup India Seed Fund Scheme", "Venture Deals by Brad Feld", "Reaching product-market fit and positive unit economics", "Successful Founder & CEO.")
                ]
            },
            {
                "category_id": cat_comm.id,
                "title": "Marketing Manager",
                "slug": "marketing-manager",
                "summary": "Brand architects driving customer acquisition, digital advertising campaigns, viral awareness, and market share.",
                "what_they_do": "Design omnichannel marketing strategies, optimize Google/Meta ad ROAS, supervise influencer partnerships, conduct consumer sentiment surveys, and craft brand narratives.",
                "min_education_level": "college_grad",
                "stream_flexibility": "Open to all disciplines; BBA, Mass Comm, B.Tech, or MBA.",
                "avg_salary_inr": "₹7,00,000 - ₹24,00,000 per annum",
                "growth_rate": "Very High (+18% YoY in digital ad spend)",
                "official_source_url": "https://www.ascionline.in",
                "official_authority_name": "Advertising Standards Council of India (ASCI)",
                "icon_name": "megaphone",
                "skills": [("Communication & Empathy", 2.0), ("Data Interpretation", 1.8), ("Visual Creativity", 1.8), ("Logical Reasoning", 1.5)],
                "requirements": [
                    ("academic", "Graduation in Marketing / Mass Comm / Any", "Undergraduate degree or MBA in Marketing.", True, "https://iimcat.ac.in"),
                    ("certification", "Google Ads & Meta Certified Media Planner", "Industry validated competency in search and paid social campaign management.", True, "https://skillshop.exceedlms.com")
                ],
                "stages": [
                    (1, "Consumer Psychology (8th-10th)", "Analyze TV commercials, social media trends, viral slogans, and why people buy products.", "Languages, Social Sciences", "School Ad-Mad Competitions", "Ogilvy on Advertising, Made to Stick", "Designing a creative billboard poster for an eco-product", "Persuasive storytelling instinct."),
                    (2, "Digital Media Foundations (11th-12th)", "Learn copywriting, search engine optimization, short-form video creation, and audience analytics.", "Any Stream (Commerce/Arts/Science)", "CUET-UG (BBA / Journalism Entrances)", "HubSpot Inbound Marketing, Seth Godin Blog", "Managing a thematic Instagram or YouTube channel to 5K followers", "Undergraduate admission."),
                    (3, "College Portfolio & Certifications", "Google Analytics 4, Meta Business Manager, performance marketing metrics (CAC, LTV, ROAS), and branding.", "Marketing, Psychology, Business", "Summer Marketing Internships", "Reforge, Marketing Brew, Neil Patel", "Executing a live ₹10,000 ad campaign that generated ₹45,000 in sales", "Campus placement as Assistant Brand Manager."),
                    (4, "Enterprise Brand Leadership", "Lead multi-crore national brand campaigns, manage external creative agencies, and head product growth.", "Brand Equity, Performance Marketing, PR", "ASCI Regulatory Guidelines", "WARC, Brand Equity Economic Times", "Launching national campaign featuring celebrity brand ambassadors", "Chief Marketing Officer (CMO).")
                ]
            },
            {
                "category_id": cat_comm.id,
                "title": "Company Secretary (CS)",
                "slug": "company-secretary-cs",
                "summary": "India's senior corporate governance and legal compliance officers advising company boards on corporate law and regulatory filings.",
                "what_they_do": "Ensure statutory compliance with Companies Act 2013, manage board meetings, oversee secretarial audits, coordinate SEBI disclosures, and maintain share registers.",
                "min_education_level": "school_11_12",
                "stream_flexibility": "Any stream in 10+2 (Commerce and Arts students frequently excel).",
                "avg_salary_inr": "₹6,50,000 - ₹22,00,000 per annum",
                "growth_rate": "Steady (+15% YoY with rapid corporate registrations)",
                "official_source_url": "https://www.icsi.edu",
                "official_authority_name": "Institute of Company Secretaries of India (ICSI)",
                "icon_name": "award",
                "skills": [("Legal Argumentation", 1.9), ("Verbal Reasoning", 1.8), ("Financial Acumen", 1.7), ("Situational Judgement", 1.6)],
                "requirements": [
                    ("academic", "10+2 in Any Stream", "Class 12th pass from recognized board.", True, "https://www.icsi.edu"),
                    ("entrance_exam", "ICSI CSEET", "CS Executive Entrance Test conducted four times a year by ICSI.", True, "https://www.icsi.edu"),
                    ("certification", "CS Professional & 21-Month Practical Training", "Clear CS Executive, CS Professional and complete statutory practical training.", True, "https://www.icsi.edu")
                ],
                "stages": [
                    (1, "Governance & Law Basics (8th-10th)", "Learn how public institutions work, Indian constitution fundamentals, and legal rights.", "Social Sciences, English", "School Mock Parliaments", "Civics NCERT, Law for the Common Man", "Drafting minutes of a mock club meeting", "Respect for procedural diligence."),
                    (2, "CSEET Entrance (11th-12th)", "Prepare for Business Communication, Legal Aptitude, and Economic & Business Environment.", "Any Stream", "ICSI CSEET Exam", "ICSI CSEET Study Materials", "Scoring 140+ in CSEET mock exams", "Clear CSEET and register for CS Executive."),
                    (3, "CS Executive & Practical Training", "Jurisprudence, Company Law, Securities Laws, Economic Laws, and Tax Laws.", "Corporate Law Core", "ICSI Executive Examinations", "Bare Acts, ICSI Modules", "Executing statutory MCA e-filings during 21-month training", "Clear CS Executive and Professional stages."),
                    (4, "Boardroom Compliance Officer", "Appointed as statutory Company Secretary of listed public company or partner in secretarial audit firm.", "SEBI LODR, Takeover Code, Corporate Restructuring", "ICSI Associate Membership (ACS)", "Chartered Secretary Journal", "Directing board documentation for major amalgamation scheme", "Head of Legal & Company Secretary.")
                ]
            },
            {
                "category_id": cat_comm.id,
                "title": "Lawyer",
                "slug": "lawyer",
                "summary": "Legal advocates and corporate counsels upholding constitutional rights, litigating court disputes, and negotiating agreements.",
                "what_they_do": "Draft petitions, represent clients before the High Courts and Supreme Court of India, conduct cross-examinations, negotiate contract terms, and resolve corporate disputes.",
                "min_education_level": "school_11_12",
                "stream_flexibility": "Any stream in 10+2 (Arts, Commerce, Science all eligible for 5-year B.A./B.B.A. LL.B.).",
                "avg_salary_inr": "₹6,00,000 - ₹30,00,000+ per annum",
                "growth_rate": "Very High (+19% YoY)",
                "official_source_url": "https://www.barcouncilofindia.org",
                "official_authority_name": "Bar Council of India (BCI)",
                "icon_name": "book",
                "skills": [("Legal Argumentation", 2.0), ("Verbal Reasoning", 1.9), ("Critical Thinking", 1.8), ("Communication & Empathy", 1.7)],
                "requirements": [
                    ("academic", "10+2 (Any Stream) for 5-Year LL.B. or Graduation for 3-Year LL.B.", "Minimum 45% aggregate in qualifying examination.", True, "https://consortiumofnlus.ac.in"),
                    ("entrance_exam", "CLAT / AILET / MH CET Law", "Common Law Admission Test conducted by Consortium of National Law Universities.", True, "https://consortiumofnlus.ac.in"),
                    ("certification", "All India Bar Examination (AIBE)", "Mandatory Bar Council of India license to practice law in Indian courts.", True, "https://www.allindiabarexamination.com")
                ],
                "stages": [
                    (1, "Critical Thinking & Debate (8th-10th)", "Develop rapid reading speed, debate both sides of controversial issues, study constitutional rights.", "English, Social Sciences", "Debates, Model United Nations (MUN)", "To Kill a Mockingbird, Indian Constitution Basics", "School debate champion certificate", "Articulate oral reasoning."),
                    (2, "CLAT Preparation (11th-12th)", "Reading comprehension, legal reasoning, critical reasoning, current affairs, and quantitative techniques.", "Any Stream (Humanities/Commerce/Science)", "CLAT-UG, AILET, SLAT", "The Hindu Editorials, CLAT Previous Years Papers", "Scoring in top 1% of national CLAT mock series", "Admission to a National Law University (NLU)."),
                    (3, "5-Year Integrated LL.B. (Law School)", "Constitutional Law, IPC/BNS, Contracts, Moot Courts, trial advocacy, and judicial clerkships.", "Law Core", "Bar Council Curriculum", "Mulla Contracts, Ratanlal Dhirajlal IPC, SCC Online", "Winner of national moot court competition; High Court internships", "LL.B. degree awarded."),
                    (4, "Bar Enrollment & Court Practice", "Enroll with State Bar Council, clear AIBE, apprentice under Senior Advocate or join Tier-1 law firm.", "Litigation / Corporate M&A", "All India Bar Examination (AIBE)", "AIR, Supreme Court Cases (SCC)", "Securing landmark relief for client before High Court", "Senior Advocate / Law Firm Equity Partner.")
                ]
            },
            {
                "category_id": cat_comm.id,
                "title": "IAS Officer",
                "slug": "ias-officer",
                "summary": "India's premier administrative leaders governing districts, directing welfare ministries, and implementing national policies.",
                "what_they_do": "Serve as District Magistrates (DM) maintaining law and order, execute multi-crore rural development schemes, manage disaster responses, and formulate government policies.",
                "min_education_level": "college_grad",
                "stream_flexibility": "Graduates in ANY discipline from a recognized Indian university.",
                "avg_salary_inr": "₹7,00,000 - ₹27,00,000 per annum + Govt Accommodations & Perks",
                "growth_rate": "Prestigious Public Service (Fixed Cadre Allocations via UPSC)",
                "official_source_url": "https://www.upsc.gov.in",
                "official_authority_name": "Union Public Service Commission (UPSC) / DoPT",
                "icon_name": "shield",
                "skills": [("Situational Judgement", 2.0), ("Verbal Reasoning", 1.9), ("Leadership & Teamwork", 1.8), ("Logical Reasoning", 1.7)],
                "requirements": [
                    ("academic", "Graduation in Any Stream", "Recognized Bachelor's degree (B.A., B.Sc., B.Com, B.Tech, MBBS).", True, "https://www.upsc.gov.in"),
                    ("certification", "Age 21-32 Years", "Indian citizen meeting age criteria specified in annual UPSC notification.", True, "https://www.upsc.gov.in"),
                    ("entrance_exam", "UPSC Civil Services Examination (CSE)", "Prelims (GS + CSAT), Mains (9 descriptive papers), and Personality Interview.", True, "https://www.upsc.gov.in")
                ],
                "stages": [
                    (1, "General Awareness & Ethics (8th-10th)", "Read daily national newspapers, understand Indian history, geography, democratic polity, and local governance.", "Social Studies, Languages", "National Quiz Competitions", "NCERT 6th to 10th Social Sciences, The Hindu", "Community welfare initiative report", "Deep public service ethos."),
                    (2, "Stream Selection & Breadth (11th-12th)", "Build analytical writing habits, understand macroeconomic policies, and master Indian Constitution.", "Any Stream (Humanities/Science/Commerce)", "College Admission Entrances", "NCERT 11th-12th History, Polity by Laxmikanth", "Analytical essay on rural education bottlenecks", "Admission to undergraduate degree."),
                    (3, "Undergraduate Degree & UPSC Preparation", "Complete graduation, select Optional Subject, solve 10 years UPSC Mains papers, master answer writing.", "Any Graduation Discipline", "UPSC CSE Prelims & Mains", "Yojana, Kurukshetra, PRS India, Vision IAS Test Series", "Writing 50 full-length GS and Optional Mains answer sheets", "Clearing UPSC CSE with top All-India Rank."),
                    (4, "LBSNAA Training & District Administration", "2-year rigorous training at LBSNAA Mussoorie, field attachments, and appointment as Sub-Divisional Magistrate (SDM).", "Public Administration, Land Revenue, Disaster Management", "UPSC Foundation Course Assessments", "National Policy Documents", "Executing district-level drought relief operation", "District Magistrate (DM) / Ministry Secretary.")
                ]
            },
            {
                "category_id": cat_comm.id,
                "title": "IPS Officer",
                "slug": "ips-officer",
                "summary": "Elite police commanders safeguarding internal security, investigating organized crime, and upholding public order.",
                "what_they_do": "Lead district police forces as Superintendent of Police (SP), coordinate counter-terror operations, investigate financial fraud, and manage riot containment.",
                "min_education_level": "college_grad",
                "stream_flexibility": "Graduates in ANY discipline from a recognized university.",
                "avg_salary_inr": "₹7,00,000 - ₹27,00,000 per annum + Govt Accommodations & Perks",
                "growth_rate": "Prestigious Public Service (Fixed Cadre Allocations via UPSC)",
                "official_source_url": "https://www.svpnpa.gov.in",
                "official_authority_name": "UPSC / Sardar Vallabhbhai Patel National Police Academy (SVPNPA)",
                "icon_name": "shield-fill",
                "skills": [("Situational Judgement", 2.0), ("Leadership & Teamwork", 1.9), ("Logical Reasoning", 1.7), ("Communication & Empathy", 1.6)],
                "requirements": [
                    ("academic", "Graduation in Any Discipline", "Bachelor's degree from recognized Indian university.", True, "https://www.upsc.gov.in"),
                    ("certification", "Physical Fitness Standards", "Minimum height (165 cm for men, 150 cm for women) and chest expansion criteria.", True, "https://www.upsc.gov.in"),
                    ("entrance_exam", "UPSC Civil Services Examination", "Rank allocation based on aggregate score across Prelims, Mains, and Interview.", True, "https://www.upsc.gov.in")
                ],
                "stages": [
                    (1, "Physical Discipline & Awareness (8th-10th)", "Maintain cardiovascular stamina, participate in NCC / scouts, study Indian penal and criminal justice basics.", "Science, Social Studies, Physical Ed", "NCC / Republic Day Camp", "Indian Police History, National Newspapers", "Physical fitness badge in athletics", "Courage and unyielding integrity."),
                    (2, "Academic & Moral Fortitude (11th-12th)", "Keep abreast of national security challenges, cybercrime, and social tensions.", "Any Stream", "College Admissions", "NCERT Books, Current Affairs", "Leading school sports team or NCC contingent", "College enrollment."),
                    (3, "College Degree & Rigorous CSE Prep", "Maintain physical fitness, master GS syllabus, write Mains papers, and practice situational interviews.", "Any Discipline", "UPSC Civil Services Exam", "Indian Police Acts, Laxmikanth, Internal Security Guides", "Complete 50km endurance trek and 100 Mains answer tests", "UPSC CSE rank qualifying for Indian Police Service (IPS)."),
                    (4, "SVPNPA Hyderabad Training & Cadre Leadership", "Intensive training in weapons, forensic science, unarmed combat, criminal laws at SVPNPA Hyderabad.", "Investigation, Cyber Forensics, Crowd Control", "SVPNPA Indoor & Outdoor Passing Out Exams", "SVP NPA Police Manuals", "Leading anti-smuggling / law and order police battalion", "Superintendent of Police (SP) / Director General of Police (DGP).")
                ]
            },
            {
                "category_id": cat_comm.id,
                "title": "Journalist",
                "slug": "journalist",
                "summary": "Investigative reporters and broadcast correspondents investigating the truth, informing citizens, and holding power to account.",
                "what_they_do": "Investigate investigative stories, interview public figures, write breaking news dispatches, produce video documentaries, and verify primary sources.",
                "min_education_level": "school_11_12",
                "stream_flexibility": "Any 10+2 stream; B.A. Journalism, Mass Comm, English, or Political Science.",
                "avg_salary_inr": "₹4,50,000 - ₹16,00,000 per annum",
                "growth_rate": "Moderate (+12% YoY with digital news portals)",
                "official_source_url": "https://www.presscouncil.nic.in",
                "official_authority_name": "Press Council of India (PCI)",
                "icon_name": "newspaper",
                "skills": [("Verbal Reasoning", 2.0), ("Communication & Empathy", 1.9), ("Situational Judgement", 1.7), ("Critical Thinking", 1.6)],
                "requirements": [
                    ("academic", "10+2 / Bachelor's in Journalism or Any", "Class 12th pass or graduation from recognized board/university.", True, "https://iimc.gov.in"),
                    ("entrance_exam", "IIMC Entrance / CUET-UG / ACJ Entrance", "Admission to premier media institutes like Indian Institute of Mass Communication.", True, "https://iimc.gov.in")
                ],
                "stages": [
                    (1, "Writing & Inquisitiveness (8th-10th)", "Read national dailies, write essays, edit the school newsletter, and interview school staff.", "English, Languages, History", "Essay & Creative Writing Competitions", "All the President's Men, The Hindu", "Founding and publishing monthly school news bulletin", "Insatiable curiosity to uncover facts."),
                    (2, "Media Awareness (11th-12th)", "Learn photojournalism, digital blogging, fact-checking principles, and international relations.", "Any Stream (Humanities/Commerce/Science)", "CUET-UG (Journalism Entrances)", "PCI Code of Journalistic Conduct", "Investigative blog post on local municipal civic issues", "Admission to B.A. Journalism / Mass Comm."),
                    (3, "College Portfolio & Newsroom Internships", "Television broadcast studios, audio podcasting, digital CMS, and investigative field reporting.", "Journalism, Mass Communication", "IIMC / ACJ Entrances", "Columbia Journalism Review, Poynter Institute", "Covering state election rallies as student correspondent", "Trainee Reporter placement at major national news publication."),
                    (4, "Senior Investigative Correspondent / Editor", "Break major national public interest stories, anchor prime-time analysis broadcasts, or head bureau.", "Investigative Reporting, Data Journalism", "Press Council Guidelines", "Reuters Institute Digital News Reports", "Documentary exposure of corporate environmental violation", "Chief Editor / Bureau Chief.")
                ]
            },
            {
                "category_id": cat_comm.id,
                "title": "Psychologist",
                "slug": "psychologist",
                "summary": "Behavioral scientists diagnosing mental health dynamics, administering psychometrics, and providing evidence-based therapies.",
                "what_they_do": "Conduct psychological assessments, administer cognitive behavioral therapy (CBT), support corporate emotional resilience, and research human behavior.",
                "min_education_level": "school_11_12",
                "stream_flexibility": "Any 10+2 stream (Psychology subject optional but advantageous).",
                "avg_salary_inr": "₹4,50,000 - ₹16,00,000 per annum",
                "growth_rate": "Very High (+24% YoY with burgeoning mental wellness awareness in India)",
                "official_source_url": "https://www.rehabcouncil.nic.in",
                "official_authority_name": "Rehabilitation Council of India (RCI)",
                "icon_name": "person-heart",
                "skills": [("Communication & Empathy", 2.0), ("Scientific Method", 1.8), ("Situational Judgement", 1.8), ("Verbal Reasoning", 1.6)],
                "requirements": [
                    ("academic", "B.A. / B.Sc. Psychology + M.A. / M.Sc. Psychology", "Specialized postgraduate qualification in clinical, counseling, or industrial psychology.", True, "https://www.rehabcouncil.nic.in"),
                    ("certification", "RCI Licensed Clinical Psychologist (M.Phil / Psy.D.)", "Mandatory statutory license to diagnose and treat clinical psychiatric conditions in India.", True, "https://www.rehabcouncil.nic.in")
                ],
                "stages": [
                    (1, "Empathy & Listening (8th-10th)", "Observe social interactions, practice active listening, and read introductory books on human behavior.", "English, Biology, Social Sciences", "Peer Counseling Clubs", "Man's Search for Meaning, Psychology NCERT", "School survey on teenage exam stress patterns", "Deep non-judgmental empathy."),
                    (2, "Psychology Foundation (11th-12th)", "Study biological bases of behavior, cognitive development, personality theories, and statistics.", "Any Stream (Humanities preferred with Psychology)", "CUET-UG Psychology Entrances", "NCERT 11th & 12th Psychology", "Experimental journal on memory recall methods", "Admission to B.A./B.Sc. Psychology."),
                    (3, "Postgraduate Specialization (Master's)", "Neuropsychology, psychometrics, counseling techniques, abnormal psychology, and clinical internships.", "Clinical / Counseling Psychology", "CUET-PG, TISS, NIMHANS Entrances", "Baron Psychology, DSM-5 Diagnostic Criteria", "Supervised 200 hours of counseling internship in hospital setting", "M.A. Psychology degree completion."),
                    (4, "RCI M.Phil / Clinical Practice", "Clear NIMHANS or CIP entrance for M.Phil Clinical Psychology to secure RCI Clinical License.", "Cognitive Behavioral Therapy (CBT), Psychometry", "RCI Licensing Board", "American Psychologist, Indian Journal of Psychiatry", "Successfully counseling over 500 patients through life transitions", "Licensed Clinical Psychologist / Practice Director.")
                ]
            },
            {
                "category_id": cat_comm.id,
                "title": "Graphic Designer",
                "slug": "graphic-designer",
                "summary": "Visual artists shaping brand identities, typography layouts, user interface assets, and digital illustrations.",
                "what_they_do": "Create brand style guides, design user interface components in Figma, compose vector illustrations in Illustrator, and curate typography for ad campaigns.",
                "min_education_level": "school_11_12",
                "stream_flexibility": "Completely stream-agnostic (Science, Commerce, Arts all eligible for B.Des).",
                "avg_salary_inr": "₹4,00,000 - ₹15,00,000 per annum",
                "growth_rate": "High (+18% YoY with booming digital product economy)",
                "official_source_url": "https://www.nid.edu",
                "official_authority_name": "National Institute of Design (NID) / UCEED",
                "icon_name": "palette",
                "skills": [("Visual Creativity", 2.0), ("Spatial Reasoning", 1.7), ("Communication & Empathy", 1.5), ("Logical Reasoning", 1.4)],
                "requirements": [
                    ("academic", "10+2 (Any Stream)", "Pass in Class 12 from any recognized education board.", True, "https://www.nid.edu"),
                    ("entrance_exam", "NID DAT / UCEED / SEED", "Design aptitude tests assessing visual visualization and problem solving.", True, "https://uceed.iitb.ac.in"),
                    ("certification", "Professional Portfolio (Behance / Dribbble)", "Demonstrated expertise in branding, typography, UI/UX, and vector illustration.", True, "https://behance.net")
                ],
                "stages": [
                    (1, "Visual Expression (8th-10th)", "Experiment with hand drawing, color theory, digital photography, and typography posters.", "Fine Arts, Geometry, English", "Art & Poster Design Contests", "Steal Like an Artist, Canva / Inkscape tutorials", "Redesigning school magazine cover with custom typography", "Eye for composition and color harmony."),
                    (2, "Design Aptitude Prep (11th-12th)", "Prepare for NID DAT / UCEED with sketching, lateral thinking puzzles, and portfolio curation.", "Any Stream", "UCEED (IIT Bombay), NID DAT", "Design entrance guides, Behance Curations", "Sketchbook of 100 perspective and product sketches", "Admission to B.Des program at NID or IIT IDC."),
                    (3, "B.Des Studio Training (College)", "Grid systems, motion design, design thinking, Figma UI design, brand identity systems.", "Visual Communication Core", "Annual Design Showcases", "The Design of Everyday Things, Dribbble", "Complete brand overhaul and mobile app UI case study for an Indian NGO", "Design agency placement."),
                    (4, "Brand / Design System Lead", "Direct multi-platform design systems, oversee marketing visuals, and lead creative agencies.", "Design Systems, Motion Graphics, Brand Strategy", "AIGA Professional Guidelines", "Eye Magazine, Brand New (UnderConsideration)", "Leading international rebrand for consumer unicorn", "Creative Director / Head of Design.")
                ]
            },
            {
                "category_id": cat_comm.id,
                "title": "Fashion Designer",
                "slug": "fashion-designer",
                "summary": "Creative innovators designing apparel collections, footwear, textile weaves, and runway accessories.",
                "what_they_do": "Sketch seasonal fashion lines, select textile fabrics, drape patterns on mannequins, supervise garment construction, and showcase collections at fashion weeks.",
                "min_education_level": "school_11_12",
                "stream_flexibility": "Any stream in 10+2 (Science, Commerce, Arts).",
                "avg_salary_inr": "₹4,50,000 - ₹18,00,000 per annum",
                "growth_rate": "High (+16% YoY with expanding Indian apparel export and retail)",
                "official_source_url": "https://www.nift.ac.in",
                "official_authority_name": "National Institute of Fashion Technology (NIFT)",
                "icon_name": "scissors",
                "skills": [("Visual Creativity", 2.0), ("Spatial Reasoning", 1.8), ("Communication & Empathy", 1.5), ("Leadership & Teamwork", 1.4)],
                "requirements": [
                    ("academic", "10+2 in Any Stream", "Class 12th pass from any recognized state or central board.", True, "https://www.nift.ac.in"),
                    ("entrance_exam", "NIFT Entrance Exam (CAT + GAT + Situation Test)", "National entrance exam conducted by NTA for NIFT campuses across India.", True, "https://nift.nta.ac.in")
                ],
                "stages": [
                    (1, "Texture & Style Exploration (8th-10th)", "Explore fabrics, indigenous Indian weaves (Khadi, Chanderi, Ikat), and sketch garment silhouettes.", "Arts, Social Sciences", "School Costume Contests", "Vogue India, Fashion Illustration books", "Hand-stitched pouch or customized clothing embellishment", "Flair for style and texture combinations."),
                    (2, "NIFT Entrance Prep (11th-12th)", "Prepare Creative Ability Test (CAT) and General Ability Test (GAT) for NIFT.", "Any Stream", "NIFT Entrance Examination", "NIFT Past 10 Years Question Banks", "Portfolio of 20 fashion collection sketches", "Admission to NIFT B.Des Fashion Design."),
                    (3, "B.Des Fashion Curriculum (4 Years)", "Pattern making, garment construction, textile science, CAD fashion illustration, and runway styling.", "Fashion Design Core", "NIFT Graduation Fashion Show", "Patternmaking for Fashion Design by Armstrong", "Creating 5-look debut collection exhibited on runway", "NIFT Degree and placement with top designer or retail brand."),
                    (4, "Couture Label / Retail Creative Director", "Manage apparel lines for export houses or launch independent luxury designer label.", "Supply Chain, Sustainable Fashion, Merchandising", "Fashion Design Council of India (FDCI)", "Business of Fashion (BoF)", "Presenting solo collection at Lakmé Fashion Week", "Renowned Fashion Designer / Creative Director.")
                ]
            },
            {
                "category_id": cat_comm.id,
                "title": "Political Scientist",
                "slug": "political-scientist",
                "summary": "Scholars and policy analysts researching constitutional structures, geopolitical alliances, and public polling dynamics.",
                "what_they_do": "Analyze electoral polling trends, model geopolitical diplomacy shifts, author public policy whitepapers for think tanks, and advise legislative members.",
                "min_education_level": "college_grad",
                "stream_flexibility": "Graduation in Political Science, International Relations, Law, or Humanities.",
                "avg_salary_inr": "₹5,50,000 - ₹18,00,000 per annum",
                "growth_rate": "Steady (+13% YoY)",
                "official_source_url": "https://www.icssr.org",
                "official_authority_name": "Indian Council of Social Science Research (ICSSR)",
                "icon_name": "bank",
                "skills": [("Verbal Reasoning", 2.0), ("Critical Thinking", 1.9), ("Data Interpretation", 1.6), ("Communication & Empathy", 1.6)],
                "requirements": [
                    ("academic", "B.A. & M.A. in Political Science / Public Policy", "Undergraduate and master's degree from recognized university.", True, "https://www.icssr.org"),
                    ("entrance_exam", "CUET-PG / UGC-NET JRF", "National eligibility test for assistant professorship and research fellowships.", True, "https://ugcnet.nta.nic.in")
                ],
                "stages": [
                    (1, "Polity & Current Events (8th-10th)", "Follow parliamentary debates, elections, global United Nations summits, and read national civics.", "Social Sciences, English", "Inter-School Debates, Mock Parliament", "NCERT Political Science, The Hindu Editorials", "Essay analyzing federalism in India", "Deep appreciation for democratic institutions."),
                    (2, "Humanities Pre-University (11th-12th)", "Master political theory, comparative politics, Indian foreign policy, and Western political thought.", "Humanities / Any Stream", "CUET-UG (DU / JNU / Ashoka)", "NCERT 11th & 12th Political Science, Heywood Politics", "Research paper on electoral reform mechanisms", "Admission to top Political Science B.A. program."),
                    (3, "Postgraduate & Think Tank Research", "Quantitative election data analysis, public policy evaluation, international security frameworks.", "Political Science Core", "CUET-PG, UGC-NET", "Foreign Affairs, Economic and Political Weekly (EPW)", "Authoring published policy brief for think tank like ORF or CPR", "Junior Policy Analyst placement."),
                    (4, "Lead Geopolitical Strategist / Professor", "Advise parliamentary committees, publish academic books, and direct policy think tank initiatives.", "Strategic Studies, Electoral Modeling, Policy Writing", "UGC NET-JRF / Ph.D.", "International Security, ICSSR Research Grants", "Directing national election voter behavior survey", "Senior Fellow at National Think Tank / Tenured Professor.")
                ]
            }
        ]

        # Insert Careers, Requirements, Skills, and Roadmaps
        for cdata in careers_def:
            slug = cdata["slug"]
            career = db.query(Career).filter(Career.slug == slug).first()
            if not career:
                career = Career(
                    category_id=cdata["category_id"],
                    title=cdata["title"],
                    slug=slug,
                    summary=cdata["summary"],
                    what_they_do=cdata["what_they_do"],
                    min_education_level=cdata["min_education_level"],
                    stream_flexibility=cdata["stream_flexibility"],
                    avg_salary_inr=cdata["avg_salary_inr"],
                    growth_rate=cdata["growth_rate"],
                    official_source_url=cdata["official_source_url"],
                    official_authority_name=cdata["official_authority_name"],
                    icon_name=cdata["icon_name"]
                )
                db.add(career)
                db.commit()
                db.refresh(career)

            # Requirements
            for req_type, req_title, req_desc, is_mand, req_link in cdata["requirements"]:
                req = db.query(CareerRequirement).filter(
                    CareerRequirement.career_id == career.id,
                    CareerRequirement.title == req_title
                ).first()
                if not req:
                    req = CareerRequirement(
                        career_id=career.id,
                        requirement_type=req_type,
                        title=req_title,
                        description=req_desc,
                        is_mandatory=is_mand,
                        official_link=req_link
                    )
                    db.add(req)

            # Career Skills
            for sk_name, weight in cdata["skills"]:
                if sk_name in skill_map:
                    cskill = db.query(CareerSkill).filter(
                        CareerSkill.career_id == career.id,
                        CareerSkill.skill_id == skill_map[sk_name].id
                    ).first()
                    if not cskill:
                        cskill = CareerSkill(
                            career_id=career.id,
                            skill_id=skill_map[sk_name].id,
                            importance_weight=weight,
                            min_proficiency_needed=60
                        )
                        db.add(cskill)

            # Roadmap & Stages
            roadmap = db.query(CareerRoadmap).filter(CareerRoadmap.career_id == career.id).first()
            if not roadmap:
                roadmap = CareerRoadmap(
                    career_id=career.id,
                    education_level="all",
                    title=f"Complete Career Roadmap to become a {career.title} in India",
                    description=f"Curated step-by-step roadmap from school to professional licensing for {career.title}."
                )
                db.add(roadmap)
                db.commit()
                db.refresh(roadmap)

                for stg_num, stg_title, stg_obj, stg_sub, stg_exam, stg_res, stg_proj, stg_out in cdata["stages"]:
                    stg = RoadmapStage(
                        roadmap_id=roadmap.id,
                        stage_number=stg_num,
                        title=stg_title,
                        objective=stg_obj,
                        recommended_subjects=stg_sub,
                        entrance_exams=stg_exam,
                        resources=stg_res,
                        practical_projects=stg_proj,
                        expected_outcome=stg_out,
                        official_source_url=career.official_source_url
                    )
                    db.add(stg)

        db.commit()

        # 5. Assessment Modules (15 Universal Modules)
        print("Seeding 15 Assessment Modules...")
        module_map = {}
        for mod_def in MODULE_DEFINITIONS:
            mod = db.query(AssessmentModule).filter(AssessmentModule.code == mod_def["code"]).first()
            if not mod:
                mod = AssessmentModule(
                    code=mod_def["code"],
                    name=mod_def["name"],
                    module_number=mod_def["module_number"],
                    primary_dimension=mod_def["primary_dimension"],
                    description=mod_def.get("description"),
                    is_active=True
                )
                db.add(mod)
                db.flush()
            module_map[mod_def["code"]] = mod
        db.commit()

        # Build career slug map for configurations and questions
        career_by_slug = {c.slug: c for c in db.query(Career).all()}

        # 6. Assessment Configurations (Fixed, Not Fixed, Clarity)
        print("Seeding Assessment Configurations...")
        for cfg in ASSESSMENT_CONFIGURATIONS:
            c_career = career_by_slug.get(cfg.get("career_slug")) if cfg.get("career_slug") else None
            existing_cfg = db.query(AssessmentConfiguration).filter(AssessmentConfiguration.code == cfg["code"]).first()
            if not existing_cfg:
                new_cfg = AssessmentConfiguration(
                    code=cfg["code"],
                    name=cfg["name"],
                    mode=cfg["mode"],
                    career_id=c_career.id if c_career else None,
                    description=cfg.get("description"),
                    modules_config_json=cfg.get("modules_config"),
                    target_questions_count=cfg.get("target_questions_count", 25),
                    time_limit_minutes=cfg.get("time_limit_minutes", 30),
                    is_active=True
                )
                db.add(new_cfg)
        db.commit()

        # 7. Universal Question Bank (315 Questions across 15 Modules)
        print(f"Seeding {len(UNIVERSAL_QUESTIONS)} Universal Questions...")
        for qdata in UNIVERSAL_QUESTIONS:
            existing_q = db.query(Question).filter(Question.question_code == qdata["question_code"]).first()
            if not existing_q:
                mod = module_map.get(qdata.get("module_code"))
                new_q = Question(
                    question_code=qdata["question_code"],
                    module_id=mod.id if mod else None,
                    career_id=None,
                    category=qdata.get("category", "aptitude"),
                    sub_topic=qdata.get("sub_topic"),
                    education_level=qdata.get("education_level", "all"),
                    difficulty=qdata.get("difficulty", "medium"),
                    skill_name=qdata.get("skill_name"),
                    text=qdata["text"],
                    question_type=qdata.get("question_type", "multiple_choice"),
                    scoring_type=qdata.get("scoring_type", "accuracy"),
                    explanation=qdata.get("explanation"),
                    is_active=True
                )
                db.add(new_q)
                db.flush()

                for opt in qdata.get("options", []):
                    q_opt = QuestionOption(
                        question_id=new_q.id,
                        option_key=opt["option_key"],
                        text=opt["text"],
                        score_value=opt.get("score_value", 0.0),
                        is_correct=opt.get("is_correct", False),
                        skill_weights_json=opt.get("skill_weights_json")
                    )
                    db.add(q_opt)
        db.commit()

        # 8. Profession-Specific Question Bank (300 Questions across 30 Professions)
        print(f"Seeding {len(PROFESSION_QUESTIONS)} Profession-Specific Questions...")
        for qdata in PROFESSION_QUESTIONS:
            existing_q = db.query(Question).filter(Question.question_code == qdata["question_code"]).first()
            if not existing_q:
                c_target = career_by_slug.get(qdata.get("career_slug"))
                new_q = Question(
                    question_code=qdata["question_code"],
                    module_id=None,
                    career_id=c_target.id if c_target else None,
                    category=qdata.get("category", "domain"),
                    sub_topic=qdata.get("sub_topic"),
                    education_level=qdata.get("education_level", "all"),
                    difficulty=qdata.get("difficulty", "medium"),
                    skill_name=qdata.get("skill_name"),
                    text=qdata["text"],
                    question_type=qdata.get("question_type", "multiple_choice"),
                    scoring_type=qdata.get("scoring_type", "accuracy"),
                    explanation=qdata.get("explanation"),
                    is_active=True
                )
                db.add(new_q)
                db.flush()

                for opt in qdata.get("options", []):
                    q_opt = QuestionOption(
                        question_id=new_q.id,
                        option_key=opt["option_key"],
                        text=opt["text"],
                        score_value=opt.get("score_value", 0.0),
                        is_correct=opt.get("is_correct", False),
                        skill_weights_json=opt.get("skill_weights_json")
                    )
                    db.add(q_opt)
        db.commit()

        # 6. Course Providers and Partner Courses
        provider_swayam = db.query(CourseProvider).filter(CourseProvider.name == "SWAYAM / NPTEL (Govt of India)").first()
        if not provider_swayam:
            provider_swayam = CourseProvider(
                name="SWAYAM / NPTEL (Govt of India)",
                website_url="https://swayam.gov.in",
                default_commission_rate=0.0
            )
            db.add(provider_swayam)

        provider_coursera = db.query(CourseProvider).filter(CourseProvider.name == "Coursera Partner").first()
        if not provider_coursera:
            provider_coursera = CourseProvider(
                name="Coursera Partner",
                website_url="https://coursera.org",
                default_commission_rate=15.0
            )
            db.add(provider_coursera)
        db.commit()
        db.refresh(provider_swayam)
        db.refresh(provider_coursera)

        courses_seed = [
            (provider_swayam.id, "Foundations of Data Structures and Algorithms", "Official NPTEL course taught by IIT Madras faculty covering core computational thinking and problem-solving.", "Technology", ["Algorithmic Thinking", "Python & Programming"], "Beginner", 0.0, True, "12 Weeks", "IIT Certificate upon proctored exam", "https://swayam.gov.in/explorer?category=Computer_Science"),
            (provider_swayam.id, "Introduction to Indian Constitution & Legal Rights", "NPTEL National Law School curriculum introducing constitutional articles, fundamental rights, and statutory law.", "Humanities & Law", ["Legal Argumentation", "Verbal Reasoning"], "Beginner", 0.0, True, "8 Weeks", "Govt verified completion certificate", "https://swayam.gov.in"),
            (provider_coursera.id, "Python for Everybody Specialization", "Comprehensive step-by-step programming track from zero to full application development by University of Michigan.", "Technology", ["Python & Programming", "Algorithmic Thinking"], "Beginner", 1499.0, False, "8 Weeks", "Shareable Professional Certificate", "https://coursera.org/specializations/python"),
            (provider_coursera.id, "Financial Markets & Corporate Valuation", "Yale University course exploring practical risk-management, equities, bonds, and behavioral finance.", "Business & Finance", ["Financial Acumen", "Numerical Aptitude"], "Intermediate", 1999.0, False, "6 Weeks", "Yale University Certificate", "https://coursera.org/learn/financial-markets-global"),
            (provider_coursera.id, "Human Anatomy & Physiology Foundations", "University of Michigan pre-medical foundation exploring organ systems, clinical pathology, and homeostasis.", "Medical Sciences", ["Biology Fundamentals", "Scientific Method"], "Intermediate", 1499.0, False, "10 Weeks", "Verified Medical Certificate", "https://coursera.org/learn/anatomy")
        ]

        for prov_id, c_title, c_desc, c_cat, c_skills, c_diff, c_price, c_free, c_dur, c_cert, c_url in courses_seed:
            c = db.query(Course).filter(Course.title == c_title).first()
            if not c:
                c = Course(
                    provider_id=prov_id,
                    title=c_title,
                    description=c_desc,
                    category=c_cat,
                    skills_taught_json=c_skills,
                    difficulty=c_diff,
                    price_inr=c_price,
                    is_free=c_free,
                    duration=c_dur,
                    certificate_info=c_cert,
                    course_url=c_url,
                    affiliate_url=f"{c_url}?ref=PATHWAY_AI"
                )
                db.add(c)
        db.commit()

        # 7. Premium Plan
        p_plan = db.query(PremiumPlan).filter(PremiumPlan.code == "ALL_ACCESS_YEARLY").first()
        if not p_plan:
            p_plan = PremiumPlan(
                name="PATHWAY AI All-Access Pass",
                code="ALL_ACCESS_YEARLY",
                price_inr=999.0,
                duration_days=365,
                features_json=[
                    "Unlimited Retakes of all 30 Career Assessments",
                    "Interactive Deep-Dive Radar and Multi-Chart Analytics",
                    "Detailed 5-Stage Indian Career Roadmap with Entrance Exam Alerts",
                    "Customized Skill Gap Bridging Plan",
                    "Direct Partner Course Discounts & Study Material Links",
                    "Downloadable Official Career PDF Report"
                ]
            )
            db.add(p_plan)
            db.commit()

        print("Database successfully seeded with 30 careers, roadmaps, questions, skills, and courses!")

    except Exception as e:
        db.rollback()
        print(f"Error during database seed: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
