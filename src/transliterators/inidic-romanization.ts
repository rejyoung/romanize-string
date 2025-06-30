import Sanscript from "@indic-transliteration/sanscript";
import { IndicLanguageCode } from "../public-types/language-types";

const languageSchemeMap: Record<IndicLanguageCode, string> = {
    hi: "devanagari",
    bn: "bengali",
    te: "telugu",
    ta: "tamil_extended",
    gu: "gujarati",
    mr: "devanagari",
    pa: "gurmukhi",
    kn: "kannada",
};

export const romanizeIndic = (
    input: string,
    language: IndicLanguageCode,
    omitDiacritics: boolean
) => {
    // Replace ।, ॥, ૰, and the Gurmukhi abbreviation sign with full-stop.
    const normalizedInput = input.replace(/[\u0964\u0965\u0A76\u0AF0]/g, ".");

    // Determine appropriate transliteration scheme
    let transliterationScheme = "iast";
    if (omitDiacritics) {
        if (["te", "ta", "kn"].includes(language)) {
            transliterationScheme = "itrans_dravidian";
        } else {
            transliterationScheme = "hk";
        }
    }

    const transliteration = Sanscript.t(
        normalizedInput,
        languageSchemeMap[language],
        transliterationScheme
    );

    const normalizedOutput = transliteration.replace(/\u09BC/g, "");

    if (omitDiacritics) {
        const asciiNormalized = normalizedOutput
            .replace(/A/g, "aa")
            .replace(/I/g, "ii")
            .replace(/U/g, "uu")
            .replace(/R/g, "ri")
            .replace(/E/g, "ee")
            .replace(/O/g, "oo")
            .replace(/M/g, "m") // anusvara
            .replace(/H/g, "h") // visarga
            .replace(/N/g, "n") // retroflex nasal
            .replace(/~n/g, "n") // palatal nasal
            .replace(/chh/g, "ch"); // optional simplification
        return asciiNormalized;
    } else {
        return normalizedOutput;
    }
};
