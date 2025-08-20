// src/plugins.ts
export type PluginFn = (input: string, ...args: unknown[]) => string;

export type PluginRegistrar = () => void;

const pluginRegistry = new Map<string, PluginFn>();

export function getPlugin(code: string) {
    return pluginRegistry.get(code);
}

const REGISTER = Symbol.for("romanize-string.registerPlugin");

(globalThis as any)[REGISTER] = (key: string, fn: PluginFn) => {
    pluginRegistry.set(key, fn);
};

// (optional) expose for debugging/tests
export const _pluginRegistry = pluginRegistry;
