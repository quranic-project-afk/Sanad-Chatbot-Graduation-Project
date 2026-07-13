import csv
from collections import Counter
from pathlib import Path

INPUT_PATH = Path(__file__).with_name("arabic-empathetic-conversations.csv")
OUTPUT_PATH = Path(__file__).with_name("arabic_empathetic_dialogues_clean.csv")

EMOTION_MAP = {
    # fear
    "afraid": "fear",
    "terrified": "fear",
    "anxious": "fear",
    "apprehensive": "fear",
    # anger
    "angry": "anger",
    "furious": "anger",
    "annoyed": "anger",
    "disgusted": "anger",
    # joy
    "joyful": "joy",
    "excited": "joy",
    "grateful": "joy",
    "proud": "joy",
    "hopeful": "joy",
    "content": "joy",
    "anticipating": "joy",
    # sadness
    "sad": "sadness",
    "lonely": "sadness",
    "devastated": "sadness",
    "disappointed": "sadness",
    "ashamed": "sadness",
    "guilty": "sadness",
    "embarrassed": "sadness",
    "sentimental": "sadness",
    "nostalgic": "sadness",
}

COLUMNS = ["emotion", "context", "response", "data_type"]


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [
            {
                "emotion": (row.get("emotion") or "").strip(),
                "context": row.get("context") or "",
                "response": row.get("response") or "",
            }
            for row in reader
        ]


def has_missing(row: dict[str, str]) -> bool:
    return not row["emotion"] or not row["context"] or not row["response"]


def deduplicate(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str, str]] = set()
    unique_rows: list[dict[str, str]] = []
    for row in rows:
        key = (row["emotion"], row["context"], row["response"])
        if key in seen:
            continue
        seen.add(key)
        unique_rows.append(row)
    return unique_rows


def main() -> None:
    original_rows = load_rows(INPUT_PATH)
    original_count = len(original_rows)

    rows = [row for row in original_rows if not has_missing(row)]
    rows = deduplicate(rows)

    cleaned_rows: list[dict[str, str]] = []
    for row in rows:
        mapped_emotion = EMOTION_MAP.get(row["emotion"])
        if mapped_emotion is None:
            continue
        cleaned_rows.append(
            {
                "emotion": mapped_emotion,
                "context": row["context"],
                "response": row["response"],
                "data_type": "dialogue",
            }
        )

    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    emotion_distribution = Counter(row["emotion"] for row in cleaned_rows)
    missing_values = sum(
        1
        for row in cleaned_rows
        if not row["emotion"] or not row["context"] or not row["response"]
    )
    duplicate_rows = len(cleaned_rows) - len(
        {(r["emotion"], r["context"], r["response"]) for r in cleaned_rows}
    )

    print("=== Preprocessing Statistics ===")
    print(f"Original number of rows: {original_count:,}")
    print(f"Number of rows after cleaning: {len(cleaned_rows):,}")
    print(f"Number of removed rows: {original_count - len(cleaned_rows):,}")
    print(f"Number of emotion classes: {len(emotion_distribution)}")
    print()
    print("Distribution of the four emotions:")
    for emotion in ("fear", "anger", "joy", "sadness"):
        count = emotion_distribution.get(emotion, 0)
        pct = (count / len(cleaned_rows) * 100) if cleaned_rows else 0
        print(f"  {emotion}: {count:,} ({pct:.2f}%)")
    print()
    print(f"Missing values: {missing_values}")
    print(f"Duplicate rows: {duplicate_rows}")
    print()
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
