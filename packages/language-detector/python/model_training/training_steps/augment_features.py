#!/usr/bin/env python3
import sys, joblib, unicodedata, shutil, regex
import numpy as np
from numpy.typing import NDArray
import pandas as pd
from pathlib import Path
from scipy.sparse import csr_matrix, hstack
from typing import TypeAlias

USAGE = "Usage: python augment_features.py <data_group> <model_dir>"


# Type Definitions
BuildFeaturesReturn: TypeAlias = tuple[
    list[str],  # bigrams
    NDArray[np.float32],  # feature matrix
    list[dict[str, float]],  # per-group totals
]


tell_character_dict = {
    "perso_arabic": {
        "ar": list("ةىأإٱكي"),
        "fa": list("ۀ"),
        "ur": list("ٹڈڑےںھۓہے"),
        "overlapping": list("پچژگکی"),
    },
    "ja_zh": {
        "ja": list(
            "働込畑辻榊栃峠枠匂駅図経発鉄県斎歳圧緑検関総郷録帰覧剣続涙桜覚広辺対薬軽験"
            "冴畳匠酎丼塚尻曽冨畠鴨鰹匂圏喩麹渚峯"
        ),
        "zh": list(
            "这那为说谁还没发见观读书车门问间闻风电飞马鸟鱼线网级处张陈员优产币广"
            "國學體經讀圖綠鐵縣亞澤辭總鄉嚴覺櫻營續淚觀變醫臺"
            "仅从众优务兰关兴决刘况冲冻净减刘务刘刚创务刘务"
            "齊顏臟廳鬥雞"
        ),
        "radicals": list("氵扌艹言金"),
    },
    "eastern_slavic": {
        "be": list("ў"),
        "ru": list("ъыэё"),
        "uk": list("їєґ"),
        "overlapping": ["і"],
    },
    "southern_slavic": {
        "bg": list("ъщ"),
        "mk": list("ѓќѕ"),
        "sr": list("ђћљњџ"),
        "overlapping": ["ј"],
    },
    "turkik": {
        "kk": list("әұі"),
        "ky": [],  # no unique single-character tells
        "mn": [],  # no unique single-character tells
        "tg": list("ҷҳӣӯ"),
        "overlapping": list("ңүөһқғ"),
    },
    "indic": {
        "hi": list("क़ख़ग़ज़ड़ढ़फ़य़"),
        "mr": list("ळऱऑॲॅॉ"),
        "ne": [],  # no unique single-character tells
        "overlapping": ["़"],  # nukta
    },
}

endings_dict = {
    "indic": {
        "hi": ["पन", "ता", "कार", "वादी", "गर", "इया", "इन", "ई", "याँ", "यों"],
        "mr": ["णे", "तील", "चा", "ची", "चे", "ला", "ना", "कर", "वाला", "पणा"],
        "ne": ["हरु", "हरू", "को", "मा", "बाट", "लाई"],
    },
    "southern_slavic": {
        "bg": ["ът", "ия", "ево", "ово"],
        "mk": ["от", "ев", "ов", "ва"],
        "sr": ["ије", "ија", "има", "ама", "ска", "ски"],
        "overlapping": ["та", "то", "те"],
    },
}

bigrams_dict = {
    "southern_slavic": {
        "bg": ["ър", "ъл", "ън", "ът", "ят", "ще", "дж"],
        "mk": ["ќе", "ќи", "ќа", "ќу", "ѓе", "ѓи", "ѓа", "ѓу", "ѕв", "ѕд"],
        "sr": ["ће", "ћа", "ћу", "ћи", "ђа", "ђе", "ђу", "џв", "џа", "џе"],
    }
}

non_unique_keys = ["overlapping", "radicals"]


