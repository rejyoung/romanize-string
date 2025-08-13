import { romanizeCyrillic } from "../../src/transliterators/cyrillic-romanization";
import { describe, it, expect } from "vitest";

/**
 * Adapted from cyrillic-to-translit-js
 * Original author: Aleksandr Filatov
 * License: MIT
 * https://github.com/greybax/cyrillic-to-translit-js
 */

describe("mn", () => {
    it("test ө ү й", () => {
        expect(romanizeCyrillic("хөөрөг", "mn")).toBe("khoorog");
        expect(romanizeCyrillic("гуталын", "mn")).toBe("gutalyn");
        expect(romanizeCyrillic("үйлдвэр", "mn")).toBe("uildver");
        expect(romanizeCyrillic("пүрэв", "mn")).toBe("purev");
    });
});
