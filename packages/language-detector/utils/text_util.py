import regex, unicodedata

def strip_ascii(text: str) -> str:
    normalized = unicodedata.normalize("NFC", text)
    return regex.sub(r"[A-Za-z0-9]+", "", normalized)