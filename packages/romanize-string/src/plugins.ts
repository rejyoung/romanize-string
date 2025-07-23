// src/plugins.ts
export type RomanizerFn = (
    input: string,
    opts?: unknown
) => string | Promise<string>;

const pluginRegistry = new Map<string, RomanizerFn>();

export function registerPlugin(code: string, fn: RomanizerFn) {
    pluginRegistry.set(code, fn);
}

export function getPlugin(code: string) {
    return pluginRegistry.get(code);
}

// (optional) expose for debugging/tests
export const _pluginRegistry = pluginRegistry;
