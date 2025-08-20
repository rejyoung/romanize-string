import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

// __filename equivalent
const __filename = fileURLToPath(import.meta.url);

// __dirname equivalent
const __dirname = path.dirname(__filename);

const out = `
'use strict';
const mod = require('./index.js');
const d = mod && mod.__esModule ? mod.default : mod;
if (d != null && (typeof d === 'function' || typeof d === 'object')) {
    Object.assign(d, mod)
}
    module.exports = d
`;

const target = path.join(__dirname, "..", "dist", "cjs", "index.cjs");

fs.mkdirSync(path.dirname(target), { recursive: true });
fs.writeFileSync(target, out.trimStart(), "utf8");
console.log("[postbuild] wrote", path.relative(process.cwd(), target));
