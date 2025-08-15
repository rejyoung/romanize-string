import { describe, it, expect } from "vitest";
import { romanizeCyrillic } from "../../src/transliterators/cyrillic-romanization";

describe("Kazakh (kk)", () => {
    describe("asciiOnly = false", () => {
        it("should transliterate with proper non-ASCII characters", () => {
            expect(romanizeCyrillic("қазақ", "kk", false)).toBe("qazaq");
            expect(romanizeCyrillic("тіл", "kk", false)).toBe("til");
        });

        it("should apply contextual rule for ғ", () => {
            expect(romanizeCyrillic("ғұмыр", "kk", false)).toBe("ghūmyr");
        });
    });

    describe("asciiOnly = true", () => {
        it("should transliterate with ASCII approximations", () => {
            expect(romanizeCyrillic("қазақ", "kk", true)).toBe("qazaq");
            expect(romanizeCyrillic("тіл", "kk", true)).toBe("til");
        });

        it("should apply contextual rule for ғ", () => {
            expect(romanizeCyrillic("ғұмыр", "kk", true)).toBe("ghumyr");
        });
    });
});
