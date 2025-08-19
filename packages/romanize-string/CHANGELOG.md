# romanize-string

## 1.3.0

### Minor Changes

- ff8e336: Thai Romanization Plugin & Core Integration

  - Adds support for plugins
    - Adds plugin registry and registration functions that utilize the global object and global symbol registry
    - Adds a .register() method to romanizeString and romanizeThai for plugin registration
  - Integrates optional `@romanize-string/thai-romanizer` plugin with `romanizeThai`, which will use it automatically when it is installed.
  - Falls back to the original Python path if plugin isn’t present.
  - Switches to PyThaiNLP's ONNX runtime transliteration engine for better accuracy
  - README and tests updated. No breaking API changes.

- aa4536a: Cyrillic Romanization Overhaul & Testing Updates

  - Overhauled Cyrillic romanization to support both ASCII-only output and BGN/PCGN romanization, improving overall transliteration accuracy.
  - Added `omitDiacritics` parameter support for Cyrillic transliteration in both `romanizeCyrillic` and `romanizeString`.
  - Updated README to document the new `omitDiacritics` parameter, ASCII-only mode, and BGN/PCGN romanization support.
  - Switched testing framework from Jest to Vitest and revised all relevant tests to reflect the updated Cyrillic romanization behavior.

## 1.2.6

### Patch Changes

- Internal: Reorganized repo into a pnpm monorepo—moved the package to `packages/romanize-string`, added a workspace root with `pnpm --filter` scripts, centralized dev deps (`@changesets/cli`, `npm-run-all2`), and set the root to `private`. No public API changes.
