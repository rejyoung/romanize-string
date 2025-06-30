import { romanizeThai } from "../../src/transliterators/thai-romanization";

describe("romanizeThai", () => {
    it("should romanize basic Thai text", () => {
        expect(romanizeThai("สวัสดี")).toBe("satti");
    });

    it("should handle Thai phrases with spaces", () => {
        expect(romanizeThai("สวัสดี ครับ")).toBe("satti khnap");
    });

    it("should return empty string for empty input", () => {
        expect(romanizeThai("")).toBe("");
    });

    it("should leave non-Thai text untouched", () => {
        expect(romanizeThai("Hello")).toBe("Hello");
    });
});
