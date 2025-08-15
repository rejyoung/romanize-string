import { pinyin } from "pinyin-pro";

export const romanizeMandarin = (input: string, omitTones?: boolean) => {
    // Check if the input contains any Chinese characters and return the original input if not.
    if (
        !/[\u3400-\u9FBF]|[\u{20000}-\u{2A6DF}]|[\u{2A700}-\u{2B73F}]|[\u{2B740}-\u{2B81F}]|[\u{2B820}-\u{2CEAF}]/u.test(
            input
        )
    ) {
        return input;
    }
    const transliteration = pinyin(input, {
        toneType: omitTones ? "none" : undefined,
    })
        .replace(/(\S)\s+([，。！？、])/gu, "$1$2") // Remove extra spaces before punctuation
        .replace(/\s+/g, " ")
        // Replace full-width punctuation with standard ASCII punctuation.
        .replace(/[，]/g, ",")
        .replace(/[。]/g, ".")
        .replace(/[？]/g, "?")
        .replace(/[！]/g, "!")
        .trim();
    return transliteration;
};
