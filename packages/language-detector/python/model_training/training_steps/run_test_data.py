"""
This model was trained using corpora provided by the Wortschatz Project
(University of Leipzig), licensed under CC BY 4.0.

Source: https://wortschatz.uni-leipzig.de/en/download
License: https://creativecommons.org/licenses/by/4.0/
"""

import logging
import sys
from pathlib import Path
from typing import Tuple, Optional

import joblib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import classification_report, ConfusionMatrixDisplay
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from scipy.sparse import csr_matrix


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_test_data(model_type: str, base: Path) -> Tuple[csr_matrix, np.ndarray]:
    """
    Load test data from disk.
    
    Args:
        model_type: Type of model to load test data for
        base: Base directory for data files
        
    Returns:
        Tuple containing test features and labels
        
    Raises:
        FileNotFoundError: If test data file is not found
        Exception: If there is an error loading the data
    """
    try:
        data_file = base / "data/processed/split" / f"ld_{model_type}_test_data.joblib"
        logger.info(f"Loading {model_type} test data from {data_file}")
        X_test, y_test = joblib.load(data_file)
        logger.info(f"Successfully loaded {X_test.shape[0]} test samples with {X_test.shape[1]} features")
        return X_test, y_test
    except FileNotFoundError:
        logger.error(f"Test data file not found: {data_file}")
        raise
    except Exception as e:
        logger.error(f"Failed to load test data for {model_type}: {e}")
        raise


def load_trained_model(model_type: str, model_assets: Path) -> VotingClassifier:
    """
    Load the trained ensemble model from disk.
    
    Args:
        model_type: Type of model to load
        model_assets: Path to model assets directory
        
    Returns:
        The trained ensemble model
        
    Raises:
        FileNotFoundError: If model file is not found
        Exception: If there is an error loading the model
    """
    try:
        model_file = model_assets / "models" / f"ld_{model_type}_ensemble_model.joblib"
        logger.info(f"Loading {model_type} ensemble model from {model_file}")
        ensemble_model = joblib.load(model_file)
        logger.info(f"Successfully loaded ensemble model")
        return ensemble_model
    except FileNotFoundError:
        logger.error(f"Model file not found: {model_file}")
        raise
    except Exception as e:
        logger.error(f"Failed to load model for {model_type}: {e}")
        raise


def create_confusion_matrix(model: VotingClassifier, X_test: np.ndarray, y_test: np.ndarray, 
                          model_type: str, results_dir: Path) -> None:
    """
    Create and save confusion matrix visualization.
    
    Args:
        model: The trained model to evaluate
        X_test: Test features
        y_test: Test labels
        model_type: Type of model being evaluated
        results_dir: Directory to save results
    """
    logger.info(f"Creating confusion matrix for {model_type}")
    
    disp = ConfusionMatrixDisplay.from_estimator(
        model, X_test, y_test, cmap="Blues", colorbar=True
    )
    
    output_path = results_dir / f"{model_type}_confusion_matrix.png"
    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close()
    
    logger.info(f"Confusion matrix saved to {output_path}")


def generate_classification_report(model: VotingClassifier, X_test: np.ndarray, y_test: np.ndarray,
                                 model_type: str, results_dir: Path) -> None:
    """
    Generate and save classification report.
    
    Args:
        model: The trained model to evaluate
        X_test: Test features
        y_test: Test labels
        model_type: Type of model being evaluated
        results_dir: Directory to save results
    """
    logger.info(f"Generating classification report for {model_type}")
    
    # Generate predictions
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred)
    
    # Calculate accuracy
    accuracy = model.score(X_test, y_test)
    
    # Save report to file
    report_file = results_dir / f"{model_type}_report.txt"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(f"Classification report for {model_type}\n\n")
        f.write(report)
        f.write("\n\n")
        f.write(f"Test accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)\n")
    
    logger.info(f"Classification report saved to {report_file}")
    logger.info(f"Test accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")

def run_test_evaluation(model_type: str, model_dir: str) -> None:
    """
    Main function to run test evaluation on a trained model.
    
    Args:
        model_type: Type of model to evaluate
        model_dir: Path to model assets directory
        
    Raises:
        Exception: If evaluation fails
    """
    logger.info(f"Starting test evaluation for {model_type}")
    
    try:
        # Setup paths
        model_assets = Path(model_dir)
        base = Path(__file__).resolve().parents[1]
        results_dir = model_assets / "results"
        results_dir.mkdir(parents=True, exist_ok=True)
        
        # Load test data and model
        X_test, y_test = load_test_data(model_type, base)
        ensemble_model = load_trained_model(model_type, model_assets)
        
        # Generate confusion matrix
        create_confusion_matrix(ensemble_model, X_test, y_test, model_type, results_dir)
        
        # Generate classification report
        generate_classification_report(ensemble_model, X_test, y_test, model_type, results_dir)
        
        # Analyze feature importance (optional)
        # analyze_feature_importance(ensemble_model, model_assets, model_type)
        
        logger.info(f"Test evaluation completed successfully for {model_type}")
        
    except Exception as e:
        logger.error(f"Test evaluation failed for {model_type}: {e}")
        raise


