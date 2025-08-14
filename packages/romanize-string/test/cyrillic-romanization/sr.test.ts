import { describe, it, expect } from "vitest";
import { romanizeCyrillic } from "../../src/transliterators/cyrillic-romanization";

describe("Serbian (sr)", () => {
    it("should transliterate digraphs and special consonants", () => {
        expect(romanizeCyrillic("ђак", "sr")).toBe("đak");
        expect(romanizeCyrillic("ћерка", "sr")).toBe("ćerka");
        expect(romanizeCyrillic("џем", "sr")).toBe("džem");
        expect(romanizeCyrillic("љубав", "sr")).toBe("ljubav");
        expect(romanizeCyrillic("њега", "sr")).toBe("njega");
    });

    it("should transliterate with ASCII approximations when asciiOnly is true", () => {
        expect(romanizeCyrillic("ђак", "sr", true)).toBe("djak");
        expect(romanizeCyrillic("ћерка", "sr", true)).toBe("cerka");
        expect(romanizeCyrillic("џем", "sr", true)).toBe("dzhem");
        expect(romanizeCyrillic("љубав", "sr", true)).toBe("ljubav");
        expect(romanizeCyrillic("њега", "sr", true)).toBe("njega");
    });
});
