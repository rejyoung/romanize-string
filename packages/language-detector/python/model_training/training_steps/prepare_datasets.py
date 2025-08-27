import logging
import sys
from pathlib import Path

import pandas as pd
from sklearn.utils import resample

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

THRESHOLDS = {
    "family": (500_000, 3_000_000),
    "perso_arabic": (2_120_000, 4_300_000),
    "cyrillic": (1_000_000, 3_000_000),
    "indic": (530_000, 3_600_000),
    "eastern_slavic": (500_000, 1_000_000),
    "southern_slavic": (500_000, 1_000_000),
    "turkic": (500_000, 1_000_000),
    "ja_zh": (1_000_000, 2_000_000),
}

RANDOM_SEED = 42
INPUT_DATA_DIR = "data/intermediate"
OUTPUT_DATA_DIR = "data/intermediate"


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
        file_path = base / INPUT_DATA_DIR / f"ld_{model_type}_data.csv"
        logger.info(f"Loading dataset from {file_path}")
        df = pd.read_csv(file_path)
        logger.info(f"Loaded {len(df)} rows for {model_type}")
        return df
    except FileNotFoundError:
        logger.error(f"Dataset file not found: {base / INPUT_DATA_DIR / f'ld_{model_type}_data.csv'}")
        raise
    except pd.errors.EmptyDataError:
        logger.error(f"Dataset file is empty: ld_{model_type}_data.csv")
        raise


def balance_dataset(df: pd.DataFrame, model_type: str) -> pd.DataFrame:
    """
    Balance dataset for a specific model type.
    
    Args:
        df: DataFrame containing the dataset
        model_type: Type of model to balance data for (e.g., 'family', 'cyrillic')

    Returns:
        DataFrame containing the balanced dataset
    """
    MIN_SIZE, MAX_SIZE = THRESHOLDS[model_type] 

    logger.info(f"Balancing {model_type} dataset (target: {MIN_SIZE:,} - {MAX_SIZE:,} samples per class)")

    grouped = df.groupby("label")
    balanced_groups = []
    
    for label, group in grouped:
        n = len(group)
        if n < MIN_SIZE:
            logger.info(f"Up-sampling {label} from {n:,} to {MIN_SIZE:,} samples")
            resampled = resample(
                group, replace=True, n_samples=MIN_SIZE, random_state=RANDOM_SEED
            )
        elif n > MAX_SIZE:
            logger.info(f"Down-sampling {label} from {n:,} to {MAX_SIZE:,} samples")
            resampled = group.sample(n=MAX_SIZE, random_state=RANDOM_SEED)
        else:
            logger.info(f"{label} is already balanced with {n:,} samples")
            resampled = group
        balanced_groups.append(resampled)

    balanced_df = pd.concat(balanced_groups).sample(frac=1, random_state=RANDOM_SEED)
    
    logger.info(f"Balanced dataset created with {len(balanced_df):,} total samples")
    return balanced_df


def write_dataset(df: pd.DataFrame, base: Path, model_type: str) -> None:
    """
    Write dataset to CSV file.
    
    Args:
        df: DataFrame containing the dataset
        base: Base directory for the output file
        model_type: Type of model to write data for (e.g., 'family', 'cyrillic')
    """
    output_file = base / OUTPUT_DATA_DIR / f"ld_balanced_{model_type}_data.csv"
    logger.info(f"Writing {model_type} balanced dataset to {output_file}")
    
    df.to_csv(output_file, index=False)
    logger.info(f"Successfully wrote {len(df):,} rows to {output_file}")


def validate_model_type(model_type: str) -> None:
    """Validate that model_type exists in THRESHOLDS."""
    if model_type not in THRESHOLDS:
        available_types = list(THRESHOLDS.keys())
        logger.error(f"Unknown model_type: {model_type}. Available: {available_types}")
        raise KeyError(f"Unknown model_type: {model_type}. Available: {available_types}")


def prepare_dataset(base: Path, model_type: str) -> None:
    """
    Prepare a single dataset by loading, balancing, and writing it.
    
    Args:
        base: Base directory for the dataset
        model_type: Type of model to prepare data for
    """
    logger.info(f"Starting preparation of {model_type} dataset")
    
    try:
        # Load dataset
        df = load_dataset(base, model_type)
        
        # Balance dataset
        balanced_df = balance_dataset(df, model_type)
        
        # Write balanced dataset
        write_dataset(balanced_df, base, model_type)
        
        logger.info(f"Successfully prepared {model_type} dataset")
        
    except Exception as e:
        logger.error(f"Failed to prepare {model_type} dataset: {e}")
        raise


def main():
    """Main function to prepare all datasets."""
    if len(sys.argv) != 2:
        logger.error("Usage: python prepare_datasets.py <model_type>")
        sys.exit(1)
    
    model_type = sys.argv[1]
    base_path = Path(__file__).resolve().parents[1]
    
    try:
        logger.info("Starting dataset preparation process")
        
        # Validate model type
        validate_model_type(model_type)
        
        # Prepare dataset
        prepare_dataset(base_path, model_type)
        
        logger.info("Dataset preparation completed successfully")
        
    except Exception as e:
        logger.error(f"Dataset preparation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
