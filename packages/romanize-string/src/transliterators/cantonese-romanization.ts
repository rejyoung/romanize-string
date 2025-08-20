import { getRoman } from "cantonese-romanisation";
import { PluginRegistrar } from "romanize-string/plugins";
const hanziRegex = /[\p{Script=Han}]/u;

export const romanizeCantonese = (input: string) => {
    let transliteration = "";
    let buffer = "";
    let lastWasHanzi = null;

    for (const char of input) {
        const isHanzi = hanziRegex.test(char);

        if (lastWasHanzi === null) {
            lastWasHanzi = isHanzi;
            buffer = char;
        } else if (isHanzi === lastWasHanzi) {
            buffer += char;
        } else {
            transliteration += lastWasHanzi
                ? getRoman(buffer)
                      .map((options) => options[0])
                      .join(" ")
                : buffer;
            buffer = char;
            lastWasHanzi = isHanzi;
        }
    }

    // Handle final buffer
    if (buffer) {
        transliteration += lastWasHanzi
            ? getRoman(buffer)
                  .map((options) => options[0])
                  .join(" ")
            : buffer;
    }

    return transliteration.replace(/\s+/g, " ").trim();
};

romanizeCantonese.register = (pluginSetup: PluginRegistrar) => {
    pluginSetup();
};
