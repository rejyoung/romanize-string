# @romanize-string/language-detector

> ⚠️ **Status: ABANDONED / NOT PRODUCTION-READY**  
> This was an experiment. No further development planned. See [STATUS.md](./STATUS.md) for the full write-up.

## What this tried to do
The aim of this project was to create a plugin that could fully automate the [`romanize-string`](https://github.com/rejyoung/romanize-string/tree/main/packages/romanize-string) library by automatically detecting the language of input text, eliminating the need for users to supply language codes for each string submitted for transliteration. The plan was to create a collection of **Python-based NLP models** specifically trained to distinguish between the 30 languages supported by `romanize-string` and supply language codes to the main library. It needed to be able to do this for short strings, like movie titles, as well as full sentences. Most importantly, it needed to be compact enough to ship as a **downloadable binary of reasonable size**.

## Why it won’t work
- **Accuracy on related languages is insufficient.**
Without access to lexicons (which would have made the binary unacceptably large), the models struggle to distinguish between languages **within the same script family** that share a significant amount of vocabulary or exhibit extremely similar morphology. While distinguishing between Cantonese and Mandarin was always expected to be effectively impossible and a workaround involving explicit user input was already prepared, the extent of similar issues across other language groups was unexpected and ultimately contributed to the decision to abandon the project.
- **Limited training data and hardware resources cap the maximum achievable model accuracy.**
Improving the accuracy of the models would require considerably more high-quality data than I have access to, which would in turn cause the training process to exceed the limitations of my machine.
- **Transliteration is less forgiving than translation.** 
Unlike translation, where mixing up two similar languages might yield something “close enough,” **phonetic transliteration** requires highly accurate language identification. Confusing even closely related languages leads to incorrect outputs.
- **Required accuracy threshold too high.** 
Since the plugin was meant to **replace human input**, it would have to have had an extremely high degree of reliability to be useful. Achieving that without sacrificing binary size proved impractical.

## What I learned
A full breakdown is in [STATUS.md](./STATUS.md), but key takeaways include:
- Automatic language detection for transliteration has fundamentally different constraints than translation.
- Packaging NLP models as a small binary forces trade-offs that severely limit accuracy.
- In some cases, accurate language detection of short strings may be **fundamentally impossible**; phrases shared between Mandarin and Japanese, for instance, can be morphologically identical but require **completely different transliterations** (e.g. "世界和平," which transliterates either as shìjiè hépíng or sekai heiwa). Even much larger and more sophisticated NLP systems, like Google Translate, fail in these cases.

## Current state
- No ongoing maintenance; issues/PRs likely won’t be addressed
- Use at your own risk
- Full analysis: [STATUS.md](./STATUS.md)

## Alternatives
- ✅ Use: [`romanize-string`](https://github.com/rejyoung/romanize-string/tree/main/packages/romanize-string) with manual language selection



### Data Attribution

This project uses corpora provided by [Projekt Deutscher Wortschatz](https://wortschatz.uni-leipzig.de/) for training language models.  
The data is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

Source: Wortschatz Corpora (<https://wortschatz.uni-leipzig.de/en/download>)
