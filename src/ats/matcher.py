import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_text(text: str) -> str:
    """Clean and normalize text for ATS comparison."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def analyze_resume_jd(resume_text: str, jd_text: str) -> dict:
    """
    Computes ATS match score using TF-IDF cosine similarity,
    extracts missing keywords, and provides professional recommendations.
    """
    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(jd_text)

    if not cleaned_resume or not cleaned_jd:
        return {
            "match_score": 0.0,
            "matched_keywords": [],
            "missing_keywords": [],
            "recommendation": "Please provide both valid resume and job description text."
        }

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform([cleaned_resume, cleaned_jd])
    
    # Cosine Similarity Score
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    match_score = round(float(similarity) * 100, 2)

    # Keyword Extraction & Gap Analysis
    feature_names = vectorizer.get_feature_names_out()
    resume_vector = tfidf_matrix[0].toarray()[0]
    jd_vector = tfidf_matrix[1].toarray()[0]  # <--- Yahan [1 ki jagah [0]] karna hai

    matched = []
    missing = []

    for idx, word in enumerate(feature_names):
        if jd_vector[idx] > 0:
            if resume_vector[idx] > 0:
                matched.append(word)
            else:
                missing.append(word)

    # Sort missing keywords by relevance/importance weight in JD
    missing_sorted = [w for _, w in sorted(zip([jd_vector[vectorizer.vocabulary_[w]] for w in missing], missing), reverse=True)]

    # Recommendation generator based on score
    if match_score >= 80:
        recommendation = "🌟 Excellent ATS Match! Your resume strongly aligns with the Job Description."
    elif match_score >= 50:
        recommendation = "⚠️ Moderate Match. Incorporate the missing technical keywords to bypass automated ATS filters."
    else:
        recommendation = "❌ Low Match. Significant alignment gap detected. Tailor your resume sections closer to the JD."

    return {
        "match_score": match_score,
        "matched_keywords": matched[:15],
        "missing_keywords": missing_sorted[:12],
        "recommendation": recommendation
    }