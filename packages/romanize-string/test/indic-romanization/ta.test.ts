import { romanizeIndic } from "../../src/transliterators/inidic-romanization";

describe("Indic language transliteration", () => {
    it("should transliterate input correctly", () => {
        const input = "வணக்கம்";
        const expected = "vaṇakkam";
        expect(romanizeIndic(input, "ta", false)).toBe(expected);
    });

    it("should transliterate ASCII-only version correctly", () => {
        const input = "வணக்கம்";
        const expectedAscii = "vanakkam";
        expect(romanizeIndic(input, "ta", true)).toBe(expectedAscii);
    });
});
