"""
PATHWAY AI - Universal Assessment Question Bank
Total: 315 Meticulously Structured Questions across 15 Modules
Capable of evaluating students across all 30 Indian Professions
"""

from typing import List, Dict, Any
from backend.app.data.modules_1_2 import get_universal_questions as get_m1_m2
from backend.app.data.modules_3_to_6 import get_modules_3_to_6
from backend.app.data.modules_7_to_9 import get_modules_7_to_9
from backend.app.data.modules_10_to_15 import get_modules_10_to_15

def load_all_universal_questions() -> List[Dict[str, Any]]:
    all_q = []
    all_q.extend(get_m1_m2())
    all_q.extend(get_modules_3_to_6())
    all_q.extend(get_modules_7_to_9())
    all_q.extend(get_modules_10_to_15())
    return all_q

UNIVERSAL_QUESTIONS = load_all_universal_questions()

if __name__ == "__main__":
    from collections import Counter
    print(f"Total Universal Questions Loaded: {len(UNIVERSAL_QUESTIONS)}")
    mod_counts = Counter(q["module_code"] for q in UNIVERSAL_QUESTIONS)
    for mod, count in sorted(mod_counts.items()):
        print(f"  {mod}: {count} questions")
