# -*- coding: utf-8 -*-
from typing import List, Dict, Any
from backend.app.data.professions_sci_tech import get_sci_tech_questions
from backend.app.data.professions_comm_arts import get_comm_arts_questions

def get_all_profession_questions() -> List[Dict[str, Any]]:
    all_q = []
    all_q.extend(get_sci_tech_questions())
    all_q.extend(get_comm_arts_questions())
    return all_q
