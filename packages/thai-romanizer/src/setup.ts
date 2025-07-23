import { registerPlugin } from "romanize-string/plugins";
import { thaiRomanizer } from "./thai-romanizer.js";
import os from "os";
import path from "path";
import { downloadBinaryIfNeeded } from "./download-binary-if-needed.js";

export let binPath: string | undefined;

export const setup = async () => {
    const platform = os.platform();
    const binaryName = getBinaryName(platform);
    const binaryPath = path.join(__dirname, "bin", binaryName);

    await downloadBinaryIfNeeded(binaryName, binaryPath);

    binPath = binaryPath;

    registerPlugin("th", thaiRomanizer);
};

const getBinaryName = (platform: string): string => {
    let name: string;
    switch (platform) {
        case "win32":
            name = "thai-win.exe";
            break;
        case "darwin":
            name = "thai-mac";
            break;
        case "linux":
            name = "thai-linux";
            break;
        default:
            throw new Error(`Unsupported platform: ${platform}`);
    }
    return name;
};
