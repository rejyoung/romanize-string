---
"@romanize-string/thai-romanizer": major
---

## Initial Release

- Platform-aware binary plugin for Thai transliteration.
- On install, downloads the appropriate binary; requires explicit registration via romanizeString.register(setup) before use.
- On errors, logs and returns the original input.
- Includes github actions that automatically build platform-specific Python binaries on release and automatically releases upon merging version bump PRs
