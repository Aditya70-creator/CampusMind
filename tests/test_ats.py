from src.ats.matcher import analyze_resume_jd

def test_analyze_resume_jd():
    sample_resume = "Proficient in Python, FastAPI, Docker, SQL, and Machine Learning workflows."
    sample_jd = "Looking for a software engineer with Python, FastAPI, Docker, Kubernetes, and AWS skills."

    result = analyze_resume_jd(sample_resume, sample_jd)

    assert "match_score" in result
    assert "matched_keywords" in result
    assert "missing_keywords" in result
    assert result["match_score"] > 0.0
    assert "python" in result["matched_keywords"] or "fastapi" in result["matched_keywords"]
    assert "kubernetes" in result["missing_keywords"] or "aws" in result["missing_keywords"]