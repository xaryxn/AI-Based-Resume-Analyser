import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ----------- CLEAN TEXT -----------

def clean_text(text):
    return text.lower()

# ----------- KEYWORD EXTRACTION -----------

def extract_keywords(text):
    words = text.split()
    return set(words)

# ----------- SCORING -----------

def calculate_scores(jd_text, resumes):
    documents = [jd_text] + resumes

    tfidf = TfidfVectorizer(stop_words="english")
    vectors = tfidf.fit_transform(documents)

    similarity = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

    # Normalize scores
    scores = (similarity * 100).round(2)

    return scores

# ----------- ANALYSIS -----------

def analyze_resume(jd_text, resume_text):
    jd_words = extract_keywords(clean_text(jd_text))
    resume_words = extract_keywords(clean_text(resume_text))

    matched = jd_words.intersection(resume_words)
    missing = jd_words.difference(resume_words)

    # Filter small/noisy words
    strengths = [w for w in matched if len(w) > 4][:3]
    gaps = [w for w in missing if len(w) > 4][:3]

    if not strengths:
        strengths_text = "Shows some alignment with the role requirements"
    else:
        strengths_text = ", ".join(strengths)

    if not gaps:
        gaps_text = "No major gaps identified"
    else:
        gaps_text = ", ".join(gaps)

    return strengths_text, gaps_text

# ----------- CLASSIFICATION -----------

def classify(score):
    if score >= 75:
        return "Strong alignment with role"
    elif score >= 50:
        return "Moderate alignment, further evaluation recommended"
    else:
        return "Limited alignment with requirements"

# ----------- CONFIDENCE -----------

def confidence_level(score):
    if score >= 75:
        return "High"
    elif score >= 50:
        return "Medium"
    else:
        return "Low"

# ----------- MAIN PROCESS -----------

def process(jd_text, resumes, names):
    scores = calculate_scores(jd_text, resumes)

    results = []

    for i, resume in enumerate(resumes):
        strengths, gaps = analyze_resume(jd_text, resume)
        recommendation = classify(scores[i])
        confidence = confidence_level(scores[i])

        results.append({
            "Candidate": names[i],
            "Score": scores[i],
            "Confidence": confidence,
            "Strengths": strengths,
            "Gaps": gaps,
            "Recommendation": recommendation
        })

    df = pd.DataFrame(results).sort_values(by="Score", ascending=False)

    return df