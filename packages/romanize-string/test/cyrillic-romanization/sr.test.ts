import { describe, expect, it } from "@jest/globals";
import { romanizeCyrillic } from "../../src/transliterators/cyrillic-romanization";

describe("Serbian (sr)", () => {
    it("should transliterate digraphs and special consonants", () => {
        expect(romanizeCyrillic("ђак", "sr")).toBe("đak");
        expect(romanizeCyrillic("ћерка", "sr")).toBe("ćerka");
        expect(romanizeCyrillic("џем", "sr")).toBe("džem");
        expect(romanizeCyrillic("љубав", "sr")).toBe("ljubav");
        expect(romanizeCyrillic("њега", "sr")).toBe("njega");
    });
});
