
# romanize-string

[![NPM version](https://img.shields.io/npm/v/romanize-string.svg?style=flat)](https://www.npmjs.com/package/romanize-string) [![NPM monthly downloads](https://img.shields.io/npm/dm/romanize-string.svg?style=flat)](https://npmjs.org/package/romanize-string) [![NPM total downloads](https://img.shields.io/npm/dt/romanize-string.svg?style=flat)](https://npmjs.org/package/romanize-string)

## Table of Contents

- [Introduction](#introduction)
- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
- [Language Codes](#language-codes)
- [TypeScript Support](#typescript-support)
- [Modular Imports](#modular-imports)
  - [Script-Based Transliteration Functions](#script-based-transliteration-functions)
  - [Type Guards](#type-guards)
- [Dependencies and Attribution](#dependencies-and-attribution)
- [Technical Notes](#technical-notes)

## Introduction

Romanize-string is a library for transliterating strings unidirectionally from non-Latin to Latin script. It unifies 10 different transliteration and parsing libraries—expanding upon some of them significantly in order to increase coverage—to create a single utility that can generate basic transliterations for 30 written languages.

Supported languages include Arabic, Belarusian*, Bulgarian*, Bengali, Cantonese, Chinese (Traditional and Simplified), Persian*(Farsi), Greek, Gujarati, Hindi, Japanese, Kazakh*, Kannada, Korean, Kyrgyz*, Macedonian*, Mongolian*, Marathi, Nepali, Punjabi, Russian, Sanskrit, Serbian*, Tamil, Telugu, Tajik*, Thai, Ukrainian, and Urdu*.

> \* Support for these languages is limited, as it was implemented without native fluency in those languages. They exist as custom extensions of the capabilities of the libraries arabic-transliterate and cyrillic-to-translit-js. [Contributions](https://github.com/rejyoung/romanize-string/issues) from community members with deeper knowledge of these languages are welcome. For information on the implementation of these expansions, see the [Technical Notes](#technical-notes) section.

## About

I created this library in the process of working on a closed-source project. I was in need of a utility that could handle transliterating media titles from multiple languages into Latin script so that their romanized forms could be used for display and for creating searchable slugs. Unfortunately, not only did no such library exist (at least not that covered all the languages I had to work with), but some of the languages had no direct transliteration libraries at all. I found that transliterating some languages required me to construct multi-step processes drawing on multiple libraries, while others (Farsi and Urdu, in particular) required a significant amount of custom code in order to produce something usable. Here I've condensed all of that into a single, unidirectional transliteration engine.

## Installation

```sh
npm install romanize-string
```

> Requires Node.js 16+

>Supports both ESM and CommonJS

### Additional Installation for Thai Transliteration

Because no suitable JavaScript library exists for Thai transliteration, this library relies on an external Python library ( [pythainlp](https://github.com/PyThaiNLP/pythainlp) ) to handle Thai script. As a result, any attempt to romanize Thai—whether via the [`romanizeThai`](#romanizethai) function or by passing `"th"` to `romanizeString`—requires both Python 3 and [pythainlp](https://github.com/PyThaiNLP/pythainlp) to be installed in the runtime environment. If either is missing, the function will return an untransliterated string and emit a descriptive console error.

1. Make sure Python 3 is installed:
   - [Download Python](https://www.python.org/downloads/) if needed

2. Install the required library:

   ```bash
   pip install pythainlp
   ```

If you're unsure which Python installation you're using:

```bash
python3 -m pip install pythainlp
```

> **NOTE:** This issue **only** affects Thai transliteration. The absence or presence of Python 3 and pythainlp has no effect on the romanization of other scripts.

## Usage

The `romanizeString` utility is capable of transliterating a string written in any of the [supported languages](#language-codes). It cannot transliterate from multiple languages at once. For scripts without native capitalization (all except Cyrillic and Greek), the output romanized strings will be lowercase.

Because one of the underlying libraries is asynchronous, you must await calls to `romanizeString`.

**Example:**

```ts
import romanizeString from "romanize-string"

const output = await romanizeString("নমস্তে, আপনি কেমন আছেন?", "bn", false) // namaste, āpani kemana āchena?
```

**Arguments:**

`input` - A string in a supported script/language.

`languageCode` - A supported language code of type `ConvertibleLanguage`

`omitDiacritics` *(optional)* - A boolean indicating whether to omit diacritics from the output by controlling the transliteration scheme (defaults to `false`)

**Returns:**

A promise resolving to a string in Latin script

> **NOTE:** The parameter `omitDiacritics` only applies to Mandarin, Greek, and Indic languages. (For Mandarin, diacritics are used to indicate tones.) When transliterating from a language other than these, passing a value for `omitDiacritics` in your function call has no effect

### Language Codes

#### Arabic Script

| Code | Language        |
|------|-----------------|
| ar   | Arabic          |
| fa   | Persian (Farsi) |
| ur   | Urdu            |

#### Cyrillic Script

| Code | Language   |
|------|------------|
| be   | Belarusian |
| bg   | Bulgarian  |
| kk   | Kazakh     |
| ky   | Kyrgyz     |
| mk   | Macedonian |
| mn   | Mongolian  |
| ru   | Russian    |
| sr   | Serbian    |
| tg   | Tajik      |
| uk   | Ukrainian  |

#### Devanagari / Other Indic Scripts

| Code | Language |
|------|----------|
| bn   | Bengali  |
| gu   | Gujarati |
| hi   | Hindi    |
| kn   | Kannada  |
| mr   | Marathi  |
| ne   | Nepali   |
| pa   | Punjabi  |
| sa   | Sanskrit |
| ta   | Tamil    |
| te   | Telugu   |

#### Greek Script

| Code | Language   |
|------|------------|
| el   | Greek      |

#### East and Southeast Asian Scripts

| Code    | Language              |
|---------|-----------------------|
| ja      | Japanese              |
| ko      | Korean                |
| th      | Thai ¹                |
| yue     | Cantonese             |
| zh-CN   | Chinese (Simplified)  |
| zh-Hant | Chinese (Traditional) |

¹ Thai transliteration requires Python and the Python library [pythainlp](https://github.com/PyThaiNLP/pythainlp) to be installed in the environment where the code is run. See the [Additional Installation for Thai Transliteration](#additional-installation-for-thai-transliteration) for more details.

### Examples

```ts
const translitFromJapanese = await romanizeString("ありがとう", "ja"); // "arigatō"
const translitFromRussian = await romanizeString("Привет", "ru");     // "privet"
const translitFromBengali = await romanizeString("বাংলা", "bn");       // "vāṃlā"
const translitFromBengaliAscii = await romanizeString("বাংলা", "bn", true);       // "vaamlaa"
```

This library also supports modular imports. For usage of each individual function, see [Modular Imports](#modular-imports).

## TypeScript Support

The romanize-string library is fully typed and includes type exports for user-supplied arguments.

```ts
import {
    ConvertibleLanguage,
    CyrillicLanguageCode,
    IndicLanguageCode
} from "romanize-string"
```

## Modular Imports

In addition to the default `romanizeString` function, this library also supports named imports for individual transliteration functions and type guard utilities. These can be imported individually to reduce bundle size or to access specialized functionality.

| Method                      | Description                                                              | Args                                   | Returns          |
| --------------------------- | ------------------------------------------------------------------------ | -------------------------------------- | ---------------- |
| `romanizeArabic()`          | Transliterate Arabic script to Latin script                              | `input`                                | string           |
| `romanizeCantonese()`       | Transliterate Hanzi script to Latin script with Cantonese pronunciation  | `input`                                | string           |
| `romanizeCyrillic()`        | Transliterate Cyrillic script to Latin script                            | `input`, `language`                    | string           |
| `romanizeIndic()`           | Transliterate an Indic script to Latin script                            | `input`, `language`, `omitDiacritics?` | string           |
| `romanizeJapanese()`        | Transliterate Kanji, Hiragana, or Katakana script to Latin script        | `input`                                | Promise\<String> |
| `romanizeKorean()`          | Transliterate Hangul script to Latin script                              | `input`                                | string           |
| `romanizeMandarin()`        | Transliterate Hanzi script to Latin script using Mandarin pronunciation  | `input`, `omitTones?`                  | string           |
| `romanizeThai()`            | Transliterate Thai script to Latin script                                | `input`                                | string           |
| `isConvertibleLanguage()`   | Check whether language code is included in the `ConvertibleLanguage` type  | `languageCode`                         | boolean          |
| `isCyrillicLanguageCode()`  | Check whether language code is included in the `CyrillicLanguageCode` type | `languageCode`                         | boolean          |
| `isIndicLanguageCode()`     | Check whether language code is included in the `IndicLanguageCode` type    | `languageCode`                         | boolean          |

### Script-Based Transliteration Functions

These functions handle transliteration for specific script families.

```ts
import {
    romanizeArabic, 
    romanizeCantonese, 
    romanizeCyrillic, 
    romanizeIndic, 
    romanizeJapanese, 
    romanizeKorean, 
    romanizeMandarin, 
    romanizeThai
} from "romanize-string"
```

#### `romanizeArabic()`

Transliterates from Arabic script.

Supported Languages: ar, fa, ur

```ts
const translit = romanizeArabic("مرحبا، كيف حالك؟") // maraḥabā,a kayafa ḥāl-k?
```

**Arguments:**

`input` - A string in Arabic script

**Returns:**

A string in Latin script

#### `romanizeCantonese()`

Transliterates from Hanzi using Cantonese pronunciation.

Supported Language: yue

```ts
const translit = romanizeCantonese(你好，今日點呀) // lee ho, gam yat dim ah?
```

**Arguments:**

`input` - A string in Hanzi script

**Returns:**

A string in Latin script

#### `romanizeCyrillic()`

Transliterates from Cyrillic.

Supported Languages: be, bg, kk, ky, mk, mn, ru, sr, tg, uk

```ts
const translit = romanizeCyrillic("Салам, кандайсың?", "ky") // Salam, kandaisyñ?
```

**Arguments:**

`input` - A string in Cyrillic script

`language` - A language code of type CyrillicLanguageCode

**Returns:**

A string in Latin script

---

#### `romanizeGreek()`

Transliterates from Greek script.

Supported Languages: el

```ts
const translit = romanizeGreek("Γειά σου, τι κάνεις", false) // Yeiá sou, ti káneis
const translitNoDia = romanizeGreek("Γειά σου, τι κάνεις", true) // Yeia sou, ti kaneis
```

**Arguments:**

`input` - string

`omitDiacritics` *(optional)* - A boolean indicating whether to exclude diacritics in the output (defaults to `false`)

**Returns:**

A string in Latin script

---

#### `romanizeIndic()`

Transliterates from Devanagari and other Indic scripts.

Supported Languages: bn, gu, hi, kn, mr, ne, pa, sa, ta, te

```ts
const translit = romanizeIndic("नमस्ते, आप कैसे हैं?", "hi", false) // namaste, āpa kaise haiṃ?
const translitNoDia = romanizeIndic("नमस्ते, आप कैसे हैं?", "hi", true) // namaste, aapa kaise haim?
```

**Arguments:**

`input` - string

`omitDiacritics` *(optional)* - A boolean indicating whether to exclude diacritics in the output (defaults to `false`)

**Returns:**

A string in Latin script

---

#### `romanizeJapanese()`

Transliterates from Kanji, Hiragana, or Katakana.

Supported Language: ja

```ts
const translit = await romanizeJapanese("こんにちは、お元気ですか？") // konnichiwa, o genkidesu ka?
const translitMixed = await romanizeJapanese("今日のディナーはカレーです。") // kyō no dinā wa karē desu.
```

**Arguments:**

`input` - string

**Returns:**

A promise resolving to a string in Latin script

> **NOTE:** The supporting library responsible for Japanese transliteration ( [Kuroshiro](https://github.com/hexenq/kuroshiro) ) operates asynchronously. All calls to romanizeJapanese must therefore be awaited.

---

#### `romanizeKorean()`

Transliterates from Hangul script.

Supported Language: ko

```ts
const translit = romanizeKorean("안녕하세요, 잘 지내세요?") // annyeonghaseyo, jal jinaeseyo?
```

**Arguments:**

`input` - string

**Returns:**

A string in Latin script

---

#### `romanizeMandarin()`

Transliterates from both Traditional and Simplified Hanzi using Mandarin pronunciation.

Supported Languages: zh-CN, zh-Hant

```ts
const translitTrad = romanizeMandarin("你好，最近好嗎？", false) // nǐ hǎo, zuì jìn hǎo má？
const translitTradNoDia = romanizeMandarin("你好，最近好嗎？", true) // ni hao, zui jin hao ma？
const translitSimplified = romanizeMandarin("你好，最近好吗？", false) // nǐ hǎo, zuì jìn hǎo ma?
```

**Arguments:**

`input` - string

`omitTones` *(optional)* - A boolean indicating whether to exclude diacritics that indicate tones from the output (defaults to `false`)

**Returns:**

A string in Latin script

---

#### `romanizeThai()`

Transliterates from Thai script.

Supported Language: th

```ts
const translit = romanizeThai("สวัสดีครับ/ค่ะ สบายดีไหม?") // satti khnap/kha spaiti mai?
```

**Arguments:**

`input` - string

**Returns:**

A string in Latin script

> **NOTE:** To use `romanizeThai`, Python 3 and the pythainlp library must be available in your environment. See [Additional Installation for Thai Transliteration](#additional-installation-for-thai-transliteration) for more information.

---

### Type Guards

These utilities help with validating language codes at runtime — useful for functions that require language code input.

```ts
import {
    isConvertibleLanguage,
    isCyrillicLanguageCode,
    isIndicLanguageCode
} from "romanize-string"
```

#### `isConvertibleLanguage()`

Returns true if the given string is a supported language code from type `ConvertibleLanguage`.

```ts
isConvertibleLanguage("ja") // true
```

**Arguments:**

`input` - a language code

**Returns:**

A boolean indicating whether the given language code is of type `ConvertibleLanguage`

---

#### `isCyrillicLanguageCode()`

```ts
isCyrillicLanguageCode("ru") // true
```

**Arguments:**

`input` - a language code

**Returns:**

A boolean indicating whether the given language code is of type `CyrillicLanguageCode` (a subset of `ConvertibleLanguageCode`)

---

#### `isIndicLanguageCode()`

```ts
isIndicLanguageCode("hi") // true
```

**Arguments:**

`input` - a language code

**Returns:**

A boolean indicating whether the given language code is of type `IndicLanguageCode` (a subset of `ConvertibleLanguageCode`)

## Dependencies and Attribution

This library draws on the capabilities of several existing libraries, many of which have been extended or combined to support broader functionality:

- [**arabic-transliterate**](https://www.npmjs.com/package/arabic-transliterate) – used as the foundation for Arabic, Persian, and Urdu transliteration, with significant customizations, details of which are provided in the Technical Notes section.
- [**@indic-transliteration/sanscript**](https://www.npmjs.com/package/@indic-transliteration/sanscript) – provides base functionality for Devanagari and other Indic scripts.
- [**kuroshiro**](https://www.npmjs.com/package/kuroshiro) – used for Japanese transliteration; includes async processing.
- [**kuroshiro-analyzer-kuromoji**](https://www.npmjs.com/package/kuroshiro-analyzer-kuromoji) – Japanese morphological analyzer required by Kuroshiro.
- [**pinyin-pro**](https://www.npmjs.com/package/pinyin-pro) – used for Mandarin transliteration from Simplified and Traditional Hanzi.
- [**cantonese-romanisation**](https://www.npmjs.com/package/cantonese-romanisation) – provides base mappings for Cantonese transliteration.
- [**oktjs**](https://www.npmjs.com/package/oktjs) – used to tokenize and normalize Korean input before transliteration.
- [**tnthai**](https://www.npmjs.com/package/tnthai) – used to segment Thai script into individual words before submitting them to the transliteration pipeline.
- [**pythainlp**](https://github.com/PyThaiNLP/pythainlp) – external Python library used for Thai transliteration. **Note:** This is not a direct JavaScript dependency. It must be installed manually (alongside Python 3) in the runtime environment for `romanizeThai` to function.

This project includes modified and vendored code from the following libraries:

- [**cyrillic-to-translit-js**](https://www.npmjs.com/package/cyrillic-to-translit-js) by Aleksandr Filatov - MIT Licensed.  Logic adapted and restructured to support additional Cyrillic languages. Not used as a dependency; see [Technical Notes](#technical-notes).
- [**@romanize/korean**](https://www.npmjs.com/package/@romanize/korean) by Kenneth Tang – MIT Licensed. Used for Hangul transliteration. Vendored and modified for structural compatibility. See `src/vendor/romanize/korean/LICENSE`.

## Technical Notes

As of the time of this writing, the [cyrillic-to-translit-js](https://github.com/greybax/cyrillic-to-translit-js) library only has presets for Russian, Mongolian, and Ukrainian. In order to expand upon the coverage it offered, its original code was integrated into this project with significant modifications. The support for reverse transliteration (Latin -> Cyrillic) was dropped, and new LLM-generated character maps were added for Belarusian, Bulgarian, Kazakh, Kyrgyz, Macedonian, Serbian, and Tajik.

Persian and Urdu posed a particular challenge, as the omission of short vowels in their written scripts makes straightforward character-mapping approaches insufficient for producing usable transliterations. This likely explains why no transliteration libraries currently support these languages. The imperfect approach taken in this library involves standardizing the Arabic script and then running it through the [**arabic-transliterate**](https://www.npmjs.com/package/arabic-transliterate) library. This standardization is done in three steps:

1. Common Persian and Urdu words are replaced with approximate LLM-generated phonetic forms (still in Arabic script), using lookup maps built from the Center for Language Engineering’s word frequency data for Persian and Urdu.

2. Remaining Persian- or Urdu-specific characters are replaced with their Arabic equivalents.

3. Short vowels are added to any remaining unvowelized words using a basic heuristic process.
