import { describe, it, expect, beforeEach, vi } from "vitest";

// Create mocks in a hoisted context so they exist before vi.mock runs
const { mockSpawnSync, mockEnsure } = vi.hoisted(() => {
    return {
        mockSpawnSync: vi.fn(),
        mockEnsure: vi.fn(),
    };
});

vi.mock("child_process", () => ({
    spawnSync: mockSpawnSync,
}));

vi.mock("../../src/utils/ensure-python-with-thai-lib.js", () => ({
    ensurePythonWithThaiLib: mockEnsure,
}));

import { romanizeThai } from "../../src/transliterators/thai-romanization.js";
import { _pluginRegistry } from "../../src/plugins.js";

beforeEach(() => {
    _pluginRegistry.clear();
    mockSpawnSync.mockReset();
    mockEnsure.mockReset();
});

describe("romanizeThai", () => {
    it("uses a registered plugin and normalizes polite suffix spacing", () => {
        _pluginRegistry.set("th", () => "sawatdi khrab / kha");

        const input = "สวัสดีครับ/ค่ะ";
        const result = romanizeThai(input);

        expect(result).toBe("sawatdi khrab/kha");
        expect(mockEnsure).not.toHaveBeenCalled();
        expect(mockSpawnSync).not.toHaveBeenCalled();
    });

    it("falls back to Python when no plugin is registered", () => {
        mockSpawnSync.mockReturnValue({
            status: 0,
            stdout: "sawatdi khrab / kha",
            stderr: "",
        } as any);

        const input = "สวัสดีครับ/ค่ะ";
        const result = romanizeThai(input);

        expect(result).toBe("sawatdi khrab/kha");
        expect(mockEnsure).toHaveBeenCalledTimes(1);
        expect(mockSpawnSync).toHaveBeenCalledTimes(1);

        const call = mockSpawnSync.mock.calls[0];
        expect(call[0]).toBe("python3");
        expect(call[1]).toContain(
            "src/transliterators/python-thai-romanization.py"
        );
    });

    it("returns the original input when Python execution fails", () => {
        mockSpawnSync.mockReturnValue({
            status: 1,
            stdout: "",
            stderr: "Some error",
        } as any);

        const consoleErr = vi
            .spyOn(console, "error")
            .mockImplementation(() => {});

        const input = "สวัสดีครับ/ค่ะ สบายดีไหม?";
        const result = romanizeThai(input);

        expect(result).toBe(input);
        expect(mockEnsure).toHaveBeenCalledTimes(1);
        expect(mockSpawnSync).toHaveBeenCalledTimes(1);

        consoleErr.mockRestore();
    });

    it("trims surrounding whitespace from the romanizer output", () => {
        _pluginRegistry.set("th", () => "  sawatdi   ");

        const result = romanizeThai("สวัสดี");
        expect(result).toBe("sawatdi");
    });
});
