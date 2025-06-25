import cyrillicToTranslit from "cyrillic-to-translit-js";
import { CyrillicLanguage } from "../types/language-types";

export const romanizeCyrillic = (input: string, language: CyrillicLanguage) => {
    let preset: "ru" | "uk" | "mn";
    if (language === "uk") {
        preset = "uk";
    } else if (language === "mn") {
        preset = "mn";
    } else {
        preset = "ru";
    }
    const transliteration = cyrillicToTranslit({ preset }).transform(input);

    return transliteration;
};
