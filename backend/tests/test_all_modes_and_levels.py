import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_not_fixed_discovery_mode_college():
    # 1. Register College Student
    reg_res = client.post("/api/auth/register", json={
        "full_name": "Kavita Rao",
        "email": "kavita.rao@example.com",
        "password": "Password@123",
        "guardian_consent": True
    })
    token = reg_res.json()["access_token"] if reg_res.status_code == 200 else client.post("/api/auth/login", json={
        "email": "kavita.rao@example.com",
        "password": "Password@123"
    }).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Set College Education
    edu_res = client.post("/api/students/education", json={
        "education_level": "college_grad",
        "degree": "B.Sc. Mathematics",
        "semester": "Year 3 (Sem 5-6)",
        "board_university": "Delhi University",
        "academic_interests": "Statistics, Economics, Predictive Analysis"
    }, headers=headers)
    assert edu_res.status_code == 200

    # 3. Start NOT FIXED Discovery Mode
    start_res = client.post("/api/assessments/start", json={
        "mode": "not_fixed",
        "target_career_id": None
    }, headers=headers)
    assert start_res.status_code == 200
    session_id = start_res.json()["session_id"]

    # 4. Fetch questions and answer
    q_res = client.get(f"/api/assessments/{session_id}/questions", headers=headers)
    for q in q_res.json()["questions"][:5]:
        client.post(f"/api/assessments/{session_id}/answer", json={
            "question_id": q["id"],
            "selected_option_id": q["options"][0]["id"]
        }, headers=headers)

    # 5. Complete
    comp_res = client.post(f"/api/assessments/{session_id}/complete", headers=headers)
    assert comp_res.status_code == 200

    # 6. Check results: Multiple ranked recommendations produced
    res = client.get(f"/api/assessments/{session_id}/results", headers=headers)
    assert res.status_code == 200
    recs = res.json()["recommendations"]
    assert len(recs) >= 3

def test_career_clarity_mode_diploma():
    # 1. Register Diploma Student
    reg_res = client.post("/api/auth/register", json={
        "full_name": "Siddharth Patil",
        "email": "siddharth.patil@example.com",
        "password": "Password@123"
    })
    token = reg_res.json()["access_token"] if reg_res.status_code == 200 else client.post("/api/auth/login", json={
        "email": "siddharth.patil@example.com",
        "password": "Password@123"
    }).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Set Diploma Education
    edu_res = client.post("/api/students/education", json={
        "education_level": "diploma",
        "diploma_branch": "Mechanical Engineering",
        "current_class_year": "3rd Year (Final Year)",
        "board_university": "MSBTE",
        "academic_interests": "CAD, Robotics, Thermodynamics"
    }, headers=headers)
    assert edu_res.status_code == 200

    # 3. Start CAREER CLARITY Mode (Comparing Mechanical Engineer vs Software Developer)
    start_res = client.post("/api/assessments/start", json={
        "mode": "clarity",
        "target_career_id": 14, # Mechanical Engineer
        "clarity_career_ids": [14, 4] # Mechanical Engineer vs Software Developer
    }, headers=headers)
    assert start_res.status_code == 200
    session_id = start_res.json()["session_id"]

    # 4. Complete session
    comp_res = client.post(f"/api/assessments/{session_id}/complete", headers=headers)
    assert comp_res.status_code == 200

    # 5. Verify Eligibility: Shows Diploma lateral entry
    res = client.get(f"/api/assessments/{session_id}/results", headers=headers)
    assert res.status_code == 200
    elig = res.json()["eligibility_analysis"]
    assert "eligible_now" in elig
    # Checks lateral entry eligibility recognized
    assert any("lateral entry" in str(e).lower() or "diploma" in str(e).lower() for e in elig["eligible_now"])
