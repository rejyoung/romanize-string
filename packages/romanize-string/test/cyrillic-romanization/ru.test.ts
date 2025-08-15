import { romanizeCyrillic } from "../../src/transliterators/cyrillic-romanization";
import { describe, it, expect } from "vitest";

/**
 * Adapted from cyrillic-to-translit-js
 * Original author: Aleksandr Filatov
 * License: MIT
 * https://github.com/greybax/cyrillic-to-translit-js
 */

describe("romanizeCyrillic (asciiOnly = false)", () => {
    it("should return empty string when input is empty", () => {
        expect(romanizeCyrillic("", "ru")).toBe("");
        expect(romanizeCyrillic(null as any, "ru")).toBe("");
    });

    it("should transliterate a Russian phrase", () => {
        expect(romanizeCyrillic("привет мир!", "ru")).toBe("privet mir!");
    });

    it("should transliterate normalized input", () => {
        expect(romanizeCyrillic("русский".normalize("NFD"), "ru")).toBe(
            "russkii"
        );
    });

    it("should handle phrases with ы, ь, and ъ", () => {
        expect(romanizeCyrillic("учебный материал 1ьъ!", "ru")).toBe(
            "uchebnyy material 1!"
        );
        expect(romanizeCyrillic("новый подъезд", "ru")).toBe("novyy podezd");
        expect(romanizeCyrillic("плохая связь", "ru")).toBe("plokhaya svyaz");
    });

    it("should transliterate digraphs and preserve casing", () => {
        expect(romanizeCyrillic("Ярославль и Екатеринбург", "ru")).toBe(
            "Yaroslavl i Yekaterinburg"
        );
    });

    it("should treat input already in Latin as-is", () => {
        expect(romanizeCyrillic("privet mir!", "ru")).toBe("privet mir!");
    });
});

describe("romanizeCyrillic (asciiOnly = true)", () => {
    it("should transliterate a Russian phrase to ASCII-only", () => {
        expect(romanizeCyrillic("привет мир!", "ru", true)).toBe("privet mir!");
    });

    it("should handle phrases with ы, ь, and ъ", () => {
        expect(romanizeCyrillic("учебный материал 1ьъ!", "ru", true)).toBe(
            "uchebnyi material 1!"
        );
        expect(romanizeCyrillic("новый подъезд", "ru", true)).toBe(
            "novyi podezd"
        );
        expect(romanizeCyrillic("плохая связь", "ru", true)).toBe(
            "plokhaya svyaz"
        );
    });

    it("should transliterate й differently depending on position", () => {
        expect(romanizeCyrillic("вкусный йогурт", "ru", true)).toBe(
            "vkusnyi yogurt"
        );
    });

    it("should transliterate digraphs and preserve casing", () => {
        expect(romanizeCyrillic("Ярославль и Екатеринбург", "ru", true)).toBe(
            "Yaroslavl i Yekaterinburg"
        );
    });

    it("should treat input already in Latin as-is", () => {
        expect(romanizeCyrillic("privet mir!", "ru", true)).toBe("privet mir!");
    });
});
