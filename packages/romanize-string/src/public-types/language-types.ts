import {
    arabicLanguageCodes,
    convertibleLanguages,
    cyrillicLanguageCodes,
    indicLanguageCodes,
    mandarinLanguageCodes,
} from "../constants/supported-languages";

export type ConvertibleLanguage = (typeof convertibleLanguages)[number];

export type IndicLanguageCode = (typeof indicLanguageCodes)[number];

export type CyrillicLanguageCode = (typeof cyrillicLanguageCodes)[number];

export type ArabicLanguageCode = (typeof arabicLanguageCodes)[number];

export type MandarinLanguageCode = (typeof mandarinLanguageCodes)[number];
