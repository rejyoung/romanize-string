import { vi, describe, it, expect, beforeEach, afterEach } from "vitest";

// Mock child_process at module level so we can control spawnSync per test in ESM
vi.mock("node:child_process", async () => {
    const actual = await vi.importActual<typeof import("node:child_process")>(
        "node:child_process"
    );
    return {
        ...actual,
        spawnSync: vi.fn(),
    };
});

// Skip the real Python dependency check in unit tests
vi.mock("../../src/utils/ensure-python-with-thai-lib", () => ({
    ensurePythonWithThaiLib: vi.fn(async () => {}),
}));

import * as cp from "node:child_process";
import { romanizeThai } from "../../src/transliterators/thai-romanization";
import {
    _pluginRegistry,
    registerPlugin,
    getPlugin,
} from "romanize-string/plugins";

// Control segmentation to verify normalization & inputs to plugin
const segmentMock = vi.fn<(arg: { input: string }) => { solution: string[] }>(
    () => ({ solution: [] })
);
vi.mock("tnthai", () => ({
    default: class ThaiAnalyzerMock {
        segmenting(input: string) {
            return segmentMock({ input });
        }
    },
}));

// Helper to register a fake plugin with a predictable return
function registerFakePlugin(returnValue: string) {
    const plugin = vi.fn().mockReturnValue(returnValue);
    registerPlugin("th", plugin);
    return plugin;
}

beforeEach(() => {
    _pluginRegistry.clear();
    segmentMock.mockReset();
    (cp.spawnSync as unknown as any).mockReset?.();
});

afterEach(() => {
    (cp.spawnSync as unknown as any).mockReset?.();
});

describe("romanizeThai – with plugin", () => {
    it("passes a normalized, segmented string to the plugin (no space before punctuation)", () => {
        // Simulate segmenter returning tokens with punctuation separated
        segmentMock.mockReturnValueOnce({ solution: ["สวัสดี", ",", "ครับ"] });

        const plugin = registerFakePlugin("ignored");

        romanizeThai("ignored");

        // Expect plugin was called with string that has no space before comma
        expect(plugin).toHaveBeenCalledTimes(1);
        expect(plugin).toHaveBeenCalledWith("สวัสดี, ครับ");
    });

    it("removes spaces around polite-suffix separators returned by plugin output (e.g., 'a / b' -> 'a/b')", () => {
        // Segment to a simple token stream
        segmentMock.mockReturnValueOnce({ solution: ["สวัสดี", "ครับ"] });

        // Return value intentionally has spaces around '/'
        registerFakePlugin("sawasdee / khrap");

        const out = romanizeThai("ignored");
        expect(out).toBe("sawasdee/khrap");
    });

    it("returns empty string for empty input after segmentation", () => {
        segmentMock.mockReturnValueOnce({ solution: [] });
        registerFakePlugin("");

        expect(romanizeThai("")).toBe("");
    });
});

describe("romanizeThai – without plugin (fallback to local Python)", () => {
    it("calls the local Python script and uses its stdout, then applies post-processing", () => {
        // No plugin registered
        segmentMock.mockReturnValueOnce({ solution: ["foo", "bar"] });

        (cp.spawnSync as unknown as any).mockReturnValue({
            pid: 123,
            status: 0,
            stdout: "fallback / result",
            stderr: "",
        });

        const out = romanizeThai("ignored");

        // Ensure spawnSync was called and looks like Python was invoked with our script
        const calls = (cp.spawnSync as unknown as any).mock.calls;
        expect(calls.length).toBe(1);
        const [cmd, args] = calls[0];
        expect(typeof cmd).toBe("string");
        expect(/python/.test(String(cmd))).toBe(true);
        expect(Array.isArray(args)).toBe(true);
        const hasScript = (args as string[]).some((a) =>
            /python-thai-romanization\.(py|js)$/.test(a)
        );
        expect(hasScript).toBe(true);

        // Post-processing should remove spaces around '/'
        expect(out).toBe("fallback/result");
    });

    it("logs and returns input on failure (non-zero exit)", () => {
        segmentMock.mockReturnValueOnce({ solution: ["foo"] });

        (cp.spawnSync as unknown as any).mockReturnValue({
            pid: 123,
            status: 1,
            stdout: "",
            stderr: "Boom",
        });

        // Should fall back to returning the original input string
        expect(romanizeThai("foo")).toBe("foo");
    });
});

describe("romanizeThai.register", () => {
    it("awaits the provided setup function (which can register a plugin)", async () => {
        expect(getPlugin("th")).toBeUndefined();

        const setupFn = vi.fn(async () => {
            registerPlugin("th", () => "ok");
        });

        await (romanizeThai as any).register(setupFn);

        expect(setupFn).toHaveBeenCalledTimes(1);
        expect(typeof getPlugin("th")).toBe("function");
    });
});
