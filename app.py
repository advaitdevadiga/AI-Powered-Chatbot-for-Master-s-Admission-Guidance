"""
Study Abroad Guide - one server for the whole project.

Run it with start.bat (Windows). It serves:
  http://localhost:5000/        -> the website (index.html, map, country pages, photos)
  http://localhost:5000/chat    -> the chatbot API

The chatbot uses a small local AI model through Ollama (free, runs on your PC).
If Ollama is not installed / not running, the chatbot still answers basic questions
using the built-in fallback answers below, so the website never looks broken.
"""
import os
import requests
from flask import Flask, request, jsonify, send_from_directory, abort
from flask_cors import CORS

ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
CORS(app)

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "tinyllama"

SYSTEM_PROMPT = (
    "You are a helpful, friendly AI chatbot who assists Indian students planning to pursue "
    "MS, MBA, or MTech. Provide clear answers (with a 200-word limit)."
)

# Very small fallback so the chatbot always says something useful
FALLBACK = [
    (("gre",), "Most top MS programmes in the USA ask for a GRE score (many now make it optional). Check each university's admissions page."),
    (("gmat",), "Top MBA programmes (ISB, INSEAD, LBS, Wharton...) usually accept GMAT or GRE. A strong score plus 2-5 years of work experience helps a lot."),
    (("cat",), "In India, IIMs and many other B-schools select MBA students using the CAT exam, followed by group discussion and interview rounds."),
    (("gate",), "GATE is the main entrance exam for MTech admissions at IITs, IISc and NITs, and it can also bring a scholarship/stipend."),
    (("ielts", "toefl"), "Universities abroad usually need IELTS or TOEFL to prove English skills. Typical targets: IELTS 6.5-7.5 / TOEFL 90-105, depending on the university."),
    (("scholarship", "fund"), "Look at university scholarships, assistantships (TA/RA) for MS/MTech, and country schemes such as Chevening (UK) or Fulbright (USA)."),
    (("mba",), "An MBA builds management and leadership skills. Compare India (IIMs, ISB), USA, Europe (INSEAD, LBS) and Australia on cost, duration and job outcomes."),
    (("mtech", "ms ", "masters", "master"), "MTech/MS is a research- and skills-focused technical degree. Compare universities by course content, faculty, funding and placements."),
    (("visa",), "Each country has a student visa route (F-1 USA, Student visa Australia, UK Student route, etc.). Always confirm requirements on the official government site."),
]


def fallback_reply(message):
    m = message.lower() + " "
    for keys, answer in FALLBACK:
        if any(k in m for k in keys):
            return answer + "\n\n(Offline mode: install Ollama + tinyllama for full AI answers.)"
    return ("I can help with MBA / MTech / MS questions - exams (GRE, GMAT, CAT, GATE), "
            "scholarships, visas and choosing a country.\n\n"
            "(Offline mode: install Ollama + tinyllama for full AI answers.)")


def generate_reply(user_message):
    try:
        r = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": f"{SYSTEM_PROMPT}\nUser: {user_message}\nAI:",
                "stream": False,
            },
            timeout=180,  # small models on a normal laptop can be slow
        )
        r.raise_for_status()
        text = r.json().get("response", "").strip()
        return text or fallback_reply(user_message)
    except requests.RequestException as e:
        print(f"[Info] Ollama not available, using fallback answers: {e}")
        return fallback_reply(user_message)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = str(data.get("message", "")).strip()
    if not user_message:
        return jsonify({"error": "Message not provided"}), 400
    return jsonify({"reply": generate_reply(user_message)})


# ---- website files -------------------------------------------------------
ALLOWED = {".html", ".css", ".js", ".jpg", ".jpeg", ".png", ".webp", ".avif", ".gif", ".svg", ".ico"}


@app.route("/")
def home():
    return send_from_directory(ROOT, "index.html")


@app.route("/<path:filename>")
def site_files(filename):
    if os.path.splitext(filename)[1].lower() not in ALLOWED:
        abort(404)
    return send_from_directory(ROOT, filename)


if __name__ == "__main__":
    print("\n  Website running at  http://localhost:5000\n  (close this window to stop it)\n")
    app.run(host="127.0.0.1", port=5000, debug=False)
