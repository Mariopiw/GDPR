from fastapi import APIRouter

from app.schemas import (
    AISystemInput,
    AssessmentRequest,
    AssessmentResponse,
    ClassificationResponse,
    FindingOut,
)
from app.services.governance import (
    applicable_controls,
    calculate_control_score,
    classify_system,
    evaluate_control,
    risk_band,
)

router = APIRouter(prefix="/governance", tags=["governance"])


@router.post("/classify", response_model=ClassificationResponse)
def classify(payload: AISystemInput) -> ClassificationResponse:
    category, reasons = classify_system(
        use_case=payload.use_case,
        processes_personal_data=payload.processes_personal_data,
        automated_decision=payload.automated_decision,
        affects_natural_persons=payload.affects_natural_persons,
    )

    return ClassificationResponse(
        category=category,
        reasons=reasons,
        requires_human_review=True,
    )


@router.post("/assess", response_model=AssessmentResponse)
def assess(payload: AssessmentRequest) -> AssessmentResponse:
    category, reasons = classify_system(
        use_case=payload.use_case,
        processes_personal_data=payload.processes_personal_data,
        automated_decision=payload.automated_decision,
        affects_natural_persons=payload.affects_natural_persons,
    )

    version, controls = applicable_controls(
        category=category,
        processes_personal_data=payload.processes_personal_data,
    )

    answer_map = {
        answer.control_id: answer
        for answer in payload.answers
    }

    findings: list[FindingOut] = []
    score_items: list[dict] = []

    for control in controls:
        submitted = answer_map.get(control["id"])
        answer_value = submitted.answer if submitted else "unknown"
        evidence = submitted.evidence if submitted else None

        evaluation = evaluate_control(
            control=control,
            answer=answer_value,
            evidence=evidence,
        )

        item = {
            "control_id": control["id"],
            "framework": control["framework"],
            "legal_reference": control["legal_reference"],
            "title": control["title"],
            "status": evaluation["status"],
            "severity": evaluation["severity"],
            "score": evaluation["score"],
            "weight": float(control["weight"]),
            "evidence": evidence,
            "remediation": evaluation["remediation"],
        }

        findings.append(FindingOut(**item))
        score_items.append(item)

    score = calculate_control_score(score_items)

    return AssessmentResponse(
        catalogue_version=version,
        classification=ClassificationResponse(
            category=category,
            reasons=reasons,
            requires_human_review=True,
        ),
        control_score=score,
        risk_band=risk_band(score),
        findings=findings,
        disclaimer=(
            "This is a decision-support assessment, not a final legal determination. "
            "Human review is required for consequential conclusions."
        ),
    )
