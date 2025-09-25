# backend/app.py
import os
import tempfile
from flask import Flask, request, jsonify, render_template, redirect, url_for
from backend.matcher import get_similarity_score
from backend.utils import extract_text, clean_text, compare_skills
from sentence_transformers import SentenceTransformer



app = Flask(__name__, template_folder="templates", static_folder="../static")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # file upload + JD text
        file = request.files.get("resume")
        jd_text = request.form.get("jd", "")
        if not file or file.filename == "":
            return render_template("index.html", error="Please upload a resume (PDF/DOCX).")
        if not jd_text.strip():
            return render_template("index.html", error="Please paste the job description (JD).")

        try:
            resume_text = extract_text(file)
            resume_text = clean_text(resume_text)
            jd_text_clean = clean_text(jd_text)
            score = get_similarity_score(resume_text, jd_text_clean)
            skills_comparison = compare_skills(resume_text, jd_text_clean)
            return render_template("index.html", score=score, skills=skills_comparison, jd=jd_text)
        except Exception as e:
            return render_template("index.html", error=f"Error processing file: {e}")

    return render_template("index.html")

@app.route("/api/match", methods=["POST"])
def api_match():
    """
    API endpoint - Accepts multipart/form-data:
      - resume: file
      - jd: text
    Returns JSON with score and skill analysis.
    """
    file = request.files.get("resume")
    jd_text = request.form.get("jd", "")
    if not file or file.filename == "" or not jd_text.strip():
        return jsonify({"error": "Please provide resume (file) and jd (text)"}), 400
    try:
        resume_text = extract_text(file)
        resume_text = clean_text(resume_text)
        jd_text_clean = clean_text(jd_text)
        score = get_similarity_score(resume_text, jd_text_clean)
        skills_comparison = compare_skills(resume_text, jd_text_clean)
        return jsonify({
            "score": score,
            "skills": skills_comparison
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # For local dev
    app.run(host="0.0.0.0", port=5000, debug=True)

