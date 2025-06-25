import { ConvertibleLanguage } from "../types/language-types";

// List of languages that require transliteration and that the current function can transliterate.
export const convertibleLanguages = [
    "ar", // Arabic
    "be", // Belarusian
    "bg", // Bulgarian
    "bn", // Bengali
    "fa", // Persian (Farsi)
    "gu", // Gujarati
    "hi", // Hindi
    "ja", // Japanese
    "kk", // Kazakh
    "kn", // Kannada
    "ko", // Korean
    "ky", // Kyrgz
    "mk", // Macedonian
    "mn", // Mongolian
    "mr", // Marathi
    "ne", // Nepali
    "pa", // Punjabi
    "ru", // Russian
    "sa", // Sanskrit
    "sr", // Serbian
    "ta", // Tamil
    "te", // Telugu
    "tg", // Tajik
    "th", // Thai
    "uk", // Ukrainian
    "ur", // Urdu
    "yue", // Cantonese
    "zh-CN", // Chinese Simplified
    "zh-Hant", // Chinese Traditional
] as const;

export const indicLanguages = [
    "hi",
    "bn",
    "te",
    "ta",
    "gu",
    "mr",
    "pa",
    "kn",
] as const;

export const cyrillicLanguages = [
    "be",
    "bg",
    "kk",
    "ky",
    "mk",
    "mn",
    "ru",
    "sr",
    "tg",
    "uk",
] as const;

export const arabicLanguages = ["ar", "ur", "fa"] as const;
