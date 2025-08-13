import { romanizeArabic } from "../../src/transliterators/arabic-romanization";
import { describe, it, expect } from "vitest";

describe("romanizeArabic (Farsi)", () => {
    it("should handle Farsi-specific characters", () => {
        const input = "پدر";
        const expected = "bidar";
        const result = romanizeArabic(input);
        expect(result).toBe(expected);
    });

    it("should replace common Farsi words from the phonetic map", () => {
        const input = "کتاب";
        const expected = "kitāb";
        const result = romanizeArabic(input);
        expect(result).toBe(expected);
    });
});
