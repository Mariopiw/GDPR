from typing import Literal

from pydantic import BaseModel, Field


class AISystemInput(BaseModel):
    name: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=10, max_length=4000)
    use_case: str = Field(min_length=2, max_length=120)
    organisation_role: Literal[
        "provider",
        "deployer",
        "importer",
        "distributor",
    ] = "deployer"
    processes_personal_data: bool = False
    automated_decision: bool = False
    affects_natural_persons: bool = False


class ControlAnswer(BaseModel):
    control_id: str
    answer: Literal[
        "yes",
        "partial",
        "no",
        "unknown",
        "not_applicable",
    ]
    evidence: str | None = Field(default=None, max_length=5000)
    notes: str | None = Field(default=None, max_length=5000)


class AssessmentRequest(AISystemInput):
    answers: list[ControlAnswer] = Field(default_factory=list)


class ClassificationResponse(BaseModel):
    category: str
    reasons: list[str]
    requires_human_review: bool = True


class FindingOut(BaseModel):
    control_id: str
    framework: str
    legal_reference: str
    title: str
    status: str
    severity: str
    score: float
    weight: float
    evidence: str | None = None
    remediation: str | None = None


class AssessmentResponse(BaseModel):
    catalogue_version: str
    classification: ClassificationResponse
    control_score: float
    risk_band: str
    findings: list[FindingOut]
    disclaimer: str
