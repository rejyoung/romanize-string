// src/plugins.ts
export type RomanizerFn = (input: string, opts?: unknown) => string;

const pluginRegistry = new Map<string, RomanizerFn>();

export function getPlugin(code: string) {
    return pluginRegistry.get(code);
}

const REGISTER = Symbol.for("romanize-string.registerPlugin");

(globalThis as any)[REGISTER] = (key: string, fn: RomanizerFn) => {
    pluginRegistry.set(key, fn);
};

// (optional) expose for debugging/tests
export const _pluginRegistry = pluginRegistry;
