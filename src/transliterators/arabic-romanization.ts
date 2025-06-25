import arabictransliterate from "arabic-transliterate";
import { farsiArabicPhoneticMap } from "../phonetic-maps/farsiArabicPhoneticMap.js";
import { urduArabicPhoneticMap } from "../phonetic-maps/urduArabicPhoneticMap.js";

export const romanizeArabic = (input: string): string => {
    const transliteratedTitle = arabictransliterate(
        standardizeArabicScript(input),
        "arabic2latin",
        "Arabic"
    ).replace(/-\s*/g, " ");
    return transliteratedTitle;
};

///////////////

// Because Persian (Farsi) and Urdu omit short vowels, there is no existing library capable of transliterating them,
// only those that transliterate Arabic. This function compensates for that.

const standardizeArabicScript = (input: string): string => {
    let output = input;

    // Step 1. Perform whole-word substitutions for the most frequently used Farsi and Urdu words
    // that require the addition of short vowels or contain non-Arabic characters.

    const farsiKeys = Object.keys(farsiArabicPhoneticMap).sort(
        (a, b) => b.length - a.length
    );
    const urduKeys = Object.keys(urduArabicPhoneticMap).sort(
        (a, b) => b.length - a.length
    );

    const wordPattern = farsiKeys.join("|") + "|" + urduKeys.join("|");
    const wordRegex = new RegExp(wordPattern, "g");

    output = input.replace(
        wordRegex,
        (match) =>
            farsiArabicPhoneticMap[match] ??
            urduArabicPhoneticMap[match] ??
            match
    );

    // Step 2. Normalize any remaining Urdu- or Farsi-specific characters to their Arabic equivalents.
    const characterPattern = Object.keys(fallbackCharMap).join("|");
    const characterRegex = new RegExp(characterPattern, "g");
    output = output.replace(
        characterRegex,
        (match) => fallbackCharMap[match] ?? match
    );

    // Step 3. Perform naive vowelization on any words lacking short vowels and not already treated in step 1.
    output = output
        .split(" ")
        .map((word) => naiveVowelize(word))
        .join(" ");

    return output;
};

const fallbackCharMap: Record<string, string> = {
    پ: "ب",
    چ: "ج",
    ژ: "ش",
    گ: "ك",
    ں: "ن",
    ک: "ك",
    ی: "ي",
    ے: "ي",
    ھ: "ه",
    ۀ: "ه",
    ہ: "ه",
    ؤ: "و",
    ئ: "ي",
    ﮨ: "ه",
    ﮩ: "ه",
    ﮪ: "ه",
    ﮫ: "ه",
};

const naiveVowelize = (word: string): string => {
    // Skip edge cases (including the unvowelized words from the phonetic maps)
    if (/^(وی|فی|تْهے،|ٱللّٰه)$/.test(word)) return word;

    // Already contains a short vowel — skip
    if (/[َُِ]/.test(word)) return word;

    // Rule 1: Add 'َ' after first consonant
    // Rule 2: If ends with ی or و, add 'ِ' before ی or 'ُ' before و
    return word
        .replace(/^([^َُِ])/, "$1َ") // Add fatha after first character
        .replace(/([^َُِ])ی$/, "$1ِی") // Add kasra before ی
        .replace(/([^َُِ])و$/, "$1ُو"); // Add damma before و
};
