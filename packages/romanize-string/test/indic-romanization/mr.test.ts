import { romanizeIndic } from "../../src/transliterators/inidic-romanization";

describe("Indic language transliteration", () => {
    it("should transliterate input correctly", () => {
        const input = "नमस्कार";
        const expected = "namaskāra";
        expect(romanizeIndic(input, "mr", false)).toBe(expected);
    });

    it("should transliterate ASCII-only version correctly", () => {
        const input = "नमस्कार";
        const expectedAscii = "namaskaara";
        expect(romanizeIndic(input, "mr", true)).toBe(expectedAscii);
    });
});
