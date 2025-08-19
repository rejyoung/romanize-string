
# @romanize-string/thai-romanizer

Thai-romanizer is a Node-only Thai romanization plugin for [`romanize-string`](https://www.npmjs.com/package/romanize-string). It runs a platform-specific binary (~50 MB) to romanize Thai script using the Python library [PyThaiNLP](https://pypi.org/project/pythainlp/).

> See the [Changelog](./CHANGELOG.md) for details on recent updates.

## Features

- Works with romanize-string's plugin system.
- Automatically downloads the appropriate platform-specific binary (~50 MB) at install.
- Fails fast with a clear error if the binary is missing or not executable.

## Installation

```sh
npm install @romanize-string/thai-romanizer
```

> Requires Node.js 18+

> **Note:** This plugin extends [`romanize-string`](https://www.npmjs.com/package/romanize-string) and must be used together with it. It will not function without romanize-string installed in your project. This package does not provide end‑user APIs by itself; it only supplies a plugin function to be registered with `romanize-string`.

## Usage

### ESM

```ts
import romanizeString, {romanizeThai} from "romanize-string"
import thaiRomanizer from "@romanize-string/thai-romanizer"

romanizeString.register(thaiRomanizer)

console.log(await romanizeString("สวัสดี ครับ", "th")) //sawatdi khrap

console.log(romanizeThai("สวัสดี ครับ")) //sawatdi khrap

```

### CommonJS

```ts
const {default: romanizeString, romanizeThai} = require("romanize-string")
const thaiRomanizer = require("@romanize-string/thai-romanizer")

romanizeString.register(thaiRomanizer)

console.log(await romanizeString("สวัสดี ครับ", "th")) //sawatdi khrap

console.log(romanizeThai("สวัสดี ครับ")) //sawatdi khrap

```

## Registration scope

Call `romanizeString.register(thaiRomanizer)` **once per process** (e.g., at app start) to enable Thai support. After registration, any call to `romanizeString("…", "th")` in the same process will work without re-registering.

## Security note

Downloaded helper binaries are verified against a known checksum during installation. The binaries are built from source that lives in this same repository; no third‑party download service is used.

## Version compatibility

Requires a version of `romanize-string` that exposes the plugin registration hook (via `Symbol.for("romanize-string.registerPlugin")`). If you see the error "The romanize-string plugin hook was not found; plugin not registered.", upgrade `romanize-string` and ensure there's only a single installed copy.

## Supported platforms

| Platform       | Binary name              |
| -------------- | ----------------------- |
| darwin-arm64   | thai-mac-arm64          |
| darwin-x64     | thai-mac-x64            |
| linux-arm64    | thai-linux-arm64        |
| linux-x64      | thai-linux-x64          |
| win32-x64      | thai-win-x64.exe        |
| win32-arm64    | thai-win-x64.exe (runs under emulation) |

## Error messages & troubleshooting

- **"The romanize-string plugin hook was not found; plugin not registered."**  
  This means the plugin could not connect to the main `romanize-string` library. In most cases, this happens if you are using an older version of `romanize-string`, have multiple copies of it installed, or are running in an unusual environment where global settings are not shared.

  **How to fix:** Make sure you are on a recent version of `romanize-string`, that your project only has one copy installed, and that you are running in a normal Node.js environment.

- **"Cannot register plugin. The thaiRomanizer binary is missing or was not successfully downloaded."**  
  The platform-specific binary was not found or could not be executed. Try reinstalling the package. If this persists, check that your system is supported and that you have permission to execute the binary.

- **"Romanization returns the original text"**  
  If romanization silently returns the input text, the native helper likely failed at runtime or was not registered. Try these quick checks:

  - Ensure you've called `romanizeString.register(thaiRomanizer)` **once before first use**.
  - Verify your Node version is supported (Node 18+ recommended).
  - Confirm file permissions allow execution of the bundled helper (on Unix-like systems, it should be executable by the current user).
  - Reinstall the package to re-fetch the correct binary for your platform: `rm -rf node_modules && pnpm install` (or `npm ci`).
  - Check for duplicate installs of `romanize-string` that can break the global registration: `npm ls romanize-string` or `pnpm why romanize-string`.

## Licenses & attribution

This package redistributes third-party components (e.g., [PyThaiNLP](https://pypi.org/project/pythainlp/), [NumPy](https://numpy.org/), [ONNX Runtime](https://onnxruntime.ai/)). Full license texts for these and for the [PyInstaller](https://pyinstaller.org/en/stable/) bootloader are included in third_party/.
