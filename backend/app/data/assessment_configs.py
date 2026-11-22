"""
PATHWAY AI - Assessment Configurations
Defines configuration schemas for:
1. 30 Dedicated Profession-Specific Assessments (Fixed Career Mode)
2. Universal Multi-Module Assessment (Not Fixed Mode)
3. Combined Comparative Assessment (Career Clarity Mode)
"""

from typing import Dict, Any, List
from backend.app.analytics.career_mapping import CAREER_MAPPING_PROFILES, MODULE_DEFINITIONS

def get_all_assessment_configurations() -> List[Dict[str, Any]]:
    configs = []

    # 1. 30 Dedicated Fixed Career Configurations
    for slug, profile in CAREER_MAPPING_PROFILES.items():
        configs.append({
            "code": f"CONFIG_FIXED_{slug.upper().replace('-', '_')}",
            "name": f"Dedicated {profile['title']} Professional Evaluation",
            "mode": "fixed",
            "career_slug": slug,
            "education_level": "all",
            "description": f"Comprehensive profession-specific assessment for aspiring {profile['title']}s. Evaluates specialized domain knowledge, aptitude dimensions, and critical competencies.",
            "modules_config": {
                "profession_specific_count": 10,
                "foundational_aptitude_count": 5,
                "domain_situational_count": 5,
                "total_target": 20
            },
            "target_questions_count": 20,
            "time_limit_minutes": 25,
            "is_active": True
        })

    # 2. Universal Not Fixed Discovery Configuration
    configs.append({
        "code": "CONFIG_UNIVERSAL_NOT_FIXED",
        "name": "Universal Career Discovery & Aptitude Assessment (15 Modules)",
        "mode": "not_fixed",
        "career_slug": None,
        "education_level": "all",
        "description": "Comprehensive 15-module diagnostic assessment evaluating general aptitude, logical reasoning, verbal ability, critical thinking, spatial reasoning, creativity, technical knowledge, commerce aptitude, computational thinking, interests, and work preferences across all 30 professions.",
        "modules_config": {
            "modules_evaluated": [m["code"] for m in MODULE_DEFINITIONS],
            "questions_per_module": 2, # Core 30 questions (2 per module across all 15 modules)
            "adaptive_drilldown_target": 10, # Up to 10 additional questions for top matched careers
            "total_target": 30
        },
        "target_questions_count": 30,
        "time_limit_minutes": 40,
        "is_active": True
    })

    # 3. Career Clarity Comparative Configuration
    configs.append({
        "code": "CONFIG_CAREER_CLARITY",
        "name": "Career Clarity Multi-Profession Comparative Framework",
        "mode": "clarity",
        "career_slug": None,
        "education_level": "all",
        "description": "Blended assessment architecture combining dedicated profession assessments for 2-3 chosen careers with core Universal diagnostic modules to evaluate trade-offs and discover alternatives across all 30 careers.",
        "modules_config": {
            "questions_per_selected_career": 6, # Dedicated questions per chosen career
            "core_universal_modules": ["M01_GEN_APTITUDE", "M02_LOGICAL_REASONING", "M04_CRITICAL_THINKING", "M10_INTEREST_DISCOVERY", "M11_WORK_PREFERENCES", "M15_CAREER_EXPLORATION"],
            "universal_questions_count": 12,
            "total_target": 24
        },
        "target_questions_count": 24,
        "time_limit_minutes": 35,
        "is_active": True
    })

    return configs

ASSESSMENT_CONFIGURATIONS = get_all_assessment_configurations()

if __name__ == "__main__":
    print(f"Total Configurations Defined: {len(ASSESSMENT_CONFIGURATIONS)}")
    for c in ASSESSMENT_CONFIGURATIONS:
        print(f"  [{c['mode']}] {c['code']} - {c['name']}")
