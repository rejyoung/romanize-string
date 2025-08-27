"""
This model was trained using corpora provided by the Wortschatz Project
(University of Leipzig), licensed under CC BY 4.0.

Source: https://wortschatz.uni-leipzig.de/en/download
License: https://creativecommons.org/licenses/by/4.0/
"""

import logging
import sys
from pathlib import Path
from typing import Tuple, Any

import joblib
from sklearn.model_selection import train_test_split

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
TEST_SIZE = 0.05
RANDOM_STATE = 42


class DataSplitError(Exception):
    """Custom exception for data splitting errors."""
    pass


def split_data(model_type: str) -> None:
    """
    Split data into training and test sets.

    Args:
        model_type: Type of model to split data for (e.g., 'family', 'cyrillic')

    Raises:
        DataSplitError: If data splitting fails
    """
    base_path = Path(__file__).resolve().parents[1]

    try:
        logger.info(f"Loading {model_type} data")
        X, y = joblib.load(
            base_path
            / "data/processed/vectorized"
            / f"ld_vectorized_{model_type}_data.joblib"
        )
        
        if len(X) == 0 or len(y) == 0:
            raise DataSplitError(f"Vectorized data file is empty for {model_type}")
            
    except FileNotFoundError:
        raise DataSplitError(f"Vectorized data file not found for {model_type}")
    except Exception as e:
        raise DataSplitError(f"Failed to load data for {model_type}: {e}")

    logger.info(f"Splitting {model_type} data with test_size={TEST_SIZE}")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    
    logger.info(f"Split complete: {len(X_train)} training, {len(X_test)} test samples")

    logger.info(f"Writing {model_type} split data to disk")
    
    # Ensure output directory exists
    output_dir = base_path / "data/processed/split"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    joblib.dump(
        (X_train, y_train),
        output_dir / f"ld_{model_type}_train_data.joblib",
    )
    joblib.dump(
        (X_test, y_test),
        output_dir / f"ld_{model_type}_test_data.joblib",
    )
    
    logger.info("Data split and save complete")


def main() -> None:
    """Main entry point for command line usage."""
    if len(sys.argv) != 2:
        logger.error("Usage: python split_data.py <model_type>")
        sys.exit(1)
    
    model_type = sys.argv[1]
    
    try:
        split_data(model_type)
        logger.info("Data splitting completed successfully")
    except DataSplitError as e:
        logger.error(f"Data splitting failed: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
