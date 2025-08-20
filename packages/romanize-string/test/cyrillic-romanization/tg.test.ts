import { describe, it, expect } from "vitest";
import { romanizeCyrillic } from "../../src/transliterators/cyrillic-romanization";

describe("Tajik (tg)", () => {
    describe("asciiOnly = false", () => {
        it("should transliterate with proper non-ASCII characters", () => {
            expect(romanizeCyrillic("ҷавоб", "tg", false)).toBe("čavob");
            expect(romanizeCyrillic("ҳақиқат", "tg", false)).toBe("ḥaqiqat");
            expect(romanizeCyrillic("барқӣ", "tg", false)).toBe("barqī");
        });

        it("should handle apostrophe-like ъ as ʾ", () => {
            expect(romanizeCyrillic("муъмин", "tg", false)).toBe("muʾmin");
        });
    });

    describe("asciiOnly = true", () => {
        it("should transliterate with ASCII approximations", () => {
            expect(romanizeCyrillic("ҷавоб", "tg", true)).toBe("chavob");
            expect(romanizeCyrillic("ҳақиқат", "tg", true)).toBe("haqiqat");
            expect(romanizeCyrillic("барқӣ", "tg", true)).toBe("barqi");
        });

        it("should handle apostrophe-like ъ as plain apostrophe or omit", () => {
            expect(romanizeCyrillic("муъмин", "tg", true)).toBe("mumin");
        });
    });
});
