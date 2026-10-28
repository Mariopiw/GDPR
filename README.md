# GovernAI — GDPR & EU AI Act Assessment Platform

GovernAI is a portfolio-grade **RegTech / AI Governance** backend that turns GDPR and EU AI Act requirements into explicit, testable controls.

It follows one core rule:

> **AI may assist with evidence discovery, but compliance findings should come from explicit controls, evidence, deterministic rules, and human review.**

## What this project demonstrates

- Python and FastAPI
- Pydantic validation
- GDPR control mapping
- EU AI Act control mapping
- deterministic compliance logic
- evidence-aware findings
- weighted control scoring
- remediation guidance
- human-review safeguards
- pytest
- Ruff
- Docker
- GitHub Actions CI

## Architecture

```text
AI System
   |
   v
Classification
   |
   v
Applicable Controls
   |
   v
Answers + Evidence
   |
   v
Deterministic Assessment
   |
   v
PASS / PARTIAL / FAIL / UNKNOWN
   |
   v
Control Score + Risk Band
   |
   v
Remediation
   |
   v
Human Review
```

## Why not ask an LLM "Are we compliant?"

Because a language model is probabilistic. GovernAI separates:

```text
LAW
  -> CONTROL
  -> QUESTION
  -> EVIDENCE
  -> FINDING
  -> REMEDIATION
```

If an assessor answers `yes` but provides no evidence, GovernAI does not award a full pass. It returns `evidence_missing`.

## Run locally

```bash
git clone https://github.com/Mariopiw/GDPR-.git
cd GDPR-
git checkout feature/governai-mvp

python3 -m venv .venv
source .venv/bin/activate

pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Example classification

```bash
curl -X POST http://127.0.0.1:8000/governance/classify \
  -H "Content-Type: application/json" \
  -d '{
    "name": "RecruitAI",
    "description": "AI system ranking job applicants.",
    "use_case": "employment",
    "organisation_role": "deployer",
    "processes_personal_data": true,
    "automated_decision": true,
    "affects_natural_persons": true
  }'
```

## Example assessment

```bash
curl -X POST http://127.0.0.1:8000/governance/assess \
  -H "Content-Type: application/json" \
  -d '{
    "name": "RecruitAI",
    "description": "AI system ranking job applicants.",
    "use_case": "employment",
    "organisation_role": "deployer",
    "processes_personal_data": true,
    "automated_decision": true,
    "affects_natural_persons": true,
    "answers": [
      {
        "control_id": "AI-HO-001",
        "answer": "no",
        "evidence": null
      },
      {
        "control_id": "GDPR-LAW-001",
        "answer": "yes",
        "evidence": "ROPA entry HR-17 and lawful-basis assessment."
      }
    ]
  }'
```

## Test

```bash
pytest -q
ruff check .
```

## Docker

```bash
docker compose up --build
```

Then open:

```text
http://localhost:8000/docs
```

## Current MVP

The first milestone deliberately focuses on the highest-value core:

- AI-system classification support
- versioned GDPR controls
- versioned AI Act controls
- deterministic assessment
- evidence-aware scoring
- remediation guidance
- mandatory human-review flag

## Roadmap

1. PostgreSQL persistence
2. authentication and RBAC
3. immutable audit log
4. PDF/DOCX policy ingestion
5. hybrid dense + lexical RAG
6. verifiable page-level citations
7. automatic control-to-evidence matching
8. remediation owners and due dates
9. retrieval/citation evaluation harness
10. governance dashboard

## Feynman explanation

If you can explain the project in one sentence, you understand it:

> GovernAI takes an AI use case, determines which control checks may apply, asks for evidence, evaluates the answers with explicit rules, highlights gaps, and leaves consequential legal judgment to a human.

## Disclaimer

This is an engineering and decision-support project. It does not provide legal advice and does not replace qualified legal review.
