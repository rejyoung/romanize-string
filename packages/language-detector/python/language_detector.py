"""
Language detection module using trained ensemble models.

This model was trained using corpora provided by the Wortschatz Project
(University of Leipzig), licensed under CC BY 4.0.

Source: https://wortschatz.uni-leipzig.de/en/download
License: https://creativecommons.org/licenses/by/4.0/
"""

import os
import sys
from pathlib import Path

import joblib
import regex
from scipy.sparse import hstack
from sklearn.ensemble import VotingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

# Disable logging in utility files when used by npm plugin
os.environ['DISABLE_LOGGING'] = '1'

from definitions.language_codes import Code_Language
from utils.build_extended_features_block import build_extended_features_block

# Constants
HERE = Path(__file__).resolve().parent
MODEL_ASSETS = HERE / "model_assets"
KANA_OR_JAPANESE_MARKS = regex.compile(r"[\u3040-\u30ff\u31f0-\u31ff\uff66-\uff9f]")


def detect_language(string: str) -> Code_Language:
    """
    Detect the language of a given string.
    
    Args:
        string: The string to detect the language of
        
    Returns:
        The language of the input string
        
    Raises:
        ValueError: If input string is empty or invalid
        Exception: If language detection fails
    """
    if not string or not string.strip():
        raise ValueError("Input string cannot be empty")
    
    # Quick check for Japanese/Korean characters
    if KANA_OR_JAPANESE_MARKS.search(string):
        return "ja"


    # First, determine the language family
    family = evaluate_input(string, "family")

    # Route to specific family models
    if family in ["el", "ko"]:
        return family
    elif family == "indic":
        return evaluate_input(string, "indic")
    elif family == "ja_zh":
        return evaluate_input(string, "ja_zh")
    elif family == "perso-arabic":
        return evaluate_input(string, "perso_arabic")
    elif family == "cyrillic":
        cyrillic_family = evaluate_input(string, "cyrillic")

        if cyrillic_family == "southern_cyrillic":
            return evaluate_input(string, "southern_cyrillic")
        elif cyrillic_family == "eastern_cyrillic":
            return evaluate_input(string, "eastern_cyrillic")
        else:
            return evaluate_input(string, "turkic")
    else:
        return family


def load_tools(model_type: str) -> tuple[TfidfVectorizer, VotingClassifier]:
    """
    Load the vectorizer and model for a given model type.
    
    Args:
        model_type: The type of model to load the tools for
        
    Returns:
        A tuple containing the vectorizer and model
        
    Raises:
        FileNotFoundError: If model files are not found
        Exception: If loading fails
    """
    try:
        vectorizer_file = MODEL_ASSETS / "vectorizers" / f"ld_{model_type}_vectorizer.joblib"
        model_file = MODEL_ASSETS / "models" / f"ld_{model_type}_ensemble_model.joblib"
        
        if not vectorizer_file.exists():
            raise FileNotFoundError(f"Vectorizer file not found: {vectorizer_file}")
        if not model_file.exists():
            raise FileNotFoundError(f"Model file not found: {model_file}")
            
        vectorizer = joblib.load(vectorizer_file)
        model = joblib.load(model_file)
        
        return vectorizer, model
        
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Model files not found for {model_type}: {e}")
    except Exception as e:
        raise Exception(f"Failed to load tools for {model_type}: {e}")


def evaluate_input(string: str, model_type: str) -> str:
    """
    Evaluate the input string for a given model type.
    
    Args:
        string: The string to evaluate
        model_type: The type of model to evaluate the input for
        
    Returns:
        The predicted language of the input string
        
    Raises:
        Exception: If evaluation fails
    """
    try:
        vectorizer, model = load_tools(model_type)

        # Transform input text
        X_base = vectorizer.transform([string])
        X_ext = build_extended_features_block([string], model_type)

        # Ensure consistent data types
        if X_ext.dtype != X_base.dtype:
            X_ext = X_ext.astype(X_base.dtype, copy=False)

        # Combine base and extended features
        X_aug = hstack([X_base, X_ext], format="csr")

        # Make prediction
        result = model.predict(X_aug)[0]
        
        return result
        
    except Exception as e:
        raise Exception(f"Evaluation failed for {model_type}: {e}")


def main() -> None:
    """Main entry point for command line usage."""
    if len(sys.argv) != 2:
        raise ValueError("Usage: python language_detector.py <input>")

    string = sys.argv[1]
    
    try:
        result = detect_language(string)
        print(result)
    except Exception as e:
        raise Exception(f"Language detection failed: {e}")


if __name__ == "__main__":
    main()

