# Initial Dataset Collection

This folder contains the initial datasets used for emotion analysis and Islamic emotional support experiments in this project.

## Included resources

- ELQV.csv
- ELQVv2.csv
- master_emotional_quran_dataset.csv
- ArabicEmpatheticDialogues/

## Purpose

These files provide the raw and partially processed material for learning Arabic emotional expression and for constructing a faith-informed companion system. The dataset combination covers:

- emotional labels in Arabic text
- Qur'anic and religious-context emotional content
- empathetic dialogue data for conversational support
- source material for model fine-tuning and evaluation

## Dataset notes

- The raw files are retained to preserve provenance and reproducibility.
- Some data is further processed in the ArabicEmpatheticDialogues subfolder.
- Final train/validation/test samples for model evaluation are also stored in the root-level Dataset - Final sample folder.

## Suggested use

Use these source datasets to:

1. inspect raw emotion labels and text distributions
2. prepare a cleaned Arabic dataset for training
3. compare model behavior across source-specific splits
4. create a final curated dataset for the emotional companion bot
