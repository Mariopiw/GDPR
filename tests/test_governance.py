from app.services.governance import (
    applicable_controls,
    calculate_control_score,
    classify_system,
    evaluate_control,
)


def test_employment_ai_is_flagged():
    category, reasons = classify_system(
        use_case="employment",
        processes_personal_data=True,
        automated_decision=True,
        affects_natural_persons=True,
    )

    assert category == "potential_high_risk"
    assert any("personal data" in reason for reason in reasons)


def test_personal_data_adds_gdpr_controls():
    _, controls = applicable_controls(
        category="general",
        processes_personal_data=True,
    )

    control_ids = {control["id"] for control in controls}

    assert "GDPR-LAW-001" in control_ids
    assert "GDPR-DPIA-001" in control_ids


def test_yes_without_evidence_is_not_full_pass():
    control = {
        "severity": "critical",
        "remediation": "Add evidence.",
    }

    result = evaluate_control(
        control=control,
        answer="yes",
        evidence=None,
    )

    assert result["status"] == "evidence_missing"
    assert result["score"] == 0.5


def test_weighted_score():
    findings = [
        {"status": "pass", "score": 1.0, "weight": 10},
        {"status": "fail", "score": 0.0, "weight": 10},
    ]

    assert calculate_control_score(findings) == 50.0
