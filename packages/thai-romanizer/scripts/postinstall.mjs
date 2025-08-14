import fs from "fs";
import path from "path";
import os from "os";
import https from "https";
import { fileURLToPath } from "url";
import { createHash } from "crypto";
import { mkdir, access, stat } from "fs/promises";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const pkgRoot = path.resolve(__dirname, "..");

const targetFileMap = {
    "darwin-arm64": "thai-mac-arm64",
    "darwin-x64": "thai-mac-x64",
    "linux-arm64": "thai-linux-arm64",
    "linux-x64": "thai-linux-x64",
    "win32-arm64": "thai-win-x64.exe",
    "win32-x64": "thai-win-x64.exe",
};

const resolveTargetFile = () => {
    const key = `${os.platform()}-${process.arch}`;
    const file = targetFileMap[key];

    if (!file) {
        console.warn(`No thai-romanizer binary for ${key}; skipping download.`);
        return null;
    }

    return file;
};

const getBinaryIfNeeded = async () => {
    const filename = resolveTargetFile();
    if (!filename) return; // unsupported platform/arch

    const pkg = JSON.parse(
        fs.readFileSync(path.join(pkgRoot, "package.json"), "utf8")
    );
    const tag = `@romanize-string/thai-romanizer@${pkg.version}`;
    const baseUrl = `https://github.com/rejyoung/romanize-string/releases/download/${tag}`;

    const destDir = path.join(pkgRoot, "dist", "bin");
    const destPath = path.join(destDir, filename);

    await mkdir(destDir, { recursive: true });

    try {
        await access(destPath);
        const st = await stat(destPath);
        if (st.size > 0) {
            // Already downloaded
            console.log("Binary already present. Skipping download.");
            return;
        }

        // size is 0 -> fall through to re-download
    } catch {}

    const url = `${baseUrl}/${filename}`;

    console.log(`[thai-romanizer] Downloading ${filename} …`);
    await new Promise((resolve, reject) => {
        const file = fs.createWriteStream(destPath, { mode: 0o755 });
        https
            .get(url, (res) => {
                if (res.statusCode === 302 || res.statusCode === 301) {
                    https.get(res.headers.location, (r2) =>
                        r2.pipe(file).on("finish", () => file.close(resolve))
                    );
                } else if (res.statusCode === 200) {
                    res.pipe(file).on("finish", () => file.close(resolve));
                } else {
                    reject(
                        new Error(`HTTP ${res.statusCode} ${res.statusMessage}`)
                    );
                }
            })
            .on("error", reject);
    });

    try {
        await fs.promises.chmod(destPath, 0o755);
    } catch {}

    await verifyBinary(baseUrl, filename, destPath);
};

const verifyBinary = async (baseUrl, filename, destPath) => {
    const shaUrl = `${baseUrl}/${filename}.sha256`;
    try {
        const listing = await new Promise((resolve, reject) => {
            let data = "";
            https
                .get(shaUrl, (res) => {
                    if (res.statusCode !== 200) {
                        reject(
                            new Error(
                                `HTTP ${res.statusCode} ${res.statusMessage}`
                            )
                        );
                        return;
                    }
                    res.setEncoding("utf8");
                    res.on("data", (chunk) => (data += chunk));
                    res.on("end", () => resolve(data));
                })
                .on("error", reject);
        });

        const expectedHash = listing.trim().split(/\s+/)[0];
        const hasher = createHash("sha256");
        await new Promise((resolve, reject) => {
            const rs = fs.createReadStream(destPath);
            rs.on("data", (chunk) => hasher.update(chunk));
            rs.on("end", () => {
                resolve();
            });
            rs.on("error", reject);
        });

        const actualHash = hasher.digest("hex");

        if (actualHash !== expectedHash) {
            // Delete the binary
            await fs.promises.rm(destPath, { force: true });
            const msg = `[thai-romanizer] Checksum mismatch for ${filename}. Expected ${expectedHash}, got ${actualHash}`;
            console.warn(msg, "Falling back at runtime.");
            return; // leave without a binary; your runtime will use fallback
        }
    } catch (error) {
        console.warn(
            "[thai-romanizer] Could not verify checksum:",
            e?.message || e
        );
    }
};

getBinaryIfNeeded().catch((err) =>
    console.warn(
        "[thai-romanizer] Postinstall error; will use fallback at runtime:",
        err?.message || err
    )
);
