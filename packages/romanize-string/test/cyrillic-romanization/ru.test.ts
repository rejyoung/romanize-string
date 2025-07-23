import { romanizeCyrillic } from "../../src/transliterators/cyrillic-romanization";

/**
 * Adapted from cyrillic-to-translit-js
 * Original author: Aleksandr Filatov
 * License: MIT
 * https://github.com/greybax/cyrillic-to-translit-js
 */

describe("romanizeCyrillic", () => {
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
            "uchebnii material 1!"
        );
        expect(romanizeCyrillic("новый подъезд", "ru")).toBe("novii podezd");
        expect(romanizeCyrillic("плохая связь", "ru")).toBe("plokhaya svyaz");
    });

    it("should transliterate й differently depending on position", () => {
        expect(romanizeCyrillic("вкусный йогурт", "ru")).toBe("vkusnii yogurt");
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
