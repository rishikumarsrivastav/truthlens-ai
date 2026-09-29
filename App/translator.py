from deep_translator import GoogleTranslator

CHUNK_SIZE = 4500


def split_text(text):
    parts = []
    while len(text) > CHUNK_SIZE:
        cut = text.rfind(" ", 0, CHUNK_SIZE)
        if cut <= 0:
            cut = CHUNK_SIZE
        parts.append(text[:cut])
        text = text[cut:].lstrip()
    if text:
        parts.append(text)
    return parts


def translate_to_english(text):
    try:
        translator = GoogleTranslator(source="auto", target="en")
        parts = [translator.translate(p) or "" for p in split_text(text)]
        result = " ".join(p for p in parts if p).strip()
        if not result:
            return text, False
        return result, True
    except Exception as e:
        print(f"Translation failed: {e}")
        return text, False