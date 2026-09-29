import re

from langdetect import DetectorFactory, LangDetectException, detect

DetectorFactory.seed = 0

emoji_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\U00002700-\U000027BF"
    "\U0001F900-\U0001F9FF"
    "\U00002600-\U000026FF"
    "]+",
    flags=re.UNICODE,
)


def decap(match):
    return match.group(0).capitalize()


def clean_whatsapp(text):
    if not text:
        return text

    text = re.sub(r"\s+", " ", text).strip()
    text = emoji_pattern.sub("", text)
    text = re.sub(r"!{2,}", "!", text)
    text = re.sub(r"\?{2,}", "?", text)
    text = re.sub(r"\b[A-Z]{3,}\b", decap, text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def detect_language(text):
    if not text or not text.strip():
        return "en"
    try:
        return detect(text)
    except LangDetectException:
        return "en"
