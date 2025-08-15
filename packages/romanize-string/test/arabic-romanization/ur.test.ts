import { romanizeArabic } from "../../src/transliterators/arabic-romanization";

describe("romanizeArabic (Urdu)", () => {
    it("should handle Urdu-specific characters", () => {
        const input = "گھر";
        const expected = "ghar";
        const result = romanizeArabic(input);
        expect(result).toBe(expected);
    });

    it("should replace common Urdu words from the phonetic map", () => {
        const input = "محبت";
        const expected = "muḥabbat";
        const result = romanizeArabic(input);
        expect(result).toBe(expected);
    });
});
