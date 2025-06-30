import { initKuroshiro, kuroshiro } from "../utils/kuroshiro.js";

export const romanizeJapanese = async (input: string) => {
    if (!kuroshiro._analyzer) {
        await initKuroshiro();
    }

    const transliteration = await kuroshiro.convert(input, {
        to: "romaji",
        mode: "spaced",
    });
    const standardizedTransliteration = transliteration
        .replace(/\b(\w+)\s+(ta|te|nai|masu|desu|da)\b/g, "$1$2") // Join common verb splits like "megumare ta" -> "megumareta".
        .replace(/\s+/g, " ");

    return standardizedTransliteration;
};
