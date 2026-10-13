"""Small authored English patterns with deterministic, disjoint holdout splits."""

from dataclasses import dataclass
from itertools import product
import math
import random
from collections import defaultdict
from collections.abc import Sequence


@dataclass(frozen=True)
class Example:
    """One complete sequence; split examples before tokenization or packing."""

    family: str
    text: str


def generate_examples() -> list[Example]:
    """Return 128 descriptions and 128 counting sequences, without downloads."""
    descriptions = [
        Example("description", f"The {color} {animal} is near the {place}.")
        for color, animal, place in product(
            ("red", "blue", "green", "yellow"),
            ("fox", "cat", "dog", "bird"),
            ("tree", "river", "hill", "lake", "house", "garden", "bridge", "forest"),
        )
    ]
    counting = [
        Example("counting", f"Count from {start}: " + ", ".join(
            str(number) for number in range(start, start + 4)
        ) + ".")
        for start in range(128)
    ]
    return descriptions + counting


def split_examples(
    examples: Sequence[Example], *, seed: int = 42, validation_fraction: float = 0.2
) -> tuple[list[Example], list[Example]]:
    """Stratify by family using a local RNG; never split fragments of a text.

    Round the holdout count per family, bounded to [1, family_size - 1].
    Both splits thus include every family even for a small corpus.
    """
    if type(seed) is not int or not 0 <= seed < 2**32:
        raise ValueError("seed must be an integer in [0, 2**32)")
    if not math.isfinite(validation_fraction) or not 0 < validation_fraction < 1:
        raise ValueError("validation_fraction must be finite and between 0 and 1")
    if not examples:
        raise ValueError("examples must not be empty")
    texts = [example.text for example in examples]
    if any(not text.strip() for text in texts) or len(set(texts)) != len(texts):
        raise ValueError("example texts must be nonempty and unique")

    families: dict[str, list[Example]] = defaultdict(list)
    for example in examples:
        if not example.family:
            raise ValueError("example family must not be empty")
        families[example.family].append(example)
    rng = random.Random(seed)
    train: list[Example] = []
    validation: list[Example] = []
    for family in sorted(families):
        group = families[family].copy()
        if len(group) < 2:
            raise ValueError("each family needs at least two examples")
        rng.shuffle(group)
        count = max(1, min(len(group) - 1, round(len(group) * validation_fraction)))
        validation.extend(group[:count])
        train.extend(group[count:])
    rng.shuffle(train)
    rng.shuffle(validation)
    return train, validation
