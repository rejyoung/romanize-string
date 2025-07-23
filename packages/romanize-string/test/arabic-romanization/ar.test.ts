import { romanizeArabic } from "../../src/transliterators/arabic-romanization";

describe("romanizeArabic (Arabic)", () => {
    it("should transliterate simple Arabic input", () => {
        const input = "السلام عليكم";
        const expected = "al-ssalām ʿlyakm";
        const result = romanizeArabic(input);
        expect(result).toBe(expected);
    });

    it("should handle input with diacritics", () => {
        const input = "مُحَمَّد";
        const expected = "muḥammad";
        const result = romanizeArabic(input);
        expect(result).toBe(expected);
    });

    it("should correctly handle edge cases with Arabic diacritics and normalization", () => {
        const input = "ٱللّٰه";
        const expected = "Allāh";
        const result = romanizeArabic(input);
        expect(result).toBe(expected);
    });
});
