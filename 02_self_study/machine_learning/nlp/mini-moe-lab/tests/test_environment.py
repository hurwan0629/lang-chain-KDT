"""M0 acceptance checks; no network, datasets, or model weights needed."""

import json
import random
import sys

import numpy as np
import pytest
import torch

from mini_moe.environment import environment_info, main, set_seed


def test_seed_replays_python_numpy_and_torch_cpu() -> None:
    set_seed(42)
    python_sample = [random.random() for _ in range(4)]
    numpy_sample = np.random.random(8)
    torch_sample = torch.rand(8, device="cpu")
    set_seed(42)
    assert [random.random() for _ in range(4)] == python_sample
    assert np.array_equal(np.random.random(8), numpy_sample)
    assert torch.equal(torch.rand(8, device="cpu"), torch_sample)
    assert torch.are_deterministic_algorithms_enabled()
    assert not torch.backends.cudnn.benchmark
    assert torch.backends.cudnn.deterministic
    set_seed(43)
    assert not torch.equal(torch.rand(8, device="cpu"), torch_sample)


@pytest.mark.parametrize("seed", [-1, 2**32, True, 1.5, "42"])
def test_seed_rejects_invalid_values(seed: object) -> None:
    with pytest.raises(ValueError, match="seed must be an integer"):
        set_seed(seed)  # type: ignore[arg-type]


def test_environment_report() -> None:
    report = environment_info()
    assert report["python"]
    assert report["cpu"]
    assert report["torch"] == str(torch.__version__)
    assert report["cuda_available"] == torch.cuda.is_available()
    assert len(report["gpu_names"]) == (
        torch.cuda.device_count() if torch.cuda.is_available() else 0
    )
    json.dumps(report)


def test_cpu_smoke_cli(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sys, "argv", ["mini_moe.environment", "--seed", "7"])
    main()
    report = json.loads(capsys.readouterr().out)
    assert report["device"] == "cpu"
    assert report["seed"] == 7
    assert report["seed_reproducible"] is True
    assert report["deterministic_algorithms"] is True
    assert report["cpu_matmul"] == [[1.0, 3.0], [3.0, 13.0]]


def test_cli_rejects_invalid_seed(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sys, "argv", ["mini_moe.environment", "--seed", "-1"])
    with pytest.raises(SystemExit) as error:
        main()
    assert error.value.code == 2
    assert "seed must be an integer" in capsys.readouterr().err
