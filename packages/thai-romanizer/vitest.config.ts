import { defineConfig } from "vitest/config";
import path from "node:path";
import { fileURLToPath } from "node:url";
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default defineConfig({
    test: {
        environment: "node",
        include: ["**/*.test.{ts,tsx,js,jsx}"],
        globals: true,
        clearMocks: true,
    },
});
