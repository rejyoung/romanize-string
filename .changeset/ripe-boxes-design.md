---
"romanize-string": minor
---

## Cyrillic Romanization Overhaul & Testing Updates**

- Overhauled Cyrillic romanization to support both ASCII-only output and BGN/PCGN romanization, improving overall transliteration accuracy.
- Added `omitDiacritics` parameter support for Cyrillic transliteration in both `romanizeCyrillic` and `romanizeString`.
- Updated README to document the new `omitDiacritics` parameter, ASCII-only mode, and BGN/PCGN romanization support.
- Switched testing framework from Jest to Vitest and revised all relevant tests to reflect the updated Cyrillic romanization behavior.
