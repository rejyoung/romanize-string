import logging
import os
import regex
import unicodedata

import numpy as np
from numpy.typing import NDArray
from scipy.sparse import csr_matrix, hstack
from typing import TypeAlias

from utils.generate_or_retrieve_tell_lists import (
    generate_or_retrieve_tell_lists,
    Generate_List_Return,
    Radical_List_Return,
    TellLists,
)

# Configure logging based on environment variable
if not os.environ.get('DISABLE_LOGGING'):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
else:
    # Create a no-op logger when logging is disabled
    logger = logging.getLogger(__name__)
    logger.disabled = True

# Type Definitions
FeatureArrayReturn: TypeAlias = (
    tuple[
        NDArray[np.float32],  # feature array
        list[dict[str, float]],  # per-group totals
    ]
    | tuple[None, None]
)

# Constants
NON_UNIQUE_KEYS = ["overlapping", "radicals"]
PUNCT_OR_SYMBOL = regex.compile(r"[\p{P}\p{S}]+")
MULTISPACE = regex.compile(r"\s+")


def build_extended_features_block(texts: list[str], model_type: str) -> csr_matrix:
    """
    Build an extended features block for a given model type.

    Args:
        texts: A list of texts to build the extended features block for
        model_type: The type of model to build the extended features block for

    Returns:
        A csr_matrix containing the extended features block
    """

    (
        character_binaries,
        radical_counts,
        ending_features,
        bigram_features,
        tells_scores,
    ) = build_extended_features_arrays(texts, model_type)

    weights = {
        "characters": 1.5,
        "tells_score": 0.5,
        "radicals": 1.0,
        "endings": 2.0,
        "bigrams": 2.0,
    }

    num_samples = len(texts)

    extended_feature_matrices = [
        prepare_feature_block(character_binaries, weights["characters"], num_samples),
        prepare_feature_block(radical_counts, weights["radicals"], num_samples),
        prepare_feature_block(ending_features, weights["endings"], num_samples),
        prepare_feature_block(bigram_features, weights["bigrams"], num_samples),
        prepare_feature_block(tells_scores, weights["tells_score"], num_samples),
    ]

    return hstack(extended_feature_matrices, format="csr")


# --- Helper to scale & safely convert arrays ---
def prepare_feature_block(feature_array: NDArray[np.float32] | None, scale: float, num_samples: int) -> csr_matrix:
    """
    Prepare a feature block for a given model type.

    Args:
        feature_array: The feature array to prepare
        scale: The scale to apply to the feature array
        num_samples: The number of samples in the feature array

    Returns:
        A csr_matrix containing the prepared feature block
    """

    if feature_array is None:
        return csr_matrix((num_samples, 0), dtype=np.float32)
    block = csr_matrix(feature_array, dtype=np.float32)
    return block * scale if scale != 1.0 else block


##### Generate all feature arrays #####
def build_extended_features_arrays(texts: list[str], model_type: str) -> tuple[
    NDArray[np.float32],
    NDArray[np.float32] | None,
    NDArray[np.float32] | None,
    NDArray[np.float32] | None,
    NDArray[np.float32],
]:
    """
    Build all feature arrays for a given model type.

    Args:
        texts: A list of texts to build the extended features block for
        model_type: The type of model to build the extended features block for

    Returns:
        A tuple containing the feature arrays for the given model type
    """
    tell_lists: TellLists = generate_or_retrieve_tell_lists(model_type)

    tell_character_lists = tell_lists["tell_character_list"]
    radical_lists = tell_lists["radical_lists"]
    ending_lists = tell_lists["ending_lists"]
    bigram_lists = tell_lists["bigram_lists"]
    lctexts = list(map(lambda s: s.casefold(), texts))

    # Add binary columns to each word's vector matrix for each of the unique characters that can help distinguish between languages
    logger.info("Building tell-letter binary features…")
    character_binaries, char_group_totals = build_character_binaries_array(
        lctexts, tell_character_lists
    )

    # Add columns to each word's vector matrix for the number of radicals present (currently ja_zh only)
    logger.info("Building radical count features…")
    radical_counts = build_radical_counts_array(lctexts, radical_lists)

    # Add binary and count columns to each word's vector matrix for the presence of special word endings (currently indic and south_slavic only)
    logger.info("Building ending binary and count features…")
    ending_features, ending_group_totals = build_ending_features_array(
        lctexts, ending_lists
    )

    # Add binary and count columns to each word's vector matrix for the presence of special bigrams (currently south_slavic only)
    logger.info("Building bigram binary and count features…")
    bigram_features, bigram_group_totals = build_bigram_features_array(
        lctexts, bigram_lists
    )

    # Add tells score to each word's vector matrix for the total number of tells present
    logger.info("Building per-group tells scores")
    tells_scores = build_tell_scores_array(
        lctexts, char_group_totals, ending_group_totals, bigram_group_totals
    )

    return (
        character_binaries,
        radical_counts,
        ending_features,
        bigram_features,
        tells_scores,
    )


