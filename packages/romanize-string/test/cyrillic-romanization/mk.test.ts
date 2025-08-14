import { describe, it, expect } from "vitest";
import { romanizeCyrillic } from "../../src/transliterators/cyrillic-romanization";

describe("Macedonian (mk)", () => {
    describe("asciiOnly = false", () => {
        it("should transliterate digraphs correctly", () => {
            expect(romanizeCyrillic("ѓавол", "mk")).toBe("ǵavol");
            expect(romanizeCyrillic("ќофти", "mk")).toBe("ḱofti");
            expect(romanizeCyrillic("љубов", "mk")).toBe("ljubov");
            expect(romanizeCyrillic("њива", "mk")).toBe("njiva");
        });
    });

    describe("asciiOnly = true", () => {
        it("should use ASCII equivalents", () => {
            expect(romanizeCyrillic("ѓавол", "mk", true)).toBe("gjavol");
            expect(romanizeCyrillic("ќофти", "mk", true)).toBe("kjofti");
            expect(romanizeCyrillic("љубов", "mk", true)).toBe("ljubov");
            expect(romanizeCyrillic("њива", "mk", true)).toBe("njiva");
        });
    });
});
