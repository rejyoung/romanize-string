import joblib, sys
from sklearn.metrics import classification_report
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from pathlib import Path


"""
This model was trained using corpora provided by the Wortschatz Project
(University of Leipzig), licensed under CC BY 4.0.

Source: https://wortschatz.uni-leipzig.de/en/download
License: https://creativecommons.org/licenses/by/4.0/
"""


def main(data_group: str, model_dir: str):
    model_assets = Path(model_dir)

    print(f"Loading {data_group} test data")
    X_test, y_test = joblib.load(
        Path("data/processed/split") / f"ld_{data_group}_test_data.joblib"
    )

    print(f"Loading {data_group} ensemble model")
    ensemble_model = joblib.load(
        model_assets / f"ld_{data_group}_ensemble_model.joblib"
    )

    print(f"Performing {data_group} data confusion estimation")
    ConfusionMatrixDisplay.from_estimator(ensemble_model, X_test, y_test)
    plt.show()

    print(f"Making {data_group} data classification report")
    print(classification_report(y_test, ensemble_model.predict(X_test)))

    print(f"Testing accuracy with unseen {data_group} test data")
    print("Test accuracy:", ensemble_model.score(X_test, y_test))


if __name__ == "__main__":
    # Expect exactly 2 user‐supplied arguments
    if len(sys.argv) != 3:
        print("Usage: python run_test_data.py <data_group> <model_dir>")
        sys.exit(1)

    data_group = sys.argv[1]
    model_dir = sys.argv[2]

    main(data_group, model_dir)
