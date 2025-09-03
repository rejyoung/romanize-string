import { spawnSync } from "child_process";
import os from "os";
import { fileURLToPath } from "url";
import path from "path";

export const detectLanguage = (str: string) => {
    const binaryPath = getBinaryPath();

    try {
        const result = spawnSync(binaryPath, [str], {
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

        return result.stdout;
    } catch (err) {
        throw new Error("Language detection failed.", { cause: err });
    }
};

const getBinaryPath = (): string => {
    const binaryName = getBinaryName();

    // Resolve current file/dir in both ESM and CJS without using the `import.meta` token
    const currentFilename =
        // In CJS, __filename exists; in ESM it does not
        typeof __filename !== "undefined"
            ? __filename
            : // Use eval so TypeScript doesn't reject `import.meta` when compiling CJS
              fileURLToPath((eval("import.meta") as any).url);
    const dir =
        typeof __dirname !== "undefined"
            ? __dirname
            : path.dirname(currentFilename);
    const parentDir = path.dirname(dir);

    const binaryPath = path.join(parentDir, "bin", binaryName);

    return binaryPath;
};

const getBinaryName = (): string => {
    const filenameMap = {
        "darwin-arm64": "ld-mac-arm64",
        "darwin-x64": "ld-mac-x64",
        "linux-arm64": "ld-linux-arm64",
        "linux-x64": "ld-linux-x64",
        "win32-arm64": "ld-win-x64.exe",
        "win32-x64": "ld-win-x64.exe",
    };
    const key = `${os.platform()}-${process.arch}`;

    return filenameMap[key];
};
