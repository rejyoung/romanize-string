
# romanize-string 
[![NPM version](https://img.shields.io/npm/v/romanize-string.svg?style=flat)](https://www.npmjs.com/package/romanize-string) [![NPM monthly downloads](https://img.shields.io/npm/dm/romanize-string.svg?style=flat)](https://npmjs.org/package/romanize-string) [![NPM total downloads](https://img.shields.io/npm/dt/romanize-string.svg?style=flat)](https://npmjs.org/package/romanize-string)

## Introduction

Romanize-string is a library for transliterating strings unidirectionally from non-Latin to Latin script. It unifies 10 different transliteration and parsing libraries—expanding upon some of them significantly in order to expand coverage—to create a single utility capable of generating basic transliterations of 29 written languages.

Supported languages include Arabic, Belarusian*, Bulgarian*, Bengali, Cantonese, Chinese (Traditional and Simplified), Persian* (Farsi), Gujarati, Hindi, Japanese, Kazakh*, Kannada, Korean, Kyrgyz*, Macedonian*, Mongolian*, Marathi, Nepali, Punjabi, Russian, Sanskrit, Serbian*, Tamil, Telugu, Tajik*, Thai, Ukranian, and Urdu*.

> \* Support for these languages is limited, as it was implemented without native fluency in those languages. They exist as my own expansions of the capabilities of the libraries arabic-transliterate and cyrillic-to-translit-js. [Contributions](https://github.com/rejyoung/romanize-string/issues) from community members with deeper knowledge of these languages are welcome. For information on the implementation of these expansions, see the Technical Notes section below.

## About
I created this library in the process of working on a closed-source project. I was in need of a utility that could handle transliterating media titles from multiple languages into Latin script so that their romanized forms could be used for display and for creating searchable slugs. Unfortunately, not only did no such library exist (at least not that covered all the languages I had to work with), but some of the languages had no direct transliteration libraries at all. I found that transliterating some languages required me to construct multi-step processes drawing on multiple libraries, while others (Farsi and Urdu, in particular) required a significant amount of custom code in order to produce something usable. Here I've condensed all of that into a single, unidirectional transliteration engine.

## Install

```sh
$ npm install romanize-string
```

## Usage


```ts
import romanizeString from "romanize-string"

const output = await romanizeString(string, languageCode, omitDiacritics[optional])
```

The romanizeString utility is capable of transliterating a string written in any of the supported languages. (Supported language codes are listed below.) It cannot transliterate from multiple languages at once. 

Because one of the underlying libraries is asynchronous, calls to romanizeString must be awaited.

The function accepts an optional boolean argument (omitDiacritics) which controls the transliteration scheme used for Mandarin and Indic languages (for Mandarin, that means controlling whether or not to include tones). When omitted, the value defaults to "false". When transliterating from a language that is not Mandarin or Indic, including a value for omitDiacritics in your function call has no effect.




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

#### East and Southeast Asian Scripts
| Code    | Language              |
|---------|-----------------------|
| ja      | Japanese              |
| ko      | Korean                |
| th*      | Thai                  |
| yue     | Cantonese             |
| zh-CN   | Chinese (Simplified)  |
| zh-Hant | Chinese (Traditional) |

\* Thai transliteration requires the presence of Python and the python library *pythainlp* in the environment where the code is run. See the romanizeThai entry in the Modular Imports section below for more details.

### Examples

```ts
const translitFromJapanese = await romanizeString("ありがとう", "ja"); // "arigatō"
const translitFromRussian = await romanizeString("Привет", "ru");     // "privet"
const tranlitFromBengali = await romanizeString("বাংলা", "bn");       // "vāṃlā"
const tranlitFromBengaliAscii = await romanizeString("বাংলা", "bn", true);       // "vaamlaa"
```


This library also supports modular imports. For usage of each individual function, see the Modular Imports section below.



## Typescript Support

The romanize-string library is fully typed and includes type exports for user-supplied arguments.abs

```ts
import {
    ConvertibleLanguage,
    CyrillicLanguageCode,
    IndicLanguageCode
} from "romanize-string"
```


## Modular Imports

Transliteration functions may be imported individually to reduce package size.

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


### romanizeArabic

Supported Languages: ar, fa, ur

```ts
romanizeArabic(input: string): string
```
<br>

### romanizeCantonese
Supported Language: yue
```ts
romanizeCantonese(input: string): string
```
<br>

### romanizeCyrillic
Supported Languages: be, bg, kk, ky, mk, mn, ru, sr, tg, uk
```ts
romanizeCyrillic(input: string, language: CyrillicLanguageCode): string
```
<br>

### romanizeIndic
Supported Languages: bn, gu, hi, kn, mr, ne, pa, sa, ta, te
```ts
romanizeIndic(input: string, language: IndicLanguageCode, omitDiacritics?: boolean): string
```
> If not specified, omitDiacritics defaults to "false".
<br>
<br>

### romanizeJapanese
Supported Language: ja
```ts
await romanizeJapanese(input: string): Promise<string>
```
> The supporting library responsible for Japanese transliteration (Kuroshiro) operates asynchronously. All calls to romanizeJapanese must therefore be awaited.
<br>
<br>

### romanizeKorean
Supported Language: ko
```ts
romanizeKorean(input: string): string
```
<br>

### romanizeMandarin
Supported Languages: zh-CN, zh-Hant
```ts
romanizeMandarin(input: string, omitTones?: boolean): string
```
> If not specified, omitTones defaults to "false".
 <br>
 <br>
---
 
### romanizeThai
Supported Language: th
```ts
romanizeThai(input: string):string
```

**NOTE**: romanizeThai uses a wrapped Python library (**pythainlp**) for the transliteration, since no suitable Javascript library currently exists. As such, the function will only work if the environment in which it is run has both Python3 and pythainlp installed. Attempts to use this function without one or both of them installed will return an untransliterated string and generate console errors explaining the problem.
<br>
<br>

## Technical Notes

As of the time of this writing, the [cyrillic-to-translit-js](https://github.com/greybax/cyrillic-to-translit-js) library only has presets for Russian, Mongolian, and Ukrainian. In order to expand upon the coverage it offered, its original code was integrated into this project with significant modifications. The support for reverse transliteration (Latin -> Cyrillic) was dropped, and new LLM-generated character maps were added for Belarusian, Bulgarian, Kazakh, Kyrgyz, Macedonian, Serbian, and Tajik.

Persian and Urdu posed a particular challenge, as the omission of short vowels in their written scripts makes straightforward character-mapping approaches insufficient for producing usable transliterations. This is likely why there are currently no transliteration libraries that support these languages. The admittedly imperfect approach taken in this library involves standardizing the Arabic script and then running it through the arabic-transliterate library. This standardization is done in three steps:

1. Common Persian and Urdu words are replaced with approximate LLM-generated phonetic forms (still in Arabic script), using lookup maps built from the Center for Language Engineering’s word frequency data for Persian and Urdu.

2. Remaining Persian- or Urdu-specific characters are replaced with their Arabic equivalents.

3. Short vowels are added to any remaining unvowelized words using a basic heuristic process.