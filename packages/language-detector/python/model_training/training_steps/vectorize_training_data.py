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
import pandas as pd
import numpy as np
from scipy.sparse import hstack, csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer

from utils.text_util import strip_ascii
from utils.build_extended_features_block import build_extended_features_block

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

VECTORIZER_CONFIGURATION = {
        "southern_slavic": dict(
            max_features=200_000, max_df=0.995, ngram_range=(3, 5), analyzer="char"
        ),
        "indic": dict(max_features=120_000, max_df=1.0),
        "ja_zh": dict(max_features=120_000, max_df=1.0),
        "eastern_slavic": dict(max_features=100_000, max_df=1.0),
        "perso_arabic": dict(max_features=80_000, max_df=0.98),
    }

def load_dataset(base: Path, model_type: str) -> pd.DataFrame:
    """
    Load dataset for a specific model type.
    
    Args:
        base: Base directory for the dataset
        model_type: Type of model to load data for (e.g., 'family', 'cyrillic')

    Returns:
        DataFrame containing the dataset

    Raises:
        FileNotFoundError: If dataset file is not found
        pd.errors.EmptyDataError: If dataset file is empty
    """
    try:
        file_path = base / "data" / "intermediate" / f"ld_balanced_{model_type}_data.csv"
        logger.info(f"Loading dataset from {file_path}")
        df = pd.read_csv(file_path, usecols=["text", "label"])
        logger.info(f"Loaded {len(df)} rows for {model_type}")
        return df
    except FileNotFoundError:
        logger.error(f"Dataset file not found: {base / 'data' / 'intermediate' / f'ld_balanced_{model_type}_data.csv'}")
        raise
    except pd.errors.EmptyDataError:
        logger.error(f"Dataset file is empty: ld_balanced_{model_type}_data.csv")
        raise


def create_vectorizer(model_type: str) -> TfidfVectorizer:
    """
    Create a TfidfVectorizer for a specific model type.
    
    Args:
        model_type: Type of model to create vectorizer for (e.g., 'family', 'cyrillic')

    Returns:
        TfidfVectorizer configured for the model type
    """

    config = VECTORIZER_CONFIGURATION.get(model_type, {})

    logger.info(f"Configuring {model_type} vectorizer with custom settings")
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

def vectorize_dataset(df: pd.DataFrame, vectorizer: TfidfVectorizer) -> tuple[csr_matrix, np.ndarray]:
    """
    Vectorize dataset using TfidfVectorizer.
    
    Args:
        df: DataFrame containing the dataset
        vectorizer: TfidfVectorizer to use for vectorization

    Returns:
        Tuple containing the vectorized data and labels
    """
    logger.info(f"Vectorizing {len(df)} text samples")
    X = vectorizer.fit_transform(df["text"])
    y = df["label"].values

    logger.info(f"Vectorization complete: {X.shape[0]} samples, {X.shape[1]} features")
    return X, y


def augment_vectorized_data(X_base: np.ndarray, df: pd.DataFrame, model_type: str) -> np.ndarray:
    """
    Augment vectorized data with extra features.
    
    Args:
        X_base: Base vectorized data
        df: DataFrame containing the dataset

    Returns:
        Augmented vectorized data or base vectorized data if no augmentation is needed
    """
    if model_type not in ["family", "cyrillic"]:
        logger.info(f"Augmenting vectorized {model_type} data with extra features")
        extended_feature_block = build_extended_features_block(df["text"], model_type)

        if extended_feature_block.dtype != X_base.dtype:
            extended_feature_block = extended_feature_block.astype(
                X_base.dtype, copy=False
            )

        # Combine base + extended features
        X_aug = hstack([X_base, extended_feature_block], format="csr")

        logger.info(f"Feature augmentation complete: base shape {X_base.shape}, extended shape {extended_feature_block.shape}, final shape {X_aug.shape}")

        return X_aug
    else:
        logger.info(f"No augmentation needed for {model_type}, using base features")
        return X_base


def write_vectorizer_and_data(vectorizer: TfidfVectorizer, X_aug: np.ndarray, y: np.ndarray, base: Path, model_assets: Path, model_type: str) -> None:
    """
    Write vectorizer and data to disk.
    
    Args:
        vectorizer: TfidfVectorizer to write
        X_aug: Augmented vectorized data
        y: Labels
        model_assets: Path to model assets directory
        model_type: Type of model to write vectorizer and data for
    """
    logger.info(f"Writing {model_type} vectorizer to disk")
    joblib.dump(
        vectorizer, model_assets / "vectorizers" / f"ld_{model_type}_vectorizer.joblib"
    )
    logger.info("Vectorizer write complete")

    logger.info(f"Writing vectorized {model_type} data to disk")
    joblib.dump(
        (X_aug, y),
        base
        / Path("data/processed/vectorized")
        / f"ld_vectorized_{model_type}_data.joblib",
    )
    logger.info("Vectorized data write complete")


def main(model_type: str, model_dir: str) -> None:
    """
    Main function to vectorize training data.
    
    Args:
        model_type: Type of model to vectorize data for (e.g., 'family', 'cyrillic')
        model_dir: Path to model assets directory

    Raises:
        FileNotFoundError: If dataset file is not found
        pd.errors.EmptyDataError: If dataset file is empty
        Exception: If an unexpected error occurs
    """

    base = Path(__file__).resolve().parents[1]
    model_assets = Path(model_dir)

    try:
        logger.info(f"Starting vectorization process for {model_type}")
        
        balanced_data = load_dataset(base, model_type)
        vectorizer = create_vectorizer(model_type)
        X_base, y = vectorize_dataset(balanced_data, vectorizer)
        X_aug = augment_vectorized_data(X_base, balanced_data, model_type)
        write_vectorizer_and_data(vectorizer, X_aug, y, base, model_assets, model_type)

        logger.info(f"Vectorization completed successfully for {model_type}")
        
    except (FileNotFoundError, pd.errors.EmptyDataError) as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Expect exactly 2 user‐supplied arguments
    if len(sys.argv) != 3:
        logger.error("Usage: python vectorize_data.py <model_type> <model_dir>")
        sys.exit(1)

    model_type = sys.argv[1]
    model_dir = sys.argv[2]

    main(model_type, model_dir)
