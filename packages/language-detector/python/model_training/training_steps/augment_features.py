#!/usr/bin/env python3
import sys, joblib, unicodedata, shutil, regex
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.sparse import csr_matrix, hstack
from typing import Tuple

USAGE = "Usage: python augment_features.py <data_group> <model_dir>"


tell_character_dict = {
    "perso_arabic": {
        "ar": list("ةىأإٱكي"),
        "fa": list("ۀ"),
        "ur": list("ٹڈڑےںھۓہے"),
        "non_ar_hints": list("پچژگکی"),
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
        "be": list("ўі"),
        "ru": list("ъыэё"),
        "uk": list("іїєґ"),
    },
    "southern_slavic": {
        "bg": list("ъщ"),
        "mk": list("ѓќѕј"),
        "sr": list("ђћљњџј"),
    },
    "turkik": {
        "kk": list("әғқңұүһі"),
        "ky": list("ңөү"),
        "mn": list("өүңһ"),  # give MN some help (not perfectly unique, still useful)
        "tg": list("ҷҳӣӯғқ"),
    },
    "indic": {  # tells to distinguish devanagari-based languages
        "hi": list("क़ख़ग़ज़ड़ढ़फ़य़"),
        "nukta": ["़"],
        "mr": list("ळऱऑॲॅॉ"),
        "ne": [],  # no unique single-letter tells
    },
}

endings_dict = {
    "indic": {
        "hi": ["पन", "ता", "कार", "वादी", "गर", "इया", "इन", "ई", "याँ", "यों"],
        "mr": ["णे", "तील", "चा", "ची", "चे", "ला", "ना", "कर", "वाला", "पणा"],
        "ne": ["हरु", "हरू", "को", "मा", "बाट", "लाई"],
    },
    "southern_slavic": {
        "bg": ["ът", "та", "то", "те", "ия", "ево", "ово"],
        "mk": ["от", "та", "то", "те", "ев", "ов", "ва"],
        "sr": ["ије", "ија", "има", "ама", "ска", "ски"],
    },
}

bigrams_dict = {
    "southern_slavic": {
        "bg": ["ър", "ъл", "ън", "ът", "ят", "ще", "дж"],
        "mk": ["ќе", "ќи", "ќа", "ќу", "ѓе", "ѓи", "ѓа", "ѓу", "ѕв", "ѕд"],
        "sr": ["ће", "ћа", "ћу", "ћи", "ђа", "ђе", "ђу", "џв", "џа", "џе"]
    }
}


def build_character_binaries_array(
    texts: list, tell_characters: list, tell_characters_set: set
) -> np.typing.NDArray[np.float32]:

    character_binaries = np.zeros((len(texts), len(tell_characters)), dtype=np.float32)
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

    return character_binaries


def build_radical_counts_array(
    texts: list, group_tell_chars: list
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
                radical_counts[i, j] = s.count(rad)

    return radical_counts


def build_ending_features_array(
    texts: list, endings: list | None
) -> np.typing.NDArray[np.float32] | None:
    endings_features = None
    if endings is not None:
        end_to_idx = {end: j for j, end in enumerate(endings)}

        end_len = len(endings)
        txt_len = len(texts)

        endings_features = np.zeros((txt_len, end_len * 2), dtype=np.float32)

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
                    endings_features[row, count_col] = count

    return endings_features

def build_bigram_features_array(texts: list, bigrams: list | None) -> np.typing.NDArray[np.float32] | None:
    bigram_features = None

    if (bigrams is not None):
        bigram_to_idx = {bi: i for i, bi in enumerate(bigrams)}
        bi_len = len(bigrams)
        txt_len = len(texts)

        bigram_features = np.zeros((txt_len, bi_len * 2), dtype=np.float32)

        for row, s in enumerate(texts):
            s = unicodedata.normalize("NFC", s)
            words = s.split()

            for bigram in bigrams:
                
                count = 0.0

                for w in words:
                    count += w.count(bigram)

                if count > 0:
                    present_col = bigram_to_idx[bigram]
                    count_col = present_col + bi_len

                    bigram_features[row, present_col] = 1.0
                    bigram_features[row, count_col] = count
    
    return bigram_features


def main(data_group: str, model_dir: str):
    model_assets = Path(model_dir)
    vec_path = (
        Path("data/processed/vectorized") / f"ld_vectorized_{data_group}_data.joblib"
    )
    csv_path = Path("data/intermediate") / f"ld_balanced_{data_group}_data.csv"

    if data_group in ["family", "cyrillic"]:
        print(f"No augmentation necessary for {data_group}")
        shutil.copy2(
            vec_path,
            Path("data/processed/augmented") / f"ld_augmented_{data_group}_data.joblib",
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

    # Compile the list of tell characters for the data group from the dictionary above
    group_tell_chars = tell_character_dict[data_group]
    keys = list(group_tell_chars)
    tell_characters_set = set([c for k in keys for c in group_tell_chars[k]])
    tell_characters = sorted(tell_characters_set)

    # Compile the list of endings for the data group from the dictionary above
    endings = None
    if data_group in endings_dict:
        group_endings = endings_dict[data_group]
        keys = list(group_endings)
        endings = sorted(set([e for k in keys for e in group_endings[k]]))

    # Compile the list of bigrams for the data group from the dictionary above
    bigrams = None
    if data_group in bigrams_dict:
        group_bigrams = bigrams_dict[data_group]
        keys = list(group_bigrams)
        bigrams = sorted(set([b for k in keys for b in group_bigrams[k]]))

    texts = df["text"].astype(str).tolist()
    lctexts = list(map(lambda s: s.lower(), texts))

    # Add binary columns to each word's vector matrix for each of the unique characters that can help distinguish between languages
    print(f"Building tell-letter binary features…")
    character_binaries = build_character_binaries_array(
        lctexts, tell_characters, tell_characters_set
    )

    # Add columns to each word's vector matrix for the number of radicals present (currently ja_zh only)
    print(f"Building radical count features…")
    radical_counts = build_radical_counts_array(lctexts, group_tell_chars)

    # Add binary and count columns to each word's vector matrix for the presence of special word endings (currently indic and south_slavic only)
    print(f"Building ending binary and count features…")
    ending_features = build_ending_features_array(lctexts, endings)

    # Add binary and count columns to each word's vector matrix for the presence of special bigrams (currently south_slavic only)
    print(f"Building bigram binary and count features…")
    bigram_features = build_bigram_features_array(lctexts, bigrams)

    # Stack all features
    feature_blocks = [X, csr_matrix(character_binaries)]
    if radical_counts is not None:
        feature_blocks.append(csr_matrix(radical_counts))
    if ending_features is not None:
        feature_blocks.append(csr_matrix(ending_features))
    if bigram_features is not None:
        feature_blocks.append(csr_matrix(bigram_features))
    X_aug = hstack(feature_blocks, format="csr")

    print(f"Augmented features: {X.shape[1]} -> {X_aug.shape[1]} columns.")
    joblib.dump(
        (X_aug, y),
        Path("data/processed/augmented") / f"ld_augmented_{data_group}_data.joblib",
    )
    joblib.dump(tell_characters, model_assets / f"ld_{data_group}_tellchars.joblib")
    if endings is not None:
        joblib.dump(endings, model_assets / f"ld_{data_group}_endings.joblib")
    print("[augment] Write complete")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(USAGE)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
