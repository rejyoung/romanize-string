import { pinyin } from "pinyin-pro";

export const romanizeMandarin = (input: string) => {
    const transliteration = pinyin(input).replace(/\s+/g, " ");
    return transliteration;
};
