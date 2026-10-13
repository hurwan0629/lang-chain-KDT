"""Synthetic corpus acceptance: reproducibility and example-level holdout."""

from collections import Counter
import random

import pytest

from mini_moe.data.synthetic import Example, generate_examples, split_examples


def test_corpus_is_unique_and_split_is_reproducible() -> None:
    examples = generate_examples()
    assert len(examples) == len({example.text for example in examples}) == 256
    assert Counter(example.family for example in examples) == {
        "description": 128, "counting": 128,
    }
    original = examples.copy()
    random_state = random.getstate()
    train, validation = split_examples(examples, seed=42)
    assert random.getstate() == random_state
    assert examples == original
    assert (train, validation) == split_examples(generate_examples(), seed=42)
    assert (train, validation) != split_examples(examples, seed=43)
    assert (len(train), len(validation)) == (204, 52)
    assert {example.text for example in train}.isdisjoint(example.text for example in validation)
    assert set(train) | set(validation) == set(examples)
    assert Counter(example.family for example in train) == {"description": 102, "counting": 102}
    assert Counter(example.family for example in validation) == {"description": 26, "counting": 26}


@pytest.mark.parametrize("fraction", [0, 1, -0.1, float("nan"), float("inf")])
def test_invalid_validation_fraction(fraction: float) -> None:
    with pytest.raises(ValueError, match="validation_fraction"):
        split_examples(generate_examples(), validation_fraction=fraction)


@pytest.mark.parametrize("seed", [-1, 2**32, True])
def test_invalid_seed(seed: int) -> None:
    with pytest.raises(ValueError, match="seed"):
        split_examples(generate_examples(), seed=seed)


@pytest.mark.parametrize("examples", [
    [],
    [Example("a", "same"), Example("b", "same")],
    [Example("a", " "), Example("a", "valid")],
    [Example("a", "only one")],
    [Example("", "one"), Example("", "two")],
])
def test_rejects_unusable_examples(examples: list[Example]) -> None:
    with pytest.raises(ValueError):
        split_examples(examples)


@pytest.mark.parametrize("fraction", [0.001, 0.999])
def test_small_families_keep_both_splits(fraction: float) -> None:
    train, validation = split_examples(
        [Example("a", "one"), Example("a", "two")], validation_fraction=fraction
    )
    assert len(train) == len(validation) == 1
