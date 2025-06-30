import { romanizeIndic } from "../../src/transliterators/inidic-romanization";

describe("Indic language transliteration", () => {
    it("should transliterate input correctly", () => {
        const input = "नमस्ते";
        const expected = "namaste";
        expect(romanizeIndic(input, "hi", false)).toBe(expected);
    });

    it("should transliterate ASCII-only version correctly", () => {
        const input = "नमस्ते";
        const expectedAscii = "namaste";
        expect(romanizeIndic(input, "hi", true)).toBe(expectedAscii);
    });
});
