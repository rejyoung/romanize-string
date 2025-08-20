import { describe, it, expect } from "vitest";
import { romanizeCyrillic } from "../../src/transliterators/cyrillic-romanization";

describe("Belarusian (be)", () => {
    describe("asciiOnly = true", () => {
        it("should transliterate basic examples", () => {
            expect(romanizeCyrillic("мова", "be", true)).toBe("mova");
            expect(romanizeCyrillic("беларусь", "be", true)).toBe("bielarus");
        });

        it("should handle ў as ŭ", () => {
            expect(romanizeCyrillic("ўсход", "be", true)).toBe("uskhod");
        });

        it("should use ye/ie for е depending on position", () => {
            expect(romanizeCyrillic("елка", "be", true)).toBe("yelka");
            expect(romanizeCyrillic("шчавелевы", "be", true)).toBe(
                "shchavielievy"
            );
        });
    });

    describe("asciiOnly = false", () => {
        it("should transliterate basic examples", () => {
            expect(romanizeCyrillic("мова", "be", false)).toBe("mova");
            expect(romanizeCyrillic("беларусь", "be", false)).toBe("bielarus");
        });

        it("should handle ў as ŭ", () => {
            expect(romanizeCyrillic("ўсход", "be", false)).toBe("ŭskhod");
        });

        it("should use ye/ie for е depending on position", () => {
            expect(romanizeCyrillic("елка", "be", false)).toBe("yelka");
            expect(romanizeCyrillic("шчавелевы", "be", false)).toBe(
                "shchavielievy"
            );
        });
    });
});
