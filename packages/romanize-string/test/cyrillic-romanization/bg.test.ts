import { describe, it, expect } from "vitest";
import { romanizeCyrillic } from "../../src/transliterators/cyrillic-romanization";

describe("Bulgarian (bg)", () => {
    describe("asciiOnly = false", () => {
        it("should transliterate with proper non-ASCII characters", () => {
            expect(romanizeCyrillic("българия", "bg", false)).toBe("bălgariia");
            expect(romanizeCyrillic("говоря", "bg", false)).toBe("govoria");
            expect(romanizeCyrillic("съюз", "bg", false)).toBe("săiuz");
            expect(romanizeCyrillic("любовь", "bg", false)).toBe("liubov");
        });
    });

    describe("asciiOnly = true", () => {
        it("should transliterate with ASCII approximations", () => {
            expect(romanizeCyrillic("българия", "bg", true)).toBe("balgariia");
            expect(romanizeCyrillic("говоря", "bg", true)).toBe("govoria");
            expect(romanizeCyrillic("съюз", "bg", true)).toBe("saiuz");
            expect(romanizeCyrillic("любовь", "bg", true)).toBe("liubov");
        });
    });
});
