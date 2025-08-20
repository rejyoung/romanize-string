import {
    normalize as koreanNormalize,
    tokenize as koreanTokenize,
} from "oktjs";

import { romanize } from "../vendor/romanize/korean/src/index.js";
import { PluginRegistrar } from "romanize-string/plugins";

export const romanizeKorean = (string: string): string => {
    // Normalize and tokenize string, omitting any extra white spaces
    const normalized = koreanNormalize(string);
    const tokens = koreanTokenize(normalized).filter((t) => t.text.trim());

    // Romanize each token individually
    const romanizedTokens = tokens.map((token) => romanize(token.text));

    // Use the index of each romanizedToken to access the pos property of the corresponding item in the tokens array.
    // If the token at the current index is a josa (Korean case marker), join it to the preceding noun with a hyphen.
    const josaJoined = romanizedTokens.reduce<string[]>(
        (acc, romToken, idx) => {
            if (tokens[idx].pos === "Josa" && acc.length) {
                acc[acc.length - 1] += `-${romToken}`;
            } else {
                acc.push(romToken);
            }
            return acc;
        },
        []
    );

    // Join the processed array of tokens into a single string, omitting any additional extra white spaces
    // that may have crept in during the process and removing white spaces before punctuation.
    return josaJoined
        .join(" ")
        .replace(/\s+/g, " ")
        .replace(/\s+([.,!?！？。、])/g, "$1");
};

romanizeKorean.register = (pluginSetup: PluginRegistrar) => {
    pluginSetup();
};
