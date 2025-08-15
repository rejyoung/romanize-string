# romanize-string

## 1.3.0

### Minor Changes

- **Cyrillic Romanization Overhaul & Testing Updates**

  - Overhauled Cyrillic romanization to support both ASCII-only output and BGN/PCGN romanization, improving overall transliteration accuracy.
  - Added `omitDiacritics` parameter support for Cyrillic transliteration in both `romanizeCyrillic` and `romanizeString`.
  - Switched testing framework from Jest to Vitest and revised all relevant tests to reflect the updated Cyrillic romanization behavior.
  - Updated README to document the new `omitDiacritics` parameter, ASCII-only mode, and BGN/PCGN romanization support.

## 1.2.6

### Patch Changes

- Internal: Reorganized repo into a pnpm monorepo—moved the package to `packages/romanize-string`, added a workspace root with `pnpm --filter` scripts, centralized dev deps (`@changesets/cli`, `npm-run-all2`), and set the root to `private`. No public API changes.
