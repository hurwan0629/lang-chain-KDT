"""A train-fitted character vocabulary with explicit framing and unknowns."""

from collections.abc import Iterable, Sequence
import json
from pathlib import Path


SPECIAL_TOKENS = ("<pad>", "<unk>", "<bos>", "<eos>")


class CharacterTokenizer:
    """Encode exact Unicode characters; no normalization or pretrained vocab.

    IDs 0..3 are PAD/UNK/BOS/EOS. Unknown characters decode as the visible
    '<unk>' marker, so roundtrip is exact only for covered characters.
    """

    pad_id = 0
    unk_id = 1
    bos_id = 2
    eos_id = 3

    def __init__(self, tokens: Sequence[str]) -> None:
        tokens = tuple(tokens)
        if (
            tokens[:4] != SPECIAL_TOKENS
            or any(not isinstance(token, str) or len(token) != 1 for token in tokens[4:])
            or len(set(tokens)) != len(tokens)
        ):
            raise ValueError("invalid character vocabulary or special token order")
        self.tokens = tokens
        self._token_ids = {token: index for index, token in enumerate(tokens)}

    @property
    def vocab_size(self) -> int:
        """Number of output classes for the future language model."""
        return len(self.tokens)

    @classmethod
    def fit(cls, train_texts: Iterable[str]) -> "CharacterTokenizer":
        """Learn sorted characters from training texts only; consumes one pass."""
        characters: set[str] = set()
        for text in train_texts:
            if not isinstance(text, str):
                raise ValueError("training texts must be strings")
            characters.update(text)
        if not characters:
            raise ValueError("training texts must contain at least one character")
        return cls((*SPECIAL_TOKENS, *sorted(characters)))

    def encode(self, text: str, *, add_special_tokens: bool = True) -> list[int]:
        """Return [T] token IDs; default framing is BOS + characters + EOS."""
        if not isinstance(text, str):
            raise ValueError("text must be a string")
        ids = [self._token_ids.get(character, self.unk_id) for character in text]
        return [self.bos_id, *ids, self.eos_id] if add_special_tokens else ids

    def decode(self, ids: Iterable[int], *, skip_special_tokens: bool = True) -> str:
        """Omit PAD/BOS/EOS by default, but preserve UNK as a visible marker."""
        tokens: list[str] = []
        for token_id in ids:
            if type(token_id) is not int or not 0 <= token_id < self.vocab_size:
                raise ValueError("token ID must be an integer within the vocabulary")
            if skip_special_tokens and token_id in (self.pad_id, self.bos_id, self.eos_id):
                continue
            tokens.append(self.tokens[token_id])
        return "".join(tokens)

    def save(self, path: str | Path) -> None:
        """Write portable UTF-8 JSON, including a format version."""
        payload = {"version": 1, "type": "character", "tokens": self.tokens}
        Path(path).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8", newline="\n",
        )

    @classmethod
    def load(cls, path: str | Path) -> "CharacterTokenizer":
        """Reject incompatible formats rather than silently changing token IDs."""
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        if (
            not isinstance(payload, dict)
            or type(payload.get("version")) is not int
            or payload["version"] != 1
            or payload.get("type") != "character"
            or not isinstance(payload.get("tokens"), list)
        ):
            raise ValueError("unsupported tokenizer format")
        return cls(payload["tokens"])
