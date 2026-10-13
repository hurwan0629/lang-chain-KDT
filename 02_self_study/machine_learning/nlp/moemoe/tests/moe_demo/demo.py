"""A tiny, dependency-free token-level MoE with manually chosen weights."""

import argparse
import math


EXPERT_NAMES = ("boost_x", "boost_y", "flip_sign")
EXPERT_GAINS = ((2.0, 1.0), (1.0, 2.0), (-1.0, -1.0))
DEFAULT_INPUTS = ((2.0, 0.0), (0.0, 2.0), (-2.0, -2.0), (1.0, 1.0))


def router_probabilities(token):
    """Linear router W*x, then softmax; x is a toy token embedding."""
    x, y = token
    logits = (x, y, -x - y)
    maximum = max(logits)
    scores = [math.exp(logit - maximum) for logit in logits]
    total = sum(scores)
    return tuple(score / total for score in scores)


def expert_forward(expert_id, token):
    """Two linear layers with ReLU between them: 2 -> 4 -> 2.

    W1 separates positive/negative parts. Each expert's W2 has different
    gains, making its behavior easy to see without training.
    """
    x, y = token
    hidden = (max(x, 0.0), max(-x, 0.0), max(y, 0.0), max(-y, 0.0))
    gain_x, gain_y = EXPERT_GAINS[expert_id]
    return (gain_x * (hidden[0] - hidden[1]),
            gain_y * (hidden[2] - hidden[3]))


def moe_forward(token, top_k=1):
    """Route one token and run only selected experts.

    Selected probabilities are renormalized to sum to one. This is a
    teaching choice; real implementations may retain the original gate.
    """
    if not 1 <= top_k <= len(EXPERT_NAMES):
        raise ValueError("top_k must be 1, 2, or 3")
    if len(token) != 2 or not all(math.isfinite(value) for value in token):
        raise ValueError("input must contain two finite numbers")

    probabilities = router_probabilities(token)
    # Equal scores keep expert ID order so the demo is reproducible.
    selected = sorted(range(len(EXPERT_NAMES)),
                      key=lambda index: probabilities[index], reverse=True)[:top_k]
    
    selected_total = sum(probabilities[index] for index in selected)
    contributions = []
    result = [0.0, 0.0]
    for expert_id in selected:
        weight = probabilities[expert_id] / selected_total
        output = expert_forward(expert_id, token)
        for dimension in range(2):
            result[dimension] += weight * output[dimension]
        contributions.append((expert_id, weight, output))
    return tuple(result), probabilities, contributions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--top-k", type=int, choices=(1, 2, 3), default=1)
    parser.add_argument("--input", type=float, nargs=2, action="append",
                        metavar=("X", "Y"), help="Toy embedding; repeat for multiple tokens")
    args = parser.parse_args()
    tokens = args.input if args.input is not None else DEFAULT_INPUTS
    if any(not all(math.isfinite(value) for value in token) for token in tokens):
        parser.error("--input requires finite numbers")

    counts = [0] * len(EXPERT_NAMES)
    print(f"MoE demo | {len(EXPERT_NAMES)} stored experts | top-k={args.top_k}")
    print("Manual weights, toy embeddings, no training or attention.\n")
    for token in tokens:
        result, probabilities, contributions = moe_forward(token, args.top_k)
        print(f"Token embedding: {tuple(token)}")
        print("  Router: " + ", ".join(
            f"{name}={probability:.3f}"
            for name, probability in zip(EXPERT_NAMES, probabilities)))
        for expert_id, weight, output in contributions:
            counts[expert_id] += 1
            print(f"  RUN {EXPERT_NAMES[expert_id]}: weight={weight:.3f}, output={output}")
        print(f"  MoE output: ({result[0]:.3f}, {result[1]:.3f})")
        all_result, _, _ = moe_forward(token, top_k=3)
        print(f"  All-expert mixture: ({all_result[0]:.3f}, {all_result[1]:.3f})\n")

    print("Selected-path expert calls: " + ", ".join(
        f"{name}={count}" for name, count in zip(EXPERT_NAMES, counts)))
    print(f"Selected path: {sum(counts)} calls; all-expert path: {len(tokens) * 3} calls.")
    print("The comparison above also runs all experts to show their combined output.")
    print("Fewer expert calls do not guarantee lower latency or lower model memory.")


if __name__ == "__main__":
    main()
