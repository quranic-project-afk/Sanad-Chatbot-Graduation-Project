# Arabic Empathetic Dialogues Dataset

This directory contains the Arabic empathetic dialogue resources used to support emotional-response modeling and human-like conversational behavior.

## Contents

### Raw dataset

- arabic-empathetic-conversations.csv

This raw file contains the original conversations used as the source for Arabic empathetic dialogue research.

### Processed dataset

- arabic_empathetic_dialogues_clean.csv
- preprocess_empathetic_dialogues.py
- create_mvp_sample.py
- Final version/
  - arabic_empathetic_dialogues_1000.csv

## Workflow

The preprocessing pipeline converts the raw dialogue source into a cleaned and filtered Arabic dataset suitable for downstream modeling tasks.

- preprocessing normalizes and cleans text
- noisy or malformed entries are filtered
- a final sample is generated for quicker experimentation and evaluation
- a 1000-sample version is included as a compact final dataset

## Usage

This dataset is used to:

- teach the model empathetic style in Arabic
- provide conversational examples of emotional support and reflection
- complement the Quranic and emotional-text dataset in the broader project

## Notes

The processed files are intended for experimentation and model development. The final project outputs are represented in the wider repository and in the final sample split files outside this folder.
