import { getRoman } from "cantonese-romanisation";

export const romanizeCantonese = (input: string) => {
    const transliteration = getRoman(input)
        .map((options) => options[0])
        .join(" ")
        .replace(/\s+/g, " ");

    return transliteration;
};
