# Smart Arabic Islamic Emotional Companion

An AI-powered Arabic conversational system that detects emotional states and provides personalized spiritual support through empathetic, culturally aware responses grounded in Islamic guidance.

## Overview

This repository contains the data, experiments, and bot pipeline for an Arabic emotional companion that recognizes emotions such as fear, joy, anger, and sadness, then responds with supportive and spiritually informed language. The system includes safety escalation rules, curated Quranic verse recommendations, and model training scripts for Arabic emotion classification.

## Core idea

- Detect emotion from Arabic user messages
- Respond with compassionate Arabic dialogue
- Use Islamic reflections and Quranic verses for comfort and guidance
- Protect users with emergency detection rules for self-harm, medical issues, violence, and disaster scenarios
- Support Sudanese and dialect-aware phrasing in the bot interaction layer

## Repository structure

```text
Smart-Arabic-Islamic-Emotional-Companion/
├── README.md
├── Dataset/
│   └── Initial /
│       ├── README.md
│       ├── ELQV.csv
│       ├── ELQVv2.csv
│       ├── master_emotional_quran_dataset.csv
│       └── ArabicEmpatheticDialogues/
│           ├── README.md
│           ├── Raw dataset/
│           │   └── arabic-empathetic-conversations.csv
│           └── Processed dataset/
│               ├── arabic_empathetic_dialogues_clean.csv
│               ├── create_mvp_sample.py
│               ├── preprocess_empathetic_dialogues.py
│               └── Final version/
│                   └── arabic_empathetic_dialogues_1000.csv
├── Dataset - Final sample/
│   ├── split_train.csv
│   ├── split_val.csv
│   ├── split_test.csv
│   ├── test_predictions.csv
│   ├── probe_results.csv
│   ├── sudanese_probe.csv
│   └── Arabic_AraBERT_Training_Clean.xlsx
├── SANAD System Notebooks /
│   ├── 01_clean_split_and_comparison.ipynb.ipynb
│   ├── 02_curated_verse_list.ipynb.ipynb
│   └── 03_bot_arabert_v3.ipynb.ipynb
├── SANAD System Scripts /
│   ├── clean_split_and_comparison.py
│   ├── curated_verse_list.py
│   └── bot_arabert_v3.py
└── .git/
```

## Data sources

The project combines several Arabic emotional datasets and dialogue resources:

- ELQV and ELQVv2: emotional and Quranic alignment data
- master_emotional_quran_dataset.csv: consolidated emotional dataset for training and evaluation
- Arabic empathetic dialogues corpus: real conversational emotion data in Arabic
- Final sample split files: train, validation, and test partitions for model comparison

## Modeling and pipeline

The workflow follows a practical NLP pipeline:

1. Clean and normalize Arabic text
2. Remove duplicates and avoid data leakage across sources
3. Split the dataset by source row or group to prevent contamination
4. Train baseline models such as TF-IDF + Logistic Regression
5. Train a transformer-based Arabic model such as AraBERT
6. Evaluate on clean test data and Sudanese probe examples
7. Use curated verse and response banks for empathetic spiritual replies
8. Deploy the final model in a bot interface

## Safety layer

The bot includes a protective safety layer designed to detect urgent cases such as:

- self-harm or suicidal intent
- medical emergencies
- violence or assault
- fire or accident scenarios

These rules are intentionally checked before normal conversational responses, so the system can redirect the user toward emergency assistance or trusted support.

## Notebooks and scripts

- 01_clean_split_and_comparison.ipynb: dataset cleaning, source-aware splitting, and model benchmarking
- 02_curated_verse_list.ipynb: creation of a curated set of verses and response templates
- 03_bot_arabert_v3.ipynb: final bot orchestration and inference path
- clean_split_and_comparison.py: Python version of the cleaning and model-comparison pipeline
- curated_verse_list.py: verse selection and assisted response logic
- bot_arabert_v3.py: Telegram bot logic with model inference, safety checks, and emotional response generation

## Recommended workflow

1. Review the dataset in the Dataset folders.
2. Run the cleaning and comparison pipeline to prepare train/validation/test splits.
3. Train or load the Arabic model weights.
4. Use the curated verse templates to ground responses in Islamic support.
5. Launch the bot script for interactive use.

## Notes

- The repository includes prepared sample outputs under Dataset - Final sample, but model checkpoints are not bundled in the repo and may need to be generated or restored from a separate training run.
- The project is designed around Arabic-language emotional support and should be adapted carefully for deployment in production settings, especially where safety-critical messaging is involved.
