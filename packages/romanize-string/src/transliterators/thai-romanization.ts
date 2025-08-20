import { spawnSync } from "child_process";
import ThaiAnalyzer from "tnthai";
import { ensurePythonWithThaiLib } from "../utils/ensure-python-with-thai-lib.js";
import { getPlugin, PluginRegistrar } from "../plugins.js";

const analyzer = new ThaiAnalyzer();

export const romanizeThai = (input: string) => {
    const { solution } = analyzer.segmenting(input);

    const separator = "\u{F0000}\u{F0001}";
    const segmentedString = solution
        .filter((word) => word.trim().length > 0)
        .map((w) => w.replaceAll(separator, "\\" + separator))
        .join(separator); // Join tokens with a two-codepoint sentinel so the Python code can split it cleanly

    const plugin = getPlugin("th");

    let transliterated;
    if (plugin) {
        transliterated = plugin(segmentedString, input);
    } else {
        transliterated = runLocalPythonRomanizer(segmentedString, input);
    }

    const romanizedString = transliterated
        .replace(/\b(\w{1,10})\s*\/\s*(\w{1,10})\b/g, "$1/$2") // Remove spaces around polite suffix separators
        .trim();

    return romanizedString;
};

romanizeThai.register = (pluginSetup: PluginRegistrar) => {
    pluginSetup();
};

const runLocalPythonRomanizer = (
    segmentedString: string,
    original: string
): string => {
    try {
        ensurePythonWithThaiLib();

        const result = spawnSync(
            "python3",
            [
                "src/transliterators/python-thai-romanization.py",
                segmentedString,
            ],
            {
                encoding: "utf-8",
                input: "",
            }
        );

        if (result.error) {
            throw new Error(`Python error: ${result.error.message}`);
        }

        if (result.status !== 0) {
            throw new Error(
                `Python script exited with code ${result.status}: ${result.stderr}`
            );
        }

        return result.stdout;
    } catch (err) {
        console.error("Thai transliteration failed.");
        console.error(err);
        return original;
    }
};
