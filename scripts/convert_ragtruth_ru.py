"""Convert translated Russian RAGTruth JSONL files to LettuceDetect format."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from lettucedetect.detectors.prompt_utils import PromptUtils


def load_jsonl(path: Path) -> list[dict]:
    """Load a JSONL file."""
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def parse_labels(raw_labels: str | list[dict], answer: str, sample_id: str) -> list[dict]:
    """Parse labels and normalize them to LettuceDetect span annotations."""
    labels = json.loads(raw_labels) if isinstance(raw_labels, str) else raw_labels
    normalized = []

    for label in labels:
        start = int(label["start"])
        end = int(label["end"])
        text = label.get("text", "")

        if text and answer[start:end] != text:
            print(
                f"Warning: label text mismatch in sample {sample_id}: "
                f"offset text={answer[start:end]!r}, label text={text!r}"
            )

        normalized.append({"start": start, "end": end, "label": "hallucination"})

    return normalized


def convert_row(row: dict, split: str) -> dict:
    """Convert one translated QA row to the processed hallucination format."""
    context = row["context"]
    passages = [part.strip() for part in context.split("\n\n") if part.strip()]
    if not passages:
        passages = [context]

    answer = row["output"]
    return {
        "prompt": PromptUtils.format_context(passages, row["query"], lang="ru"),
        "answer": answer,
        "labels": parse_labels(row["hallucination_labels"], answer, str(row.get("id", ""))),
        "split": split,
        "task_type": "qa",
        "dataset": "ragtruth",
        "language": "ru",
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert data/ragtruth-ru/train.jsonl and test.jsonl to ragtruth_data.json"
    )
    parser.add_argument("--input-dir", type=Path, default=Path("data/ragtruth-ru"))
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/ragtruth-ru/ragtruth_data.json"),
    )
    args = parser.parse_args()

    samples = []
    for split in ("train", "test"):
        path = args.input_dir / f"{split}.jsonl"
        for row in load_jsonl(path):
            samples.append(convert_row(row, split))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(samples, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(samples)} samples to {args.output}")


if __name__ == "__main__":
    main()
