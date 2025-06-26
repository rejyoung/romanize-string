import { romanizeArabic } from "./transliterators/arabic-romanization.js";
import { romanizeKorean } from "./transliterators/korean-romanization.js";
import { romanizeJapanese } from "./transliterators/japanese-romanization.js";
import { ConvertibleLanguage } from "./types/language-types.js";
import {
    isArabicLanguage,
    isCyrillicLanguage,
    isIndicLanguage,
} from "./utils/type-guards.js";
import { romanizeIndic } from "./transliterators/inidic-romanization.js";
import { romanizeThai } from "./transliterators/thai-romanization.js";
import { romanizeCantonese } from "./transliterators/cantonese-romanization.js";
import { romanizeMandarin } from "./transliterators/mandarin-romanization.js";
import { romanizeCyrillic } from "./transliterators/cyrillic-romanization.js";

export const romanizeString = async (
    string: string,
    language: ConvertibleLanguage,
    needsAsciiOnly?: false
): Promise<string> => {
    if (!string.trim()) return "";
    let transliteratedString: string;

    // Kanji or Hiragana
    if (language === ("ja" as ConvertibleLanguage)) {
        transliteratedString = await romanizeJapanese(string);

        // Hangul
    } else if (language === ("ko" as ConvertibleLanguage)) {
        transliteratedString = romanizeKorean(string);

        // Hanzi - Mandarin
    } else if (
        (["zh-CN", "zh-Hant"] as readonly ConvertibleLanguage[]).includes(
            language
        )
    ) {
        transliteratedString = romanizeMandarin(string);

        // Hanzi - Cantonese
    } else if (language === "yue") {
        transliteratedString = romanizeCantonese(string);

        // Devanagari
    } else if (isIndicLanguage(language)) {
        transliteratedString = romanizeIndic(string, language, needsAsciiOnly);

        // Cyrillic
    } else if (language === ("th" as ConvertibleLanguage)) {
        transliteratedString = romanizeThai(string);
    } else if (isCyrillicLanguage(language)) {
        transliteratedString = romanizeCyrillic(string, language);

        // Arabic
    } else if (isArabicLanguage(language)) {
        transliteratedString = romanizeArabic(string);
    } else {
        transliteratedString = string;
    }
    console.log("TRANSLITERATED TITLE:", transliteratedString);
    return (
        transliteratedString.slice(0, 1).toUpperCase() +
        transliteratedString.slice(1)
    ).trim();
};

///////////////

romanizeString("Қазақ тілі — мемлекеттік тіл.", "kk");
