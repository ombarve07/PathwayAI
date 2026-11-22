import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database import SessionLocal
from backend.app.models.entities import Career, AssessmentConfiguration, AssessmentModule

client = TestClient(app)

def test_fixed_career_mode_doctor_and_ca():
    # 1. Register Student
    email = "fixed.tester@example.com"
    reg = client.post("/api/auth/register", json={
        "full_name": "Rohan Mehra",
        "email": email,
        "password": "Password@123",
        "guardian_consent": True
    })
    token = reg.json()["access_token"] if reg.status_code == 200 else client.post("/api/auth/login", json={
        "email": email, "password": "Password@123"
    }).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Set 11th-12th PCB education
    client.post("/api/students/education", json={
        "education_level": "school_11_12",
        "stream": "Science PCB",
        "subjects": "Physics, Chemistry, Biology, English",
        "board_university": "CBSE"
    }, headers=headers)

    # Fetch Doctor career
    db = SessionLocal()
    doctor = db.query(Career).filter(Career.slug == "doctor-mbbs").first()
    db.close()
    assert doctor is not None

    # Start FIXED CAREER mode for Doctor
    start_res = client.post("/api/assessments/start", json={
        "mode": "fixed",
        "target_career_id": doctor.id
    }, headers=headers)
    assert start_res.status_code == 200
    session_id = start_res.json()["session_id"]
    assert start_res.json()["mode"] == "fixed"

    # Fetch questions
    q_res = client.get(f"/api/assessments/{session_id}/questions", headers=headers)
    assert q_res.status_code == 200
    questions = q_res.json()["questions"]
    assert len(questions) >= 15

    # Check that questions include dedicated domain questions
    domain_qs = [q for q in questions if "doctor" in q["section_title"].lower() or "medical" in q["section_title"].lower() or q["category"] == "domain"]
    assert len(domain_qs) > 0

    # Answer all questions
    for q in questions:
        client.post(f"/api/assessments/{session_id}/answer", json={
            "question_id": q["id"],
            "selected_option_id": q["options"][0]["id"]
        }, headers=headers)

    # Complete assessment
    comp_res = client.post(f"/api/assessments/{session_id}/complete", headers=headers)
    assert comp_res.status_code == 200

    # Verify results
    res = client.get(f"/api/assessments/{session_id}/results", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["mode"] == "fixed"
    assert "dimensions_breakdown" in data
    assert len(data["selected_careers"]) == 1
    assert data["selected_careers"][0]["title"] == "Doctor (MBBS)"
    assert data["selected_careers"][0]["is_selected_choice"] == True
    assert data["selected_careers"][0]["evidence_status"] == "high_confidence"
    assert len(data["alternative_recommendations"]) >= 3


def test_not_fixed_universal_discovery_mode():
    email = "universal.tester@example.com"
    reg = client.post("/api/auth/register", json={
        "full_name": "Ananya Sen",
        "email": email,
        "password": "Password@123",
        "guardian_consent": True
    })
    token = reg.json()["access_token"] if reg.status_code == 200 else client.post("/api/auth/login", json={
        "email": email, "password": "Password@123"
    }).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Set 8th-10th education
    client.post("/api/students/education", json={
        "education_level": "school_8_10",
        "current_class_year": "Class 9th",
        "board_university": "ICSE"
    }, headers=headers)

    # Start NOT FIXED discovery mode
    start_res = client.post("/api/assessments/start", json={
        "mode": "not_fixed",
        "target_career_id": None
    }, headers=headers)
    assert start_res.status_code == 200
    session_id = start_res.json()["session_id"]
    assert start_res.json()["mode"] == "not_fixed"

    # Fetch questions
    q_res = client.get(f"/api/assessments/{session_id}/questions", headers=headers)
    assert q_res.status_code == 200
    questions = q_res.json()["questions"]
    # Check that questions span multiple modules
    module_numbers = {q["module_number"] for q in questions if "module_number" in q}
    assert len(module_numbers) >= 10, f"Expected questions across many modules, got {module_numbers}"

    # Answer questions
    for q in questions[:10]:
        client.post(f"/api/assessments/{session_id}/answer", json={
            "question_id": q["id"],
            "selected_option_id": q["options"][0]["id"]
        }, headers=headers)

    # Complete
    comp_res = client.post(f"/api/assessments/{session_id}/complete", headers=headers)
    assert comp_res.status_code == 200

    # Verify results
    res = client.get(f"/api/assessments/{session_id}/results", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["mode"] == "not_fixed"
    assert len(data["dimensions_breakdown"]) == 15
    assert len(data["recommendations"]) >= 10
    assert "evidence_status" in data


def test_career_clarity_mode_tri_comparison():
    email = "clarity.tester@example.com"
    reg = client.post("/api/auth/register", json={
        "full_name": "Arjun Varma",
        "email": email,
        "password": "Password@123",
        "guardian_consent": True
    })
    token = reg.json()["access_token"] if reg.status_code == 200 else client.post("/api/auth/login", json={
        "email": email, "password": "Password@123"
    }).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    client.post("/api/students/education", json={
        "education_level": "college_grad",
        "degree": "B.Tech Computer Science",
        "board_university": "VTU"
    }, headers=headers)

    db = SessionLocal()
    ds = db.query(Career).filter(Career.slug == "data-scientist").first()
    ai = db.query(Career).filter(Career.slug == "artificial-intelligence-engineer").first()
    fa = db.query(Career).filter(Career.slug == "financial-analyst").first()
    db.close()

    assert ds and ai and fa

    # Start CAREER CLARITY comparing 3 careers
    start_res = client.post("/api/assessments/start", json={
        "mode": "clarity",
        "target_career_id": ds.id,
        "clarity_career_ids": [ds.id, ai.id, fa.id]
    }, headers=headers)
    assert start_res.status_code == 200
    session_id = start_res.json()["session_id"]
    assert start_res.json()["mode"] == "clarity"

    # Fetch questions
    q_res = client.get(f"/api/assessments/{session_id}/questions", headers=headers)
    assert q_res.status_code == 200
    questions = q_res.json()["questions"]
    assert len(questions) >= 15

    # Answer all
    for q in questions:
        client.post(f"/api/assessments/{session_id}/answer", json={
            "question_id": q["id"],
            "selected_option_id": q["options"][0]["id"]
        }, headers=headers)

    # Trigger adaptive next stage test
    adapt_res = client.post(f"/api/assessments/{session_id}/adaptive-next", headers=headers)
    assert adapt_res.status_code == 200
    adapt_data = adapt_res.json()
    assert adapt_data["stage"] == "adaptive"
    assert len(adapt_data["top_candidate_careers"]) > 0

    # Complete
    comp_res = client.post(f"/api/assessments/{session_id}/complete", headers=headers)
    assert comp_res.status_code == 200

    # Verify results
    res = client.get(f"/api/assessments/{session_id}/results", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["mode"] == "clarity"
    assert len(data["selected_careers"]) == 3
    for sel in data["selected_careers"]:
        assert sel["is_selected_choice"] == True
        assert sel["compatibility_score"] > 0
    assert len(data["alternative_recommendations"]) >= 3
