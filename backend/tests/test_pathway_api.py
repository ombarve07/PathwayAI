import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database import SessionLocal
from backend.app.models.entities import User, Career, AssessmentSession, Payment

client = TestClient(app)

def test_health_and_catalogue():
    response = client.get("/api/careers")
    assert response.status_code == 200
    careers = response.json()
    assert len(careers) == 30, f"Expected 30 careers, found {len(careers)}"

    # Verify both categories exist
    categories_res = client.get("/api/careers/categories")
    assert categories_res.status_code == 200
    cats = categories_res.json()
    slugs = [c["slug"] for c in cats]
    assert "science-technology" in slugs
    assert "commerce-business-arts-humanities" in slugs

def test_full_student_journey():
    # 1. Registration
    reg_payload = {
        "full_name": "Aarav Sharma",
        "email": "aarav.sharma@example.com",
        "password": "Password@123",
        "mobile": "+919876543210",
        "dob": "2009-08-15",
        "guardian_consent": True
    }
    reg_res = client.post("/api/auth/register", json=reg_payload)
    assert reg_res.status_code in [200, 400]
    
    # 2. Login
    login_res = client.post("/api/auth/login", json={
        "email": "aarav.sharma@example.com",
        "password": "Password@123"
    })
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Education Selection: School 8th-10th
    edu_payload = {
        "education_level": "school_8_10",
        "current_class_year": "Class 10th",
        "board_university": "CBSE",
        "subjects": "Mathematics, Science, English, Social Science",
        "academic_interests": "Computers, Algorithms, Physics"
    }
    edu_res = client.post("/api/students/education", json=edu_payload, headers=headers)
    assert edu_res.status_code == 200
    assert edu_res.json()["education_level"] == "school_8_10"

    # 4. Career Selection: Software Developer (Fixed Career Mode)
    careers_res = client.get("/api/careers?search=Software%20Developer")
    assert careers_res.status_code == 200
    sw_dev = careers_res.json()[0]
    assert sw_dev["title"] == "Software Developer"

    # 5. Start Assessment
    start_res = client.post("/api/assessments/start", json={
        "mode": "fixed",
        "target_career_id": sw_dev["id"]
    }, headers=headers)
    assert start_res.status_code == 200
    session_id = start_res.json()["session_id"]

    # 6. Fetch Questions
    q_res = client.get(f"/api/assessments/{session_id}/questions", headers=headers)
    assert q_res.status_code == 200
    q_data = q_res.json()
    assert len(q_data["questions"]) > 0

    # 7. Submit Answers to questions
    for q in q_data["questions"]:
        opt_id = q["options"][0]["id"]
        client.post(f"/api/assessments/{session_id}/answer", json={
            "question_id": q["id"],
            "selected_option_id": opt_id,
            "response_time_seconds": 12
        }, headers=headers)

    # 8. Complete Assessment & Calculate Results
    comp_res = client.post(f"/api/assessments/{session_id}/complete", headers=headers)
    assert comp_res.status_code == 200
    assert comp_res.json()["overall_score"] > 0

    # 9. Retrieve Results & Radar Breakdown
    results_res = client.get(f"/api/assessments/{session_id}/results", headers=headers)
    assert results_res.status_code == 200
    res_json = results_res.json()
    assert "skill_breakdown" in res_json
    assert "recommendations" in res_json
    assert len(res_json["recommendations"]) > 0
    assert res_json["is_unlocked"] == False  # locked before purchase

    # 10. Create ₹99 Order
    order_res = client.post("/api/payments/create-order", json={
        "session_id": session_id,
        "item_type": "analytics_report"
    }, headers=headers)
    assert order_res.status_code == 200
    order_data = order_res.json()
    assert order_data["amount"] == 99.0

    # 11. Verify Payment in test mode
    verify_res = client.post("/api/payments/verify", json={
        "order_id": order_data["order_id"],
        "payment_id": "pay_test_123456789",
        "signature": "sim_valid_test_signature"
    }, headers=headers)
    assert verify_res.status_code == 200
    assert verify_res.json()["status"] == "success"

    # 12. Confirm Report is now unlocked permanently
    unlocked_res = client.get(f"/api/assessments/{session_id}/results", headers=headers)
    assert unlocked_res.status_code == 200
    assert unlocked_res.json()["is_unlocked"] == True

    # 13. Update Skill Progress
    prog_res = client.post("/api/progress/skills", json={
        "skill_id": 1,
        "proficiency_level": 75,
        "evidence_note": "Completed 50 Leetcode problems"
    }, headers=headers)
    assert prog_res.status_code == 200
    assert prog_res.json()["new_level"] == 75

def test_admin_access_control():
    # Regular user cannot access admin routes
    reg_res = client.post("/api/auth/register", json={
        "full_name": "Student NonAdmin",
        "email": "student.regular@example.com",
        "password": "Password@123"
    })
    token = reg_res.json()["access_token"] if reg_res.status_code == 200 else client.post("/api/auth/login", json={
        "email": "student.regular@example.com",
        "password": "Password@123"
    }).json()["access_token"]

    forbidden_res = client.get("/api/admin/dashboard", headers={"Authorization": f"Bearer {token}"})
    assert forbidden_res.status_code == 403

    # Admin user can access admin routes
    admin_login = client.post("/api/auth/login", json={
        "email": "admin@pathway.ai",
        "password": "Admin@12345"
    })
    assert admin_login.status_code == 200
    admin_token = admin_login.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    admin_dash = client.get("/api/admin/dashboard", headers=admin_headers)
    assert admin_dash.status_code == 200
    assert "total_students" in admin_dash.json()
