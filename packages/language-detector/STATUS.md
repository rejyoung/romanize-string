# @romanize-string/language-detector

## STATUS: Abandoned (Post-Mortem)

### 1. Overview

This package was intended to be a plugin for [`romanize-string`](https://github.com/rejyoung/romanize-string/tree/main/packages/romanize-string) that would **fully automate transliteration** by **detecting the language** of input text without requiring users to supply language codes.

The goal was to

- accept short strings (like movie titles) as well as full sentences;
- reliably distinguish between the 30 supported languages across multiple scripts;
- remain compact enough to ship as a **small, downloadable binary**; and
- act as a **drop-in plugin** for [`romanize-string`](https://github.com/rejyoung/romanize-string/tree/main/packages/romanize-string).

Ultimately, the project was abandoned due to fundamental accuracy limitations and binary size constraints.

### 2. Context & Goals

The main library [`romanize-string`](https://github.com/rejyoung/romanize-string/tree/main/packages/romanize-string) supports 30 languages and produces transliterations. Users currently need to supply ISO language codes for each string run through the romanizer.

This plugin's purpose was to

- eliminate manual language selection by predicting the language automatically;
- enable seamless integrations where users need not know or care which language they're working with; and
- keep the experience lightweight by packaging trained models into a single binary.

### 3. Approach

#### 3.1 Architecture

- Built a Python-based NLP classifier using scikit-learn.
- Adopted a multi-tier design to both improve accuracy (the single-tier design performed poorly) and stay within hardware limits (single-tier training consumed too much memory and took unacceptably long to complete):
  -  **Primary Tier** - A script-family router (single multi-class model) that classifies input into broad script families (Latin, Cyrillic, Arabic, Han, Devanagari, etc.).
  - **Intermediate Tier (Cyrillic Only)** - A router that groups closely-related languages into subgroups (e.g., Serbian/Bosnian/Croatian; Russian/Ukrainian/Belarusian) for further processing by more sensitive models.
  - **Final Tier** - Script-specific models trained only on a single script (or, for Cyrillic, a single subgroup) for finer discrimination.
- Split training process into separate script-specific jobs, executed sequentially using `subprocess.run()`, to optimize memory usage and avoid overloading system resources.
- Planned to package trained models into a downloadable binary callable from a JavaScript wrapper in Node.js.

#### 3.2. Data Sources

- Used [Projekt Deutscher Wortschatz](https://wortschatz.uni-leipzig.de/) corpora 
  - Limited to high-quality sources: news outlets and Wikipedia.
  - Balanced datasets per model by resampling to stay within model-specific thresholds:
    - Minimum size: **500,000** samples.
    - Maximum size: **4,300,000** samples.
    - Per-model ranges never exceeded **2,500,000**.
- Preprocessed data for consistency and size constraints:
  - Normalized Unicode across all corpora
  - Removed strings consisting solely of Latin characters, digits, and punctuation.
  - Removed all Japanese strings containing Hiragana or Katakana so that the model was trained only on Han characters. (The language detector script uses the presence of Hiragana and Katakana to automatically identify the language as Japanese, bypassing the model altogether.)
  - Stripped remaining strings of any Latin characters and digits.
  - Tokenized text using fine-tuned n-gram ranges while capping total feature count to stay within the memory limitations of my machine.

#### 3.3 Model Design

- Explored several approaches:
  - **Multinomial Naive Bayes** -> fast, lightweight.
  - **Logistic Regression** -> slightly higher accuracy, larger binary.
  - **Linear SVC** -> slower inference and lower accuracy, didn't justify trade-off.
- Settled on a **VotingClassifier** combining Naive Bayes + Logistic Regression.

#### 3.4 Evaluation Strategy

- Training: 95% / Testing: 5%
- Reported:
    - Overall accuracy
    - Per-language confusion matrices
    - F1 scores


### 4. Results

#### Overall Language Performance Metrics

> Note: For multi-stage pipelines, overall metrics are calculated considering error propagation through sequential stages. Complete reports, along with confusion matrices for each model, can be found in the [`python/model_assets/results/`](./python/model_assets/results/) directory.

| Language | Code | Pipeline Stages | **Overall Precision** | **Overall Recall** | **Overall F1-Score** | Support |
|----------|------|----------------|----------------------|-------------------|---------------------|---------|
| Arabic | ar | family → perso_arabic | **0.89** | **0.96** | **0.92** | 176,167 |
| Belarusian | be | family → cyrillic → eastern_slavic | **0.80** | **0.71** | **0.75** | 50,000 |
| Bengali | bn | family → indic | **1.00** | **1.00** | **1.00** | 118,012 |
| Bulgarian | bg | family → cyrillic → southern_slavic | **0.63** | **0.66** | **0.64** | 50,000 |
| Chinese | zh | family → ja_zh | **0.94** | **0.90** | **0.92** | 100,000 |
| Greek | el | family → direct | **1.00** | **1.00** | **1.00** | 94,386 |
| Gujarati | gu | family → indic | **1.00** | **1.00** | **1.00** | 58,262 |
| Hindi | hi | family → indic | **0.72** | **0.53** | **0.61** | 60,153 |
| Japanese | ja | family → ja_zh | **0.80** | **0.93** | **0.86** | 50,000 |
| Kannada | kn | family → indic | **1.00** | **1.00** | **1.00** | 101,372 |
| Kazakh | kk | family → cyrillic → turkic | **0.82** | **0.70** | **0.76** | 50,000 |
| Korean | ko | family → direct | **0.99** | **0.99** | **0.99** | 150,000 |
| Kyrgyz | ky | family → cyrillic → turkic | **0.75** | **0.73** | **0.74** | 50,000 |
| Macedonian | mk | family → cyrillic → southern_slavic | **0.56** | **0.62** | **0.59** | 50,000 |
| Marathi | mr | family → indic | **0.74** | **0.91** | **0.82** | 104,361 |
| Mongolian | mn | family → cyrillic → turkic | **0.74** | **0.76** | **0.75** | 25,000 |
| Nepali | ne | family → indic | **0.83** | **0.75** | **0.79** | 64,158 |
| Persian/Farsi | fa | family → perso_arabic | **0.85** | **0.79** | **0.82** | 113,751 |
| Punjabi | pa | family → indic | **0.98** | **1.00** | **0.99** | 26,500 |
| Russian | ru | family → cyrillic → eastern_slavic | **0.70** | **0.71** | **0.71** | 50,000 |
| Serbian | sr | family → cyrillic → southern_slavic | **0.58** | **0.71** | **0.64** | 50,000 |
| Tajik | tg | family → cyrillic → turkic | **0.68** | **0.76** | **0.72** | 26,004 |
| Tamil | ta | family → indic | **1.00** | **1.00** | **1.00** | 136,513 |
| Telugu | te | family → indic | **1.00** | **1.00** | **1.00** | 95,100 |
| Thai | th | family → direct | **1.00** | **1.00** | **1.00** | 25,000 |
| Ukrainian | uk | family → cyrillic → eastern_slavic | **0.78** | **0.64** | **0.70** | 50,000 |
| Urdu | ur | family → perso_arabic | **0.90** | **0.82** | **0.86** | 106,000 |

#### Understanding the Metrics
- **Precision**: Of all predictions for a language, what % were correct? (High = fewer false positives)
- **Recall**: Of all actual instances of a language, what % were caught? (High = fewer false negatives)  
- **F1-Score**: Harmonic mean of precision and recall (balanced performance measure)
- **Support**: Number of test samples (larger = more reliable metrics)

#### Calculation Methodology

##### For Two-Stage Classification:
- **Overall Precision** = Family_Precision × Final_Stage_Precision
- **Overall Recall** = Family_Recall × Final_Stage_Recall

##### For Three-Stage Classification (Cyrillic):
- **Overall Precision** = Family_Precision × Cyrillic_Precision × Final_Stage_Precision
- **Overall Recall** = Family_Recall × Cyrillic_Recall × Final_Stage_Recall

#### Performance Summary by Pipeline Complexity

| Pipeline Type | Languages | Avg Precision | Avg Recall | Avg F1-Score | Performance Level |
|---------------|-----------|---------------|------------|--------------|-------------------|
| Direct (1 stage) | 3 | 1.00 | 1.00 | 1.00 | Excellent |
| Two-stage | 14 | 0.89 | 0.88 | 0.88 | Very Good |
| Three-stage (Cyrillic) | 10 | 0.68 | 0.69 | 0.68 | Moderate |

#### Overall System Performance

| Metric | Value |
|--------|-------|
| Total Languages Supported | 30 |
| **Average Precision** | **0.85** |
| **Average Recall** | **0.85** |
| **Average F1-Score** | **0.85** |
| Overall Performance Level | Good |

#### Key Insights

##### Performance Highlights
- **Perfect Performance**: Greek, Thai, Bengali, Gujarati, Kannada, Tamil, Telugu
- **Near Perfect**: Korean, Punjabi
- **High Performance**: Chinese, Arabic

##### Performance Challenges (More Severe Than Initially Thought)
- **Lowest Overall**: Macedonian (F1: 0.59) - significant degradation in three-stage pipeline
- **Cyrillic Branch**: Much more challenging than initially calculated - average F1 drops to 0.68
- **Hindi**: Still challenging (F1: 0.61) but not as severe as cyrillic languages

##### System Impact of Error Propagation
- **Two-stage pipelines**: ~11% performance degradation from individual model metrics
- **Three-stage pipelines**: ~20% performance degradation from individual model metrics
- **Overall system**: 15% lower performance than naive calculation suggested

##### Critical Findings
1. **Error propagation is significant** - the hierarchical approach compounds errors
2. **Cyrillic branch is the weakest link** - three-stage classification severely impacts performance
3. **Direct classification remains optimal** - single-stage languages maintain perfect performance
4. **System performance is more modest** than initially calculated - 85% average vs 90%


### 5. Major Blockers

#### 5.1 High-Precision Requirements

Because transliteration is primarily concerned with phonetics and less with meaning, correctly identifying the language of the original text is paramount. Pronunciations can differ substantially between even closely related languages, and applying the phonetic rules of one language to the orthography of another can produce garbled transliterations that don't make sense in either language.

For this plugin to be practical, therefore, it needs near-perfect accuracy across all languages. The `romanize-string` library is well suited for bulk transliteration, and at that scale, even 98% accuracy would be risky; anything below 95% would render the plugin unusable. 

| Accuracy | Errors per 1,000 Strings |
|----------|--------------------------|
| 98%      | 20                       |
| 95%      | 50                       |
| 90%      | 100                      |

With the models I produced, only 9 of 30 languages approached acceptable accuracy levels.

#### 5.2 Data and Hardware Constraints

Achieving production-ready accuracy would require larger, cleaner, and more balanced datasets and the addition of language-specific lexicons. Not only would this explode the binary size beyond what is acceptable, but it would push training time and memory usage beyond what's feasible on consumer-grade hardware. And even then, there are some specific languages for which achieving 99+% accuracy may be impossible.

#### 5.3 Hanzi vs Kanji

Distinguishing Chinese from Japanese text is straightforward when Japanese includes Hiragana or Katakana, but a large portion of Japanese writing uses Kanji, many of which are identical to Chinese Hanzi characters and use the same Unicode code points. This overlap makes it effectively impossible for a model to reliably differentiate between the two in kanji/hanzi-only strings. 

The consequence is that transliterations for such texts may look valid but are often incorrect, producing outputs that are misleading and confusing rather than helpful. For example, the phrase "世界和平," which translates as "world peace" in either language, would be transliterated as *shìjiè hépíng* in Mandarin or *sekai wahei* in Japanese.

In an attempt to solve this problem, I trained the ja_zh model solely on Chinese text and Japanese text containing only Kanji characters. While results were quite good overall by normal standards, the model still misidentified the language of kanji/hanzi-only text roughly 1 out of 10 times. That level of inaccuracy is too high in the context of this plugin.

<details>
<summary><strong>Japanese-Chinese Model Accuracy Report</strong></summary>

|            |precision|recall|f1-score|support|
|------------|---------|------|--------|-------|
|         ja |     0.82|  0.93|    0.87|50,000 |
|         zh |     0.96|  0.90|    0.93|100,000|

|            |precision|recall|f1-score|support|
|------------|---------|------|--------|-------|
|overall accuracy |         |      |    0.91|150,000|
|  macro avg |     0.89|  0.92|    0.90|150,000|
|weighted avg|     0.92|  0.91|    0.91|150,000|


**Test accuracy:** 0.9094 (90.94%)

</details>

#### 5.4 Mandarin vs Cantonese

Even before I began this project, I knew that it would be impossible to develop a model that could distinguish between Mandarin and Cantonese. There is simply no information contained in the written text that can indicate which transliteration system to apply. I did not, however, consider this limitation to be project-ending on its own, and I had already planned a workaround using direct user input. This solution became irrelevant in light of the other challenges that arose.

#### 5.5 Speed

The plugin’s architecture relies on invoking a pre-downloaded Python binary via Node's `spawnSync()` for each detection call, creating a structural bottleneck rather than merely an inefficiency. Each call takes nearly 30 seconds, which is prohibitively slow compared to similar plugins. For example, the [@romanize-string/thai-engine](https://github.com/rejyoung/romanize-string/tree/main/packages/thai-engine) plugin, which uses the same process, takes only around 5 seconds to execute. The larger dependency load (scikit-learn + NumPy/SciPy) and multi-model pipeline make cold-start performance significantly slower compared to the Thai plugin.

Addressing this would require significant changes such as maintaining a persistent Python process, batching calls, or migrating to ONNX. Given the fundamental accuracy limitations, investing effort into these fixes was not justified.


### 6. Lessons Learned

While this plugin was ultimately abandoned, the process of creating it was invaluable to my professional development.

#### 6.1 Technical Lessons

- Automatic language detection for transliteration has much stricter accuracy requirements than for translation.
- Training a model accurate enough for this application is likely beyond the capabilities of the average personal computer.
- Short-string language detection is inherently unreliable for languages with high orthographic overlap.
- Larger, production-grade NLPs (like Google Translate) fail at the same edge cases - some tasks are fundamentally unsolvable.
- The number and size of imported assets and libraries has a much greater impact on performance than anticipated when packaged as a binary vs when run natively.


#### 6.2 Personal Growth

Although the primary goal of this project was to build a production-ready plugin, my secondary purpose was to gain experience working with Python-based NLP pipelines, model training, and packaging strategies. While the plugin ultimately proved impractical, the process was invaluable, as I learned how to train and evaluate NLP models using scikit-learn, handle multilingual corpora preprocessing at scale, interpret confusion matrices, and evaluate trade-offs. I also gained more experience building and packaging cross-language binaries and improved my ability to integrate AI-assisted tools into my development workflow.

### 7. Data Attribution

This project uses corpora provided by [Projekt Deutscher Wortschatz](https://wortschatz.uni-leipzig.de/) for training language models.  
The data is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

Source: Wortschatz Corpora (<https://wortschatz.uni-leipzig.de/en/download>)
