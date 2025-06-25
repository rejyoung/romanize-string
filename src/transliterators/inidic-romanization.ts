import Sanscript from "@indic-transliteration/sanscript";
import { IndicLanguage } from "../types/language-types";

const languageSchemeMap: Record<IndicLanguage, string> = {
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
    language: IndicLanguage,
    needsAsciiOnly: boolean
) => {
    // Replace ।, ॥, ૰, and the Gurmukhi abbreviation sign with full-stop.
    const normalizedInput = input.replace(/[\u0964\u0965\u0A76\u0AF0]/g, ".");

    // Determine appropriate transliteration scheme
    let transliterationScheme = "iast";
    if (needsAsciiOnly) {
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
    return normalizedOutput;
};
