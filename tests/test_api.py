from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_analyze_ats_endpoint():
    payload = {
        "resume_text": "Experienced Python Developer with expertise in FastAPI, Docker, and PostgreSQL.",
        "job_description": "We need a backend developer skilled in Python, FastAPI, Docker, and Kubernetes."
    }
    response = client.post("/analyze-ats", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "match_score" in data
    assert "matched_keywords" in data
    assert data["match_score"] > 0