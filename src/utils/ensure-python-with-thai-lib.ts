import { execSync } from "child_process";

export const ensurePythonWithThaiLib = (): void => {
    try {
        // Check if Python 3 is installed
        execSync("python3 --version", { stdio: "ignore" });
    } catch {
        throw new Error(
            "Python 3 is not installed. Thai transliteration requires Python 3 and the 'pythainlp' library."
        );
    }

    try {
        // Check if pythainlp is installed
        execSync('python3 -c "import pythainlp"', { stdio: "ignore" });
    } catch {
        throw new Error(
            "The 'pythainlp' library is not installed. Please run 'pip3 install pythainlp' to enable Thai transliteration."
        );
    }
};
