import { registerPlugin } from "romanize-string/plugins";
import { thaiRomanizer } from "./thai-romanizer.js";
import { fileURLToPath } from "url";
import os from "os";
import path from "path";
import { access } from "fs/promises";

export let binPath: string | undefined;

export const setup = async () => {
    const binaryName = getBinaryName();

    const currentFilename = fileURLToPath(import.meta.url);
    const dir = path.dirname(currentFilename);
    const parentDir = path.dirname(dir);

    const binaryPath = path.join(parentDir, "bin", binaryName);

    try {
        await access(binaryPath);

        binPath = binaryPath;
        registerPlugin("th", thaiRomanizer);
    } catch (error) {
        console.warn(
            "Cannot register plugin. The thaiRomanizer binary is missing or was not successfully downloaded."
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
