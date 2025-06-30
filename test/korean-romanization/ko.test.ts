import { romanizeKorean } from "../../src/transliterators/korean-romanization";

describe("romanizeKorean", () => {
    it("should correctly romanize basic Hangul syllables", () => {
        expect(romanizeKorean("안녕하세요")).toBe("annyeonghaseyo");
        expect(romanizeKorean("감사합니다")).toBe("gamsahamnida");
    });

    it("should handle batchim properly", () => {
        expect(romanizeKorean("밥")).toBe("bap");
        expect(romanizeKorean("집")).toBe("jip");
    });

    it("should handle syllables with double consonants", () => {
        expect(romanizeKorean("까")).toBe("kka");
        expect(romanizeKorean("따")).toBe("tta");
    });

    it("should handle syllables with aspirated consonants", () => {
        expect(romanizeKorean("카")).toBe("ka");
        expect(romanizeKorean("타")).toBe("ta");
    });

    it("should return empty string when given empty input", () => {
        expect(romanizeKorean("")).toBe("");
    });

    it("should leave non-Korean text untouched", () => {
        expect(romanizeKorean("Hello")).toBe("Hello");
        expect(romanizeKorean("123")).toBe("123");
    });

    it("should handle mixed Korean and non-Korean input", () => {
        expect(romanizeKorean("안녕 Hello")).toBe("annyeong Hello");
    });
});
