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
        .replace(/\b(\w+)\s+(ta|te|nai|masu|desu|da)\b/g, "$1$2") // Join artificial verb splits (like "megumare ta" -> "megumareta"), which are artifacts of Kuroshiro's spaced mode.
        .replace(/\s+/g, " ")
        .replace(/\s+([.,!?！？。、])/g, "$1");

    return standardizedTransliteration;
};
