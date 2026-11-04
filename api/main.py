from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from src.ats.matcher import analyze_resume_jd

app = FastAPI(
    title="CampusMind AI API",
    description="Placement & Career Intelligence Platform Backend",
    version="1.0.0"
)

class ATSRequest(BaseModel):
    resume_text: str = Field(..., description="Full text content of the applicant's resume")
    job_description: str = Field(..., description="Full text content of the target job description")

class ATSResponse(BaseModel):
    match_score: float
    matched_keywords: list[str]
    missing_keywords: list[str]
    recommendation: str

@app.get("/health", tags=["System"])
def health_check():
    """Service readiness and health check endpoint."""
    return {"status": "healthy", "service": "CampusMind API", "status_code": 200}

@app.post("/analyze-ats", response_model=ATSResponse, tags=["ATS Matcher"])
def analyze_ats(payload: ATSRequest):
    """
    Analyzes resume text against a target job description,
    returning an ATS match percentage, keyword gaps, and hiring recommendations.
    """
    try:
        result = analyze_resume_jd(payload.resume_text, payload.job_description)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))