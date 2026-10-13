# Project specification — Mini MoE LLM + Agent Harness

## Goal
Make an educational, inspectable, fully local end-to-end AI system. Codex is the *development* agent that builds it; the project itself contains a second, minimal *runtime* agent harness that uses the newly trained tiny LLM. Those are separate harnesses.

This is a learning system, not an attempt to match GPT/Claude. No purchased inference API is required for the project's runtime; Codex access is separately required to use Codex as the coding agent.

## Environment and dependencies
- Python 3.11+, PyTorch, pytest, optionally `tokenizers` for learning a BPE tokenizer from the project's own training text.
- CPU-first default; GPU optional and detected dynamically.
- Use `pyproject.toml` or `requirements.txt`, document installation and OS-specific differences.
- No network access required for deterministic synthetic smoke tests.

## Proposed directory layout (Codex may refine)
```
mini-moe-lab/
  AGENTS.md
  SPEC.md
  TASKS.md
  README.md
  pyproject.toml
  src/mini_moe/
    data/           # synthetic corpus, optional public data import, splits
    tokenizer/      # train, load, encode, decode
    model/          # attention, decoder blocks, expert router
    training/       # pretrain, supervised tool-use finetuning, metrics
    inference/      # sampling and checkpoints
    agent/          # tool schemas, executor, harness loop, traces
  tests/
  scripts/
```

## Learning-data requirements
1. `synthetic`: create deterministic short English training sequences, with at least two different pattern families. Seed and split are fixed; generate a manifest with train/validation counts. This proves plumbing, NOT natural language intelligence.
2. `public-small` (optional): integrate a subset of TinyStories or another explicitly identified public corpus. Show source URL, exact dataset revision if available, licensing considerations, sample count, and local download/cache path. Fail gracefully offline; never quietly scrape copyrighted websites.
3. Train tokenizer on training set only; encode validation using that tokenizer. For synthetic tool-use examples, keep held-out expressions/templates from training to test some generalization.
4. Provide a small example `dataset_card.md` documenting collection/generation, limitations, and risks of data leakage.

## Model requirements
- Tiny decoder-only causal Transformer; initial defaults: d_model=128, 4 heads, 4 layers, context length=128, 4 FFN experts, top-k=2, modest expert width. Keep values configurable and report actual parameter count.
- Use a clear learned/rotary/other positional strategy; implement causal masking correctly.
- Define MoE routing for a flattened batch of tokens; combine chosen expert outputs with normalized selected gate weights; preserve [batch, seq, hidden] shape. Track per-expert token counts.
- Add a measurable auxiliary load-balancing term to training, and explain its formula. Ensure router and selected experts get gradients.
- Avoid a false sparse implementation that computes all experts for all tokens in the production path.
- Provide a dense FFN baseline with similar active-compute budget for a controlled experiment, not as a replacement for the MoE model.

## Training and inference requirements
- Next-token cross-entropy and a separate weighted router auxiliary loss, clearly logged.
- Seeded deterministic smoke run for 10–30 small steps on CPU; separate normal training configuration.
- Holdout validation; log train/validation losses and router distribution to CSV or JSONL, save hyperparameters with checkpoint, support resume.
- Sampling: greedy or temperature/top-k, including EOS/maximum tokens and an explicit device setting.
- Never assert coherent language generation from the tiny initial model unless demonstrated.

## Runtime agent harness and tool learning
- First implement an `agent` module that takes a model interface (`generate(messages) -> final or tool_call`), supports max_steps, clear stop reasons, safe allowlisted tools, schema checking and replayable traces.
- Safe tools: integer/decimal arithmetic with AST validation and a local `lookup_note` function over a bundled fixture. No raw `eval`, shell, network, file deletion, or arbitrary code execution of model output.
- Add a fake deterministic model for tests, proving harness orchestration independently from model quality.
- Then design a small synthetic supervised tool-use dataset with examples of `TOOL_CALL`/`TOOL_RESULT`/`FINAL` or another documented parseable protocol. Explain how message framing and target masking work if used.
- Fine-tune (SFT) the locally trained tiny model for outputting tool calls, and evaluate on held-out inputs. Model-selected execution must be explicitly distinguished from scripted or regex-based routing. Invalid calls count as failures.
- Save evaluation cases and a machine-readable summary (tool-choice accuracy, schema validity, end-to-end completion rate, denominator, and examples of failed attempts).
- A learned tool-call demo may not succeed with a tiny model. Report results honestly; don't paper over failures using hidden routing heuristics.

## Tests and acceptance criteria
- Model forward pass returns logits [B,T,V]; gradients flow; causal test checks future-token changes do not alter earlier logits.
- Expert router has valid top-k indices/weights; selected-expert implementation matches a slow reference within tolerance; stats add up to B*T*k.
- Synthetic data split is reproducible and train/validation are disjoint.
- Tokenizer encode/decode round-trip for representative samples and special-token conventions are tested.
- CPU one-batch overfit diagnostic improves loss; checkpoint save + reload gives matching output in eval mode.
- Harness fake-model test covers single call, invalid arguments, tool failure, max steps and final answer, with a trace.
- Document exact installation, data generation, training, evaluation and demo commands in README.

## Design decisions to record
For each milestone, append a short note in README or a `docs/decisions.md`: decision, alternatives, why chosen, what was measured. Prefer clarity over cleverness. All benchmarks must state hardware, batch size, sequence length, and whether run on CPU or GPU.
