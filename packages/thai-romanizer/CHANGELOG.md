# @romanize-string/thai-romanizer

## 1.0.1

### Patch Changes

- 2efd1c4: Updates docs to integrate changelog
- Updated dependencies [2efd1c4]
  - romanize-string@1.3.1

## 1.0.0

### Initial Release

- ff8e336: Initial Release

  - Platform-aware binary plugin for Thai transliteration.
  - On install, downloads the appropriate binary; requires explicit registration via romanizeString.register(setup) before use.
  - On errors, logs and returns the original input.
  - Includes github actions that automatically build platform-specific Python binaries on release and automatically releases upon merging version bump PRs
