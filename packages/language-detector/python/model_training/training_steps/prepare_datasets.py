import pandas as pd
import sys, gc
from sklearn.utils import resample
from pathlib import Path


THRESHOLDS = {
    "family": (500_000, 3_000_000),
    "perso_arabic": (2_120_000, 4_300_000),
    "cyrillic": (1_000_000, 3_000_000),
    "indic": (530_000, 3_600_000),
    "eastern_slavic": (500_000, 1_000_000),
    "southern_slavic": (500_000, 1_000_000),
    "turkik": (500_000, 1_000_000),
    "ja_zh": (1_000_000, 2_000_000),
}


def main(data_group: str):

    MIN_SIZE, MAX_SIZE = THRESHOLDS[data_group]

    print(f"Reading {data_group} data")
    df = pd.read_csv(Path("data/intermediate") / f"ld_{data_group}_data.csv")

    grouped = df.groupby("label")
    del df
    df = None
    gc.collect()

    print("Balancing data")

    balanced_groups = []
    for label, group in grouped:
        n = len(group)
        if n < MIN_SIZE:
            print(f"Up-sampling {label}")
            resampled = resample(
                group, replace=True, n_samples=MIN_SIZE, random_state=42
            )
        elif n > MAX_SIZE:
            print(f"Down-sampling {label}")
            resampled = group.sample(n=MAX_SIZE, random_state=42)
        else:
            print(f"{label} is already balanced")
            resampled = group
        balanced_groups.append(resampled)

    del grouped
    grouped = None
    gc.collect()

    balanced_df = pd.concat(balanced_groups).sample(frac=1, random_state=42)

    print(f"Writing {data_group} data to csv")
    balanced_df.to_csv(
        Path("data/intermediate") / f"ld_balanced_{data_group}_data.csv",
        index=False,
    )
    print("Write complete")


if __name__ == "__main__":
    # Get arg
    if len(sys.argv) != 2:
        print("Usage: python prepare_datasets.py <data_group>")
        sys.exit(1)

    data_group = sys.argv[1]

    main(data_group)
