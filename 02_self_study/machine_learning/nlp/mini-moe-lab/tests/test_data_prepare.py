"""Offline pipeline tests, including a held-out-only character leakage trap."""

import hashlib
import json
from pathlib import Path
import sys

import pytest

from mini_moe.data import prepare
from mini_moe.data.synthetic import Example
from mini_moe.tokenizer.character import CharacterTokenizer


def read_split(output_dir: Path, name: str) -> list[dict[str, str]]:
    return [json.loads(line) for line in (output_dir / f"{name}.jsonl").read_text(
        encoding="utf-8"
    ).splitlines()]


def test_saved_artifacts_are_reproducible_and_roundtrip(tmp_path: Path) -> None:
    first, second = tmp_path / "first", tmp_path / "second"
    manifest = prepare.prepare_dataset(first)
    assert manifest == prepare.prepare_dataset(second)
    for path in first.iterdir():
        assert path.read_bytes() == (second / path.name).read_bytes()
    assert json.loads((first / "manifest.json").read_text(encoding="utf-8")) == manifest
    assert manifest["counts"] == {"train": 204, "validation": 52}
    tokenizer = CharacterTokenizer.load(first / "tokenizer.json")
    train, validation = read_split(first, "train"), read_split(first, "validation")
    assert {item["text"] for item in train}.isdisjoint(item["text"] for item in validation)
    assert tokenizer.tokens == CharacterTokenizer.fit(item["text"] for item in train).tokens
    for example in train + validation:
        assert tokenizer.decode(tokenizer.encode(example["text"])) == example["text"]
    for filename, digest in manifest["sha256"].items():
        assert hashlib.sha256((first / filename).read_bytes()).hexdigest() == digest
    assert "Limitations and leakage risks" in (first / "dataset_card.md").read_text(encoding="utf-8")
    assert manifest["validation_unknown_characters"] == 0


def test_pipeline_fits_train_only(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    train = [Example("fixture", "train only")]
    validation = [Example("fixture", "heldout Ω")]
    monkeypatch.setattr(prepare, "split_examples", lambda *args, **kwargs: (train, validation))
    manifest = prepare.prepare_dataset(tmp_path)
    tokenizer = CharacterTokenizer.load(tmp_path / "tokenizer.json")
    assert tokenizer.tokens == CharacterTokenizer.fit(["train only"]).tokens
    assert "Ω" not in tokenizer.tokens
    assert manifest["validation_unknown_characters"] > 0
    assert read_split(tmp_path, "train") == [{"family": "fixture", "text": "train only"}]


def test_cli_prints_three_saved_encode_decode_examples(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sys, "argv", ["prepare", "--output-dir", str(tmp_path)])
    prepare.main()
    output = capsys.readouterr().out
    report, offset = json.JSONDecoder().raw_decode(output)
    examples = [json.loads(line) for line in output[offset:].strip().splitlines()]
    assert report["manifest"]["counts"] == {"train": 204, "validation": 52}
    assert len(examples) == 3
    assert {example["split"] for example in examples} == {"train", "validation"}
    assert all(example["roundtrip"] and example["text"] == example["decoded"] for example in examples)


def test_invalid_cli_leaves_no_artifacts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    output = tmp_path / "invalid"
    monkeypatch.setattr(sys, "argv", [
        "prepare", "--output-dir", str(output), "--validation-fraction", "1",
    ])
    with pytest.raises(SystemExit) as error:
        prepare.main()
    assert error.value.code == 2
    assert "validation_fraction" in capsys.readouterr().err
    assert not output.exists()
