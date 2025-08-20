import arabictransliterate from "arabic-transliterate";
import { farsiArabicPhoneticMap } from "../phonetic-maps/farsiArabicPhoneticMap.js";
import { urduArabicPhoneticMap } from "../phonetic-maps/urduArabicPhoneticMap.js";
import { PluginRegistrar } from "romanize-string/plugins";

export const romanizeArabic = (input: string): string => {
    // Step 1: Standardize Arabic script for Persian/Urdu (phonetic map, fallback chars, naive vowels)
    const standardized = standardizeArabicScript(input);

    // Step 2: Use arabic-transliterate to Romanize
    const transliterated = arabictransliterate(
        standardized,
        "arabic2latin",
        "Arabic"
    );

    return transliterated
        .replace(/-\s*/g, "-") // remove spaces after hyphens
        .replace(/\bal-lāh\b/, "Allāh") // replace al-lāh with Allāh
        .replace(/([,؛:])([^\s]|$)/g, "$1 $2"); // add a space after commas, semicolons, and colons
};

// Because Persian (Farsi) and Urdu omit short vowels, there is no existing library capable of transliterating them,
// only those that transliterate Arabic. This function compensates for that.

const standardizeArabicScript = (input: string): string => {
    let output = input;

    // Step 1. Perform whole-word substitutions for the most frequently used Farsi and Urdu words
    // that require the addition of short vowels or contain non-Arabic characters.

    const allKeys = [
        ...Object.keys(farsiArabicPhoneticMap),
        ...Object.keys(urduArabicPhoneticMap),
    ];
    allKeys.sort((a, b) => b.length - a.length);

    const wordPattern = allKeys.join("|");
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
    ٱ: "ا", // wasla-alef => standard alef (missing from arabic-transliterate)
    "ٰ": "ا", // dagger alef => standard alef (missing from arabic-transliterate)
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
    const ARABIC_DIACRITICS = /[\u064B-\u0652\u0670]/;
    // Skip edge cases (including the unvowelized words from the phonetic maps)
    if (/^(وی|فی|تْهے|ٱللّٰه)$/.test(word)) return word;

    // Word is already fully vowelized — skip
    if (/[َُِّٰ]/.test(word)) return word;

    let result = "";
    for (let i = 0; i < word.length; i++) {
        const char = word[i];
        const next = word[i + 1];
        // If the next character is a diacritic, skip adding a vowel
        if (ARABIC_DIACRITICS.test(next ?? "")) {
            result += char;
        } else {
            // Default to fatha for now (or adapt as needed)
            result += char + "َ";
        }
    }
    return result;
};

romanizeArabic.register = (pluginSetup: PluginRegistrar) => {
    pluginSetup();
};
