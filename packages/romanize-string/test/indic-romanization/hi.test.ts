import { romanizeIndic } from "../../src/transliterators/indic-romanization";
import { describe, it, expect } from "vitest";

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
