# SANAD – Smart Qur'anic Emotional Companion

SANAD is a Telegram companion for Sudanese-Arabic users. It reads a message, detects one of four emotions (fear, joy, anger, sadness), and replies with a short Sudanese-dialect response and a Qur'anic verse with its tafsir, taken from a manually curated list of 99 verses. A rule-based safety layer reads every message first and answers risk messages with a fixed emergency reply.

This is the code and data of a BSc (Information Technology) graduation project, University of Khartoum, 2026.

> **Not a clinical tool.** SANAD offers emotional and spiritual comfort only. It does not diagnose, treat, or give religious rulings, and it does not replace a doctor, a counsellor, or emergency services. It generates no text: every reply is built from prepared sentences and a verified verse.

## How it works

```
Telegram message
   │
   ▼
Safety layer (6 categories, 93 regex patterns) ──► fixed emergency reply (number 999) ─► stop
   │
   ▼
Greeting check ──► prepared greeting ─► stop
   │
   ▼
Emotion: AraBERT classifier + decision rules (negation, confidence 0.55, explicit words, confusion phrases, hardship words)
   │
   ▼
Verse selection from 99 curated verses (trigger words, last 8 verses not repeated)
   │
   ▼
Reply assembled from Sudanese-dialect sentence banks + verse + Al-Muyassar tafsir
```

Verse text and tafsir are fetched from the [Al-Quran Cloud API](https://alquran.cloud/api), and each reference is checked against a key phrase before it is accepted.

## Results

Evaluated on a test set split by source dialogue (no dialogue appears in more than one partition). Test set: 382 sentences.

| Model | Accuracy | Macro-F1 |
| --- | --- | --- |
| TF-IDF + Logistic Regression | 97.91% | 0.9775 |
| AraBERT (`aubmindlab/bert-base-arabertv02`) | 92.15% | 0.9148 |

On a small probe set of 37 Sudanese-dialect sentences written by the team, AraBERT was correct on 29 (78.4%) and the TF-IDF baseline on 17 (45.9%). The training data keep only sentences with an explicit emotion, so the simple baseline does very well on the test set. The probe set is a qualitative check, not a benchmark.

## Repository structure

| Path | Content |
| --- | --- |
| `Dataset/Initial/` | Source data: ELQV files, the Arabic EmpatheticDialogues corpus (raw and processed), and the preprocessing scripts |
| `Dataset - Final sample/` | Final training file, the train/validation/test splits, test predictions, and probe results |
| `SANAD System Notebooks/` | `01` clean split and model comparison, `02` curated verse list, `03` Telegram bot |
| `SANAD System Scripts/` | The same three steps as Python scripts |

## Run it

The notebooks were developed on Google Colab with a T4 GPU (Python 3.13, PyTorch 2.11, Transformers 5.21, scikit-learn 1.6.1, python-telegram-bot 22.8).

1. **Train and compare** – run notebook `01`. It builds the grouped split, trains the TF-IDF baseline and AraBERT (4 epochs, learning rate 2e-5, batch size 16, seed 42), prints the metrics, and saves the model to Google Drive.
2. **Build the verse list** – run notebook `02`. It fetches the 99 verses and their tafsir from Al-Quran Cloud and rejects any reference whose key phrase is not found. This step needs an internet connection.
3. **Run the bot** – create a bot with [@BotFather](https://t.me/BotFather), store its token in Colab **Secrets** (key icon in the left bar), and run notebook `03`. The bot runs only while the notebook session is running.

**Never put the bot token in the code or in a commit.** If a token was ever committed, revoke it with BotFather.

Model weights are not included in this repository.

## Limitations

- Four emotions only; mixed emotions and intensity are not represented.
- The training data are Modern Standard Arabic and explicit emotion statements; Sudanese dialect, implicit emotion, and negation are handled only by hand-written rules, and negation handling was not fully verified end to end.
- The 99 verses were chosen by the project team and have not been reviewed by a religious scholar.
- The safety layer detects only the expressions it lists. Emergency number 999 was checked against public sources and may be unavailable in conflict-affected areas.
- There is no user study; the system was tested manually through Telegram.

## Data and licences

- **Arabic EmpatheticDialogues** (Naous et al., 2021), translated from EmpatheticDialogues (Rashkin et al., 2019). The paper states no data licence.
- **ELQV** (Almarzoqi and Alsuhaibani, 2025), `github.com/Arwaalmrzoqi/ELQV`. The paper states no data licence.
- The rights to these datasets belong to their authors. Check the original repositories before reusing the data.
- The code in this repository is released under the MIT licence (see `LICENSE`).

## Citation

If you use this work, please cite it using `CITATION.cff` (GitHub shows a "Cite this repository" button), and cite the datasets above.

## Team

**[ADD: names of the team members]** – Supervisor: Dr. Omayma Hussien.
