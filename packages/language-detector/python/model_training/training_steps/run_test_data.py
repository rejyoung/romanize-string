import joblib, sys
from sklearn.metrics import classification_report
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.multiclass import OneVsRestClassifier
from sklearn.ensemble import VotingClassifier


"""
This model was trained using corpora provided by the Wortschatz Project
(University of Leipzig), licensed under CC BY 4.0.

Source: https://wortschatz.uni-leipzig.de/en/download
License: https://creativecommons.org/licenses/by/4.0/
"""



def main(data_group: str, model_dir: str):
    model_assets = Path(model_dir)

    base = Path(__file__).resolve().parents[1]

    print(f"Loading {data_group} test data")
    X_test, y_test = joblib.load(
        base / Path("data/processed/split") / f"ld_{data_group}_test_data.joblib"
    )

    print(f"Loading {data_group} ensemble model")
    ensemble_model = joblib.load(
        model_assets / f"ld_{data_group}_ensemble_model.joblib"
    )

    results_dir = model_assets / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    # Save confusion matrix
    print(f"Performing {data_group} data confusion estimation")
    disp = ConfusionMatrixDisplay.from_estimator(ensemble_model, X_test, y_test, cmap="Blues", colorbar=True)
    
    output_path = results_dir / f"{data_group}_confusion_matrix.png"
    plt.safefig(output_path, bbox_inches="tight", dpi=300)
    plt.close()

    # Saving reports

    print(f"Making {data_group} data classification report")
    report = classification_report(y_test, ensemble_model.predict(X_test))

    print(f"Testing accuracy with unseen {data_group} test data")
    accuracy = ensemble_model.score(X_test, y_test)

    with open(results_dir / f"{data_group}_report.txt", "w", encoding="utf-8") as f:
        f.write(f"Classifcation report for {data_group}\n\n")
        f.write(report)
        f.write("\n\n")
        f.write(f"Test accuracy: {accuracy:.4f}\n")

    # print_most_influential_features(ensemble_model, model_assets)



def print_most_influential_features (ensemble_model, model_assets):

    vectorizer = joblib.load(model_assets / f"ld_{data_group}_vectorizer.joblib")

    coefs, source = extract_linear_coefs(ensemble_model)
    print(f"Extracted linear coefs from: {source}")
    feat_names = vectorizer.get_feature_names_out()

    assets = joblib.load(model_assets / f"ld_{data_group}_tell_lists.joblib")
    tell_characters = assets.get("tell_characters", [])
    endings = assets.get("endings", [])
    bigrams = assets.get("bigrams", [])

    # derive tell-score group order
    tell_groups = assets.get("tell_groups")
    if not tell_groups:
        # fallback: same sorted class order the training used
        tell_groups = sorted(map(str, getattr(ensemble_model, "classes_", [])))

    aug_names = []
    # ⚠️ Keep this order identical to how you stacked columns in augment_features.py
    # Example (adjust if your augment_features uses a different order):
    #   [tell_characters] + [endings] + [bigrams_present] + [bigrams_count]
    aug_names.extend([f"tc:{c}" for c in tell_characters])
    aug_names.extend([f"tell:{g}" for g in tell_groups])
    aug_names.extend([f"end:{e}:present" for e in endings])
    aug_names.extend([f"end:{e}:count" for e in endings])
    aug_names.extend([f"bi:{b}:present" for b in bigrams])
    aug_names.extend([f"bi:{b}:count" for b in bigrams])

    all_names = np.concatenate([feat_names, np.array(aug_names, dtype=object)])

    # 3) Sanity check: names length must match model feature count (coefs.shape[1])
    if all_names.shape[0] != coefs.shape[1]:
        raise RuntimeError(
            f"Feature-name length mismatch: names={all_names.shape[0]} vs model={coefs.shape[1]}. "
            "Ensure aug_names ordering matches augment_features.py stacking."
        )

    top_k = 20
    for cls_idx in range(coefs.shape[0]):
        idx = np.argsort(coefs[cls_idx])[-top_k:][::-1]
        print(f"\nClass {cls_idx} top {top_k}:")
        for i in idx:
            print(f"  {all_names[i]}  {coefs[cls_idx, i]:.6f}")

def _unwrap(est):
    return est.steps[-1][1] if isinstance(est, Pipeline) else est


def extract_linear_coefs(clf):
    """Return (coefs, source). coefs shape: (n_classes, n_features) or (1, n_features)."""
    c = _unwrap(clf)

    if hasattr(c, "coef_"):
        return c.coef_, c.__class__.__name__

    if isinstance(c, OneVsRestClassifier):
        inners = [e for e in c.estimators_ if hasattr(e, "coef_")]
        if not inners:
            raise AttributeError("OVR inner estimators lack coef_.")
        return np.vstack([e.coef_ for e in inners]), "OneVsRest"

    if isinstance(c, VotingClassifier):
        names = [n for n, _ in c.estimators]  # preserve order
        weights = c.weights or [1.0] * len(names)
        mats, wts = [], []
        for i, name in enumerate(names):
            est = c.named_estimators_.get(name)
            if est is None:
                continue
            est = _unwrap(est)
            if isinstance(est, OneVsRestClassifier):
                inners = [e for e in est.estimators_ if hasattr(e, "coef_")]
                if not inners:
                    continue
                coefs = np.vstack([e.coef_ for e in inners])
            elif hasattr(est, "coef_"):
                coefs = est.coef_
            else:
                continue
            mats.append(coefs)
            wts.append(weights[i])
        if not mats:
            raise AttributeError("No base estimator exposes coef_.")
        maxc = max(m.shape[0] for m in mats)
        mats = [
            (w * (np.vstack([m] * maxc) if m.shape[0] == 1 and maxc > 1 else m))
            for w, m in zip(wts, mats)
        ]
        return sum(mats) / sum(wts), "Voting(avg)"

    raise AttributeError("Classifier does not expose coef_.")


if __name__ == "__main__":
    # Expect exactly 2 user‐supplied arguments
    if len(sys.argv) != 3:
        print("Usage: python run_test_data.py <data_group> <model_dir>")
        sys.exit(1)

    data_group = sys.argv[1]
    model_dir = sys.argv[2]

    main(data_group, model_dir)
