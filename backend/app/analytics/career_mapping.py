"""
PATHWAY AI - Multi-Dimensional Career-Skill Mapping System
Maps all 30 professions to:
1. Primary module dimension weights (15 Universal Modules)
2. Domain technical knowledge requirements
3. Soft skill & work preference indicators
4. Minimum proficiency thresholds
5. Evidence requirement indicators
"""

from typing import Dict, Any, List

CAREER_MAPPING_PROFILES: Dict[str, Dict[str, Any]] = {
    # ========================================================
    # CATEGORY 1: SCIENCE AND TECHNOLOGY (15 Professions)
    # ========================================================
    "doctor-mbbs": {
        "title": "Doctor (MBBS)",
        "category": "Science and Technology",
        "primary_stream": "PCB",
        "dimension_weights": {
            "numerical_aptitude": 0.5,
            "logical_reasoning": 0.8,
            "verbal_ability": 0.7,
            "critical_thinking": 1.0,
            "spatial_abstract": 0.6,
            "creativity": 0.4,
            "science_tech": 1.2,
            "commerce_finance": 0.1,
            "computational_thinking": 0.4,
            "interest_discovery": 0.9,
            "work_preferences": 0.9,
            "communication": 0.9,
            "situational_judgement": 1.1,
            "learning_style": 0.8,
            "career_exploration": 1.0
        },
        "critical_skills": ["Biology Fundamentals", "Clinical Empathy", "Diagnostic Reasoning", "Medical Ethics", "Stress Resilience"],
        "min_proficiency_threshold": 68.0,
        "evidence_requirements": ["science_tech", "situational_judgement", "critical_thinking"]
    },
    "engineer": {
        "title": "Engineer",
        "category": "Science and Technology",
        "primary_stream": "PCM",
        "dimension_weights": {
            "numerical_aptitude": 1.1,
            "logical_reasoning": 1.1,
            "verbal_ability": 0.5,
            "critical_thinking": 1.0,
            "spatial_abstract": 0.9,
            "creativity": 0.7,
            "science_tech": 1.1,
            "commerce_finance": 0.3,
            "computational_thinking": 0.8,
            "interest_discovery": 0.7,
            "work_preferences": 0.6,
            "communication": 0.6,
            "situational_judgement": 0.6,
            "learning_style": 0.8,
            "career_exploration": 0.8
        },
        "critical_skills": ["Physics Fundamentals", "Applied Mathematics", "System Design", "Analytical Problem Solving"],
        "min_proficiency_threshold": 65.0,
        "evidence_requirements": ["numerical_aptitude", "logical_reasoning", "science_tech"]
    },
    "data-scientist": {
        "title": "Data Scientist",
        "category": "Science and Technology",
        "primary_stream": "PCM / Stats",
        "dimension_weights": {
            "numerical_aptitude": 1.2,
            "logical_reasoning": 1.2,
            "verbal_ability": 0.6,
            "critical_thinking": 1.0,
            "spatial_abstract": 0.6,
            "creativity": 0.6,
            "science_tech": 0.8,
            "commerce_finance": 0.6,
            "computational_thinking": 1.2,
            "interest_discovery": 0.8,
            "work_preferences": 0.6,
            "communication": 0.6,
            "situational_judgement": 0.5,
            "learning_style": 0.9,
            "career_exploration": 0.8
        },
        "critical_skills": ["Statistical Inference", "Linear Algebra", "Data Interpretation", "Python/R Modeling", "Algorithmic Logic"],
        "min_proficiency_threshold": 68.0,
        "evidence_requirements": ["numerical_aptitude", "logical_reasoning", "computational_thinking"]
    },
    "software-developer": {
        "title": "Software Developer",
        "category": "Science and Technology",
        "primary_stream": "PCM / CS",
        "dimension_weights": {
            "numerical_aptitude": 0.9,
            "logical_reasoning": 1.2,
            "verbal_ability": 0.6,
            "critical_thinking": 1.0,
            "spatial_abstract": 0.6,
            "creativity": 0.7,
            "science_tech": 0.7,
            "commerce_finance": 0.2,
            "computational_thinking": 1.3,
            "interest_discovery": 0.8,
            "work_preferences": 0.6,
            "communication": 0.6,
            "situational_judgement": 0.5,
            "learning_style": 0.9,
            "career_exploration": 0.8
        },
        "critical_skills": ["Algorithmic Thinking", "Code Architecture", "Debugging", "Modular Problem Decomposition"],
        "min_proficiency_threshold": 65.0,
        "evidence_requirements": ["computational_thinking", "logical_reasoning"]
    },
    "artificial-intelligence-engineer": {
        "title": "Artificial Intelligence Engineer",
        "category": "Science and Technology",
        "primary_stream": "PCM / CS",
        "dimension_weights": {
            "numerical_aptitude": 1.2,
            "logical_reasoning": 1.2,
            "verbal_ability": 0.6,
            "critical_thinking": 1.1,
            "spatial_abstract": 0.7,
            "creativity": 0.8,
            "science_tech": 0.9,
            "commerce_finance": 0.3,
            "computational_thinking": 1.3,
            "interest_discovery": 0.9,
            "work_preferences": 0.7,
            "communication": 0.6,
            "situational_judgement": 0.6,
            "learning_style": 1.0,
            "career_exploration": 0.9
        },
        "critical_skills": ["Machine Learning Theory", "Calculus & Optimization", "Deep Neural Networks", "Computational Logic"],
        "min_proficiency_threshold": 70.0,
        "evidence_requirements": ["computational_thinking", "numerical_aptitude", "logical_reasoning"]
    },
    "pharmacist": {
        "title": "Pharmacist",
        "category": "Science and Technology",
        "primary_stream": "PCB / PCM",
        "dimension_weights": {
            "numerical_aptitude": 0.7,
            "logical_reasoning": 0.7,
            "verbal_ability": 0.7,
            "critical_thinking": 0.9,
            "spatial_abstract": 0.5,
            "creativity": 0.4,
            "science_tech": 1.2,
            "commerce_finance": 0.5,
            "computational_thinking": 0.4,
            "interest_discovery": 0.8,
            "work_preferences": 0.8,
            "communication": 0.8,
            "situational_judgement": 0.9,
            "learning_style": 0.7,
            "career_exploration": 0.8
        },
        "critical_skills": ["Chemistry & Pharmacology", "Dosage Calculations", "Quality Control", "Regulatory Compliance"],
        "min_proficiency_threshold": 62.0,
        "evidence_requirements": ["science_tech", "critical_thinking"]
    },
    "architect": {
        "title": "Architect",
        "category": "Science and Technology",
        "primary_stream": "PCM",
        "dimension_weights": {
            "numerical_aptitude": 0.8,
            "logical_reasoning": 0.8,
            "verbal_ability": 0.6,
            "critical_thinking": 0.8,
            "spatial_abstract": 1.3,
            "creativity": 1.2,
            "science_tech": 0.8,
            "commerce_finance": 0.4,
            "computational_thinking": 0.6,
            "interest_discovery": 0.9,
            "work_preferences": 0.7,
            "communication": 0.8,
            "situational_judgement": 0.6,
            "learning_style": 0.8,
            "career_exploration": 0.9
        },
        "critical_skills": ["3D Spatial Perception", "Visual Aesthetics", "Structural Geometry", "Design Thinking", "Urban Planning"],
        "min_proficiency_threshold": 65.0,
        "evidence_requirements": ["spatial_abstract", "creativity"]
    },
    "pilot": {
        "title": "Pilot",
        "category": "Science and Technology",
        "primary_stream": "PCM",
        "dimension_weights": {
            "numerical_aptitude": 0.9,
            "logical_reasoning": 1.0,
            "verbal_ability": 0.8,
            "critical_thinking": 1.1,
            "spatial_abstract": 1.2,
            "creativity": 0.3,
            "science_tech": 1.0,
            "commerce_finance": 0.2,
            "computational_thinking": 0.5,
            "interest_discovery": 0.8,
            "work_preferences": 0.9,
            "communication": 1.0,
            "situational_judgement": 1.2,
            "learning_style": 0.8,
            "career_exploration": 0.9
        },
        "critical_skills": ["Spatial Orientation", "Rapid Situational Judgment", "Multi-Task Coordination", "Aviation Meteorology", "Standard Radiotelephony"],
        "min_proficiency_threshold": 70.0,
        "evidence_requirements": ["spatial_abstract", "situational_judgement", "critical_thinking"]
    },
    "biotechnologist": {
        "title": "Biotechnologist",
        "category": "Science and Technology",
        "primary_stream": "PCB / PCM",
        "dimension_weights": {
            "numerical_aptitude": 0.8,
            "logical_reasoning": 0.9,
            "verbal_ability": 0.7,
            "critical_thinking": 1.0,
            "spatial_abstract": 0.6,
            "creativity": 0.7,
            "science_tech": 1.3,
            "commerce_finance": 0.3,
            "computational_thinking": 0.7,
            "interest_discovery": 0.9,
            "work_preferences": 0.7,
            "communication": 0.6,
            "situational_judgement": 0.8,
            "learning_style": 0.9,
            "career_exploration": 0.8
        },
        "critical_skills": ["Molecular Biology", "Genetic Engineering", "Bioinformatics", "Laboratory Instrumentation"],
        "min_proficiency_threshold": 65.0,
        "evidence_requirements": ["science_tech", "critical_thinking"]
    },
    "research-scientist": {
        "title": "Research Scientist",
        "category": "Science and Technology",
        "primary_stream": "Science",
        "dimension_weights": {
            "numerical_aptitude": 1.0,
            "logical_reasoning": 1.1,
            "verbal_ability": 0.8,
            "critical_thinking": 1.2,
            "spatial_abstract": 0.7,
            "creativity": 0.9,
            "science_tech": 1.3,
            "commerce_finance": 0.2,
            "computational_thinking": 0.8,
            "interest_discovery": 1.0,
            "work_preferences": 0.8,
            "communication": 0.7,
            "situational_judgement": 0.8,
            "learning_style": 1.1,
            "career_exploration": 0.8
        },
        "critical_skills": ["Scientific Hypothesis Formulation", "Experimental Rigor", "Data Synthesis", "Peer Research Writing"],
        "min_proficiency_threshold": 68.0,
        "evidence_requirements": ["science_tech", "critical_thinking", "learning_style"]
    },
    "dentist": {
        "title": "Dentist",
        "category": "Science and Technology",
        "primary_stream": "PCB",
        "dimension_weights": {
            "numerical_aptitude": 0.6,
            "logical_reasoning": 0.8,
            "verbal_ability": 0.7,
            "critical_thinking": 0.9,
            "spatial_abstract": 0.9,
            "creativity": 0.6,
            "science_tech": 1.1,
            "commerce_finance": 0.4,
            "computational_thinking": 0.3,
            "interest_discovery": 0.8,
            "work_preferences": 0.8,
            "communication": 0.9,
            "situational_judgement": 1.0,
            "learning_style": 0.7,
            "career_exploration": 0.8
        },
        "critical_skills": ["Dental Anatomy & Surgery", "Fine Motor Dexterity", "Patient Communication", "Clinical Sterilization"],
        "min_proficiency_threshold": 65.0,
        "evidence_requirements": ["science_tech", "spatial_abstract", "situational_judgement"]
    },
    "physiotherapist": {
        "title": "Physiotherapist",
        "category": "Science and Technology",
        "primary_stream": "PCB",
        "dimension_weights": {
            "numerical_aptitude": 0.5,
            "logical_reasoning": 0.7,
            "verbal_ability": 0.7,
            "critical_thinking": 0.9,
            "spatial_abstract": 0.7,
            "creativity": 0.5,
            "science_tech": 1.1,
            "commerce_finance": 0.3,
            "computational_thinking": 0.3,
            "interest_discovery": 0.8,
            "work_preferences": 0.8,
            "communication": 1.0,
            "situational_judgement": 0.9,
            "learning_style": 0.8,
            "career_exploration": 0.8
        },
        "critical_skills": ["Musculoskeletal Kinesiology", "Rehabilitation Protocols", "Active Listening", "Patient Encouragement"],
        "min_proficiency_threshold": 62.0,
        "evidence_requirements": ["science_tech", "communication"]
    },
    "cybersecurity-analyst": {
        "title": "Cybersecurity Analyst",
        "category": "Science and Technology",
        "primary_stream": "PCM / CS",
        "dimension_weights": {
            "numerical_aptitude": 0.8,
            "logical_reasoning": 1.2,
            "verbal_ability": 0.6,
            "critical_thinking": 1.2,
            "spatial_abstract": 0.6,
            "creativity": 0.6,
            "science_tech": 0.8,
            "commerce_finance": 0.4,
            "computational_thinking": 1.3,
            "interest_discovery": 0.8,
            "work_preferences": 0.7,
            "communication": 0.6,
            "situational_judgement": 0.9,
            "learning_style": 0.9,
            "career_exploration": 0.8
        },
        "critical_skills": ["Threat Vector Modeling", "Network Protocol Auditing", "Vulnerability Assessment", "Incident Response"],
        "min_proficiency_threshold": 68.0,
        "evidence_requirements": ["computational_thinking", "critical_thinking", "logical_reasoning"]
    },
    "mechanical-engineer": {
        "title": "Mechanical Engineer",
        "category": "Science and Technology",
        "primary_stream": "PCM",
        "dimension_weights": {
            "numerical_aptitude": 1.1,
            "logical_reasoning": 1.0,
            "verbal_ability": 0.5,
            "critical_thinking": 1.0,
            "spatial_abstract": 1.1,
            "creativity": 0.7,
            "science_tech": 1.2,
            "commerce_finance": 0.3,
            "computational_thinking": 0.7,
            "interest_discovery": 0.7,
            "work_preferences": 0.7,
            "communication": 0.6,
            "situational_judgement": 0.7,
            "learning_style": 0.8,
            "career_exploration": 0.8
        },
        "critical_skills": ["Thermodynamics", "Statics & Dynamics", "CAD/SolidWorks Modeling", "Manufacturing Processes"],
        "min_proficiency_threshold": 65.0,
        "evidence_requirements": ["numerical_aptitude", "spatial_abstract", "science_tech"]
    },
    "statistician": {
        "title": "Statistician",
        "category": "Science and Technology",
        "primary_stream": "Math / Stats",
        "dimension_weights": {
            "numerical_aptitude": 1.3,
            "logical_reasoning": 1.2,
            "verbal_ability": 0.6,
            "critical_thinking": 1.0,
            "spatial_abstract": 0.5,
            "creativity": 0.5,
            "science_tech": 0.7,
            "commerce_finance": 0.7,
            "computational_thinking": 1.0,
            "interest_discovery": 0.8,
            "work_preferences": 0.7,
            "communication": 0.6,
            "situational_judgement": 0.5,
            "learning_style": 0.8,
            "career_exploration": 0.8
        },
        "critical_skills": ["Probability Distributions", "Hypothesis Testing", "Biostatistics & Econometrics", "Sampling Design"],
        "min_proficiency_threshold": 70.0,
        "evidence_requirements": ["numerical_aptitude", "logical_reasoning"]
    },

    # ========================================================
    # CATEGORY 2: COMMERCE, BUSINESS, ARTS & HUMANITIES (15)
    # ========================================================
    "chartered-accountant-ca": {
        "title": "Chartered Accountant (CA)",
        "category": "Commerce, Business, Arts and Humanities",
        "primary_stream": "Commerce / Any",
        "dimension_weights": {
            "numerical_aptitude": 1.2,
            "logical_reasoning": 1.0,
            "verbal_ability": 0.7,
            "critical_thinking": 1.1,
            "spatial_abstract": 0.3,
            "creativity": 0.4,
            "science_tech": 0.2,
            "commerce_finance": 1.3,
            "computational_thinking": 0.5,
            "interest_discovery": 0.9,
            "work_preferences": 0.9,
            "communication": 0.7,
            "situational_judgement": 1.1,
            "learning_style": 0.8,
            "career_exploration": 0.9
        },
        "critical_skills": ["Double-Entry Accounting", "Indian Tax Laws (GST/IT Act)", "Auditing Standards", "Financial Precision"],
        "min_proficiency_threshold": 70.0,
        "evidence_requirements": ["commerce_finance", "numerical_aptitude", "situational_judgement"]
    },
    "investment-banker": {
        "title": "Investment Banker",
        "category": "Commerce, Business, Arts and Humanities",
        "primary_stream": "Commerce / Math / Eco",
        "dimension_weights": {
            "numerical_aptitude": 1.2,
            "logical_reasoning": 1.1,
            "verbal_ability": 0.8,
            "critical_thinking": 1.1,
            "spatial_abstract": 0.4,
            "creativity": 0.6,
            "science_tech": 0.2,
            "commerce_finance": 1.3,
            "computational_thinking": 0.7,
            "interest_discovery": 0.9,
            "work_preferences": 0.9,
            "communication": 0.9,
            "situational_judgement": 0.9,
            "learning_style": 0.9,
            "career_exploration": 0.9
        },
        "critical_skills": ["Financial Valuation (DCF/LBO)", "M&A Deal Structuring", "Market Capital Analysis", "Pitch Presentation"],
        "min_proficiency_threshold": 72.0,
        "evidence_requirements": ["commerce_finance", "numerical_aptitude", "critical_thinking"]
    },
    "financial-analyst": {
        "title": "Financial Analyst",
        "category": "Commerce, Business, Arts and Humanities",
        "primary_stream": "Commerce / Eco / Math",
        "dimension_weights": {
            "numerical_aptitude": 1.2,
            "logical_reasoning": 1.1,
            "verbal_ability": 0.7,
            "critical_thinking": 1.0,
            "spatial_abstract": 0.4,
            "creativity": 0.5,
            "science_tech": 0.3,
            "commerce_finance": 1.3,
            "computational_thinking": 0.8,
            "interest_discovery": 0.8,
            "work_preferences": 0.7,
            "communication": 0.7,
            "situational_judgement": 0.7,
            "learning_style": 0.8,
            "career_exploration": 0.8
        },
        "critical_skills": ["Financial Statement Modeling", "Variance Analysis", "Portfolio Optimization", "Macroeconomic Forecasting"],
        "min_proficiency_threshold": 68.0,
        "evidence_requirements": ["commerce_finance", "numerical_aptitude"]
    },
    "business-manager": {
        "title": "Business Manager",
        "category": "Commerce, Business, Arts and Humanities",
        "primary_stream": "Any Stream",
        "dimension_weights": {
            "numerical_aptitude": 0.8,
            "logical_reasoning": 0.9,
            "verbal_ability": 0.9,
            "critical_thinking": 1.0,
            "spatial_abstract": 0.4,
            "creativity": 0.7,
            "science_tech": 0.3,
            "commerce_finance": 1.0,
            "computational_thinking": 0.5,
            "interest_discovery": 0.9,
            "work_preferences": 0.9,
            "communication": 1.2,
            "situational_judgement": 1.1,
            "learning_style": 0.8,
            "career_exploration": 0.9
        },
        "critical_skills": ["Operations Strategy", "People Leadership", "Budget Oversight", "Stakeholder Alignment", "Conflict Resolution"],
        "min_proficiency_threshold": 66.0,
        "evidence_requirements": ["communication", "situational_judgement", "commerce_finance"]
    },
    "entrepreneur": {
        "title": "Entrepreneur",
        "category": "Commerce, Business, Arts and Humanities",
        "primary_stream": "Any Stream",
        "dimension_weights": {
            "numerical_aptitude": 0.8,
            "logical_reasoning": 1.0,
            "verbal_ability": 0.9,
            "critical_thinking": 1.1,
            "spatial_abstract": 0.5,
            "creativity": 1.2,
            "science_tech": 0.5,
            "commerce_finance": 1.0,
            "computational_thinking": 0.7,
            "interest_discovery": 1.0,
            "work_preferences": 1.0,
            "communication": 1.1,
            "situational_judgement": 1.1,
            "learning_style": 1.0,
            "career_exploration": 0.9
        },
        "critical_skills": ["Venture Creation", "Product-Market Fit", "Calculated Risk-Taking", "Customer Empathy", "Capital Allocation"],
        "min_proficiency_threshold": 68.0,
        "evidence_requirements": ["creativity", "situational_judgement", "critical_thinking"]
    },
    "marketing-manager": {
        "title": "Marketing Manager",
        "category": "Commerce, Business, Arts and Humanities",
        "primary_stream": "Any Stream",
        "dimension_weights": {
            "numerical_aptitude": 0.7,
            "logical_reasoning": 0.8,
            "verbal_ability": 1.0,
            "critical_thinking": 0.9,
            "spatial_abstract": 0.6,
            "creativity": 1.2,
            "science_tech": 0.3,
            "commerce_finance": 0.8,
            "computational_thinking": 0.6,
            "interest_discovery": 0.9,
            "work_preferences": 0.8,
            "communication": 1.2,
            "situational_judgement": 0.8,
            "learning_style": 0.8,
            "career_exploration": 0.9
        },
        "critical_skills": ["Consumer Behavioral Psychology", "Brand Strategy", "Campaign Analytics", "Narrative Storytelling"],
        "min_proficiency_threshold": 65.0,
        "evidence_requirements": ["creativity", "communication"]
    },
    "company-secretary-cs": {
        "title": "Company Secretary (CS)",
        "category": "Commerce, Business, Arts and Humanities",
        "primary_stream": "Commerce / Arts",
        "dimension_weights": {
            "numerical_aptitude": 0.7,
            "logical_reasoning": 0.9,
            "verbal_ability": 1.1,
            "critical_thinking": 1.1,
            "spatial_abstract": 0.3,
            "creativity": 0.4,
            "science_tech": 0.1,
            "commerce_finance": 1.1,
            "computational_thinking": 0.4,
            "interest_discovery": 0.8,
            "work_preferences": 0.9,
            "communication": 0.9,
            "situational_judgement": 1.2,
            "learning_style": 0.8,
            "career_exploration": 0.8
        },
        "critical_skills": ["Companies Act 2013", "Corporate Governance", "Board Secretarial Compliance", "SEBI Regulations"],
        "min_proficiency_threshold": 68.0,
        "evidence_requirements": ["verbal_ability", "situational_judgement", "commerce_finance"]
    },
    "lawyer": {
        "title": "Lawyer",
        "category": "Commerce, Business, Arts and Humanities",
        "primary_stream": "Any Stream",
        "dimension_weights": {
            "numerical_aptitude": 0.5,
            "logical_reasoning": 1.1,
            "verbal_ability": 1.3,
            "critical_thinking": 1.3,
            "spatial_abstract": 0.3,
            "creativity": 0.7,
            "science_tech": 0.2,
            "commerce_finance": 0.6,
            "computational_thinking": 0.4,
            "interest_discovery": 0.9,
            "work_preferences": 0.9,
            "communication": 1.2,
            "situational_judgement": 1.2,
            "learning_style": 0.9,
            "career_exploration": 0.9
        },
        "critical_skills": ["Constitutional Law", "Legal Precedent Synthesis", "Courtroom Advocacy", "Contractual Drafting"],
        "min_proficiency_threshold": 70.0,
        "evidence_requirements": ["verbal_ability", "critical_thinking", "situational_judgement"]
    },
    "ias-officer": {
        "title": "IAS Officer",
        "category": "Commerce, Business, Arts and Humanities",
        "primary_stream": "Any Stream",
        "dimension_weights": {
            "numerical_aptitude": 0.7,
            "logical_reasoning": 1.0,
            "verbal_ability": 1.2,
            "critical_thinking": 1.3,
            "spatial_abstract": 0.5,
            "creativity": 0.7,
            "science_tech": 0.5,
            "commerce_finance": 0.7,
            "computational_thinking": 0.5,
            "interest_discovery": 1.0,
            "work_preferences": 1.0,
            "communication": 1.2,
            "situational_judgement": 1.3,
            "learning_style": 1.0,
            "career_exploration": 1.0
        },
        "critical_skills": ["Public Policy Administration", "Constitutional Ethos", "Crisis Management", "Inter-Departmental Coordination"],
        "min_proficiency_threshold": 75.0,
        "evidence_requirements": ["critical_thinking", "situational_judgement", "verbal_ability", "communication"]
    },
    "ips-officer": {
        "title": "IPS Officer",
        "category": "Commerce, Business, Arts and Humanities",
        "primary_stream": "Any Stream",
        "dimension_weights": {
            "numerical_aptitude": 0.6,
            "logical_reasoning": 1.1,
            "verbal_ability": 1.0,
            "critical_thinking": 1.2,
            "spatial_abstract": 0.8,
            "creativity": 0.5,
            "science_tech": 0.5,
            "commerce_finance": 0.4,
            "computational_thinking": 0.5,
            "interest_discovery": 0.9,
            "work_preferences": 1.1,
            "communication": 1.1,
            "situational_judgement": 1.3,
            "learning_style": 0.9,
            "career_exploration": 0.9
        },
        "critical_skills": ["Law Enforcement & IPC/CrPC", "Emergency Incident Command", "Investigative Analysis", "Physical Stamina"],
        "min_proficiency_threshold": 72.0,
        "evidence_requirements": ["situational_judgement", "critical_thinking", "logical_reasoning"]
    },
    "journalist": {
        "title": "Journalist",
        "category": "Commerce, Business, Arts and Humanities",
        "primary_stream": "Any Stream",
        "dimension_weights": {
            "numerical_aptitude": 0.5,
            "logical_reasoning": 0.9,
            "verbal_ability": 1.3,
            "critical_thinking": 1.2,
            "spatial_abstract": 0.4,
            "creativity": 1.0,
            "science_tech": 0.4,
            "commerce_finance": 0.5,
            "computational_thinking": 0.5,
            "interest_discovery": 1.0,
            "work_preferences": 0.8,
            "communication": 1.3,
            "situational_judgement": 1.1,
            "learning_style": 0.9,
            "career_exploration": 0.9
        },
        "critical_skills": ["Investigative Reporting", "Ethical Fact Verification", "Editorial Writing", "Interviewing & Field Media"],
        "min_proficiency_threshold": 66.0,
        "evidence_requirements": ["verbal_ability", "communication", "critical_thinking"]
    },
    "psychologist": {
        "title": "Psychologist",
        "category": "Commerce, Business, Arts and Humanities",
        "primary_stream": "Humanities / Science",
        "dimension_weights": {
            "numerical_aptitude": 0.6,
            "logical_reasoning": 0.8,
            "verbal_ability": 1.1,
            "critical_thinking": 1.1,
            "spatial_abstract": 0.4,
            "creativity": 0.7,
            "science_tech": 0.8,
            "commerce_finance": 0.2,
            "computational_thinking": 0.4,
            "interest_discovery": 1.0,
            "work_preferences": 0.9,
            "communication": 1.3,
            "situational_judgement": 1.2,
            "learning_style": 0.9,
            "career_exploration": 0.9
        },
        "critical_skills": ["Cognitive Behavioral Assessment", "Active Counseling Empathy", "Psychometric Statistics", "Clinical Ethics"],
        "min_proficiency_threshold": 67.0,
        "evidence_requirements": ["communication", "situational_judgement", "verbal_ability"]
    },
    "graphic-designer": {
        "title": "Graphic Designer",
        "category": "Commerce, Business, Arts and Humanities",
        "primary_stream": "Any Stream",
        "dimension_weights": {
            "numerical_aptitude": 0.4,
            "logical_reasoning": 0.6,
            "verbal_ability": 0.7,
            "critical_thinking": 0.7,
            "spatial_abstract": 1.3,
            "creativity": 1.4,
            "science_tech": 0.3,
            "commerce_finance": 0.4,
            "computational_thinking": 0.7,
            "interest_discovery": 0.9,
            "work_preferences": 0.7,
            "communication": 0.8,
            "situational_judgement": 0.5,
            "learning_style": 0.8,
            "career_exploration": 0.9
        },
        "critical_skills": ["Visual Typography & Hierarchy", "Color Theory", "UI/Digital Asset Creation", "Adobe Creative Suite"],
        "min_proficiency_threshold": 65.0,
        "evidence_requirements": ["creativity", "spatial_abstract"]
    },
    "fashion-designer": {
        "title": "Fashion Designer",
        "category": "Commerce, Business, Arts and Humanities",
        "primary_stream": "Any Stream",
        "dimension_weights": {
            "numerical_aptitude": 0.4,
            "logical_reasoning": 0.6,
            "verbal_ability": 0.7,
            "critical_thinking": 0.7,
            "spatial_abstract": 1.2,
            "creativity": 1.4,
            "science_tech": 0.4,
            "commerce_finance": 0.6,
            "computational_thinking": 0.5,
            "interest_discovery": 0.9,
            "work_preferences": 0.7,
            "communication": 0.8,
            "situational_judgement": 0.5,
            "learning_style": 0.8,
            "career_exploration": 0.9
        },
        "critical_skills": ["Garment Construction & Draping", "Textile Science", "Trend Forecasting", "Fashion Portfolio Design"],
        "min_proficiency_threshold": 65.0,
        "evidence_requirements": ["creativity", "spatial_abstract"]
    },
    "political-scientist": {
        "title": "Political Scientist",
        "category": "Commerce, Business, Arts and Humanities",
        "primary_stream": "Humanities / Arts",
        "dimension_weights": {
            "numerical_aptitude": 0.6,
            "logical_reasoning": 1.0,
            "verbal_ability": 1.3,
            "critical_thinking": 1.3,
            "spatial_abstract": 0.3,
            "creativity": 0.7,
            "science_tech": 0.3,
            "commerce_finance": 0.6,
            "computational_thinking": 0.5,
            "interest_discovery": 1.0,
            "work_preferences": 0.8,
            "communication": 1.1,
            "situational_judgement": 1.1,
            "learning_style": 1.0,
            "career_exploration": 0.9
        },
        "critical_skills": ["Comparative Political Systems", "Geopolitical Discourse", "Public Opinion Polling", "Governance Critique"],
        "min_proficiency_threshold": 68.0,
        "evidence_requirements": ["verbal_ability", "critical_thinking"]
    }
}

