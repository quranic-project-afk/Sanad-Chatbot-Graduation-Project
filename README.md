# SANAD – Smart Qur'anic Emotional Companion

SANAD is a Telegram companion for Sudanese-Arabic users. It reads a message, detects one of four emotions (fear, joy, anger, sadness), and replies with a short Sudanese-dialect response and a Qur'anic verse with its tafsir, selected from a manually curated list. A rule-based safety layer checks every message first and returns a fixed response for messages matching its emergency rules.

This is the code and data of a BSc (Information Technology) graduation project, University of Khartoum, 2026.

> **Not a clinical tool.** SANAD offers emotional and spiritual comfort only. It does not diagnose, treat, or give religious rulings, and it does not replace a doctor, counsellor, or emergency services. Replies are assembled from prepared sentences and curated verse content; the system is not a general-purpose text generator.

## How it works

```text
Telegram message
   │
   ▼
Safety layer ──► fixed safety response when a rule matches ──► stop
   │
   ▼
Greeting check ──► prepared greeting ──► stop
   │
   ▼
Emotion: AraBERT classifier + decision rules
   │
   ▼
Curated verse selection using trigger words and recent-verse history
   │
   ▼
Reply assembled from Sudanese-dialect sentence banks + verse + tafsir
```

Verse text and tafsir are fetched from the [Al-Quran Cloud API](https://alquran.cloud/api). The code checks each verse reference against a key phrase before accepting it. An internet connection is needed when building the curated verse data if it is not already available in Google Drive.

## Results

The reported evaluation uses a test set split by source dialogue, so a source dialogue does not appear in more than one partition. The test set contains 382 sentences.

| Model | Accuracy | Macro-F1 |
| --- | ---: | ---: |
| TF-IDF + Logistic Regression | 97.91% | 0.9775 |
| AraBERT (`aubmindlab/bert-base-arabertv02`) | 92.15% | 0.9148 |

On a probe set of 37 Sudanese-dialect sentences written by the team, AraBERT was correct on 29 (78.4%) and the TF-IDF baseline on 17 (45.9%). The training data keep sentences with explicit emotion labels, so the baseline performs very well on the test set. The small probe set is a qualitative check, not a benchmark.

## Repository structure

The paths below reflect the current names in GitHub. Some directory names have a trailing space; that space is part of the current path.

| Path | Content |
| --- | --- |
| `Dataset/Initial /` | Initial data folder, including ELQV files, the master dataset, and the ArabicEmpatheticDialogues subfolder. |
| `Dataset - Final sample/` | `Arabic_AraBERT_Training_Clean.xlsx`, train/validation/test splits, test predictions, probe results, and Sudanese probe examples. A CSV copy of the XLSX training file is not currently included. |
| `SANAD System Notebooks /` | ` 01_clean_split_and_comparison.ipynb` (filename begins with a space), `02_curated_verse_list.ipynb`, and `03_bot_arabert_v3.ipynb`. |
| `SANAD System Scripts /` | `clean_split_and_comparison.py`, `curated_verse_list.py`, and `bot_arabert_v3.py`. |
| `README.md` | Project documentation. |
| `CITATION.cff` | Citation metadata; replace the team names and repository URL there if they change. |
| `LICENSE` | MIT licence for the project code. Dataset rights and terms are separate. |

The `00_data_audit` notebook is not currently included in this repository.

## Run it

The notebooks were developed for Google Colab. Training uses Google Drive and a T4 GPU. The training script sets seed 42, creates grouped train/validation/test splits, trains a TF-IDF baseline and AraBERT (4 epochs, learning rate 2e-5, batch size 16), evaluates them, and saves the model and results to Drive. The training script expects `Arabic_AraBERT_Training_Clean.csv` in the root of Drive, while the repository currently contains the final training file as an `.xlsx`; convert it to CSV or adjust the input path before running the training notebook.

1. **Train and compare** – run `SANAD System Notebooks /  01_clean_split_and_comparison.ipynb` (the filename itself starts with a space). This generates grouped splits, trains and evaluates the models, and saves the checkpoint to Google Drive.
2. **Build the verse list** – run `SANAD System Notebooks /02_curated_verse_list.ipynb`. It fetches verse text and tafsir, so this step requires internet access.
3. **Run the bot** – store the Telegram bot token in Google Colab **Secrets** under the name `TELEGRAM_TOKEN`, then run `SANAD System Notebooks /03_bot_arabert_v3.ipynb`. The bot runs only while the notebook session is active. The bot expects trained model files in Google Drive.

**Never put the bot token in code or in a commit.** If a token was ever committed, revoke it with BotFather. Model weights are not included in this repository.

## Limitations

- The system classifies four emotions only; mixed emotions and intensity are not represented.
- The training data contain Modern Standard Arabic and explicit emotion statements. Sudanese dialect, implicit emotion, and negation are handled partly by hand-written rules; negation handling has not been fully verified end to end.
- The curated verses were selected by the project team and have not been reviewed by a religious scholar.
- The safety layer only detects expressions covered by its rules. Its fixed emergency number may not be available in all locations or circumstances.
- There has been no user study; the system was tested manually through Telegram.

## Data and licences

- **Arabic EmpatheticDialogues** (Naous et al., 2021), translated from EmpatheticDialogues (Rashkin et al., 2019). The cited paper does not state a data licence.
- **ELQV** (Almarzoqi and Alsuhaibani, 2025), available from `https://github.com/Arwaalmrzoqi/ELQV`. The cited paper does not state a data licence.
- Dataset rights remain with their respective authors. Check the original sources and licence terms before reuse or redistribution. The MIT licence in this repository applies to project code, not automatically to third-party datasets.

## Citation

If you use this work, please cite it using [`CITATION.cff`](CITATION.cff), and cite the source datasets separately. The citation metadata should be updated with the final author names and correct repository URL before the project is archived.

## Team

**Eithar Ibrahim, Hajer Mohammed, Doaa Ahmed** – BSc in Computer Science and Information Technology, 2026. Supervisor: Dr. Omayma Hussien.
