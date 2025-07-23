import { spawnSync } from "child_process";
import ThaiAnalyzer from "tnthai";
import { ensurePythonWithThaiLib } from "../utils/ensure-python-with-thai-lib.js";
import { getPlugin } from "../plugins.js";

const analyzer = new ThaiAnalyzer();

export const romanizeThai = (input: string) => {
    const { solution } = analyzer.segmenting(input);
    const segmentedString = solution
        .filter((word) => word.trim().length > 0)
        .join(" ")
        .replace(/\s+([.,!?;:])/g, "$1");

    const plugin = getPlugin("th");

    let transliterated;
    if (plugin) {
        transliterated = plugin(segmentedString);
    } else {
        transliterated = runLocalPythonRomanizer(segmentedString);
    }

    const romanizedString = transliterated
        .replace(/\b(\w{1,10})\s*\/\s*(\w{1,10})\b/g, "$1/$2") // Remove spaces around polite suffix separators
        .trim();

    return romanizedString;
};

romanizeThai.register = async (pluginSetup: () => Promise<void>) => {
    await pluginSetup();
};

const runLocalPythonRomanizer = (input: string): string => {
    try {
        ensurePythonWithThaiLib();

        const result = spawnSync(
            "python3",
            ["src/transliterators/python-thai-romanization.py", input],
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
        return input;
    }
};
