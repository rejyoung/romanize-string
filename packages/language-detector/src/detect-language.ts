import { spawnSync } from "child_process";

export const detectLanguage = (str: string) => {
    try {
        const result = spawnSync(
            "python3",
            ["python/language_detector.py", str],
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
        throw new Error("Language detection failed.", { cause: err });
    }
};
