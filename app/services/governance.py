import json
from pathlib import Path
from typing import Any

CONTROL_FILE = Path(__file__).resolve().parent.parent / "data" / "controls.json"

HIGH_RISK_USE_CASES = {
    "employment",
    "recruitment",
    "education",
    "credit_scoring",
    "law_enforcement",
    "migration",
    "biometrics",
    "essential_services",
}

ANSWER_SCORE = {
    "yes": 1.0,
    "partial": 0.5,
    "no": 0.0,
    "unknown": 0.0,
}


def load_catalogue() -> dict[str, Any]:
    with CONTROL_FILE.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def classify_system(
    *,
    use_case: str,
    processes_personal_data: bool,
    automated_decision: bool,
    affects_natural_persons: bool,
) -> tuple[str, list[str]]:
    normalized = use_case.strip().lower().replace(" ", "_")
    category = "general"
    reasons: list[str] = []

    if normalized in HIGH_RISK_USE_CASES:
        category = "potential_high_risk"
        reasons.append(
            f"Use case '{use_case}' may fall within a high-risk AI Act category."
        )

    if affects_natural_persons:
        reasons.append("The system affects natural persons.")

    if automated_decision:
        reasons.append("The system participates in automated decision-making.")

    if processes_personal_data:
        reasons.append("The system processes personal data, so GDPR controls may apply.")

    if not reasons:
        reasons.append("No elevated trigger was identified by the automated rules.")

    return category, reasons


def applicable_controls(
    *,
    category: str,
    processes_personal_data: bool,
) -> tuple[str, list[dict[str, Any]]]:
    catalogue = load_catalogue()
    tags = {category}

    if processes_personal_data:
        tags.add("personal_data")

    controls = [
        control
        for control in catalogue["controls"]
        if set(control.get("applies_to", [])).intersection(tags)
    ]

    return catalogue["catalogue_version"], controls


def evaluate_control(
    *,
    control: dict[str, Any],
    answer: str,
    evidence: str | None,
) -> dict[str, Any]:
    if answer == "not_applicable":
        return {
            "status": "not_applicable",
            "score": 0.0,
            "severity": control["severity"],
            "remediation": None,
        }

    score = ANSWER_SCORE.get(answer, 0.0)

    if answer == "yes" and evidence:
        status = "pass"
    elif answer == "yes":
        status = "evidence_missing"
        score = 0.5
    elif answer == "partial":
        status = "partial"
    elif answer == "no":
        status = "fail"
    else:
        status = "unknown"

    return {
        "status": status,
        "score": score,
        "severity": control["severity"],
        "remediation": None if status == "pass" else control.get("remediation"),
    }


def calculate_control_score(findings: list[dict[str, Any]]) -> float:
    included = [
        finding
        for finding in findings
        if finding["status"] != "not_applicable"
    ]

    total_weight = sum(float(finding["weight"]) for finding in included)
    if total_weight == 0:
        return 0.0

    achieved = sum(
        float(finding["weight"]) * float(finding["score"])
        for finding in included
    )

    return round((achieved / total_weight) * 100, 2)


def risk_band(score: float) -> str:
    if score >= 90:
        return "low"
    if score >= 75:
        return "moderate"
    if score >= 50:
        return "high"
    return "critical"
