import { romanizeIndic } from "../../src/transliterators/inidic-romanization";

describe("Indic language transliteration", () => {
    it("should transliterate input correctly", () => {
        const input = "ਸਤ ਸ੍ਰੀ ਅਕਾਲ";
        const expected = "sata srī akāla";
        expect(romanizeIndic(input, "pa", false)).toBe(expected);
    });

    it("should transliterate ASCII-only version correctly", () => {
        const input = "ਸਤ ਸ੍ਰੀ ਅਕਾਲ";
        const expectedAscii = "sata srii akaala";
        expect(romanizeIndic(input, "pa", true)).toBe(expectedAscii);
    });
});
