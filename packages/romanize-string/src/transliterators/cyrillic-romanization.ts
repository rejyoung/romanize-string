import { PluginRegistrar } from "romanize-string/plugins";
import { CyrillicLanguageCode } from "../public-types/language-types";

/**
 * Adapted from cyrillic-to-translit-js
 * Original author: Aleksandr Filatov
 * License: MIT
 * https://github.com/greybax/cyrillic-to-translit-js
 */

export const romanizeCyrillic = (
    input: string,
    language: CyrillicLanguageCode,
    asciiOnly: boolean = false
): string => {
    if (!input) {
        return "";
    }

    const { initialCharacterMap, nonInitialCharacterMap } =
        getCharacterMapsForLanguage(language, asciiOnly);

    // We must normalize string for transform all unicode chars to uniform form
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/normalize
    const normalizedInput = input.normalize();

    let newStr = "";
    let isWordBoundary = false;
    const belarusianETriggerChars = "аеёіоуыэюя";
    const russianYaTriggerChars = "аеёиоуыэюяь";

    for (let i = 0; i < normalizedInput.length; i++) {
        const isUpperCaseOrWhatever =
            normalizedInput[i] === normalizedInput[i].toUpperCase();
        let strLowerCase = normalizedInput[i].toLowerCase();

        // Contextual character info for advanced rules
        const prevChar = i > 0 ? normalizedInput[i - 1].toLowerCase() : "";
        const nextChar =
            i < normalizedInput.length - 1
                ? normalizedInput[i + 1].toLowerCase()
                : "";
        const nextNextChar =
            i < normalizedInput.length - 2
                ? normalizedInput[i + 2].toLowerCase()
                : "";
        if (strLowerCase === " ") {
            newStr += " ";
            isWordBoundary = true;
            continue;
        }

        let newLetter;

        if (language === "be" && strLowerCase === "е") {
            if (i === 0 || isWordBoundary) {
                newLetter = "ye";
            } else if (!belarusianETriggerChars.includes(prevChar)) {
                newLetter = "ie";
            } else {
                newLetter = "e";
            }
        }

        if (language === "ru") {
            if (strLowerCase === "я") {
                newLetter = "ya";
            }
            if (strLowerCase === "ы") {
                // final "-ый"
                const isWordEnd =
                    nextNextChar === "" ||
                    nextNextChar.match(/[\s.,!?;:()\[\]'"«»]/);
                if (nextChar === "й" && isWordEnd) {
                    if (asciiOnly === true) {
                        newLetter = "yi";
                    } else {
                        newLetter = "yy";
                    }
                    i++; // skip the 'й' so it isn't transliterated again
                }
            }
        }

        // Handle contextual forms

        if (
            language === "uk" &&
            normalizedInput.slice(i - 1, i + 1).toLowerCase() === "зг"
        ) {
            // handle ukrainian special case зг > zgh
            newLetter = "gh";
        } else if (
            typeof newLetter === "undefined" &&
            (i === 0 || isWordBoundary)
        ) {
            newLetter = initialCharacterMap[strLowerCase];
            isWordBoundary = false;
        } else if (typeof newLetter === "undefined") {
            newLetter = nonInitialCharacterMap[strLowerCase];
        }

        if ("undefined" === typeof newLetter) {
            newStr += isUpperCaseOrWhatever
                ? strLowerCase.toUpperCase()
                : strLowerCase;
        } else if (isUpperCaseOrWhatever) {
            // handle multi-symbol letters
            newLetter.length > 1
                ? (newStr += newLetter[0].toUpperCase() + newLetter.slice(1))
                : (newStr += newLetter.toUpperCase());
        } else {
            newStr += newLetter;
        }
    }

    // Convert any remaining Cyrillic homoglyphs to their Latin counterparts.
    const normalizedOutput = replaceCyrillicHomoglyphs(newStr);

    return normalizedOutput;
};

type CharacterMaps = {
    initialCharacterMap: Record<string, string>;
    nonInitialCharacterMap: Record<string, string>;
};

const getCharacterMapsForLanguage = (
    language: CyrillicLanguageCode,
    asciiOnly: boolean
): CharacterMaps => {
    /***********
     * Note: Global lists include characters common to all supported Cyrillic languages as well as characters unique to particular languages.
     ***********/
    const globalCharacterMap: Record<string, string> = {
        А: "A",
        а: "a",
        Ә: "Ä",
        ә: "ä",
        Б: "B",
        б: "b",
        В: "V",
        в: "v",
        Г: "G",
        г: "g",
        Ғ: "Gh",
        ғ: "gh",
        Ґ: "G",
        ґ: "g",
        Д: "D",
        д: "d",
        Ђ: "Đ",
        ђ: "đ",
        Ћ: "Ć",
        ћ: "ć",
        Ѓ: "Ǵ",
        ѓ: "ǵ",
        Ё: "Yo",
        ё: "yo",
        Ж: "Zh",
        ж: "zh",
        З: "Z",
        з: "z",
        И: "I",
        и: "i",
        І: "I",
        і: "i",
        Ј: "J",
        ј: "j",
        Љ: "Lj",
        љ: "lj",
        К: "K",
        к: "k",
        Қ: "Q",
        қ: "q",
        Ќ: "Ḱ",
        ќ: "ḱ",
        Л: "L",
        л: "l",
        Њ: "Nj",
        њ: "nj",
        М: "M",
        м: "m",
        Н: "N",
        н: "n",
        Ң: "Ŋ",
        ң: "ŋ",
        О: "O",
        о: "o",
        Ө: "Ö",
        ө: "ö",
        П: "P",
        п: "p",
        Р: "R",
        р: "r",
        С: "S",
        с: "s",
        Т: "T",
        т: "t",
        У: "U",
        у: "u",
        Ӯ: "U",
        ӯ: "u",
        Ў: "U",
        ў: "u",
        Ү: "Ü",
        ү: "ü",
        Ӣ: "Y",
        ӣ: "y",
        Ф: "F",
        ф: "f",
        Х: "Kh",
        х: "kh",
        Ҳ: "H",
        ҳ: "h",
        Һ: "H",
        һ: "h",
        Ц: "Ts",
        ц: "ts",
        Ч: "Ch",
        ч: "ch",
        Ҷ: "Č",
        ҷ: "č",
        Ш: "Sh",
        ш: "sh",
        Щ: "Shch",
        щ: "shch",
        Ъ: "",
        ъ: "",
        Ы: "Y",
        ы: "y",
        Ь: "",
        ь: "",
        Ѕ: "Dz",
        ѕ: "dz",
        Э: "E",
        э: "e",
        Џ: "Dž",
        џ: "dž",
        Ұ: "U̇",
        ұ: "u̇",
    };

    const asciiOnlyOverrides: Record<string, string> = {
        Ә: "Ae",
        ә: "ae",
        Ӣ: "I",
        ӣ: "i",
        Ң: "Ng",
        ң: "ng",
        Ө: "Oe",
        ө: "oe",
        Ү: "Ue",
        ү: "ue",
        Ұ: "U",
        ұ: "u",
        Ѓ: "Gj",
        ѓ: "gj",
        Ќ: "Kj",
        ќ: "kj",
        Ҷ: "Ch",
        ҷ: "ch",
        Џ: "Dzh",
        џ: "dzh",
        Љ: "Lj",
        љ: "lj",
        Њ: "Nj",
        њ: "nj",
        Ћ: "C",
        ћ: "c",
        Ђ: "Dj",
        ђ: "dj",
        Ѕ: "Dz",
        ѕ: "dz",
    };

    const effectiveGlobalCharacterMap = asciiOnly
        ? { ...globalCharacterMap, ...asciiOnlyOverrides }
        : globalCharacterMap;

    /*
    CHARACTER MAPPINGS FOR INITIAL POSITION
    */

    // Characters whose transliterations differ if they appear at the beginning of a word
    const globalInitialCharacterMap: Record<string, string> = {
        Е: "E",
        е: "e",
        є: "ye",
        Є: "Ye",
        ї: "yi",
        Ї: "Yi",
        й: "y",
        Й: "Y",
        ю: "yu",
        Ю: "Yu",
        я: "ya",
        Я: "Ya",
    };

    const initialCharacterMap = {
        ...effectiveGlobalCharacterMap,
        ...globalInitialCharacterMap,
    };

    // language-specific overrides
    switch (language) {
        case "ru":
            Object.assign(initialCharacterMap, {
                е: "ye",
                Е: "Ye",
            });
            break;
        case "uk":
            Object.assign(initialCharacterMap, {
                г: "h",
                Г: "H",
                и: "y",
                И: "Y",
            });
            break;
        case "mn":
            Object.assign(initialCharacterMap, {
                ө: "o",
                Ө: "O",
                ү: "u",
                Ү: "U",
            });
            break;
        case "be":
            Object.assign(initialCharacterMap, {
                ў: asciiOnly ? "u" : "ŭ",
                Ў: asciiOnly ? "U" : "Ŭ",
                е: "ye",
                Е: "Ye",
            });
            break;
        case "bg":
            Object.assign(
                initialCharacterMap,
                asciiOnly
                    ? {
                          ъ: "a",
                          Ъ: "A",
                      }
                    : {
                          ъ: "ă",
                          Ъ: "Ă",
                      }
            );
            break;
        case "ky":
            Object.assign(
                initialCharacterMap,
                asciiOnly
                    ? {
                          ң: "ng",
                          Ң: "Ng",
                          ө: "o",
                          Ө: "O",
                          ү: "u",
                          Ү: "U",
                      }
                    : {
                          ң: "ng",
                          Ң: "Ng",
                          ө: "ö",
                          Ө: "Ö",
                          ү: "ü",
                          Ү: "Ü",
                      }
            );
            break;
        case "kk":
            Object.assign(
                initialCharacterMap,
                asciiOnly
                    ? {
                          ә: "a",
                          Ә: "A",
                          ң: "ng",
                          Ң: "Ng",
                          ө: "o",
                          Ө: "O",
                          ү: "u",
                          Ү: "U",
                      }
                    : {
                          ә: "ä",
                          Ә: "Ä",
                          ң: "ŋ",
                          Ң: "Ŋ",
                          ө: "ö",
                          Ө: "Ö",
                          ү: "ü",
                          Ү: "Ü",
                      }
            );
            break;
        case "sr":
            Object.assign(
                initialCharacterMap,
                asciiOnly
                    ? {
                          ђ: "dj",
                          Ђ: "Dj",
                          ћ: "c",
                          Ћ: "C",
                      }
                    : {
                          ђ: "đ",
                          Ђ: "Đ",
                          ћ: "ć",
                          Ћ: "Ć",
                      }
            );
            break;
        case "tg":
            Object.assign(initialCharacterMap, {
                ҳ: asciiOnly ? "h" : "ḥ",
                Ҳ: asciiOnly ? "H" : "Ḥ",
                Ӣ: asciiOnly ? "I" : "Ī",
                ӣ: asciiOnly ? "i" : "ī",
            });
            break;
        default:
            break;
    }

    if (["uk", "be", "kk", "tg"].includes(language)) {
        Object.assign(initialCharacterMap, {
            "'": "",
            "’": "",
            ʼ: "",
        });
    }

    /*
    CHARACTER MAPPINGS FOR NON-INITIAL POSITION
    */

    // Characters whose transliterations differ if they appear after the first character of a word
    const globalNonInitialCharacterMap: Record<string, string> = {
        Е: "E",
        е: "e",
        Є: "ie",
        є: "ie",
        Ї: "i",
        ї: "i",
        Й: "i",
        й: "i",
        Ю: "iu",
        ю: "iu",
        Я: "ia",
        я: "ia",
    };

    const nonInitialCharacterMap = {
        ...effectiveGlobalCharacterMap,
        ...globalNonInitialCharacterMap,
    };

    // language-specific overrides
    switch (language) {
        case "bg":
            Object.assign(
                nonInitialCharacterMap,
                asciiOnly
                    ? {
                          е: "ie",
                          Е: "Ie",
                          ъ: "a",
                          Ъ: "A",
                      }
                    : {
                          е: "ie",
                          Е: "Ie",
                          ъ: "ă",
                          Ъ: "Ă",
                      }
            );
            break;
        case "kk":
            Object.assign(
                nonInitialCharacterMap,
                asciiOnly
                    ? {
                          ұ: "u",
                          Ұ: "U",
                      }
                    : {
                          ұ: "ū",
                          Ұ: "Ū",
                      }
            );
            break;
        case "tg":
            Object.assign(nonInitialCharacterMap, {
                ъ: asciiOnly ? "" : "ʾ",
                Ъ: asciiOnly ? "" : "ʾ",
                ҳ: asciiOnly ? "h" : "ḥ",
                Ҳ: asciiOnly ? "H" : "Ḥ",
                Ӣ: asciiOnly ? "I" : "Ī",
                ӣ: asciiOnly ? "i" : "ī",
            });
            break;
        case "uk":
            Object.assign(nonInitialCharacterMap, {
                г: "h",
                Г: "H",
                и: "y",
                И: "Y",
            });
            break;
        case "mn":
            Object.assign(nonInitialCharacterMap, {
                ө: "o",
                Ө: "O",
                ү: "u",
                Ү: "U",
            });
            break;
        default:
            break;
    }

    if (["uk", "be", "kk", "tg"].includes(language)) {
        Object.assign(nonInitialCharacterMap, {
            "'": "",
            "’": "",
            ʼ: "",
        });
    }

    return { initialCharacterMap, nonInitialCharacterMap };
};

const replaceCyrillicHomoglyphs = (input: string): string => {
    const homoglyphReplacements: Record<string, string> = {
        е: "e",
        а: "a",
        о: "o",
        р: "p",
        с: "c",
        у: "y",
        х: "x",
        к: "k",
        м: "m",
        т: "t",
        в: "b",
        н: "h",
        ј: "j",
    };

    const output = input.replace(
        /[еаорсухкмтвнј]/g,
        (char) => homoglyphReplacements[char] || char
    );

    return output;
};

romanizeCyrillic.register = (pluginSetup: PluginRegistrar) => {
    pluginSetup();
};
