from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_assessment_endpoint():
    response = client.post(
        "/governance/assess",
        json={
            "name": "RecruitAI",
            "description": "AI system used to rank job candidates.",
            "use_case": "employment",
            "organisation_role": "deployer",
            "processes_personal_data": True,
            "automated_decision": True,
            "affects_natural_persons": True,
            "answers": [
                {
                    "control_id": "AI-HO-001",
                    "answer": "no",
                    "evidence": None
                }
            ]
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["classification"]["category"] == "potential_high_risk"
    assert body["risk_band"] in {"low", "moderate", "high", "critical"}
