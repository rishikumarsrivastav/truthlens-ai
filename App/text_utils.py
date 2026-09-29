import re
import unicodedata

html_tag = re.compile(r"<[^>]+>")
link = re.compile(r"https?://\S+|www\.\S+|pic\.twitter\.com/\S+", re.IGNORECASE)
handle = re.compile(r"@\w+")
dateline = re.compile(r"^\s*.{0,80}?\(reuters\)\s*[-\u2013\u2014:]*\s*", re.IGNORECASE)
reuters_word = re.compile(r"\breuters\b", re.IGNORECASE)
apostrophes = re.compile(r"['\u2018\u2019\u201b`\u00b4]")
not_alnum = re.compile(r"[^a-z0-9]+")


def normalize_text(text):
    """Turn any text into the plain lowercase form the model is trained on.

    The same function is used in train_model.py and in routes.py, so a message
    typed into the app looks exactly like the training data:
    no links, @handles, datelines, quotes, punctuation or apostrophes
    ("don't", "don’t" and "dont" all become "dont").
    """
    if not isinstance(text, str):
        return ""

    text = unicodedata.normalize("NFKC", text)
    text = html_tag.sub(" ", text)
    text = link.sub(" ", text)
    text = handle.sub(" ", text)
    text = dateline.sub("", text)
    text = reuters_word.sub(" ", text)
    text = apostrophes.sub("", text.lower())
    text = not_alnum.sub(" ", text)

    return text.strip()