##### Individual Array Generators #####


def build_character_binaries_array(
    texts: list[str], tell_character_list: Generate_List_Return
) -> FeatureArrayReturn:
    """
    Build a character binary array for a given model type.

    Args:
        texts: A list of texts to build the character binary array for
        tell_character_list: A tuple containing the tell character lists for the given model type

    Returns:
        A tuple containing the character binary array and the per-group totals
    """

    group_tell_chars, tell_characters, groups = tell_character_list
    tell_chars_set = set(tell_characters)

    character_binaries = np.zeros((len(texts), len(tell_characters)), dtype=np.float32)
    per_group_totals = []

    char_to_idx = {
        ch: j for j, ch in enumerate(tell_characters)
    }  # create a dictionary for looking up the index of each character in the tell_characters list

    for i, s in enumerate(texts):
        s = unicodedata.normalize("NFC", s)

        present_chars = (
            set(s) & tell_chars_set
        )  # a set containing only the tell_characters present in the current word

        for ch in present_chars:
            character_binaries[i, char_to_idx[ch]] = 1.0

        row_group_totals = {gr: 0.0 for gr in groups if gr not in NON_UNIQUE_KEYS}
        for group in groups:
            if group in NON_UNIQUE_KEYS:
                continue

            total = 0

            for char in group_tell_chars[group]:
                total += s.count(char)

            row_group_totals[group] = float(total)
        per_group_totals.append(row_group_totals)

    return character_binaries, per_group_totals


def build_radical_counts_array(
    texts: list[str], radical_lists: Radical_List_Return
) -> NDArray[np.float32] | None:
    """
    Build a radical count array for a given model type.

    Args:
        texts: A list of texts to build the radical count array for
        radical_lists: A tuple containing the radical lists for the given model type

    Returns:
        A numpy array containing the radical count features
    """
    group_tell_chars, radicals = radical_lists
    # For ja_zh group, add radical count features if "radicals" key exists
    radical_counts = None
    if radicals is not None:
        logger.info(f"Building {len(radicals)} radical count features…")
        radical_counts = np.zeros((len(texts), len(radicals)), dtype=np.float32)
        for i, s in enumerate(texts):
            s = unicodedata.normalize("NFC", s)
            for j, rad in enumerate(radicals):
                radical_counts[i, j] = float(s.count(rad))

    return radical_counts


def build_ending_features_array(
    texts: list[str], ending_lists: Generate_List_Return
) -> FeatureArrayReturn:
    """
    Build an ending features array for a given model type.

    Args:
        texts: A list of texts to build the ending features array for
        ending_lists: A tuple containing the ending lists for the given model type

    Returns:
        A tuple containing the ending features array and the per-group totals
    """

    group_endings, endings, ending_groups = ending_lists

    if group_endings is None:
        return None, None

    end_to_idx = {end: j for j, end in enumerate(endings)}

    end_len = len(endings)
    txt_len = len(texts)

    endings_features = np.zeros((txt_len, end_len * 2), dtype=np.float32)
    per_group_totals = []

    for row, s in enumerate(texts):
        s = unicodedata.normalize("NFC", s)
        cleaned = MULTISPACE.sub(" ", PUNCT_OR_SYMBOL.sub(" ", s)).strip()
        words = cleaned.split()

        for end in endings:

            count = 0.0

            for w in words:
                if w.endswith(end):
                    count += 1.0

            if count > 0:
                present_col = end_to_idx[end]
                count_col = present_col + end_len

                endings_features[row, present_col] = 1.0
                endings_features[row, count_col] = float(count)

        row_group_totals = {
            gr: 0.0 for gr in ending_groups if gr not in NON_UNIQUE_KEYS
        }
        for group in ending_groups:
            if group in NON_UNIQUE_KEYS:
                continue

            total = 0.0
            for e in group_endings[group]:

                for w in words:
                    if w.endswith(e):
                        total += 1
            row_group_totals[group] = float(total)
        per_group_totals.append(row_group_totals)

    return endings_features, per_group_totals


