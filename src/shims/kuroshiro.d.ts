declare module "kuroshiro" {
  export interface ConvertOptions {
    to?: "hiragana" | "katakana" | "romaji";
    mode?: "normal" | "spaced" | "okurigana" | "furigana";
    romajiSystem?: "nippon" | "passport" | "hepburn";
    delimiter_start?: string;
    delimeter_end?: string;
  }
  export interface Util {
    hasJapanese(str: string): boolean;
    isHiragana(str: string): boolean;
    isKatakana(str: string): boolean;
    isKana(str: string): boolean;
    isKanji(str: string): boolean;
    hasHiragana(str: string): boolean;
    hasKatakana(str: string): boolean;
    hasKana(str: string): boolean;
    hasKanji(str: string): boolean;
    kanaToHiragna(str: string): string;
    kanaToKatakana(str: string): string;
    kanaToRomaji(str: string): string;
  }
  export default class Kuroshiro {
    init(analyzer: any): Promise<void>;
    convert(string: string, options?: ConvertOptions): Promise<string>;

    static Util: Util;
  }
}
