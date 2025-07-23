import { romanizeGreek } from "../../src/transliterators/greek-romanization.js";

describe("romanizeGreek", () => {
    it("should transliterate basic Greek letters without diacritics", () => {
        expect(romanizeGreek("Καλημέρα", true)).toBe("Kalimera");
        expect(romanizeGreek("Ελλάδα", true)).toBe("Ellada");
    });

    it("should transliterate Greek letters with diacritics when enabled", () => {
        expect(romanizeGreek("Καλημέρα", false)).toBe("Kaliméra");
        expect(romanizeGreek("Ελλάδα", undefined)).toBe("Elláda");
    });

    it("should handle soft gamma before front vowels", () => {
        expect(romanizeGreek("γεία", true)).toBe("yeia");
        expect(romanizeGreek("Γιώργος", true)).toBe("Yiorgos");
    });

    it("should transliterate diphthongs ου, ευ, αυ correctly", () => {
        expect(romanizeGreek("ουρανός", true)).toBe("ouranos");
        expect(romanizeGreek("ευτυχία", true)).toBe("eftychia");
        expect(romanizeGreek("αυλή", true)).toBe("avli");
        expect(romanizeGreek("ΑΥΛΗ", true)).toBe("Avli");
    });

    it("should handle word-initial digraphs μπ, ντ, γκ", () => {
        expect(romanizeGreek("μπανάνα", true)).toBe("banana");
        expect(romanizeGreek("ντομάτα", true)).toBe("domata");
        expect(romanizeGreek("γκολ", true)).toBe("gol");
    });

    it("should handle internal digraphs μπ, ντ, γκ, γγ", () => {
        expect(romanizeGreek("λάμπα", true)).toBe("lampa");
        expect(romanizeGreek("πάντα", true)).toBe("panta");
        expect(romanizeGreek("αγκαλιά", true)).toBe("angalia");
        expect(romanizeGreek("άγγελος", true)).toBe("angelos");
    });

    it("should transliterate complex sentence", () => {
        const input = "Καληνύχτα και όνειρα γλυκά.";
        const outputPlain = "Kalinychta kai oneira glyka.";
        const outputAccented = "Kalinýchta kai óneira glyká.";

        expect(romanizeGreek(input, true)).toBe(outputPlain);
        expect(romanizeGreek(input, false)).toBe(outputAccented);
    });
});
