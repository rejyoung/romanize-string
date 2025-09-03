from typing import TypeAlias, TypedDict
from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent  # /python
TELL_LISTS_DIR = BASE_DIR / "model_assets" / "tell_lists"

# Type Definitions
Generate_List_Return: TypeAlias = (
    tuple[
        dict[str, tuple[str, ...]], tuple[str, ...], tuple[str, ...]
    ]  # (group_map, items, groups)
    | tuple[None, None, None]
)

Radical_List_Return: TypeAlias = (
    tuple[dict[str, tuple[str, ...]], tuple[str, ...]] | tuple[None, None]
)


class TellLists(TypedDict):
    tell_character_list: Generate_List_Return
    radical_lists: Radical_List_Return
    ending_lists: Generate_List_Return
    bigram_lists: Generate_List_Return


def generate_or_retrieve_tell_lists(model_type: str) -> TellLists:
    """
    Generate or retrieve tell lists for a given model type.

    Args:
        model_type: Type of model to generate tell lists for

    Returns:
        TellLists: A dictionary containing the tell lists for the given model type  
    """

    ## Load tell lists or generate new tell lists if file is not found
    filepath = TELL_LISTS_DIR / f"ld_{model_type}_tell_lists.joblib"
    filepath.parent.mkdir(parents=True, exist_ok=True)

    try:
        tell_lists: TellLists = joblib.load(filepath)
    except FileNotFoundError:
        group_tell_chars = tell_character_dict[model_type]
        group_endings = endings_dict.get(model_type)
        group_bigrams = bigrams_dict.get(model_type)

        tell_lists: TellLists = {
            "tell_character_list": generate_tell_char_lists(group_tell_chars),
            "radical_lists": generate_radical_lists(group_tell_chars),
            "ending_lists": generate_endings_lists(group_endings),
            "bigram_lists": generate_bigram_lists(group_bigrams),
        }

        joblib.dump(tell_lists, filepath)

    return tell_lists


###### Helper Functions ######


def generate_tell_char_lists(
    group_tell_chars: dict[str, tuple[str, ...]] | None,
) -> Generate_List_Return:
    """
    Generate tell character lists for a given model type.

    Args:
        group_tell_chars: A dictionary containing the tell characters for the given model type

    Returns:
        Generate_List_Return: A tuple containing the tell character lists for the given model type
    """
    if not group_tell_chars:
        raise ValueError("Input group_tell_chars cannot be None.")
    # Compile the list of tell characters for the data group from the dictionary above
    tell_char_groups = tuple(sorted(group_tell_chars))
    tell_characters_set = {c for g in tell_char_groups for c in group_tell_chars[g]}
    tell_characters = tuple(sorted(tell_characters_set))

    return group_tell_chars, tell_characters, tell_char_groups


def generate_radical_lists(
    group_tell_chars: dict[str, tuple[str, ...]] | None,
) -> Radical_List_Return:
    """
    Generate radical lists for a given model type.

    Args:
        group_tell_chars: A dictionary containing the tell characters for the given model type

    Returns:
        Radical_List_Return: A tuple containing the radical lists for the given model type
    """
    if not group_tell_chars:
        raise ValueError("Input group_tell_chars cannot be None.")
    if "radicals" not in group_tell_chars:
        return None, None

    radicals = tuple(sorted(group_tell_chars["radicals"]))

    return group_tell_chars, radicals


def generate_endings_lists(
    group_endings: dict[str, tuple[str, ...]] | None,
) -> Generate_List_Return:
    """
    Generate endings lists for a given model type.

    Args:
        group_endings: A dictionary containing the endings for the given model type

    Returns:
        Generate_List_Return: A tuple containing the endings lists for the given model type
    """
    if not group_endings:
        return None, None, None

    # Compile the list of endings for the data group from the dictionary above
    end_groups = tuple(sorted(group_endings))
    endings = tuple(sorted({e for g in end_groups for e in group_endings[g]}))

    return group_endings, endings, end_groups


