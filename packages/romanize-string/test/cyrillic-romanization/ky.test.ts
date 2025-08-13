import { describe, it, expect } from "vitest";
import { romanizeCyrillic } from "../../src/transliterators/cyrillic-romanization";

describe("Kyrgyz (ky)", () => {
    it("should transliterate special vowels correctly", () => {
        expect(romanizeCyrillic("кыргыз", "ky")).toBe("kyrgyz");
        expect(romanizeCyrillic("төрт", "ky")).toBe("tört");
        expect(romanizeCyrillic("үч", "ky")).toBe("üch");
    });

    it("should handle ң as ñ", () => {
        expect(romanizeCyrillic("жаңылык", "ky")).toBe("zhañylyk");
    });
});
