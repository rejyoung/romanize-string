import { romanizeIndic } from "../../src/transliterators/inidic-romanization";
import { describe, it, expect } from "vitest";

describe("Indic language transliteration", () => {
    it("should transliterate input correctly", () => {
        const input = "నమస్కారం";
        const expected = "namaskāraṃ";
        expect(romanizeIndic(input, "te", false)).toBe(expected);
    });

    it("should transliterate ASCII-only version correctly", () => {
        const input = "నమస్కారం";
        const expectedAscii = "namaskaaram";
        expect(romanizeIndic(input, "te", true)).toBe(expectedAscii);
    });
});
