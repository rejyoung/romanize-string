import { spawnSync } from "child_process";
import { binPath } from "./setup.js";

export const thaiRomanizer = async (input: string) => {
    try {
        if (!binPath) {
            throw new Error(
                "Thai romanizer not registered with romanize-string library"
            );
        }

        const result = spawnSync(binPath, [input], {
            encoding: "utf-8",
            input: "",
        });

        if (result.error) {
            throw new Error(`Python error: ${result.error.message}`);
        }

        if (result.status !== 0) {
            throw new Error(
                `Python script exited with code ${result.status}: ${result.stderr}`
            );
        }

        return result.stdout
            .replace(/\b(\w{1,10})\s*\/\s*(\w{1,10})\b/g, "$1/$2") // Remove spaces around polite suffix separators
            .trim();
    } catch (err) {
        console.error("Thai transliteration failed.");
        console.error(err);
        return input;
    }
};
