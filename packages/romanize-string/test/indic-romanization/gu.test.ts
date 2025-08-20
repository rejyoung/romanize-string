import { romanizeIndic } from "../../src/transliterators/indic-romanization";
import { describe, it, expect } from "vitest";

describe("Indic language transliteration", () => {
    it("should transliterate input correctly", () => {
        const input = "નમસ્તે";
        const expected = "namaste";
        expect(romanizeIndic(input, "gu", false)).toBe(expected);
    });

    it("should transliterate ASCII-only version correctly", () => {
        const input = "નમસ્તે";
        const expectedAscii = "namaste";
        expect(romanizeIndic(input, "gu", true)).toBe(expectedAscii);
    });
});
