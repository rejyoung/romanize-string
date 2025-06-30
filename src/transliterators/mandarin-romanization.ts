import { pinyin } from "pinyin-pro";

export const romanizeMandarin = (input: string, omitTones?: boolean) => {
    // Check if the input contains any Chinese characters
    if (
        !/[\u3400-\u9FBF]|[\u{20000}-\u{2A6DF}]|[\u{2A700}-\u{2B73F}]|[\u{2B740}-\u{2B81F}]|[\u{2B820}-\u{2CEAF}]/u.test(
            input
        )
    ) {
        return input;
    }
    const transliteration = pinyin(input, {
        toneType: omitTones ? "none" : undefined,
    }).replace(/\s+/g, " ");
    return transliteration;
};
