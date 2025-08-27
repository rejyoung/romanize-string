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
    "ara": "perso-arabic",
    "bel": "cyrillic",
    "ben": "indic",
    "bul": "cyrillic",
    "cmn": "ja_zh",
    "ell": "el",
    "fas": "perso-arabic",
    "guj": "indic",
    "hin": "indic",
    "jpn": "ja_zh",
    "kan": "indic",
    "kaz": "cyrillic",
    "kir": "cyrillic",
    "kor": "ko",
    "mar": "indic",
    "mkd": "cyrillic",
    "mon": "cyrillic",
    "nep": "indic",
    "pan": "indic",
    "pes": "perso-arabic",
    "rus": "cyrillic",
    "san": "indic",
    "srp": "cyrillic",
    "tam": "indic",
    "tel": "indic",
    "tgk": "cyrillic",
    "tha": "th",
    "ukr": "cyrillic",
    "urd": "perso-arabic",
    "zho": "ja_zh",
}


arabic_classes = ["ar", "fa", "ur"]
cyrillic_classes = ["be", "bg", "kk", "ky", "mk", "mn", "ru", "sr", "tg", "uk"]
indic_classes = ["bn", "gu", "hi", "kn", "mr", "ne", "pa", "ta", "te"]
eastern_slavic = ["be", "ru", "uk"]
southern_slavic = ["bg", "mk", "sr"]
turkic = ["kk", "ky", "mn", "tg"]


def main():

    base = Path(__file__).resolve().parents[1]
    training_folder = base / Path("data/raw")
    exclude_pattern = regex.compile(r"^[\p{Latin}\p{Nd}\p{P}\p{S}\p{Z}]+$")

    dataset_names = [
        "family",
        "perso_arabic",
        "cyrillic",
        "indic",
        "ja_zh",
        "eastern_slavic",
        "southern_slavic",
        "turkic",
    ]

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
        kana_or_japanese_marks = regex.compile(
            r"[\p{Script=Hiragana}\p{Script=Katakana}\u30FC\uFF70\u30FB\u3005]"
        )

        df_raw = pd.read_csv(file_path, sep="\t", header=None, quoting=csv.QUOTE_NONE)

        # Make an np array out of the data in column 1 of the training data,
        # excluding any strings not containing untransliterated script

        file_x = np.array(
            df_raw[1][
                ~df_raw[1].astype(str).apply(lambda s: bool(exclude_pattern.match(s)))
            ]
        )
        if language_code == "ja":
            file_x = np.array(
                [s for s in file_x if not kana_or_japanese_marks.search(str(s))]
            )

        file_y_script = np.full(file_x.shape, family_language_code)
        file_y_language = np.full(file_x.shape, language_code)

        datasets["family_word_data"].extend(file_x)
        datasets["family_labels"].extend(file_y_script)

        if language_code in arabic_classes:
            datasets["perso_arabic_word_data"].extend(file_x)
            datasets["perso_arabic_labels"].extend(file_y_language)
        elif language_code in indic_classes:
            datasets["indic_word_data"].extend(file_x)
            datasets["indic_labels"].extend(file_y_language)
        elif language_code in cyrillic_classes:
            datasets["cyrillic_word_data"].extend(file_x)

            if language_code in southern_slavic:
                datasets["southern_slavic_word_data"].extend(file_x)
                file_y_subfamily = np.full(file_x.shape, "southern_slavic")
                datasets["southern_slavic_labels"].extend(file_y_language)
            elif language_code in eastern_slavic:
                datasets["eastern_slavic_word_data"].extend(file_x)
                file_y_subfamily = np.full(file_x.shape, "eastern_slavic")
                datasets["eastern_slavic_labels"].extend(file_y_language)
            elif language_code in turkic:
                datasets["turkic_word_data"].extend(file_x)
                file_y_subfamily = np.full(file_x.shape, "turkic")
                datasets["turkic_labels"].extend(file_y_language)

            # Set Cyrillic labels to appropriate subfamily code
            datasets["cyrillic_labels"].extend(file_y_subfamily)
        elif language_code in ["ja", "zh"]:
            datasets["ja_zh_word_data"].extend(file_x)
            file_y_subfamily = np.full(file_x.shape, "ja_zh")
            datasets["ja_zh_labels"].extend(file_y_language)

    for datatype in dataset_names:

        print(f"Constructing and writing {datatype} data frame to csv")
        pd.DataFrame(
            {
                "text": datasets[f"{datatype}_word_data"],
                "label": datasets[f"{datatype}_labels"],
            }
        ).to_csv(
            base / Path("data/intermediate") / f"ld_{datatype}_data.csv", index=False
        )
        print("Write complete")

        del datasets[f"{datatype}_word_data"]
        del datasets[f"{datatype}_labels"]


if __name__ == "__main__":
    main()
