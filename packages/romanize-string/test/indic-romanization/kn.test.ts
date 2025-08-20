import { romanizeIndic } from "../../src/transliterators/inidic-romanization";
import { describe, it, expect } from "vitest";

describe("Indic language transliteration", () => {
    it("should transliterate input correctly", () => {
        const input = "ನಮಸ್ಕಾರ";
        const expected = "namaskāra";
        expect(romanizeIndic(input, "kn", false)).toBe(expected);
    });

    it("should transliterate ASCII-only version correctly", () => {
        const input = "ನಮಸ್ಕಾರ";
        const expectedAscii = "namaskaara";
        expect(romanizeIndic(input, "kn", true)).toBe(expectedAscii);
    });
});
