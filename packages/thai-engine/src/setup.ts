import { thaiEngine } from "./thai-engine.js";
import { fileURLToPath } from "url";
import os from "os";
import path from "path";
import { accessSync, constants } from "fs";

export let binPath: string | undefined;

export const setup = () => {
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

    try {
        // Ensure that binary exists at that path and is executable
        accessSync(binaryPath, constants.X_OK);

        binPath = binaryPath;

        const REGISTER = Symbol.for("romanize-string.registerPlugin");
        const registerPlugin = (globalThis as any)[REGISTER] as
            | ((code: string, fn: (s: string, o: string) => string) => void)
            | undefined;

        if (registerPlugin) {
            registerPlugin("th", thaiEngine);
        } else {
            console.warn(
                "The romanize-string plugin hook was not found; plugin not registered"
            );
        }
    } catch (error) {
        console.warn(
            "Cannot register plugin. The thaiEngine binary is missing or was not successfully downloaded."
        );
    }
};

const getBinaryName = (): string => {
    const filenameMap = {
        "darwin-arm64": "thai-mac-arm64",
        "darwin-x64": "thai-mac-x64",
        "linux-arm64": "thai-linux-arm64",
        "linux-x64": "thai-linux-x64",
        "win32-arm64": "thai-win-x64.exe",
        "win32-x64": "thai-win-x64.exe",
    };
    const key = `${os.platform()}-${process.arch}`;

    return filenameMap[key];
};
