"""Environment inspection and repeatable Python/NumPy/PyTorch CPU checks."""

import argparse
import json
import os
import platform
import random

import numpy as np
import torch


def set_seed(seed: int) -> None:
    """Seed Python/NumPy/PyTorch RNGs and require deterministic operations.

    Reproducibility is scoped to the same software and hardware environment.
    PYTHONHASHSEED must be set before process launch if hash ordering matters.
    """
    if type(seed) is not int or not 0 <= seed < 2**32:
        raise ValueError("seed must be an integer in [0, 2**32)")
    # cuBLAS reads this before CUDA work; call seed setup before GPU operations.
    os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.use_deterministic_algorithms(True)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True


def environment_info() -> dict[str, object]:
    """Describe the runtime; CUDA availability does not change the device."""
    cuda_available = torch.cuda.is_available()
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "cpu": platform.processor() or platform.machine(),
        "cpu_count": os.cpu_count(),
        "torch": str(torch.__version__),
        "numpy": np.__version__,
        "torch_threads": torch.get_num_threads(),
        "cuda_build": torch.version.cuda,
        "cuda_available": cuda_available,
        "gpu_names": [
            torch.cuda.get_device_name(index)
            for index in range(torch.cuda.device_count() if cuda_available else 0)
        ],
    }


def main() -> None:
    """Print a JSON environment report and run a finite CPU smoke check."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    try:
        set_seed(args.seed)
    except ValueError as error:
        parser.error(str(error))

    python_sample = random.random()
    numpy_sample = np.random.random(4)
    sample = torch.rand(4, device="cpu")
    set_seed(args.seed)
    seed_reproducible = (
        python_sample == random.random()
        and np.array_equal(numpy_sample, np.random.random(4))
        and torch.equal(sample, torch.rand(4, device="cpu"))
    )
    if not seed_reproducible:
        raise RuntimeError("CPU seed replay failed")

    # A [2, 2] matrix multiply exercises PyTorch without a model or dataset.
    matrix = torch.arange(4, dtype=torch.float32, device="cpu").reshape(2, 2)
    product = matrix @ matrix.T
    expected = torch.tensor([[1.0, 3.0], [3.0, 13.0]], device="cpu")
    if not torch.equal(product, expected):
        raise RuntimeError("CPU matrix multiply failed")

    print(json.dumps({
        "environment": environment_info(),
        "device": str(matrix.device),
        "seed": args.seed,
        "seed_reproducible": seed_reproducible,
        "deterministic_algorithms": torch.are_deterministic_algorithms_enabled(),
        "cpu_sample": sample.tolist(),
        "cpu_matmul": product.tolist(),
    }, indent=2))


if __name__ == "__main__":
    main()