##### Feature importance analysis #####

def _unwrap(estimator) -> object:
    """
    Unwrap estimator from pipeline if necessary.
    
    Args:
        estimator: The estimator to unwrap
        
    Returns:
        The unwrapped estimator
    """
    return estimator.steps[-1][1] if isinstance(estimator, Pipeline) else estimator


def extract_linear_coefficients(classifier) -> Tuple[np.ndarray, str]:
    """
    Extract linear coefficients from various classifier types.
    
    Args:
        classifier: The classifier to extract coefficients from
        
    Returns:
        Tuple of (coefficients, source_description)
        
    Raises:
        AttributeError: If classifier does not expose coefficients
    """
    c = _unwrap(classifier)

    if hasattr(c, "coef_"):
        return c.coef_, c.__class__.__name__

    if isinstance(c, OneVsRestClassifier):
        inners = [e for e in c.estimators_ if hasattr(e, "coef_")]
        if not inners:
            raise AttributeError("OneVsRest inner estimators lack coef_.")
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


def analyze_feature_importance(ensemble_model: VotingClassifier, model_assets: Path, 
                             model_type: str, top_k: int = 20) -> None:
    """
    Analyze and display most influential features for each class.
    
    Args:
        ensemble_model: The trained ensemble model
        model_assets: Path to model assets directory
        model_type: Type of model being analyzed
        top_k: Number of top features to display per class
    """
    try:
        logger.info(f"Analyzing feature importance for {model_type}")
        
        # Load vectorizer
        vectorizer_file = model_assets / f"ld_{model_type}_vectorizer.joblib"
        if not vectorizer_file.exists():
            logger.warning(f"Vectorizer file not found: {vectorizer_file}")
            return
            
        vectorizer = joblib.load(vectorizer_file)
        
        # Extract coefficients
        coefs, source = extract_linear_coefficients(ensemble_model)
        logger.info(f"Extracted linear coefficients from: {source}")
        
        # Get feature names
        feat_names = vectorizer.get_feature_names_out()
        
        # Load tell lists and other assets
        assets_file = model_assets / f"ld_{model_type}_tell_lists.joblib"
        if not assets_file.exists():
            logger.warning(f"Tell lists file not found: {assets_file}")
            return
            
        assets = joblib.load(assets_file)
        tell_characters = assets.get("tell_characters", [])
        endings = assets.get("endings", [])
        bigrams = assets.get("bigrams", [])
        
        # Derive tell-score group order
        tell_groups = assets.get("tell_groups")
        if not tell_groups:
            # Fallback: same sorted class order the training used
            tell_groups = sorted(map(str, getattr(ensemble_model, "classes_", [])))
        
        # Build augmented feature names
        aug_names = []
        # ⚠️ Keep this order identical to how columns are stacked in build_extended_features_block.py and vectorize_training_data.py
        aug_names.extend([f"tc:{c}" for c in tell_characters])
        aug_names.extend([f"tell:{g}" for g in tell_groups])
        aug_names.extend([f"end:{e}:present" for e in endings])
        aug_names.extend([f"end:{e}:count" for e in endings])
        aug_names.extend([f"bi:{b}:present" for b in bigrams])
        aug_names.extend([f"bi:{b}:count" for b in bigrams])
        
        all_names = np.concatenate([feat_names, np.array(aug_names, dtype=object)])
        
        # Sanity check: names length must match model feature count
        if all_names.shape[0] != coefs.shape[1]:
            raise RuntimeError(
                f"Feature-name length mismatch: names={all_names.shape[0]} vs model={coefs.shape[1]}. "
                "Ensure aug_names ordering matches augment_features.py stacking."
            )
        
        # Display top features for each class
        logger.info(f"Top {top_k} most influential features per class:")
        for cls_idx in range(coefs.shape[0]):
            idx = np.argsort(coefs[cls_idx])[-top_k:][::-1]
            logger.info(f"\nClass {cls_idx} top {top_k}:")
            for i in idx:
                logger.info(f"  {all_names[i]}  {coefs[cls_idx, i]:.6f}")
                
    except Exception as e:
        logger.error(f"Feature importance analysis failed: {e}")


##### Main function #####

def main() -> None:
    """Main entry point for command line usage."""
    if len(sys.argv) != 3:
        logger.error("Usage: python run_test_data.py <model_type> <model_dir>")
        sys.exit(1)
    
    model_type = sys.argv[1]
    model_dir = sys.argv[2]
    
    try:
        run_test_evaluation(model_type, model_dir)
        logger.info("Test evaluation completed successfully")
    except Exception as e:
        logger.error(f"Test evaluation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
