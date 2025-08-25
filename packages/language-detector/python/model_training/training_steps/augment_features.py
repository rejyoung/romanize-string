#!/usr/bin/env python3
import sys, joblib, shutil
import pandas as pd
from pathlib import Path
from scipy.sparse import csr_matrix, hstack


USAGE = "Usage: python augment_features.py <data_group> <model_dir>"








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


    texts = df["text"].astype(str).tolist()
    



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
