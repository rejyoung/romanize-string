import { describe, it, expect } from "vitest";
import { romanizeCyrillic } from "../../src/transliterators/cyrillic-romanization";

describe("Kazakh (kk)", () => {
    it("should transliterate basic examples", () => {
        expect(romanizeCyrillic("қазақ", "kk")).toBe("qazaq");
        expect(romanizeCyrillic("тіл", "kk")).toBe("til");
    });

    it("should apply contextual rule for ғ", () => {
        expect(romanizeCyrillic("ғұмыр", "kk")).toBe("ghūmyr");
    });
});
