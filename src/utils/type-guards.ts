import {
    arabicLanguageCodes,
    convertibleLanguages,
    cyrillicLanguageCodes,
    indicLanguageCodes,
    mandarinLanguageCodes,
} from "../constants/supported-languages.js";
import {
    ArabicLanguageCode,
    ConvertibleLanguage,
    CyrillicLanguageCode,
    IndicLanguageCode,
    MandarinLanguageCode,
} from "../public-types/language-types.js";

export function isConvertibleLanguage(
    lang: string
): lang is ConvertibleLanguage {
    return (convertibleLanguages as readonly string[]).includes(
        lang as ConvertibleLanguage
    );
}

export function isIndicLanguageCode(
    lang: ConvertibleLanguage
): lang is IndicLanguageCode {
    return (indicLanguageCodes as unknown as ConvertibleLanguage[]).includes(
        lang
    );
}

export function isCyrillicLanguageCode(
    lang: ConvertibleLanguage
): lang is CyrillicLanguageCode {
    return (cyrillicLanguageCodes as unknown as ConvertibleLanguage[]).includes(
        lang
    );
}

export function isArabicLanguageCode(
    lang: ConvertibleLanguage
): lang is ArabicLanguageCode {
    return (arabicLanguageCodes as unknown as ConvertibleLanguage[]).includes(
        lang
    );
}

export function isMandarinLanguageCode(
    lang: ConvertibleLanguage
): lang is MandarinLanguageCode {
    return (mandarinLanguageCodes as unknown as ConvertibleLanguage[]).includes(
        lang
    );
}
