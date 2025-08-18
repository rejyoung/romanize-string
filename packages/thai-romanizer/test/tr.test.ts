import {
    describe,
    it,
    expect,
    vi,
    beforeEach,
    afterEach,
    type Mock,
} from "vitest";

// Mock the child_process spawnSync used by thai-romanizer
vi.mock("child_process", () => ({
    spawnSync: vi.fn(),
}));

// We'll dynamically mock fs.accessSync per test
vi.mock("fs", () => ({
    accessSync: vi.fn(),
    constants: { X_OK: 1, F_OK: 0, R_OK: 4, W_OK: 2 },
}));

// Mock the internal import path used by setup.ts ("./thai-romanizer.js")
vi.mock("../src/thai-romanizer.js", async () => {
    const actual = await vi.importActual<object>("../src/thai-romanizer");
    return {
        ...(actual as any),
    };
});

vi.mock("os", () => {
    const platform = vi.fn();
    return {
        default: { platform },
        platform,
    };
});

import * as os from "os";
import { spawnSync } from "child_process";
import { accessSync } from "fs";

// Global registration hook used by romanize-string core
const REGISTER = Symbol.for("romanize-string.registerPlugin");

let setupMod: typeof import("../src/setup.js");
let thaiRomanizer: typeof import("../src/thai-romanizer.js")["thaiRomanizer"];

describe("thai-romanizer plugin integration", () => {
    const origArch = process.arch;

    beforeEach(async () => {
        vi.restoreAllMocks();
        vi.resetModules();
        setupMod = await import("../src/setup.js");

        ({ thaiRomanizer } = await import("../src/thai-romanizer.js"));

        (os.platform as unknown as Mock).mockReturnValue("darwin");
        // @ts-ignore - defineProperty to override readonly arch for test
        Object.defineProperty(process, "arch", {
            value: "x64",
            configurable: true,
        });

        // Provide a mock global hook for plugin registration
        (globalThis as any)[REGISTER] = vi.fn();

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
        delete (globalThis as any)[REGISTER];
        vi.clearAllMocks();
    });

    it("setup registers the plugin when the binary exists", async () => {
        // Arrange
        (accessSync as unknown as Mock).mockImplementation(() => undefined);

        // Act
        await setupMod.setup();

        // Assert
        expect((setupMod as any).binPath).toBeTruthy();
        const register = (globalThis as any)[REGISTER] as Mock;
        expect(register).toHaveBeenCalledWith("th", expect.any(Function));
        expect(console.warn).not.toHaveBeenCalled();
    });

    it("setup warns and does not register when binary is missing", async () => {
        // Arrange
        (accessSync as unknown as Mock).mockImplementation(() => {
            throw new Error("nope");
        });

        // Act
        await setupMod.setup();

        // Assert
        expect((setupMod as any).binPath).toBeUndefined();
        const register = (globalThis as any)[REGISTER] as Mock;
        expect(register).not.toHaveBeenCalled();
        expect(console.warn).toHaveBeenCalledWith(
            "Cannot register plugin. The thaiRomanizer binary is missing or was not successfully downloaded."
        );
    });

    it("getBinaryName mapping returns expected filename for darwin-x64", async () => {
        // Arrange
        (accessSync as unknown as Mock).mockImplementation(() => undefined);

        // Act
        await setupMod.setup();

        // Assert: the computed binPath should end with the expected filename
        const bp = (setupMod as any).binPath as string | undefined;
        expect(bp).toBeTruthy();
        expect(bp && bp.endsWith("thai-mac-x64")).toBe(true);
    });

    describe("thaiRomanizer behavior", () => {
        it("returns cleaned stdout on success (trims and fixes polite suffix spacing)", async () => {
            (spawnSync as unknown as Mock).mockReturnValue({
                status: 0,
                stdout: "  kha / khrap  \n",
                stderr: "",
                error: undefined,
            });

            await setupMod.setup();
            const out = await thaiRomanizer("สวัสดี");
            expect(out).toBe("kha/khrap");
            expect(console.error).not.toHaveBeenCalled();
        });

        it("returns input when spawnSync returns a non-zero status", async () => {
            (spawnSync as unknown as Mock).mockReturnValue({
                status: 1,
                stdout: "",
                stderr: "boom",
                error: undefined,
            });

            await setupMod.setup();
            const input = "ทดสอบ";
            const out = await thaiRomanizer(input);
            expect(out).toBe(input);
            expect(console.error).toHaveBeenCalled(); // error path logs
        });

        it("returns input when spawnSync returns an error", async () => {
            (spawnSync as unknown as Mock).mockReturnValue({
                status: 0,
                stdout: "",
                stderr: "",
                error: new Error("python blew up"),
            });

            await setupMod.setup();
            const input = "แบบทดสอบ";
            const out = await thaiRomanizer(input);
            expect(out).toBe(input);
            expect(console.error).toHaveBeenCalled();
        });

        it("returns input and logs when binPath is not set", async () => {
            const input = "สวัสดีครับ";
            const out = await thaiRomanizer(input);
            expect(out).toBe(input);
            expect(console.error).toHaveBeenCalled();
        });

        it("trims stdout whitespace", async () => {
            (spawnSync as unknown as Mock).mockReturnValue({
                status: 0,
                stdout: "  sawa dee   \n",
                stderr: "",
                error: undefined,
            });

            await setupMod.setup();
            const out = await thaiRomanizer("ทดสอบ");
            expect(out).toBe("sawa dee");
        });
    });
});
