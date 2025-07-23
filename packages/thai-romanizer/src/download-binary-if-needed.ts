import fs from "fs";
import https from "https";
import { pipeline } from "stream/promises";
import path from "path";
import { mkdir, access } from "fs/promises";

export const downloadBinaryIfNeeded = async (name: string, dest: string) => {
    try {
        await access(dest); // Already downloaded
        return;
    } catch {}

    await mkdir(path.dirname(dest), { recursive: true });

    const url = `https://github.com/rejyoung/romanize-string/releases/latest/download/${name}`;
    const file = fs.createWriteStream(dest, { mode: 0o755 });

    await new Promise<void>((resolve, reject) => {
        https
            .get(url, async (res) => {
                try {
                    await pipeline(res, file);
                    resolve();
                } catch (err) {
                    reject(err);
                }
            })
            .on("error", reject);
    });
};
