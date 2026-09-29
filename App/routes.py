import os
import pickle

from flask import Blueprint, jsonify, request

from .credibility import score_domain
from .explainer import get_lime_highlights
from .preprocessor import clean_whatsapp, detect_language
from .text_utils import normalize_text
from .translator import translate_to_english

api = Blueprint("api", __name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "Model", "lr_model.pkl")
VEC_PATH = os.path.join(BASE_DIR, "Model", "tfidf_vectorizer.pkl")

MIN_KNOWN_TERMS = 5
TRUE_ABOVE = 0.60
FALSE_BELOW = 0.40

tfidf = None
clf = None


def load_model():
    global tfidf, clf

    if os.path.exists(MODEL_PATH) and os.path.exists(VEC_PATH):
        with open(MODEL_PATH, "rb") as f:
            clf = pickle.load(f)

        with open(VEC_PATH, "rb") as f:
            tfidf = pickle.load(f)

        print("Model loaded")
    else:
        print("Model files not found, run train_model.py first")


load_model()


def get_verdict(trust_score):
    if trust_score >= TRUE_ABOVE:
        return "true"
    if trust_score <= FALSE_BELOW:
        return "false"
    return "unverified"


def get_confidence_level(confidence):
    if confidence >= 0.85:
        return "High"
    if confidence >= 0.65:
        return "Medium"
    return "Low"


@api.route("/status")
def status():
    return jsonify({
        "status": "TruthLens API Running",
        "model_loaded": clf is not None
    })


@api.route("/predict", methods=["POST"])
def predict():

    if clf is None or tfidf is None:
        return jsonify({
            "error": "Model not loaded. Run data_cleaning.py and train_model.py first."
        }), 500

    data = request.get_json(silent=True) or {}

    raw_text = (data.get("text") or "").strip()
    source_url = (data.get("source_url") or "").strip()

    if not raw_text:
        return jsonify({
            "error": "No text provided."
        }), 400

    text = clean_whatsapp(raw_text)
    detected_language = detect_language(text)

    translation_ok = True
    if detected_language != "en":
        translated_text, translation_ok = translate_to_english(text)
    else:
        translated_text = text

    model_text = normalize_text(translated_text)
    vec = tfidf.transform([model_text])
    known_terms = int(vec.nnz)

    fake_index = list(clf.classes_).index(1)
    p_fake = float(clf.predict_proba(vec)[0][fake_index])

    note = None
    if known_terms < MIN_KNOWN_TERMS:
        p_fake = 0.5
        note = "This message is too short or has too few familiar words to judge. Try pasting more of the text."
        if not translation_ok:
            note = "Translation failed, so the message could not be judged. Check your internet connection."

    text_trust = 1 - p_fake
    confidence = max(p_fake, 1 - p_fake)

    if source_url:
        source_score = score_domain(source_url)
        trust_score = (0.7 * text_trust) + (0.3 * (source_score / 100))
    else:
        source_score = None
        trust_score = text_trust

    trust_score = round(trust_score, 2)
    verdict = get_verdict(trust_score)

    if verdict == "true" and source_score is not None and source_score <= 30:
        verdict = "unverified"
        note = "The text reads like real reporting, but the link is from a site known for false content."

    if known_terms >= MIN_KNOWN_TERMS:
        highlights = get_lime_highlights(model_text, clf, tfidf)
    else:
        highlights = {"fake_words": [], "real_words": []}

    response = {
        "label": 1 if p_fake >= 0.5 else 0,
        "label_text": "Fake" if p_fake >= 0.5 else "Real",
        "verdict": verdict,
        "p_fake": round(p_fake, 3),
        "confidence": round(confidence, 2),
        "confidence_level": get_confidence_level(confidence),
        "trust_score": trust_score,
        "source_score": source_score,
        "known_terms": known_terms,
        "note": note,
        "highlights": highlights,
        "original_text": text,
        "translated_text": translated_text,
        "detected_language": detected_language,
    }

    return jsonify(response)