def build_bigram_features_array(
    texts: list[str], bigram_lists: Generate_List_Return
) -> FeatureArrayReturn:
    """
    Build a bigram features array for a given model type.

    Args:
        texts: A list of texts to build the bigram features array for
        bigram_lists: A tuple containing the bigram lists for the given model type

    Returns:
        A tuple containing the bigram features array and the per-group totals
    """

    group_bigrams, bigrams, bigram_groups = bigram_lists

    if group_bigrams is None:
        return None, None

    bigram_to_idx = {bi: i for i, bi in enumerate(bigrams)}
    bi_len = len(bigrams)
    txt_len = len(texts)

    bigram_features = np.zeros((txt_len, bi_len * 2), dtype=np.float32)
    per_group_totals = []

    for row, s in enumerate(texts):
        s = unicodedata.normalize("NFC", s)

        for bigram in bigrams:

            count = s.count(bigram)

            if count > 0:
                present_col = bigram_to_idx[bigram]
                count_col = present_col + bi_len

                bigram_features[row, present_col] = 1.0
                bigram_features[row, count_col] = float(count)

        row_group_totals = {
            gr: 0.0 for gr in bigram_groups if gr not in NON_UNIQUE_KEYS
        }
        for group in bigram_groups:
            if group in NON_UNIQUE_KEYS:
                continue

            for bi in group_bigrams[group]:
                row_group_totals[group] += float(s.count(bi))

        per_group_totals.append(row_group_totals)

    return bigram_features, per_group_totals


def build_tell_scores_array(
    texts: list[str],
    char_group_totals: list[dict[str, float]],
    ending_group_totals: list[dict[str, float]] | None,
    bigram_group_totals: list[dict[str, float]] | None,
) -> NDArray[np.float32]:
    """
    Build a tell scores array for a given model type.

    Args:
        texts: A list of texts to build the tell scores array for
        char_group_totals: A list of dictionaries containing the character group totals
        ending_group_totals: A list of dictionaries containing the ending group totals
        bigram_group_totals: A list of dictionaries containing the bigram group totals

    Returns:
        A numpy array containing the tell scores features
    """

    texts_len = len(texts)

    groups = sorted(char_group_totals[0].keys())
    tell_scores = np.zeros((texts_len, len(groups)), dtype=np.float32)

    if char_group_totals is not None and texts_len != len(char_group_totals):
        raise RuntimeError(
            f"Row count mismatch between texts ({texts_len}) and char_group_totals ({len(char_group_totals)}). "
        )

    if ending_group_totals is not None and texts_len != len(ending_group_totals):
        raise RuntimeError(
            f"Row count mismatch between texts ({texts_len}) and ending_group_totals ({len(ending_group_totals)}). "
        )

    if bigram_group_totals is not None and texts_len != len(bigram_group_totals):
        raise RuntimeError(
            f"Row count mismatch between texts ({texts_len}) and bigram_group_totals ({len(bigram_group_totals)}). "
        )

    for row, s in enumerate(texts):
        str_len = max(1, len(s))

        char_row = char_group_totals[row]
        end_row = ending_group_totals[row] if ending_group_totals is not None else None
        bi_row = bigram_group_totals[row] if bigram_group_totals is not None else None

        for j, g in enumerate(groups):

            total = char_row.get(g, 0.0)

            if end_row is not None:
                total += end_row.get(g, 0.0)

            if bi_row is not None:
                total += bi_row.get(g, 0.0)

            tell_scores[row, j] = float(total / str_len)

    # Clip extreme counts to reduce outlier impact
    np.clip(tell_scores, 0, 4, out=tell_scores)

    # Damp growth for high counts — helps Cyrillic where tells can pile up
    tell_scores = np.sqrt(tell_scores)

    return tell_scores
