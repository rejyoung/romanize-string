import joblib, sys, regex
from pathlib import Path
from scipy.sparse import hstack
from definitions.language_codes import Code_Language
from utils.build_extended_features_block import build_extended_features_block

HERE = Path(__file__).resolve().parent
MODEL_ASSETS = HERE / "model_assets"


def detect_language(string: str) -> Code_Language:

    kana_or_japanese_marks = regex.compile(
        r"[\p{Script=Hiragana}\p{Script=Katakana}\u30FC\uFF70\u30FB\u3005]"
    )

    if kana_or_japanese_marks.search(string):
        return "ja"

    family = evaluate_input(string, "family")

    if family in ["el", "ko"]:
        return family
    elif family == "indic":
        return evaluate_input(string, "indic")
    elif family == "ja_zh":
        return evaluate_input(string, "ja_zh")
    elif family == "perso_arabic":
        return evaluate_input(string, "perso_arabic")
    elif family == "cyrillic":
        cyrillic_family = evaluate_input(string, "cyrillic")

        if cyrillic_family == "southern_cyrillic":
            return evaluate_input(string, "southern_cyrillic")
        elif cyrillic_family == "eastern_cyrillic":
            return evaluate_input(string, "eastern_cyrillic")
        else:
            return evaluate_input(string, "turkic")


def load_tools(model_type: str):
    vectorizer = joblib.load(
        MODEL_ASSETS / "vectorizer" / f"ld_{model_type}_vectorizer.joblib"
    )
    model = joblib.load(MODEL_ASSETS / "models" / f"ld_{model_type}_model.joblib")

    return vectorizer, model


def evaluate_input(string: str, model_type: str) -> str:
    vectorizer, model = load_tools(model_type)

    X_base = vectorizer.transform([string])
    X_ext = build_extended_features_block([string], model_type)

    if X_ext.dtype != X_base.dtype:
        X_ext = X_ext.astype(X_base.dtype, copy=False)

    X_aug = hstack([X_base, X_ext], format="csr")

    result = model.predict(X_aug)[0]

    return result


if __name__ == "__main__":
    # Expect exactly 2 user‐supplied arguments
    if len(sys.argv) != 2:
        print("Usage: python language_detector.py <input>")
        sys.exit(1)

    string = sys.argv[1]

    result = detect_language(string)
    print(result)
