"""Generate, split, fit on train only, save, reload, and inspect synthetic data."""

import argparse
from collections import Counter
from dataclasses import asdict
import hashlib
import json
from pathlib import Path

from mini_moe.data.synthetic import generate_examples, split_examples
from mini_moe.tokenizer.character import CharacterTokenizer, SPECIAL_TOKENS


def prepare_dataset(
    output_dir: Path, *, seed: int = 42, validation_fraction: float = 0.2
) -> dict[str, object]:
    """Save deterministic artifacts; overwrites the five named output files."""
    # Splitting happens before fit. Validation is never passed to the tokenizer.
    train, validation = split_examples(
        generate_examples(), seed=seed, validation_fraction=validation_fraction
    )
    tokenizer = CharacterTokenizer.fit(example.text for example in train)
    output_dir.mkdir(parents=True, exist_ok=True)
    splits = {"train": train, "validation": validation}
    for name, examples in splits.items():
        content = "".join(
            json.dumps(asdict(example), ensure_ascii=False, sort_keys=True) + "\n"
            for example in examples
        )
        (output_dir / f"{name}.jsonl").write_text(content, encoding="utf-8", newline="\n")
    tokenizer.save(output_dir / "tokenizer.json")
    reloaded = CharacterTokenizer.load(output_dir / "tokenizer.json")
    if reloaded.tokens != tokenizer.tokens:
        raise RuntimeError("saved tokenizer changed vocabulary")

    manifest = {
        "version": 1,
        "source": "local authored synthetic templates v1",
        "seed": seed,
        "validation_fraction": validation_fraction,
        "split_strategy": "family-stratified shuffle; rounded, bounded holdout counts",
        "counts": {name: len(examples) for name, examples in splits.items()},
        "family_counts": {
            name: dict(sorted(Counter(example.family for example in examples).items()))
            for name, examples in splits.items()
        },
        "sha256": {
            filename: hashlib.sha256((output_dir / filename).read_bytes()).hexdigest()
            for filename in ("train.jsonl", "validation.jsonl", "tokenizer.json")
        },
        "tokenizer": {
            "type": "character", "trained_on": "train",
            "vocab_size": reloaded.vocab_size, "special_tokens": list(SPECIAL_TOKENS),
        },
        "validation_unknown_characters": sum(
            reloaded.encode(example.text, add_special_tokens=False).count(reloaded.unk_id)
            for example in validation
        ),
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8", newline="\n",
    )
    (output_dir / "dataset_card.md").write_text(
        f"""# Synthetic dataset card

## Source and generation
Local authored templates in `src/mini_moe/data/synthetic.py`; no external corpus,
downloads, pretrained vocabulary, or LLM API. No third-party dataset license
applies; this repository has not declared a redistribution license.
128 color/animal/location descriptions and 128 four-number counting sequences.
Generator revision: v1. Split seed: {seed}; requested validation fraction: {validation_fraction}.

## Split and tokenizer
Train: {len(train)}; validation: {len(validation)}. Complete, unique texts are
shuffled within each family before tokenization; rounded holdout sizes are bounded
to keep both splits nonempty. `manifest.json` records counts and SHA-256 hashes.
Character vocabulary is fitted on train only, then saved and reloaded.
PAD=0, UNK=1, BOS=2, EOS=3; vocab size: {reloaded.vocab_size}.
Encoding adds BOS/EOS; decoding removes PAD/BOS/EOS and visibly preserves UNK.
Validation unknown character count: {manifest['validation_unknown_characters']}.

## Limitations and leakage risks
This corpus proves local data plumbing, not natural language intelligence.
Train and validation texts are disjoint, but templates, words, and nearby numbers
are shared. This is an in-distribution holdout, not a test of unseen-template or
tool-use generalization. No tool-use examples are included in M1.
Never refit the tokenizer on validation, concatenate validation into training, or
split packed token windows after mixing both splits. Unknown characters lose
information and decode as `<unk>`; covered Unicode and whitespace roundtrip exactly.
Files contain synthetic patterns only, with no collected personal information.
""",
        encoding="utf-8", newline="\n",
    )
    return manifest


def main() -> None:
    """Prepare the corpus offline and print three actual encode/decode examples."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("data/synthetic"))
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--validation-fraction", type=float, default=0.2)
    args = parser.parse_args()
    try:
        manifest = prepare_dataset(
            args.output_dir, seed=args.seed, validation_fraction=args.validation_fraction
        )
    except ValueError as error:
        parser.error(str(error))
    tokenizer = CharacterTokenizer.load(args.output_dir / "tokenizer.json")
    print(json.dumps({"output_dir": str(args.output_dir), "manifest": manifest}, indent=2))
    # Read saved data, so the inspection also checks the actual output artifacts.
    train = [json.loads(line) for line in (args.output_dir / "train.jsonl").read_text(
        encoding="utf-8"
    ).splitlines()]
    validation = [json.loads(line) for line in (args.output_dir / "validation.jsonl").read_text(
        encoding="utf-8"
    ).splitlines()]
    for split, example in (("train", train[0]), ("validation", validation[0]), ("validation", validation[-1])):
        ids = tokenizer.encode(example["text"])
        print(json.dumps({
            "split": split, "family": example["family"], "text": example["text"],
            "ids": ids, "decoded": tokenizer.decode(ids),
            "roundtrip": tokenizer.decode(ids) == example["text"],
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()
