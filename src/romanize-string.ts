import { romanizeArabic } from "./transliterators/arabic-romanization.js";
import { romanizeKorean } from "./transliterators/korean-romanization.js";
import { romanizeJapanese } from "./transliterators/japanese-romanization.js";
import { ConvertibleLanguage } from "./public-types/language-types.js";
import {
    isArabicLanguageCode,
    isCyrillicLanguageCode,
    isIndicLanguageCode,
    isMandarinLanguageCode,
} from "./utils/type-guards.js";
import { romanizeIndic } from "./transliterators/inidic-romanization.js";
import { romanizeThai } from "./transliterators/thai-romanization.js";
import { romanizeCantonese } from "./transliterators/cantonese-romanization.js";
import { romanizeMandarin } from "./transliterators/mandarin-romanization.js";
import { romanizeCyrillic } from "./transliterators/cyrillic-romanization.js";

export const romanizeString = async (
    string: string,
    language: ConvertibleLanguage,
    omitDiacritics?: boolean
): Promise<string> => {
    if (!string.trim()) return "";
    let transliteratedString: string;

    // Kanji, Hiragana, or Katakana
    if (language === ("ja" as ConvertibleLanguage)) {
        transliteratedString = await romanizeJapanese(string);

        // Hangul
    } else if (language === ("ko" as ConvertibleLanguage)) {
        transliteratedString = romanizeKorean(string);

        // Hanzi - Mandarin
    } else if (isMandarinLanguageCode(language)) {
        transliteratedString = romanizeMandarin(string, omitDiacritics);

        // Hanzi - Cantonese
    } else if (language === "yue") {
        transliteratedString = romanizeCantonese(string);

        // Devanagari
    } else if (isIndicLanguageCode(language)) {
        transliteratedString = romanizeIndic(string, language, omitDiacritics);

        // Cyrillic
    } else if (language === ("th" as ConvertibleLanguage)) {
        transliteratedString = romanizeThai(string);
    } else if (isCyrillicLanguageCode(language)) {
        transliteratedString = romanizeCyrillic(string, language);

        // Arabic
    } else if (isArabicLanguageCode(language)) {
        transliteratedString = romanizeArabic(string);
    } else {
        transliteratedString = string;
    }

    return transliteratedString.trim();
};
