import {
    arabicLanguages,
    cyrillicLanguages,
    indicLanguages,
} from "../constants/supported-languages.js";
import {
    ArabicLanguage,
    ConvertibleLanguage,
    CyrillicLanguage,
    IndicLanguage,
} from "../types/language-types.js";

export function isIndicLanguage(
    lang: ConvertibleLanguage
): lang is IndicLanguage {
    return (indicLanguages as unknown as ConvertibleLanguage[]).includes(lang);
}

export function isCyrillicLanguage(
    lang: ConvertibleLanguage
): lang is CyrillicLanguage {
    return (cyrillicLanguages as unknown as ConvertibleLanguage[]).includes(
        lang
    );
}

export function isArabicLanguage(
    lang: ConvertibleLanguage
): lang is ArabicLanguage {
    return (arabicLanguages as unknown as ConvertibleLanguage[]).includes(lang);
}
