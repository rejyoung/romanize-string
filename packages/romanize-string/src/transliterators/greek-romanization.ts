const greekToLatinBaseMap = {
    Α: "A",
    Β: "V",
    Γ: "G",
    Δ: "D",
    Ε: "E",
    Ζ: "Z",
    Η: "I",
    Θ: "Th",
    Ι: "I",
    Κ: "K",
    Λ: "L",
    Μ: "M",
    Ν: "N",
    Ξ: "X",
    Ο: "O",
    Π: "P",
    Ρ: "R",
    Σ: "S",
    Τ: "T",
    Υ: "Y",
    Φ: "F",
    Χ: "Ch",
    Ψ: "Ps",
    Ω: "O",

    α: "a",
    β: "v",
    γ: "g",
    δ: "d",
    ε: "e",
    ζ: "z",
    η: "i",
    θ: "th",
    ι: "i",
    κ: "k",
    λ: "l",
    μ: "m",
    ν: "n",
    ξ: "x",
    ο: "o",
    π: "p",
    ρ: "r",
    σ: "s",
    ς: "s",
    τ: "t",
    υ: "y",
    φ: "f",
    χ: "ch",
    ψ: "ps",
    ω: "o",

    // Diaeresis forms — same in both modes
    ϊ: "i",
    ΐ: "i",
    ϋ: "y",
    ΰ: "y",
    Ϊ: "I",
    Ϋ: "Y",
};
const greekToLatinPlainMap = {
    ά: "a",
    έ: "e",
    ή: "i",
    ί: "i",
    ό: "o",
    ύ: "y",
    ώ: "o",
    Ά: "A",
    Έ: "E",
    Ή: "I",
    Ί: "I",
    Ό: "O",
    Ύ: "Y",
    Ώ: "O",
};

const greekToLatinAccentedMap = {
    ά: "á",
    έ: "é",
    ή: "í",
    ί: "í",
    ό: "ó",
    ύ: "ý",
    ώ: "ó",
    Ά: "Á",
    Έ: "É",
    Ή: "Í",
    Ί: "Í",
    Ό: "Ó",
    Ύ: "Ý",
    Ώ: "Ó",
};

export const romanizeGreek = (
    input: string,
    omitDiacritics?: boolean
): string => {
    // Normalize all-uppercase Greek words to sentence case
    const tokens = input.split(/(\p{L}+)/gu);
    input = tokens
        .map((token) => {
            if (!/\p{L}/u.test(token)) return token;
            const isAllGreekCaps = /^[Α-ΩΆΈΉΊΌΎΏΪΫ]+$/.test(
                token.replace(/[^\p{L}]/gu, "")
            );
            return isAllGreekCaps
                ? token.charAt(0) + token.slice(1).toLowerCase()
                : token;
        })
        .join("");

    // Handle ου
    input = input.replace(/ου/g, "ou").replace(/ΟΥ/g, "OU");

    // Handle ευ/αυ based on voicing of next consonant
    const voicelessConsonants = /[πκξστφχψθ]/i;
    input = input.replace(/ευ(?=[^αειουηω\s])/gi, (match) => {
        const nextIndex = input.indexOf(match) + match.length;
        const nextChar = input[nextIndex] || "";
        const isVoiceless = voicelessConsonants.test(nextChar);
        const isUpper = match[0] === "Ε";
        return isVoiceless ? (isUpper ? "Ef" : "ef") : isUpper ? "Ev" : "ev";
    });
    input = input.replace(/αυ(?=[^αειουηω\s])/gi, (match) => {
        const nextIndex = input.indexOf(match) + match.length;
        const nextChar = input[nextIndex] || "";
        const isVoiceless = voicelessConsonants.test(nextChar);
        const isUpper = match[0] === "Α";
        return isVoiceless ? (isUpper ? "Af" : "af") : isUpper ? "Av" : "av";
    });

    // Consonant digraphs and position-sensitive rules
    input = input
        // Word-initial μπ, ντ, γκ → b, d, g (punctuation-aware)
        .replace(/(^|[\s.,:;!?()«»"'])μπ/gi, (_, prefix) => `${prefix}b`)
        .replace(/(^|[\s.,:;!?()«»"'])ντ/gi, (_, prefix) => `${prefix}d`)
        .replace(/(^|[\s.,:;!?()«»"'])γκ/gi, (_, prefix) => `${prefix}g`)

        // Internal μπ, ντ, γκ → mp, nt, ng
        .replace(/μπ/gi, "mp")
        .replace(/ντ/gi, "nt")
        .replace(/γκ/gi, "ng")

        // γγ → ng (case sensitive)
        .replace(/γγ/g, "ng")
        .replace(/Γγ/g, "Ng")
        .replace(/γΓ/g, "nG")
        .replace(/ΓΓ/g, "NG")

        // τζ, τσ
        .replace(/τζ/gi, "tz")
        .replace(/τσ/gi, "ts");

    // Soft gamma before front vowels
    input = input.replace(/Γ(?=[αιεηι])/g, "Y").replace(/γ(?=[αιεηι])/g, "y");

    return input
        .split("")
        .map((char) => {
            if (!omitDiacritics && greekToLatinAccentedMap[char])
                return greekToLatinAccentedMap[char];
            if (omitDiacritics && greekToLatinPlainMap[char])
                return greekToLatinPlainMap[char];
            if (greekToLatinBaseMap[char]) return greekToLatinBaseMap[char];
            return char;
        })
        .join("");
};
