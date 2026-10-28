from fastapi import FastAPI

from app.api import governance, health

app = FastAPI(
    title="GovernAI GDPR & AI Act Platform",
    version="0.1.0",
    description=(
        "Evidence-based GDPR and EU AI Act assessment engine with "
        "deterministic controls and human-review safeguards."
    ),
)

app.include_router(health.router)
app.include_router(governance.router)
