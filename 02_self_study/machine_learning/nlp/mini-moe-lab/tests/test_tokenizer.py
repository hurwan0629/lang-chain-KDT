"""Vocabulary fitting, Unicode roundtrip, framing, and serialization checks."""

import json
from pathlib import Path

import pytest

from mini_moe.tokenizer.character import CharacterTokenizer, SPECIAL_TOKENS


def test_exact_roundtrip_and_special_token_conventions(tmp_path: Path) -> None:
    texts = ["The red fox.", "Count: 1, 2, 3.", "\t한글 🙂\n<bos>", ""]
    tokenizer = CharacterTokenizer.fit(iter(texts))
    assert tokenizer.tokens[:4] == SPECIAL_TOKENS
    assert (tokenizer.pad_id, tokenizer.unk_id, tokenizer.bos_id, tokenizer.eos_id) == (0, 1, 2, 3)
    assert tokenizer.tokens == CharacterTokenizer.fit(reversed(texts)).tokens
    for text in texts:
        ids = tokenizer.encode(text)
        assert ids[0] == 2 and ids[-1] == 3
        assert len(ids) == len(text) + 2
        assert tokenizer.decode([0, *ids, 0]) == text
        assert tokenizer.decode(tokenizer.encode(text, add_special_tokens=False)) == text
        assert tokenizer.decode(ids, skip_special_tokens=False) == f"<bos>{text}<eos>"
    path = tmp_path / "tokenizer.json"
    tokenizer.save(path)
    reloaded = CharacterTokenizer.load(path)
    assert reloaded.tokens == tokenizer.tokens
    for text in texts:
        assert reloaded.encode(text) == tokenizer.encode(text)
        assert reloaded.decode(reloaded.encode(text)) == text


def test_unseen_validation_character_does_not_grow_vocabulary() -> None:
    tokenizer = CharacterTokenizer.fit(["train only"])
    original = tokenizer.tokens
    ids = tokenizer.encode("train Ω")
    assert "Ω" not in tokenizer.tokens
    assert ids.count(tokenizer.unk_id) == 1
    assert tokenizer.decode(ids) == "train <unk>"
    assert tokenizer.tokens == original


@pytest.mark.parametrize("texts", [[], [""], [123]])
def test_fit_rejects_empty_or_invalid_training_text(texts: list) -> None:
    with pytest.raises(ValueError):
        CharacterTokenizer.fit(texts)


@pytest.mark.parametrize("token_id", [-1, 999, True, 1.0, "1"])
def test_decode_rejects_invalid_ids(token_id: object) -> None:
    tokenizer = CharacterTokenizer.fit(["a"])
    with pytest.raises(ValueError, match="token ID"):
        tokenizer.decode([token_id])  # type: ignore[list-item]


@pytest.mark.parametrize("payload", [
    [],
    {"version": 2, "type": "character", "tokens": list(SPECIAL_TOKENS)},
    {"version": 1, "type": "bpe", "tokens": list(SPECIAL_TOKENS)},
    {"version": 1, "type": "character", "tokens": "invalid"},
    {"version": 1, "type": "character", "tokens": ["<unk>", "<pad>", "<bos>", "<eos>"]},
    {"version": 1, "type": "character", "tokens": [*SPECIAL_TOKENS, "a", "a"]},
    {"version": 1, "type": "character", "tokens": [*SPECIAL_TOKENS, "word"]},
])
def test_load_rejects_invalid_schema(tmp_path: Path, payload: object) -> None:
    path = tmp_path / "invalid.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError):
        CharacterTokenizer.load(path)
