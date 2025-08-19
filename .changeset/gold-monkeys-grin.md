---
"romanize-string": minor
---

## Thai Romanization Plugin & Core Integration

- Adds support for plugins
  - Adds plugin registry and registration functions that utilize the global object and global symbol registry
  - Adds a .register() method to romanizeString and romanizeThai for plugin registration
- Integrates optional `@romanize-string/thai-romanizer` plugin with `romanizeThai`, which will use it automatically when it is installed.
- Falls back to the original Python path if plugin isn’t present.
- Switches to PyThaiNLP's ONNX runtime transliteration engine for better accuracy
- README and tests updated. No breaking API changes.
