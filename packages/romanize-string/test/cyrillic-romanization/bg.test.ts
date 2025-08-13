import { describe, it, expect } from "vitest";
import { romanizeCyrillic } from "../../src/transliterators/cyrillic-romanization";

describe("Bulgarian (bg)", () => {
    it("should transliterate basic examples", () => {
        expect(romanizeCyrillic("българия", "bg")).toBe("balgariia");
        expect(romanizeCyrillic("говоря", "bg")).toBe("govoria");
    });

    it("should handle ъ as a and ь as silent", () => {
        expect(romanizeCyrillic("съюз", "bg")).toBe("saiuz");
        expect(romanizeCyrillic("любовь", "bg")).toBe("liubov");
    });
});
