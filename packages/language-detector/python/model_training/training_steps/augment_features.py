#!/usr/bin/env python3
import sys, joblib, unicodedata, shutil
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.sparse import csr_matrix, hstack

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
        ),
        "zh": list(
            "这那为说谁还没发见观读书车门问间闻风电飞马鸟鱼线网级处张陈员优产币广"
            "國學體經讀圖綠鐵縣亞澤辭總鄉嚴覺櫻營續淚觀變醫臺"
        ),
    },
    "eastern_slavic": {
        "be": list("ўі"),
        "ru": list("ъыэё"),
        "uk": list("іїєґ"),
    },
    "southern_slavic": {
        "bg": list("ъщ"),
        "mk": list("ѓќѕ"),
        "sr": list("ђћ"),
    },
    "turkik": {
        "kk": list("әғқңұүһі"),
        "ky": list("ңөү"),
        "mn": [],  # no unique single-letter tells
        "tg": list("ҷҳӣӯғқ"),
    },
    "indic": {  # tells to distinguish devanagari-based languages
        "hi": list("क़ख़ग़ज़ड़ढ़फ़य़"),
        "nukta": ["़"],
        "mr": list("ळऱऑॲॅॉ"),
        "ne": [],  # no unique single-letter tells
    },
}


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
    tell_characters = [c for k in keys for c in group_tell_chars[k]]
    tell_set = set(tell_characters)

    # Add columns to each word's vector matrix for each of the unique characters that can help distinguish between languages
    print(f"Building {len(tell_characters)} tell-letter binary features…")
    texts = df["text"].astype(str).tolist()
    arr = np.zeros((len(texts), len(tell_characters)), dtype=np.float32)

    for i, s in enumerate(texts):
        s = unicodedata.normalize("NFC", s)
        char_to_idx = {
            ch: j for j, ch in enumerate(tell_characters)
        }  # create a dictionary for looking up the index of each character in the tell_characters list

        present_chars = (
            set(s) & tell_set
        )  # a set containing only the tell_characters present in the current word

        for ch in present_chars:
            arr[i, char_to_idx[ch]] = 1.0

    X_aug = hstack([X, csr_matrix(arr)], format="csr")

    print(f"Augmented features: {X.shape[1]} -> {X_aug.shape[1]} columns.")
    joblib.dump(
        (X_aug, y),
        Path("data/processed/augmented") / f"ld_augmented_{data_group}_data.joblib",
    )
    joblib.dump(tell_characters, model_assets / f"ld_{data_group}_tellchars.joblib")
    print("[augment] Write complete")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(USAGE)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
