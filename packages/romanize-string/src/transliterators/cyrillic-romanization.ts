import { CyrillicLanguageCode } from "../public-types/language-types";

/**
 * Adapted from cyrillic-to-translit-js
 * Original author: Aleksandr Filatov
 * License: MIT
 * https://github.com/greybax/cyrillic-to-translit-js
 */

export const romanizeCyrillic = (
    input: string,
    language: CyrillicLanguageCode
): string => {
    if (!input) {
        return "";
    }

    const { firstAssociations, nonFirstAssociations } =
        getAssociationsForLanguage(language);

    // We must normalize string for transform all unicode chars to uniform form
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/normalize
    const normalizedInput = input.normalize();

    let newStr = "";
    let isWordBoundary = false;
    const vowels = "аеёиоуыэюяіїґәөүұhєі";

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

        if (strLowerCase === " ") {
            newStr += " ";
            isWordBoundary = true;
            continue;
        }

        let newLetter;

        if (language === "be" && strLowerCase === "е") {
            if (i === 0 || isWordBoundary) {
                newLetter = "ye";
            } else if (!vowels.includes(prevChar)) {
                newLetter = "ie";
            } else {
                newLetter = "e";
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
            newLetter = firstAssociations[strLowerCase];
            isWordBoundary = false;
        } else if (typeof newLetter === "undefined") {
            newLetter = nonFirstAssociations[strLowerCase];
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

type Associations = {
    firstAssociations: Record<string, string>;
    nonFirstAssociations: Record<string, string>;
};

const getAssociationsForLanguage = (
    language: CyrillicLanguageCode
): Associations => {
    /*
    ASSOCIATIONS FOR INITIAL POSITION
    */

    // letters shared between languages
    const firstLetters = {
        а: "a",
        б: "b",
        в: "v",
        д: "d",
        з: "z",
        й: "y",
        к: "k",
        л: "l",
        м: "m",
        н: "n",
        о: "o",
        п: "p",
        р: "r",
        с: "s",
        т: "t",
        у: "u",
        ф: "f",
        ь: "",
    };

    // digraphs appearing only in initial position
    let initialDigraphs: Record<string, string> = {};

    // language-specific mappings
    switch (language) {
        case "ru":
            Object.assign(firstLetters, {
                г: "g",
                и: "i",
                ъ: "",
                ы: "i",
                э: "e",
            });
            initialDigraphs = { е: "ye" };
            break;
        case "uk":
            Object.assign(firstLetters, {
                г: "h",
                ґ: "g",
                е: "e",
                и: "y",
                і: "i",
            });
            initialDigraphs = { є: "ye", ї: "yi" };
            break;
        case "mn":
            Object.assign(firstLetters, {
                г: "g",
                ө: "o",
                ү: "u",
                и: "i",
                ы: "y",
                э: "e",
                ъ: "",
            });
            break;
        case "be":
            Object.assign(firstLetters, {
                і: "i",
                ў: "u",
                э: "e",
                и: "i",
                ы: "y",
            });
            initialDigraphs = { е: "ye" };
            break;
        case "bg":
            Object.assign(firstLetters, {
                ъ: "a",
                ь: "",
                и: "i",
                г: "g",
            });
            break;
        case "ky":
            Object.assign(firstLetters, {
                ң: "ñ",
                ө: "ö",
                ү: "ü",
                и: "i",
                г: "g",
                ы: "y",
                э: "e",
                ъ: "",
            });
            break;
        case "kk":
            Object.assign(firstLetters, {
                ә: "a",
                ғ: "gh",
                қ: "q",
                ң: "ng",
                ө: "o",
                ұ: "ū",
                ү: "u",
                h: "h",
                і: "i",
                и: "i",
                ы: "y",
            });
            break;
        case "mk":
            Object.assign(firstLetters, {
                ѓ: "gj",
                ѕ: "dz",
                ј: "j",
                љ: "lj",
                њ: "nj",
                ќ: "ḱ",
                и: "i",
                г: "g",
                ы: "y",
                э: "e",
                ъ: "",
            });
            initialDigraphs = { ѓ: "gj", ќ: "ḱ" };
            break;
        case "sr":
            Object.assign(firstLetters, {
                ђ: "đ",
                ј: "j",
                љ: "lj",
                њ: "nj",
                ћ: "ć",
                џ: "dž",
                и: "i",
                г: "g",
                ы: "y",
                э: "e",
                ъ: "",
            });
            initialDigraphs = { ђ: "đ", ћ: "ć", џ: "dž" };
            break;
        case "tg":
            Object.assign(firstLetters, {
                ъ: "",
                ҳ: "h",
                ӣ: "i",
                ҷ: "j",
                ӯ: "u",
                и: "i",
                г: "g",
                ы: "y",
                э: "e",
                қ: "q",
            });
            initialDigraphs = { ҷ: "j" };
            break;
        default:
            break;
    }

    if (["uk", "be", "kk", "tg"].includes(language)) {
        Object.assign(firstLetters, {
            "'": "",
            "’": "",
            ʼ: "",
        });
    }

    // digraphs appearing in all positions
    const regularDigraphs = {
        ё: "yo",
        ж: "zh",
        х: "kh",
        ц: "ts",
        ч: "ch",
        ш: "sh",
        щ: "shch",
        ю: "yu",
        я: "ya",
        ј: "j",
        љ: "lj",
        њ: "nj",
        џ: "dž",
        ѓ: "gj",
        ќ: "kj",
        ѕ: "dz",
    };

    const firstDigraphs = Object.assign({}, regularDigraphs, initialDigraphs);

    const firstAssociations = Object.assign({}, firstLetters, firstDigraphs);

    /*
    ASSOCIATIONS FOR NON-INITIAL POSITION
    */

    const nonFirstLetters = Object.assign({}, firstLetters, { й: "i" });

    // digraphs appearing only in non-initial positions
    let nonInitialDigraphs: Record<string, string> = {};

    // language-specific mappings
    switch (language) {
        case "ru":
            Object.assign(nonFirstLetters, { е: "e" });
            break;
        case "uk":
            Object.assign(nonFirstLetters, { ї: "i" });
            nonInitialDigraphs = {
                є: "ie",
                ю: "iu",
                я: "ia",
            };
            break;
        case "mn":
            Object.assign(nonFirstLetters, { е: "e" });
            break;
        case "be":
            Object.assign(nonFirstLetters, { ы: "y", ў: "u" });
            nonInitialDigraphs = {
                ю: "iu",
                я: "ia",
            };
            break;
        case "bg":
            nonInitialDigraphs = {
                е: "ie",
                ю: "iu",
                я: "ia",
            };
            break;
        case "mk":
            nonInitialDigraphs = {
                ѓ: "gj",
                ќ: "ḱ",
            };
            break;
        case "sr":
            nonInitialDigraphs = {
                ђ: "đ",
                ћ: "ć",
                џ: "dž",
            };
            break;
        case "tg":
            nonInitialDigraphs = {
                ҷ: "j",
            };
            Object.assign(nonFirstLetters, {
                қ: "q",
                ъ: "",
                ӣ: "i",
                ӯ: "u",
            });
            break;
        case "kk":
            Object.assign(nonFirstLetters, {
                ғ: "gh",
                қ: "q",
                ұ: "ū",
                ә: "a",
                ө: "o",
                ү: "u",
            });
            break;
        default:
            break;
    }

    const nonFirstDigraphs = Object.assign(
        {},
        regularDigraphs,
        nonInitialDigraphs
    );

    const nonFirstAssociations = Object.assign(
        {},
        nonFirstLetters,
        nonFirstDigraphs
    );

    return { firstAssociations, nonFirstAssociations };
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
