# romanize.py
import re, sys
from pythainlp.transliterate import romanize


text = sys.argv[1]

THAI_ONLY = re.compile(r"^[\u0E00-\u0E7F]+$")


def romanize_thai_tokens(s: str) -> str:
    separator = "\U000f0000\U000f0001"
    parts = s.split(separator)
    out = []

    for part in parts:
        if THAI_ONLY.match(part):
            out.append(romanize(part, engine="thai2rom_onnx"))
        else:
            out.append(part)

    translit = " ".join(out)

    translit = re.sub(r"\s*/\s*", "/", translit)
    translit = re.sub(
        r'\s+([/.,!?;:()\[\]{}"\'“”‘’‹›«»…—–，。、：；！？฿ฯๆ])', r"\1", translit
    )
    translit = re.sub(r"\s{2,}", " ", translit).strip()
    # Rare ONNX artifact: drop a trailing standalone 'a' before end or punctuation
    translit = re.sub(r"\s+a(?=$|[.!?])", "", translit)

    return translit


print(romanize_thai_tokens(text))
