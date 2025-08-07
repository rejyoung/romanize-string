import pandas as pd
import sys, joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path


"""
This model was trained using corpora provided by the Wortschatz Project
(University of Leipzig), licensed under CC BY 4.0.

Source: https://wortschatz.uni-leipzig.de/en/download
License: https://creativecommons.org/licenses/by/4.0/
"""


def main(data_group: str, model_dir: Path):
    print(f"Reading {data_group} data")
    df = pd.read_csv(Path("data/intermediate") / f"ld_balanced_{data_group}_data.csv")
    cv = TfidfVectorizer(analyzer="char", ngram_range=(2, 5), max_features=50000)

    print(f"Vectorizing {data_group} data")
    X = cv.fit_transform(df["text"])
    y = df["label"].values

    print(f"Writing vectorized {data_group} data to disk")
    joblib.dump(
        (X, y),
        Path("data/processed/vectorized") / f"ld_vectorized_{data_group}_data.joblib",
    )

    print(f"Writing {data_group} vectorizer to disk")
    joblib.dump(cv, model_dir / f"ld_{data_group}_vectorizer.joblib")
    print("Write complete")


if __name__ == "__main__":
    # Expect exactly 2 user‐supplied arguments
    if len(sys.argv) != 3:
        print("Usage: python vectorize_data.py <data_group> <model_dir>")
        sys.exit(1)

    data_group = sys.argv[1]
    model_dir = sys.argv[2]

    main(data_group, model_dir)
