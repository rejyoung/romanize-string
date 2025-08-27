import regex, unicodedata

def strip_ascii(text: str) -> str:
    """
    Strip ASCII characters from a given text.

    Args:
        text: The text to strip ASCII characters from

    Returns:
        The text with ASCII characters stripped
    """
    normalized = unicodedata.normalize("NFC", text)
    return regex.sub(r"[A-Za-z0-9]+", "", normalized)