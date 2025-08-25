import joblib, gc, sys
from sklearn.naive_bayes import ComplementNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import VotingClassifier
from sklearn.multiclass import OneVsRestClassifier
from pathlib import Path


"""
This model was trained using corpora provided by the Wortschatz Project
(University of Leipzig), licensed under CC BY 4.0.

Source: https://wortschatz.uni-leipzig.de/en/download
License: https://creativecommons.org/licenses/by/4.0/
"""


def main(data_group: str, model_dir: str):
    model_assets = Path(model_dir)
    base = Path(__file__).resolve().parents[1]

    print(f"Reading prepared {data_group} training data")
    X_train, y_train = joblib.load(
        base / Path("data/processed/split") / f"ld_{data_group}_train_data.joblib"
    )

    logreg_classifier = LogisticRegression(
        max_iter=1000,
        solver="saga",
        penalty="l2",
        C=2.0,  # ← was default 1.0
        class_weight="balanced",
        verbose=1,
        tol=1e-3,
    )

    ensemble_model = VotingClassifier(
        estimators=[
            ("nb", ComplementNB(alpha=0.3)),
            ("logreg", OneVsRestClassifier(logreg_classifier, n_jobs=-1)),
        ],
        voting="soft",
    )

    print(f"Fitting {data_group} ensemble model")
    ensemble_model.fit(X_train, y_train)

    print(f"Writing {data_group} ensemble model to disk")
    joblib.dump(ensemble_model, model_assets / "models" / f"ld_{data_group}_ensemble_model.joblib")
    print("Write complete")

    print(f"Testing {data_group} accuracy with train data")
    print("Train accuracy:", ensemble_model.score(X_train, y_train))


if __name__ == "__main__":
    # Expect exactly 2 user‐supplied arguments
    if len(sys.argv) != 3:
        print("Usage: python train_data.py <data_group> <model_dir>")
        sys.exit(1)

    data_group = sys.argv[1]
    model_dir = sys.argv[2]

    main(data_group, model_dir)
