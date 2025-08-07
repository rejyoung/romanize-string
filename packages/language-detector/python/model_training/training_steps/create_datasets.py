import pandas as pd
import numpy as np
import regex, csv
from pathlib import Path

"""
This model was trained using corpora provided by the Wortschatz Project
(University of Leipzig), licensed under CC BY 4.0.

Source: https://wortschatz.uni-leipzig.de/en/download
License: https://creativecommons.org/licenses/by/4.0/
"""

code_language_map = {
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
    "zho": "zh",
}

code_script_map = {
    "ara": "ar",
    "bel": "cy",
    "ben": "in",
    "bul": "cy",
    "cmn": "zh",
    "ell": "el",
    "fas": "ar",
    "guj": "in",
    "hin": "in",
    "jpn": "ja",
    "kan": "in",
    "kaz": "cy",
    "kir": "cy",
    "kor": "ko",
    "mar": "in",
    "mkd": "cy",
    "mon": "cy",
    "nep": "in",
    "pan": "in",
    "pes": "ar",
    "rus": "cy",
    "san": "in",
    "srp": "cy",
    "tam": "in",
    "tel": "in",
    "tgk": "cy",
    "tha": "th",
    "ukr": "cy",
    "urd": "ar",
    "zho": "zh",
}


arabic_classes = ["ar", "fa", "ur"]
cyrillic_classes = ["be", "bg", "kk", "ky", "mk", "mn", "ru", "sr", "tg", "uk"]
indic_classes = ["bn", "gu", "hi", "kn", "mr", "ne", "pa", "ta", "te"]


def main():

    training_folder = Path("data/raw")
    exclude_pattern = regex.compile(r"^[\p{Latin}\p{Nd}\p{P}\p{S}\p{Z}]+$")

    dataset_names = ["family", "ar", "cy", "in"]

    datasets = {
        new_key: new_val
        for datatype in dataset_names
        for new_key, new_val in (
            (f"{datatype}_word_data", []),
            (f"{datatype}_labels", []),
        )
    }

    for file_path in training_folder.iterdir():
        if file_path.suffix != ".txt":
            continue  # Skip unexpected files like .DS_Store

        print("Processing", file_path.name)
        family_language_code = code_script_map[file_path.name[:3]]
        language_code = code_language_map[file_path.name[:3]]

        df_raw = pd.read_csv(file_path, sep="\t", header=None, quoting=csv.QUOTE_NONE)

        # Make an np array out of the data in column 1 of the training data,
        # excluding any strings not containing untransliterated script
        file_x = np.array(
            df_raw[1][
                ~df_raw[1].astype(str).apply(lambda s: bool(exclude_pattern.match(s)))
            ]
        )
        file_y_script = np.full(file_x.shape, family_language_code)
        file_y_language = np.full(file_x.shape, language_code)

        datasets["family_word_data"].extend(file_x)
        datasets["family_labels"].extend(file_y_script)

        if language_code in arabic_classes:
            datasets["ar_word_data"].extend(file_x)
            datasets["ar_labels"].extend(file_y_language)
        elif language_code in cyrillic_classes:
            datasets["cy_word_data"].extend(file_x)
            datasets["cy_labels"].extend(file_y_language)
        elif language_code in indic_classes:
            datasets["in_word_data"].extend(file_x)
            datasets["in_labels"].extend(file_y_language)

    for datatype in dataset_names:

        print(f"Constructing and writing {datatype} data frame to csv")
        pd.DataFrame(
            {
                "text": datasets[f"{datatype}_word_data"],
                "label": datasets[f"{datatype}_labels"],
            }
        ).to_csv(Path("data/intermediate") / f"ld_{datatype}_data.csv", index=False)
        print("Write complete")

        del datasets[f"{datatype}_word_data"]
        del datasets[f"{datatype}_labels"]


if __name__ == "__main__":
    main()
