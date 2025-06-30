import { romanizeCantonese } from "../../src/transliterators/cantonese-romanization";

describe("romanizeCantonese", () => {
    it("should romanize simple Cantonese characters", () => {
        expect(romanizeCantonese("你好")).toBe("lee ho");
    });

    it("should handle phrases with spaces", () => {
        expect(romanizeCantonese("早晨 你好")).toBe("jo san lee ho");
    });

    it("should return empty string for empty input", () => {
        expect(romanizeCantonese("")).toBe("");
    });

    it("should ignore non-Chinese characters", () => {
        expect(romanizeCantonese("123 abc")).toBe(" ");
    });
});
