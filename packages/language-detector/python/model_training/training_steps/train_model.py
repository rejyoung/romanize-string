
"""
This model was trained using corpora provided by the Wortschatz Project
(University of Leipzig), licensed under CC BY 4.0.

Source: https://wortschatz.uni-leipzig.de/en/download
License: https://creativecommons.org/licenses/by/4.0/
"""

import logging
import sys
from pathlib import Path

import joblib
import numpy as np
from scipy.sparse import csr_matrix

from sklearn.naive_bayes import ComplementNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import VotingClassifier
from sklearn.multiclass import OneVsRestClassifier


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_data(model_type: str, base: Path) -> tuple[csr_matrix, np.ndarray]:
    """
    Load training data from disk.

    Args:
        model_type: Type of model to load data for (e.g., 'family', 'cyrillic')
        base: Base directory for data files

    Returns:
        Tuple containing the training data (sparse matrix) and labels (numpy array)

    Raises:
        FileNotFoundError: If the data file is not found
        Exception: If there is an error loading the data
    """
    logger.info(f"Loading {model_type} training data")
    try:
        data_file = base / "data/processed/split" / f"ld_{model_type}_train_data.joblib"
        X_train, y_train = joblib.load(data_file)
        logger.info(f"Successfully loaded {X_train.shape[0]} training samples with {X_train.shape[1]} features")
        return X_train, y_train
    except FileNotFoundError:
        logger.error(f"Data file not found: {data_file}")
        raise
    except Exception as e:
        logger.error(f"Failed to load data for {model_type}: {e}")
        raise


def create_and_fit_model(X_train: csr_matrix, y_train: np.ndarray, model_type: str) -> VotingClassifier:
    """
    Create and train an ensemble model using the training data.

    Args:
        X_train: Training data features (sparse matrix)
        y_train: Training labels (numpy array)
        model_type: Type of model being trained

    Returns:
        The trained ensemble model
    """
    logger.info(f"Creating ensemble model for {model_type} with {X_train.shape[0]} samples")
    
    # Create base classifiers
    nb_classifier = ComplementNB(alpha=0.3)
    logreg_classifier = LogisticRegression(
        max_iter=1000,
        solver="saga",
        penalty="l2",
        C=2.0,
        class_weight="balanced",
        verbose=1,
        tol=1e-3,
    )

    # Create ensemble model
    ensemble_model = VotingClassifier(
        estimators=[
            ("nb", nb_classifier),
            ("logreg", OneVsRestClassifier(logreg_classifier, n_jobs=-1)),
        ],
        voting="soft",
    )

    logger.info(f"Fitting {model_type} ensemble model")
    ensemble_model.fit(X_train, y_train)
    logger.info(f"Model training completed successfully")

    return ensemble_model


def save_model(model: VotingClassifier, model_assets: Path, model_type: str) -> None:
    """
    Save the trained model to disk.

    Args:
        model: The trained model to save
        model_assets: Path to model assets directory
        model_type: Type of model being saved
    """
    output_file = model_assets / "models" / f"ld_{model_type}_ensemble_model.joblib"
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Saving {model_type} ensemble model to {output_file}")
    joblib.dump(model, output_file)
    logger.info(f"Model saved successfully to {output_file}")


def evaluate_model(model: VotingClassifier, X_train: csr_matrix, y_train: np.ndarray, model_type: str) -> None:
    """
    Evaluate the model performance on training data.

    Args:
        model: The trained model to evaluate
        X_train: Training data features (sparse matrix)
        y_train: Training labels (numpy array)
        model_type: Type of model being evaluated
    """
    logger.info(f"Evaluating {model_type} model performance")
    
    train_accuracy = model.score(X_train, y_train)
    logger.info(f"Training accuracy: {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
    
    # Additional evaluation metrics could be added here
    logger.info(f"Model evaluation completed")


def train_model(model_type: str, model_dir: str) -> None:
    """
    Main function to train and evaluate a model.

    Args:
        model_type: Type of model to train (e.g., 'family', 'cyrillic')
        model_dir: Path to model assets directory
        
    Raises:
        Exception: If any step in the training process fails
    """
    logger.info(f"Starting model training process for {model_type}")
    
    try:
        # Setup paths
        model_assets = Path(model_dir)
        base = Path(__file__).resolve().parents[1]
        
        # Load training data
        X_train, y_train = load_data(model_type, base)
        
        # Create and train model
        model = create_and_fit_model(X_train, y_train, model_type)
        
        # Save model
        save_model(model, model_assets, model_type)
        
        # Evaluate model
        evaluate_model(model, X_train, y_train, model_type)
        
        logger.info(f"Model training process completed successfully for {model_type}")
        
    except Exception as e:
        logger.error(f"Model training failed for {model_type}: {e}")
        raise


def main() -> None:
    """Main entry point for command line usage."""
    if len(sys.argv) != 3:
        logger.error("Usage: python train_model.py <model_type> <model_dir>")
        sys.exit(1)

    model_type = sys.argv[1]
    model_dir = sys.argv[2]

    try:
        train_model(model_type, model_dir)
        logger.info("Model training completed successfully")
    except Exception as e:
        logger.error(f"Model training failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
