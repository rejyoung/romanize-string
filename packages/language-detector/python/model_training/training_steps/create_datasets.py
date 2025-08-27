"""
This model was trained using corpora provided by the Wortschatz Project
(University of Leipzig), licensed under CC BY 4.0.

Source: https://wortschatz.uni-leipzig.de/en/download
License: https://creativecommons.org/licenses/by/4.0/
"""

import logging
from typing import Dict, List
import csv
from pathlib import Path

import numpy as np
import pandas as pd
import regex

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration constants
LANGUAGE_CODE_LENGTH = 3
EXCLUDE_PATTERN = regex.compile(r"^[\p{Latin}\p{Nd}\p{P}\p{S}\p{Z}]+$")
KANA_OR_JAPANESE_MARKS = regex.compile(
    r"[\p{Script=Hiragana}\p{Script=Katakana}\u30FC\uFF70\u30FB\u3005]"
)

CODE_LANGUAGE_MAP = {
    "ara": "ar", "bel": "be", "ben": "bn", "bul": "bg", "cmn": "zh",
    "ell": "el", "fas": "fa", "guj": "gu", "hin": "hi", "jpn": "ja",
    "kan": "kn", "kaz": "kk", "kir": "ky", "kor": "ko", "mar": "mr",
    "mkd": "mk", "mon": "mn", "nep": "ne", "pan": "pa", "pes": "fa",
    "rus": "ru", "san": "sa", "srp": "sr", "tam": "ta", "tel": "te",
    "tgk": "tg", "tha": "th", "ukr": "uk", "urd": "ur", "zho": "zh",
}

CODE_SCRIPT_MAP = {
    "ara": "perso-arabic", "bel": "cyrillic", "ben": "indic", "bul": "cyrillic",
    "cmn": "ja_zh", "ell": "el", "fas": "perso-arabic", "guj": "indic",
    "hin": "indic", "jpn": "ja_zh", "kan": "indic", "kaz": "cyrillic",
    "kir": "cyrillic", "kor": "ko", "mar": "indic", "mkd": "cyrillic",
    "mon": "cyrillic", "nep": "indic", "pan": "indic", "pes": "perso-arabic",
    "rus": "cyrillic", "san": "indic", "srp": "cyrillic", "tam": "indic",
    "tel": "indic", "tgk": "cyrillic", "tha": "th", "ukr": "cyrillic",
    "urd": "perso-arabic", "zho": "ja_zh",
}


LANGUAGE_CLASSIFICATIONS = {
    "arabic": ["ar", "fa", "ur"],
    "cyrillic": ["be", "bg", "kk", "ky", "mk", "mn", "ru", "sr", "tg", "uk"],
    "indic": ["bn", "gu", "hi", "kn", "mr", "ne", "pa", "ta", "te"],
    "eastern_slavic": ["be", "ru", "uk"],
    "southern_slavic": ["bg", "mk", "sr"],
    "turkic": ["kk", "ky", "mn", "tg"],
    "ja_zh": ["ja", "zh"],
}

DATASET_NAMES = [
    "family", "perso_arabic", "cyrillic", "indic", "ja_zh",
    "eastern_slavic", "southern_slavic", "turkic",
]


def initialize_datasets() -> Dict[str, List]:
    """Initialize empty datasets for all categories."""
    datasets = {}
    for datatype in DATASET_NAMES:
        datasets[f"{datatype}_word_data"] = []
        datasets[f"{datatype}_labels"] = []
    return datasets


def load_training_data(file_path: Path) -> pd.DataFrame:
    """
    Load training data from CSV file.
    
    Args:
        file_path: Path to the training data file
        
    Returns:
        DataFrame containing the training data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        pd.errors.EmptyDataError: If file is empty
    """
    try:
        return pd.read_csv(
            file_path, 
            sep="\t", 
            header=None, 
            quoting=csv.QUOTE_NONE, 
            usecols=["rank", "text", "occurrences"]
        )
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except pd.errors.EmptyDataError:
        logger.error(f"Empty file: {file_path}")
        raise

def filter_non_script_text(df: pd.DataFrame) -> np.ndarray:
    """
    Filter out text that does not contain untransliterated script.
    
    Args:
        df: DataFrame containing the training data
    
    Returns:
        np.ndarray containing the filtered text
    """
    return np.array(
        df["text"][
            ~df["text"].astype(str).apply(lambda s: bool(EXCLUDE_PATTERN.match(s)))
        ]
    )

def filter_japanese_marks(text: np.ndarray) -> np.ndarray:
    """
   Filters out text that contains Japanese marks.
    
    Args:
        text: np.ndarray containing the text from the training data filtered to remove non-script text
        
    Returns:
        np.ndarray containing the filtered text
    """
    return np.array(
        [s for s in text if not KANA_OR_JAPANESE_MARKS.search(str(s))]
    )


def classify_language(language_code: str) -> list[str]:
    """
    Classify language into appropriate categories.
    
    Args:
        language_code: ISO language code
        
    Returns:
        Dictionary mapping category names to classification values
    """
    return [
        category
        for category, codes in LANGUAGE_CLASSIFICATIONS.items()
        if language_code in codes
    ]

def process_file(file_path: Path, datasets: Dict[str, List]) -> None:
    """
    Process a single file and update the datasets.
    
    Args:
        file_path: Path to the file to process
        datasets: Dictionary containing datasets to update
    """
    df_raw = load_training_data(file_path)

    file_prefix = file_path.name[:LANGUAGE_CODE_LENGTH]
    family_language_code = CODE_SCRIPT_MAP[file_prefix]
    language_code = CODE_LANGUAGE_MAP[file_prefix]
    
    file_text = filter_non_script_text(df_raw)

    if language_code == "ja":
        file_text = filter_japanese_marks(file_text)

    file_script_label = np.full(file_text.shape, family_language_code)
    file_language_label = np.full(file_text.shape, language_code)

    datasets["family_word_data"].extend(file_text)
    datasets["family_labels"].extend(file_script_label)

    for category in classify_language(language_code):
        datasets[f"{category}_word_data"].extend(file_text)
        datasets[f"{category}_labels"].extend(file_script_label if category == "cyrillic" else file_language_label)


def write_datasets(datasets: Dict[str, List], base: Path) -> None:
    """
    Write datasets to CSV files.
    
    Args:
        datasets: Dictionary containing datasets to write
        base: Base directory for output files
    """
    for datatype in DATASET_NAMES:
        logger.info(f"Constructing and writing {datatype} data frame to csv")
        pd.DataFrame(
            {
                "text": datasets[f"{datatype}_word_data"],
                "label": datasets[f"{datatype}_labels"],
            }
        ).to_csv(
            base / Path("data/intermediate") / f"ld_{datatype}_data.csv", index=False
        )
        logger.info("Write complete")

        del datasets[f"{datatype}_word_data"]
        del datasets[f"{datatype}_labels"]


def main():

    base = Path(__file__).resolve().parents[1]
    training_folder = base / Path("data/raw")

    datasets = initialize_datasets()


    for file_path in training_folder.iterdir():
        if file_path.suffix != ".txt":
            continue  # Skip unexpected files like .DS_Store

        logger.info("Processing %s", file_path.name)
        process_file(file_path, datasets)
    
    write_datasets(datasets, base)


if __name__ == "__main__":
    main()
