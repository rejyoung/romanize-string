import { spawnSync } from "child_process";
import ThaiAnalyzer from "tnthai";
import { ensurePythonWithThaiLib } from "../utils/ensure-python-with-thai-lib.js";

const analyzer = new ThaiAnalyzer();

export const romanizeThai = (input: string) => {
    try {
        ensurePythonWithThaiLib();

        const { solution } = analyzer.segmenting(input);
        const segmentedString = solution
            .filter((word) => word.trim().length > 0)
            .join(" ")
            .replace(/\s+([.,!?;:])/g, "$1");

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

        return result.stdout.trim();
    } catch (err) {
        console.error("Thai transliteration failed.");
        console.error(err);
        return input;
    }
};
