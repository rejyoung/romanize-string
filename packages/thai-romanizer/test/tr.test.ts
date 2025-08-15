import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";

// Mocks that are shared across tests
vi.mock("romanize-string/plugins", () => ({
    registerPlugin: vi.fn(),
}));

// Mock the child_process spawnSync used by thai-romanizer
vi.mock("child_process", () => ({
    spawnSync: vi.fn(),
}));

// We'll dynamically mock fs/promises.access per test
vi.mock("fs/promises", () => ({
    access: vi.fn(),
}));

// Mock the internal import path used by setup.ts ("./thai-romanizer.js")
vi.mock("../src/thai-romanizer.js", async () => {
    const actual = await vi.importActual<object>("../src/thai-romanizer");
    return {
        ...(actual as any),
    };
});

import * as os from "os";
import { spawnSync } from "child_process";
import { access } from "fs/promises";
import { registerPlugin } from "romanize-string/plugins";

import * as setupMod from "../src/setup";
import { thaiRomanizer } from "../src/thai-romanizer";

describe("thai-romanizer plugin integration", () => {
    const origArch = process.arch;
    let platformSpy: vi.SpyInstance;

    beforeEach(() => {
        vi.restoreAllMocks();
        // Reset exported binPath between tests
        (setupMod as any).binPath = undefined;

        // Default: darwin-x64 for deterministic binary name
        platformSpy = vi
            .spyOn(os, "platform")
            .mockReturnValue("darwin" as NodeJS.Platform);
        // @ts-ignore - defineProperty to override readonly arch for test
        Object.defineProperty(process, "arch", {
            value: "x64",
            configurable: true,
        });

        // Quiet console output in tests, but keep a hook if we want to assert later
        vi.spyOn(console, "warn").mockImplementation(() => {});
        vi.spyOn(console, "error").mockImplementation(() => {});
    });

    afterEach(() => {
        // restore arch
        Object.defineProperty(process, "arch", {
            value: origArch,
            configurable: true,
        });
        platformSpy?.mockRestore();
        vi.clearAllMocks();
    });

    it("setup registers the plugin when the binary exists", async () => {
        // Arrange
        (access as unknown as vi.Mock).mockResolvedValue(undefined);

        // Act
        await setupMod.setup();

        // Assert
        expect((setupMod as any).binPath).toBeTruthy();
        expect(registerPlugin).toHaveBeenCalledWith("th", expect.any(Function));
        expect(console.warn).not.toHaveBeenCalled();
    });

    it("setup warns and does not register when binary is missing", async () => {
        // Arrange
        (access as unknown as vi.Mock).mockRejectedValue(new Error("nope"));

        // Act
        await setupMod.setup();

        // Assert
        expect((setupMod as any).binPath).toBeUndefined();
        expect(registerPlugin).not.toHaveBeenCalled();
        expect(console.warn).toHaveBeenCalledWith(
            "Cannot register plugin. The thaiRomanizer binary is missing or was not successfully downloaded."
        );
    });

    it("getBinaryName mapping returns expected filename for darwin-x64", async () => {
        // Arrange
        (access as unknown as vi.Mock).mockResolvedValue(undefined);

        // Act
        await setupMod.setup();

        // Assert: the computed binPath should end with the expected filename
        const bp = (setupMod as any).binPath as string | undefined;
        expect(bp).toBeTruthy();
        expect(bp && bp.endsWith("thai-mac-x64")).toBe(true);
    });

    describe("thaiRomanizer behavior", () => {
        it("returns cleaned stdout on success (trims and fixes polite suffix spacing)", async () => {
            (setupMod as any).binPath = "/fake/path/thai-mac-x64";
            (spawnSync as unknown as vi.Mock).mockReturnValue({
                status: 0,
                stdout: "  kha / khrap  \n",
                stderr: "",
                error: undefined,
            });

            const out = await thaiRomanizer("สวัสดี");
            expect(out).toBe("kha/khrap");
            expect(console.error).not.toHaveBeenCalled();
        });

        it("returns input when spawnSync returns a non-zero status", async () => {
            (setupMod as any).binPath = "/fake/path/thai-mac-x64";
            (spawnSync as unknown as vi.Mock).mockReturnValue({
                status: 1,
                stdout: "",
                stderr: "boom",
                error: undefined,
            });

            const input = "ทดสอบ";
            const out = await thaiRomanizer(input);
            expect(out).toBe(input);
            expect(console.error).toHaveBeenCalled(); // error path logs
        });

        it("returns input when spawnSync returns an error", async () => {
            (setupMod as any).binPath = "/fake/path/thai-mac-x64";
            (spawnSync as unknown as vi.Mock).mockReturnValue({
                status: 0,
                stdout: "",
                stderr: "",
                error: new Error("python blew up"),
            });

            const input = "แบบทดสอบ";
            const out = await thaiRomanizer(input);
            expect(out).toBe(input);
            expect(console.error).toHaveBeenCalled();
        });

        it("returns input and logs when binPath is not set", async () => {
            (setupMod as any).binPath = undefined;
            const input = "สวัสดีครับ";
            const out = await thaiRomanizer(input);
            expect(out).toBe(input);
            expect(console.error).toHaveBeenCalled();
        });

        it("trims stdout whitespace", async () => {
            (setupMod as any).binPath = "/fake/path/thai-mac-x64";
            (spawnSync as unknown as vi.Mock).mockReturnValue({
                status: 0,
                stdout: "  sawa dee   \n",
                stderr: "",
                error: undefined,
            });

            const out = await thaiRomanizer("ทดสอบ");
            expect(out).toBe("sawa dee");
        });
    });
});
