import pandas as pd
import numpy as np
import regex
import csv
from sklearn.utils import resample
from pathlib import Path
import gc

"""
This model was trained using corpora provided by the Wortschatz Project
(University of Leipzig), licensed under CC BY 4.0.

Source: https://wortschatz.uni-leipzig.de/en/download
License: https://creativecommons.org/licenses/by/4.0/
"""

code_map = {
    "ara": "ar",
    "bel": "be",
    "ben": "bn",
    "bul": "bg",
    "cmn": "zh",
    "ell": "el",
    "fas": "fa",
    "guj": "gu",
    "hin": "hi",
    "jpn": "ja",
    "kan": "kn",
    "kaz": "kk",
    "kir": "ky",
    "kor": "ko",
    "mar": "mr",
    "mkd": "mk",
    "mon": "mn",
    "nep": "ne",
    "pan": "pa",
    "pes": "fa",
    "rus": "ru",
    "san": "sa",
    "srp": "sr",
    "tam": "ta",
    "tel": "te",
    "tgk": "tg",
    "tha": "th",
    "ukr": "uk",
    "urd": "ur",
    "zho": "zh"
}

all_classes = sorted(set(code_map.values()))

training_folder = Path("training_data")
exclude_pattern = regex.compile(r'^[\p{Latin}\p{Nd}\p{P}\p{S}\p{Z}]+$')

word_data = []
language_codes = []

for file_path in training_folder.iterdir():
    if not file_path.name.endswith(".txt"):
        continue  # Skip unexpected files like .DS_Store

    print("Processing", file_path.name)
    language_code = code_map[file_path.name[:3]]
    data = pd.read_csv(file_path, sep="\t", header=None, quoting=csv.QUOTE_NONE)

    # Make an np array out of the data in column 1 of the training data, 
    # excluding any strings not containing untransliterated script
    file_x = np.array(data[1][~data[1].astype(str).apply(lambda s: bool(exclude_pattern.match(s)))])
    file_y = np.full(file_x.shape, language_code)


    word_data.extend(file_x)
    language_codes.extend(file_y)



df = pd.DataFrame({'text': word_data, 'label': language_codes})

word_data = language_codes = None
gc.collect()

grouped = df.groupby('label')
df = None
gc.collect()

MIN_SIZE = 500_000
MAX_SIZE = 3_000_000

print("Balancing data")

balanced_groups = []
for label, group in grouped:
    n = len(group)
    if n < MIN_SIZE:
        resampled = resample(group, replace=True, n_samples=MIN_SIZE, random_state=42)
    elif n > MAX_SIZE:
        resampled = group.sample(n=MAX_SIZE, random_state=42)
    else: 
        resampled = group
    balanced_groups.append(resampled)

del grouped; grouped = None
gc.collect()

balanced_df = pd.concat(balanced_groups).sample(frac=1, random_state=42)

print("Writing data to csv")
balanced_df.to_csv("ld_balanced_data.csv", index=False)
print("Write complete")