def build_character_binaries_array(
    texts: list, group_tell_chars: dict[str, list[str]]
) -> BuildFeaturesReturn:

    # Compile the list of tell characters for the data group from the dictionary above
    all_keys = list(group_tell_chars)
    tell_characters_set = set([c for k in all_keys for c in group_tell_chars[k]])
    tell_characters = sorted(tell_characters_set)

    character_binaries = np.zeros((len(texts), len(tell_characters)), dtype=np.float32)
    per_group_totals = []

    char_to_idx = {
        ch: j for j, ch in enumerate(tell_characters)
    }  # create a dictionary for looking up the index of each character in the tell_characters list

    for i, s in enumerate(texts):
        s = unicodedata.normalize("NFC", s)

        present_chars = (
            set(s) & tell_characters_set
        )  # a set containing only the tell_characters present in the current word

        for ch in present_chars:
            character_binaries[i, char_to_idx[ch]] = 1.0

        row_group_totals = {gr: 0.0 for gr in all_keys if gr not in non_unique_keys}
        for group in all_keys:
            if group in non_unique_keys:
                continue

            total = 0

            for char in group_tell_chars[group]:
                total += s.count(char)

            row_group_totals[group] = float(total)
        per_group_totals.append(row_group_totals)

    return tell_characters, character_binaries, per_group_totals


def build_radical_counts_array(
    texts: list, group_tell_chars: dict[str, list[str]]
) -> np.typing.NDArray[np.float32] | None:
    # For ja_zh group, add radical count features if "radicals" key exists
    radical_counts = None
    if "radicals" in group_tell_chars:
        radicals = group_tell_chars["radicals"]
        print(f"Building {len(radicals)} radical count features…")
        radical_counts = np.zeros((len(texts), len(radicals)), dtype=np.float32)
        for i, s in enumerate(texts):
            s = unicodedata.normalize("NFC", s)
            for j, rad in enumerate(radicals):
                radical_counts[i, j] = float(s.count(rad))

    return radical_counts


def build_ending_features_array(
    texts: list, group_endings: dict[str, list[str]] | None
) -> BuildFeaturesReturn | tuple[None, None, None]:
    if group_endings is None:
        return None, None, None

    # Compile the list of endings for the data group from the dictionary above
    all_keys = list(group_endings)
    endings = sorted(set([e for k in all_keys for e in group_endings[k]]))

    end_to_idx = {end: j for j, end in enumerate(endings)}

    end_len = len(endings)
    txt_len = len(texts)

    endings_features = np.zeros((txt_len, end_len * 2), dtype=np.float32)
    per_group_totals = []

    for row, s in enumerate(texts):
        s = unicodedata.normalize("NFC", s)
        cleaned = regex.sub(r"[\p{P}\p{S}]+", " ", s)
        cleaned = regex.sub(r"\s+", " ", cleaned).strip()
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

        row_group_totals = {gr: 0.0 for gr in all_keys if gr not in non_unique_keys}
        for group in all_keys:
            if group in non_unique_keys:
                continue

            total = 0.0
            for e in group_endings[group]:

                for w in words:
                    if w.endswith(e):
                        total += 1
            row_group_totals[group] = float(total)
        per_group_totals.append(row_group_totals)

    return endings, endings_features, per_group_totals


def build_bigram_features_array(
    texts: list, group_bigrams: dict[str, list[str]] | None
) -> BuildFeaturesReturn | tuple[None, None, None]:
    if group_bigrams is None:
        return None, None, None

    # Compile the list of bigrams for the data group from the dictionary above
    all_keys = list(group_bigrams)
    bigrams = sorted(set([b for k in all_keys for b in group_bigrams[k]]))

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

        row_group_totals = {gr: 0.0 for gr in all_keys if gr not in non_unique_keys}
        for group in all_keys:
            if group in non_unique_keys:
                continue

            for bi in group_bigrams[group]:
                row_group_totals[group] += float(s.count(bi))

        per_group_totals.append(row_group_totals)

    return bigrams, bigram_features, per_group_totals


