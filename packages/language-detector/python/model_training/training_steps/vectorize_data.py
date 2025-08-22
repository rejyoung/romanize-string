import pandas as pd
import numpy as np
import sys, joblib, regex, unicodedata
from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path
from utils.text_util import strip_ascii


"""
This model was trained using corpora provided by the Wortschatz Project
(University of Leipzig), licensed under CC BY 4.0.

Source: https://wortschatz.uni-leipzig.de/en/download
License: https://creativecommons.org/licenses/by/4.0/
"""


def main(data_group: str, model_dir: str):

    model_assets = Path(model_dir)

    print(f"Reading {data_group} data")

    base = Path(__file__).resolve().parents[1]
    df = pd.read_csv(
        base / "data" / "intermediate" / f"ld_balanced_{data_group}_data.csv"
    )

    CONFIGURATION = {
        "southern_slavic": dict(
            max_features=200_000, max_df=0.995, ngram_range=(3, 5), analyzer="char"
        ),
        "indic": dict(max_features=120_000, max_df=1.0),
        "ja_zh": dict(max_features=120_000, max_df=1.0),
        "eastern_slavic": dict(max_features=100_000, max_df=1.0),
        "perso_arabic": dict(max_features=80_000, max_df=0.98),
    }

    config = CONFIGURATION.get(data_group, {})
    cv = TfidfVectorizer(
        analyzer=config.get("analyzer", "char_wb"),
        ngram_range=config.get("ngram_range", (1, 5)),
        max_features=config.get("max_features", 30_000),
        preprocessor=strip_ascii,
        min_df=2,
        max_df=config.get("max_df", 0.95),
        sublinear_tf=True,  # dampen very frequent ngrams
        dtype=np.float32,
    )

    print(f"Vectorizing {data_group} data")
    X = cv.fit_transform(df["text"])
    y = df["label"].values

    print(f"Writing vectorized {data_group} data to disk")
    joblib.dump(
        (X, y),
        base
        / Path("data/processed/vectorized")
        / f"ld_vectorized_{data_group}_data.joblib",
    )

    print(f"Writing {data_group} vectorizer to disk")
    joblib.dump(cv, model_assets / f"ld_{data_group}_vectorizer.joblib")
    print("Write complete")


if __name__ == "__main__":
    # Expect exactly 2 user‐supplied arguments
    if len(sys.argv) != 3:
        print("Usage: python vectorize_data.py <data_group> <model_dir>")
        sys.exit(1)

    data_group = sys.argv[1]
    model_dir = sys.argv[2]

    main(data_group, model_dir)
