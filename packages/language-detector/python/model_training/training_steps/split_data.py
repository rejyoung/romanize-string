import joblib, sys
from sklearn.model_selection import train_test_split
from pathlib import Path


"""
This model was trained using corpora provided by the Wortschatz Project
(University of Leipzig), licensed under CC BY 4.0.

Source: https://wortschatz.uni-leipzig.de/en/download
License: https://creativecommons.org/licenses/by/4.0/
"""


def main(data_group: str):
    base = Path(__file__).resolve().parents[1]

    print(f"Loading {data_group} data")
    X, y = joblib.load(
        base
        / Path("data/processed/augmented")
        / f"ld_augmented_{data_group}_data.joblib"
    )

    print(f"Splitting {data_group} data")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.05, random_state=42, stratify=y
    )

    print(f"Writing {data_group} split data to disk")
    joblib.dump(
        (X_train, y_train),
        base / Path("data/processed/split") / f"ld_{data_group}_train_data.joblib",
    )
    joblib.dump(
        (X_test, y_test),
        base / Path("data/processed/split") / f"ld_{data_group}_test_data.joblib",
    )
    print("Write complete")


if __name__ == "__main__":
    # Get arg
    if len(sys.argv) != 2:
        print("Usage: python split_data.py <data_group>")
        sys.exit(1)

    data_group = sys.argv[1]

    main(data_group)
