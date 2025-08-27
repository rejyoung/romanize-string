import joblib, sys
from sklearn.model_selection import train_test_split
from pathlib import Path


"""
This model was trained using corpora provided by the Wortschatz Project
(University of Leipzig), licensed under CC BY 4.0.

Source: https://wortschatz.uni-leipzig.de/en/download
License: https://creativecommons.org/licenses/by/4.0/
"""


def main(model_type: str):
    base = Path(__file__).resolve().parents[1]

    print(f"Loading {model_type} data")
    X, y = joblib.load(
        base
        / Path("data/processed/vectorized")
        / f"ld_vectorized_{model_type}_data.joblib"
    )

    print(f"Splitting {model_type} data")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.05, random_state=42, stratify=y
    )

    print(f"Writing {model_type} split data to disk")
    joblib.dump(
        (X_train, y_train),
        base / Path("data/processed/split") / f"ld_{model_type}_train_data.joblib",
    )
    joblib.dump(
        (X_test, y_test),
        base / Path("data/processed/split") / f"ld_{model_type}_test_data.joblib",
    )
    print("Write complete")


if __name__ == "__main__":
    # Get arg
    if len(sys.argv) != 2:
        print("Usage: python split_data.py <model_type>")
        sys.exit(1)

    model_type = sys.argv[1]

    main(model_type)
