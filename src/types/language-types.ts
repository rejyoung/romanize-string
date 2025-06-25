import {
    arabicLanguages,
    convertibleLanguages,
    cyrillicLanguages,
    indicLanguages,
} from "../constants/supported-languages";

export type ConvertibleLanguage = (typeof convertibleLanguages)[number];

export type IndicLanguage = (typeof indicLanguages)[number];

export type CyrillicLanguage = (typeof cyrillicLanguages)[number];

export type ArabicLanguage = (typeof arabicLanguages)[number];
