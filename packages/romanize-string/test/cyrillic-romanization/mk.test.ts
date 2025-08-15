import { describe, expect, it } from "@jest/globals";
import { romanizeCyrillic } from "../../src/transliterators/cyrillic-romanization";

describe("Macedonian (mk)", () => {
    it("should transliterate digraphs correctly", () => {
        expect(romanizeCyrillic("ѓавол", "mk")).toBe("gjavol");
        expect(romanizeCyrillic("ќофти", "mk")).toBe("ḱofti");
        expect(romanizeCyrillic("љубов", "mk")).toBe("ljubov");
    });
});
