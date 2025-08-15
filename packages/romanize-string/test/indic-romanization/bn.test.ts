import { romanizeIndic } from "../../src/transliterators/inidic-romanization";

describe("Indic language transliteration", () => {
    it("should transliterate input correctly", () => {
        const input = "নমস্কার";
        const expected = "namaskāra";
        expect(romanizeIndic(input, "bn", false)).toBe(expected);
    });

    it("should transliterate ASCII-only version correctly", () => {
        const input = "নমস্কার";
        const expectedAscii = "namaskaara";
        expect(romanizeIndic(input, "bn", true)).toBe(expectedAscii);
    });
});
