import pandas as pd
import numpy as np
import sys, joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path
from utils.text_util import strip_ascii
from utils.build_extended_features_block import build_extended_features_block
from scipy.sparse import hstack


"""
This model was trained using corpora provided by the Wortschatz Project
(University of Leipzig), licensed under CC BY 4.0.

Source: https://wortschatz.uni-leipzig.de/en/download
License: https://creativecommons.org/licenses/by/4.0/
"""


def main(data_group: str, model_dir: str):
    model_assets = Path(model_dir)

    print(f"Reading {data_group} data")

    base = Path(__file__).resolve().parents[2]
    df = pd.read_csv(
        base / "data" / "intermediate" / f"ld_balanced_{data_group}_data.csv", usecols=["text", "label"]
    )

    vectorizer = create_vectorizer(data_group)

    print(f"Vectorizing {data_group} data")
    X_base = vectorizer.fit_transform(df["text"])
    y = df["label"].values

    print(f"Augmenting vectorized {data_group} data with extra features")
    extended_feature_block = build_extended_features_block(df["text"], data_group)

    if extended_feature_block.dtype != X_base.dtype:
       extended_feature_block = extended_feature_block.astype(X_base.dtype, copy=False)

    # Combine base + extended features
    X_aug = hstack([X_base, extended_feature_block], format="csr")

    print("X_base:", X_base.shape, "X_ext:", extended_feature_block.shape, "X_aug:", X_aug.shape)

    print(f"Writing {data_group} vectorizer to disk")
    joblib.dump(vectorizer, model_assets / "vectorizers" / f"ld_{data_group}_vectorizer.joblib")
    print("Write complete")

    print(f"Writing vectorized {data_group} data to disk")
    joblib.dump(
        (X_aug, y),
        base
        / Path("data/processed/vectorized")
        / f"ld_vectorized_{data_group}_data.joblib",
    )

    


def create_vectorizer(data_group: str):

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

    print(f"Configuring {data_group} vectorizer.")
    vectorizer = TfidfVectorizer(
        analyzer=config.get("analyzer", "char_wb"),
        ngram_range=config.get("ngram_range", (1, 5)),
        max_features=config.get("max_features", 30_000),
        preprocessor=strip_ascii,
        min_df=2,
        max_df=config.get("max_df", 0.95),
        sublinear_tf=True,  # dampen very frequent ngrams
        dtype=np.float32,
    )

    return vectorizer

if __name__ == "__main__":
    # Expect exactly 2 user‐supplied arguments
    if len(sys.argv) != 3:
        print("Usage: python vectorize_data.py <data_group> <model_dir>")
        sys.exit(1)

    data_group = sys.argv[1]
    model_dir = sys.argv[2]

    main(data_group, model_dir)
