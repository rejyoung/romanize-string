import { describe, it, expect } from "vitest";
import { romanizeCyrillic } from "../../src/transliterators/cyrillic-romanization";

describe("Belarusian (be)", () => {
    it("should transliterate basic examples", () => {
        expect(romanizeCyrillic("мова", "be")).toBe("mova");
        expect(romanizeCyrillic("беларусь", "be")).toBe("bielarus");
    });

    it("should handle ў as ŭ", () => {
        expect(romanizeCyrillic("Беларусь сёння", "be")).toBe(
            "Bielarus syonnia"
        );
        expect(romanizeCyrillic("ўсход", "be")).toBe("uskhod");
    });

    it("should use ye/ie for е depending on position", () => {
        expect(romanizeCyrillic("елка", "be")).toBe("yelka");
        expect(romanizeCyrillic("шчавелевы", "be")).toBe("shchavielievy");
    });
});
