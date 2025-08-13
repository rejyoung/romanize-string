import { initKuroshiro } from "../../src/utils/kuroshiro.js";
import { romanizeJapanese } from "../../src/transliterators/japanese-romanization.js";
import { describe, it, expect, beforeAll } from "vitest";

beforeAll(async () => {
    await initKuroshiro();
});

describe("romanizeJapanese", () => {
    it("should transliterate simple phrases correctly", async () => {
        const result = await romanizeJapanese("ありがとう");
        expect(result).toBe("arigatō");
    });

    it("should join split verb phrases like 'megumare ta' to 'megumareta'", async () => {
        const result = await romanizeJapanese("恵まれた");
        expect(result).toBe("megumareta");
    });

    it("should normalize whitespace", async () => {
        const result = await romanizeJapanese("私  は  元気 です");
        expect(result).toBe("watashi wa genkidesu");
    });
});