def build_tell_scores_array(
    texts: list[str],
    char_group_totals: list[dict[str, float]],
    ending_group_totals: list[dict[str, float]] | None,
    bigram_group_totals: list[dict[str, float]] | None,
) -> np.typing.NDArray[np.float32]:

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


def main(data_group: str, model_dir: str):
    model_assets = Path(model_dir)
    base = Path(__file__).resolve().parents[1]
    vec_path = (
        base
        / Path("data/processed/vectorized")
        / f"ld_vectorized_{data_group}_data.joblib"
    )
    csv_path = base / Path("data/intermediate") / f"ld_balanced_{data_group}_data.csv"

    if data_group in ["family", "cyrillic"]:
        print(f"No augmentation necessary for {data_group}")
        shutil.copy2(
            vec_path,
            base
            / Path("data/processed/augmented")
            / f"ld_augmented_{data_group}_data.joblib",
        )
        return

    print(f"Loading vectorized data: {vec_path}")
    X, y = joblib.load(vec_path)

    print(f"Loading raw tokens for alignment: {csv_path}")

    df = pd.read_csv(csv_path, usecols=["text", "label"])

    if len(df) != X.shape[0]:
        raise RuntimeError(
            f"Row count mismatch between CSV ({len(df)}) and X ({X.shape[0]}). "
            "Make sure this runs right after vectorize_data.py, before split_data.py."
        )

    group_tell_chars = tell_character_dict[data_group]

    group_endings = None
    if data_group in endings_dict:
        group_endings = endings_dict[data_group]

    group_bigrams = None
    if data_group in bigrams_dict:
        group_bigrams = bigrams_dict[data_group]

    texts = df["text"].astype(str).tolist()
    lctexts = list(map(lambda s: s.casefold(), texts))

    # Add binary columns to each word's vector matrix for each of the unique characters that can help distinguish between languages
    print(f"Building tell-letter binary features…")
    tell_characters, character_binaries, char_group_totals = (
        build_character_binaries_array(lctexts, group_tell_chars)
    )

    # Add columns to each word's vector matrix for the number of radicals present (currently ja_zh only)
    print(f"Building radical count features…")
    radical_counts = build_radical_counts_array(lctexts, group_tell_chars)

    # Add binary and count columns to each word's vector matrix for the presence of special word endings (currently indic and south_slavic only)
    print(f"Building ending binary and count features…")
    endings, ending_features, ending_group_totals = build_ending_features_array(
        lctexts, group_endings
    )

    # Add binary and count columns to each word's vector matrix for the presence of special bigrams (currently south_slavic only)
    print(f"Building bigram binary and count features…")
    bigrams, bigram_features, bigram_group_totals = build_bigram_features_array(
        lctexts, group_bigrams
    )

    # Add tells score to each word's vector matrix for the total number of tells present
    print(f"Building per-group tells scores")
    tells_scores = build_tell_scores_array(
        lctexts, char_group_totals, ending_group_totals, bigram_group_totals
    )

    # Stack all features
    feature_blocks = [X, csr_matrix(character_binaries) * 1.5]
    feature_blocks.append(csr_matrix(tells_scores) * 0.5)
    if radical_counts is not None:
        feature_blocks.append(csr_matrix(radical_counts) * 1.0)
    if ending_features is not None:
        feature_blocks.append(csr_matrix(ending_features) * 2.0)
    if bigram_features is not None:
        feature_blocks.append(csr_matrix(bigram_features) * 2.0)
    X_aug = hstack(feature_blocks, format="csr")

    print(f"Augmented features: {X.shape[1]} -> {X_aug.shape[1]} columns.")
    joblib.dump(
        (X_aug, y),
        base
        / Path("data/processed/augmented")
        / f"ld_augmented_{data_group}_data.joblib",
    )
    joblib.dump(
        {"tell_characters": tell_characters, "endings": endings, "bigrams": bigrams},
        model_assets / f"ld_{data_group}_tell_lists.joblib",
    )
    print("[augment] Write complete")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(USAGE)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