MODULE_DEFINITIONS: List[Dict[str, Any]] = [
    {
        "code": "M01_GEN_APTITUDE",
        "module_number": 1,
        "name": "General Aptitude",
        "primary_dimension": "numerical_aptitude",
        "description": "Numerical aptitude, basic mathematical reasoning, quantitative ability, and data interpretation."
    },
    {
        "code": "M02_LOGICAL_REASONING",
        "module_number": 2,
        "name": "Logical Reasoning",
        "primary_dimension": "logical_reasoning",
        "description": "Number series, pattern recognition, logical sequences, deductive and inductive reasoning, and analytical puzzles."
    },
    {
        "code": "M03_VERBAL_ABILITY",
        "module_number": 3,
        "name": "Verbal Ability",
        "primary_dimension": "verbal_ability",
        "description": "Reading comprehension, vocabulary in context, language reasoning, verbal logic, and communication understanding."
    },
    {
        "code": "M04_CRITICAL_THINKING",
        "module_number": 4,
        "name": "Critical Thinking",
        "primary_dimension": "critical_thinking",
        "description": "Evaluating information, identifying unspoken assumptions, evidence-based reasoning, and problem analysis."
    },
    {
        "code": "M05_SPATIAL_ABSTRACT",
        "module_number": 5,
        "name": "Spatial and Abstract Reasoning",
        "primary_dimension": "spatial_abstract",
        "description": "Visual patterns, 2D/3D shape manipulation, spatial orientation, and abstract matrix analogies."
    },
    {
        "code": "M06_CREATIVITY_INNOVATION",
        "module_number": 6,
        "name": "Creativity and Innovation",
        "primary_dimension": "creativity",
        "description": "Creative problem solving, design thinking, lateral idea generation, and visual imagination."
    },
    {
        "code": "M07_SCIENCE_TECHNICAL",
        "module_number": 7,
        "name": "Science and Technical Interest",
        "primary_dimension": "science_tech",
        "description": "Scientific curiosity, physics, chemistry, biology fundamentals, and practical technological awareness."
    },
    {
        "code": "M08_COMMERCE_FINANCE",
        "module_number": 8,
        "name": "Commerce and Financial Aptitude",
        "primary_dimension": "commerce_finance",
        "description": "Financial reasoning, basic accounting concepts, economic fundamentals, and commercial decision-making."
    },
    {
        "code": "M09_COMPUTATIONAL_THINKING",
        "module_number": 9,
        "name": "Digital and Computational Thinking",
        "primary_dimension": "computational_thinking",
        "description": "Understanding algorithms, step-by-step problem decomposition, logic gates, and technological logic."
    },
    {
        "code": "M10_INTEREST_DISCOVERY",
        "module_number": 10,
        "name": "Interest Discovery",
        "primary_dimension": "interest_discovery",
        "description": "Subject preferences, passion areas, preferred workplace environments, and intellectual curiosities."
    },
    {
        "code": "M11_WORK_PREFERENCES",
        "module_number": 11,
        "name": "Personality-Related Work Preferences",
        "primary_dimension": "work_preferences",
        "description": "Autonomous vs team collaboration, leadership willingness, adaptability, and structured vs exploratory work."
    },
    {
        "code": "M12_COMMUNICATION_SKILLS",
        "module_number": 12,
        "name": "Communication and Interpersonal Skills",
        "primary_dimension": "communication",
        "description": "Collaboration scenarios, empathetic listening, dispute negotiation, and verbal articulation."
    },
    {
        "code": "M13_SITUATIONAL_JUDGEMENT",
        "module_number": 13,
        "name": "Situational Judgement",
        "primary_dimension": "situational_judgement",
        "description": "Ethical workplace dilemmas, crisis decision-making under uncertainty, and professional integrity."
    },
    {
        "code": "M14_LEARNING_STYLE",
        "module_number": 14,
        "name": "Learning and Problem-Solving Style",
        "primary_dimension": "learning_style",
        "description": "Hands-on experimentation vs theoretical mastery, persistence under roadblock, and learning retention."
    },
    {
        "code": "M15_CAREER_EXPLORATION",
        "module_number": 15,
        "name": "Career Interest Exploration",
        "primary_dimension": "career_exploration",
        "description": "Explicit interest evaluation across the 30 professions and willingness to commit to training pathways."
    }
]
