import { romanizeMandarin } from "../../src/transliterators/mandarin-romanization";

describe("romanizeMandarin", () => {
    it("should romanize simplified Chinese text", () => {
        expect(romanizeMandarin("你好")).toBe("nǐ hǎo");
    });

    it("should romanize traditional Chinese text", () => {
        expect(romanizeMandarin("妳好")).toBe("nǎi hǎo");
    });

    it("should handle phrases with spaces", () => {
        expect(romanizeMandarin("早上好 你好")).toBe("zǎo shàng hǎo nǐ hǎo");
    });

    it("should omit diacritics with needsAsciiOnly set to true", () => {
        expect(romanizeMandarin("早上好 你好", true)).toBe(
            "zao shang hao ni hao"
        );
    });

    it("should return empty string for empty input", () => {
        expect(romanizeMandarin("")).toBe("");
    });

    it("should leave non-Chinese text untouched", () => {
        expect(romanizeMandarin("Hello")).toBe("Hello");
    });
});
