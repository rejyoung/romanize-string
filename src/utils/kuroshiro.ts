import kuroshiroPkg from "kuroshiro";
import KuromojiAnalyzer from "kuroshiro-analyzer-kuromoji";

const Kuroshiro = (kuroshiroPkg as any).default ?? kuroshiroPkg;

// Japanese Script Converter (Katakana/Kanji => Hiragana)

const kuroshiro = new Kuroshiro();
let initialized = false;

export async function initKuroshiro() {
    if (!initialized) {
        await kuroshiro.init(new KuromojiAnalyzer());
        initialized = true;
    }
}

export { kuroshiro };
