import { describe, it, expect } from "vitest";
import { romanizeCyrillic } from "../../src/transliterators/cyrillic-romanization";

describe("Tajik (tg)", () => {
    it("should transliterate special characters", () => {
        expect(romanizeCyrillic("ҷавоб", "tg")).toBe("javob");
        expect(romanizeCyrillic("ҳақиқат", "tg")).toBe("haqiqat");
        expect(romanizeCyrillic("барқӣ", "tg")).toBe("barqi");
    });

    it("should handle apostrophe-like ъ as ʾ", () => {
        expect(romanizeCyrillic("муъмин", "tg")).toBe("mumin");
    });
});
