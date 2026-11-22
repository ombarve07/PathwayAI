# -*- coding: utf-8 -*-
"""
Builder for 300 Profession-Specific Questions (10 per profession across all 30 careers).
"""

import sys
from backend.app.data.build_profession_data import get_all_profession_questions

def load_all_profession_questions():
    return get_all_profession_questions()

PROFESSION_QUESTIONS = load_all_profession_questions()

if __name__ == "__main__":
    from collections import Counter
    print(f"Total Profession Questions Loaded: {len(PROFESSION_QUESTIONS)}")
    slug_counts = Counter(q["career_slug"] for q in PROFESSION_QUESTIONS)
    print(f"Total Unique Careers Covered: {len(slug_counts)}")
    for slug, count in sorted(slug_counts.items()):
        print(f"  {slug}: {count} questions")
