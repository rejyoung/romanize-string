import { romanizeKorean } from "../../src/transliterators/korean-romanization";
import { HangulSyllable } from "../../src/vendor/romanize/korean/src/lib/decompose-hangul";
import { romanize } from "../../src/vendor/romanize/korean/src";

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

describe("HangulSyllable", () => {
    it("should decompose 훌 into choseong, jungseong, and jongseong", () => {
        const hangul = new HangulSyllable("훌");
        expect([hangul.initial, hangul.medial, hangul.final]).toEqual([
            "ᄒ",
            "ᅮ",
            "ᆯ",
        ]);
    });
});

describe("romanizeHangul1", () => {
    it("should correctly romanize common syllables and sentences", () => {
        expect(romanize("훌")).toEqual("hul");
        expect(romanize("버")).toEqual("beo");
        expect(
            romanize(`훌쩍 커버렸어
        함께한 기억처럼
        널 보는 내 마음은
        어느새 여름 지나 가을`)
        ).toEqual(`huljjeok keobeoryeosseo
    hamkkehan gieokcheoreom
    neol boneun nae maeumeun
    eoneusae yeoreum jina gaeul`);
    });
});

describe("romanizeHangul2", () => {
    it("should match expected romanizations for multiple words and phrases", () => {
        const tests = {
            안녕하세요: "annyeonghaseyo",
            안녕: "annyeong",
            안녕하십니까: "annyeonghasimnikka",
            좋고: "joko",
            놓다: "nota",
            잡혀: "japyeo",
            낳지: "nachi",
        };
        for (const [hangul, romanized] of Object.entries(tests)) {
            expect(romanize(hangul)).toEqual(romanized);
        }
    });
});
