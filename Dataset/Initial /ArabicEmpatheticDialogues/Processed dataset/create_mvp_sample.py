import csv
import random
from collections import Counter, defaultdict
from pathlib import Path

INPUT_PATH = Path(__file__).with_name("arabic_empathetic_dialogues_clean.csv")
OUTPUT_PATH = Path(__file__).with_name("arabic_empathetic_dialogues_1000.csv")

RANDOM_STATE = 42
SAMPLE_SIZE = 1000
COLUMNS = ["emotion", "context", "response", "data_type"]


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def allocate_sample_sizes(counts: Counter[str], total: int) -> dict[str, int]:
    total_rows = sum(counts.values())
    raw = {label: (counts[label] / total_rows) * total for label in counts}
    base = {label: int(value) for label, value in raw.items()}
    remainder = total - sum(base.values())

    labels_by_fraction = sorted(
        counts.keys(),
        key=lambda label: (raw[label] - base[label], counts[label]),
        reverse=True,
    )
    for label in labels_by_fraction[:remainder]:
        base[label] += 1

    return base


def stratified_sample(
    rows: list[dict[str, str]], sample_size: int, random_state: int
) -> list[dict[str, str]]:
    rng = random.Random(random_state)
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["emotion"]].append(row)

    counts = Counter(row["emotion"] for row in rows)
    targets = allocate_sample_sizes(counts, sample_size)

    sampled: list[dict[str, str]] = []
    for emotion in sorted(targets):
        pool = grouped[emotion]
        n = targets[emotion]
        if n > len(pool):
            raise ValueError(
                f"Requested {n} rows for '{emotion}', but only {len(pool)} available."
            )
        sampled.extend(rng.sample(pool, n))

    rng.shuffle(sampled)
    return sampled


def distribution(counts: Counter[str], total: int) -> dict[str, dict[str, float | int]]:
    return {
        label: {
            "count": counts.get(label, 0),
            "percentage": (counts.get(label, 0) / total * 100) if total else 0.0,
        }
        for label in sorted(counts)
    }


def max_distribution_error(
    original: Counter[str], sample: Counter[str], original_total: int, sample_total: int
) -> float:
    errors = []
    for label in sorted(original):
        orig_pct = original[label] / original_total * 100
        sample_pct = sample.get(label, 0) / sample_total * 100
        errors.append(abs(orig_pct - sample_pct))
    return max(errors)


def has_missing(row: dict[str, str]) -> bool:
    return any(not row[col] for col in COLUMNS)


def count_duplicates(rows: list[dict[str, str]]) -> int:
    seen: set[tuple[str, ...]] = set()
    duplicates = 0
    for row in rows:
        key = tuple(row[col] for col in COLUMNS)
        if key in seen:
            duplicates += 1
        seen.add(key)
    return duplicates


def print_distribution(title: str, counts: Counter[str], total: int) -> None:
    print(title)
    for label in sorted(counts):
        count = counts[label]
        pct = count / total * 100 if total else 0
        print(f"  {label}: {count:,} ({pct:.2f}%)")


def main() -> None:
    rows = load_rows(INPUT_PATH)
    original_counts = Counter(row["emotion"] for row in rows)
    sampled_rows = stratified_sample(rows, SAMPLE_SIZE, RANDOM_STATE)
    sample_counts = Counter(row["emotion"] for row in sampled_rows)

    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(sampled_rows)

    missing_values = sum(1 for row in sampled_rows if has_missing(row))
    duplicate_rows = count_duplicates(sampled_rows)
    max_error = max_distribution_error(
        original_counts, sample_counts, len(rows), len(sampled_rows)
    )

    print("=== MVP Sample Statistics ===")
    print(f"Original dataset size: {len(rows):,}")
    print(f"Sample size: {len(sampled_rows):,}")
    print(f"Number of emotion classes: {len(sample_counts)}")
    print()
    print_distribution("Distribution of the four emotion classes:", sample_counts, len(sampled_rows))
    print()
    print(f"Missing values: {missing_values}")
    print(f"Duplicate rows: {duplicate_rows}")
    print()
    print("=== Distribution Preservation Check ===")
    print_distribution("Original distribution:", original_counts, len(rows))
    print()
    print_distribution("Sampled distribution:", sample_counts, len(sampled_rows))
    print()
    print("Per-class sampling error (absolute percentage point difference):")
    for label in sorted(original_counts):
        orig_pct = original_counts[label] / len(rows) * 100
        sample_pct = sample_counts[label] / len(sampled_rows) * 100
        diff = sample_pct - orig_pct
        print(f"  {label}: {diff:+.2f} pp")
    print()
    print(f"Maximum absolute sampling error: {max_error:.2f} pp")
    if max_error <= 1.0:
        print("Verification: PASS (max error <= 1.00 pp)")
    else:
        print("Verification: REVIEW (max error > 1.00 pp)")
    print()
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