def generate_bigram_lists(
    group_bigrams: dict[str, tuple[str, ...]] | None,
) -> Generate_List_Return:
    """
    Generate bigram lists for a given model type.

    Args:
        group_bigrams: A dictionary containing the bigrams for the given model type

    Returns:
        Generate_List_Return: A tuple containing the bigram lists for the given model type
    """
    
    if not group_bigrams:
        return None, None, None

    # Compile the list of bigrams for the data group from the dictionary above
    bigram_groups = tuple(sorted(group_bigrams))
    bigrams = tuple(sorted({e for g in bigram_groups for e in group_bigrams[g]}))

    return group_bigrams, bigrams, bigram_groups


###### Tell Dictionaries ######

tell_character_dict = {
    "perso_arabic": {
        "ar": tuple(sorted("ةىأإٱكي")),
        "fa": tuple(sorted("ۀ")),
        "ur": tuple(sorted("ٹڈڑےںھۓہے")),
        "overlapping": tuple(sorted("پچژگکی")),
    },
    "ja_zh": {
        "ja": tuple(
            sorted(
                "働込畑辻榊栃峠枠匂駅図経発鉄県斎歳圧緑検関総郷録帰覧剣続涙桜覚広辺対薬軽験"
                "冴畳匠酎丼塚尻曽冨畠鴨鰹匂圏喩麹渚峯"
            )
        ),
        "zh": tuple(
            sorted(
                "这那为说谁还没发见观读书车门问间闻风电飞马鸟鱼线网级处张陈员优产币广"
                "國學體經讀圖綠鐵縣亞澤辭總鄉嚴覺櫻營續淚觀變醫臺"
                "仅从众优务兰关兴决刘况冲冻净减刘务刘刚创务刘务"
                "齊顏臟廳鬥雞"
            )
        ),
        "radicals": tuple(sorted("氵扌艹言金")),
    },
    "eastern_slavic": {
        "be": tuple(sorted("ў")),
        "ru": tuple(sorted("ъыэё")),
        "uk": tuple(sorted("їєґ")),
        "overlapping": tuple(sorted(["і"])),
    },
    "southern_slavic": {
        "bg": tuple(sorted("ъщ")),
        "mk": tuple(sorted("ѓќѕ")),
        "sr": tuple(sorted("ђћљњџ")),
        "overlapping": tuple(sorted(["ј"])),
    },
    "turkic": {
        "kk": tuple(sorted("әұі")),
        "ky": tuple(),  # no unique single-character tells
        "mn": tuple(),  # no unique single-character tells
        "tg": tuple(sorted("ҷҳӣӯ")),
        "overlapping": tuple(sorted("ңүөһқғ")),
    },
    "indic": {
        "hi": tuple(sorted("क़ख़ग़ज़ड़ढ़फ़य़")),
        "mr": tuple(sorted("ळऱऑॲॅॉ")),
        "ne": tuple(),  # no unique single-character tells
        "overlapping": tuple(sorted(["़"])),  # nukta
    },
}

endings_dict = {
    "indic": {
        "hi": tuple(
            sorted(["पन", "ता", "कार", "वादी", "गर", "इया", "इन", "ई", "याँ", "यों"])
        ),
        "mr": tuple(
            sorted(["णे", "तील", "चा", "ची", "चे", "ला", "ना", "कर", "वाला", "पणा"])
        ),
        "ne": tuple(sorted(["हरु", "हरू", "को", "मा", "बाट", "लाई"])),
    },
    "southern_slavic": {
        "bg": tuple(sorted(["ът", "ия", "ево", "ово"])),
        "mk": tuple(sorted(["от", "ев", "ов", "ва"])),
        "sr": tuple(sorted(["ије", "ија", "има", "ама", "ска", "ски"])),
        "overlapping": tuple(sorted(["та", "то", "те"])),
    },
}

bigrams_dict = {
    "southern_slavic": {
        "bg": tuple(sorted(["ър", "ъл", "ън", "ът", "ят", "ще", "дж"])),
        "mk": tuple(
            sorted(["ќе", "ќи", "ќа", "ќу", "ѓе", "ѓи", "ѓа", "ѓу", "ѕв", "ѕд"])
        ),
        "sr": tuple(
            sorted(["ће", "ћа", "ћу", "ћи", "ђа", "ђе", "ђу", "џв", "џа", "џе"])
        ),
    }
}
