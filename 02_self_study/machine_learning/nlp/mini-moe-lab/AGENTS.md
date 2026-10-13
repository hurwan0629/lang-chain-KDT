# Codex Instructions — From-Scratch Mini MoE LLM + Agent Harness

## Mission
Build an educational, fully local Python project that goes from dataset to tokenizer, causal MoE Transformer, training, text generation, tool-use training, and a minimal agent harness. Implement the project in this repository; this file is guidance, not application source code.

## Ground rules
- Work in milestones defined in TASKS.md; consult SPEC.md for acceptance criteria. On a new task, inspect existing code and the current milestone first.
- Use Python 3.11+, PyTorch, pytest, and a small tokenizer library if useful. Implement the Transformer, MoE router, and agent loop ourselves; do not load pretrained model weights or import a ready-made Transformer/agent framework.
- Make the CPU smoke path work before optimizing for a GPU. Avoid any required cloud/API key. External datasets must be optional; record their source and applicable license.
- Prefer simple, legible modules with type hints and docstrings. Explain important tensor shapes, routing decisions, losses, and data transformations in code comments.
- Do not claim that a toy model has robust general intelligence or that a scripted tool action is an LLM-selected tool call.
- Never run untrusted model-generated shell commands. Limit the demo harness to allowlisted, validated, side-effect-free tools with a bounded step count.
- Keep secrets, checkpoints, and downloaded datasets out of git. Do not commit changes unless asked.

## How to work
1. Read SPEC.md and TASKS.md. Select the earliest incomplete milestone; summarize what you will build and how you will verify it.
2. Make a small, reviewable change and write or update relevant tests.
3. Run the tests and the milestone's CPU smoke command; fix failures. If execution is impossible, distinguish tests run from tests not run.
4. Update TASKS.md with actual completion status and measured evidence. Never mark a task done without checking the acceptance criteria.
5. Report: changed files, commands run, outcomes, known limitations, and the next milestone.

## Architecture rules
- Separate `data/`, `model/`, `training/`, `inference/`, `agent/`, and `tests/` by responsibility; create packages as needed.
- Model: causal decoder-only Transformer, token embeddings, positional information, residual blocks, normalization, attention, MoE FFN, output projection. Start with 4 experts and top-2 routing.
- Routing: expose per-expert token counts and an auxiliary balancing metric. In the sparse implementation compute only selected experts per token; a dense reference may be used only for tests.
- Data: deterministic synthetic smoke data first; optional small public corpus later. Split examples into train/validation BEFORE fitting the tokenizer. Never put validation texts in training samples.
- Training: fixed seed, gradient clipping, held-out validation loss, checkpoint save/load, and minimal metrics logs. CPU smoke training must be finite and fast.
- Agent: distinguish (a) scripted baseline, (b) model-emitted structured tool call, and (c) verified execution. Do not label baseline behavior as learned tool use.
- Tools: use JSON-like structured call schema, validate the arguments, reject unsupported calls, cap loops, record a trace, and return tool results to the model's context.

## Definition of done
The project is done only when: a fresh local install runs tests; synthetic data can be generated; training loss/validation loss are recorded; the checkpoint reloads; token sampling works; router statistics can be inspected; a safe scripted harness loop works; and there is at least one evaluated attempt at model-driven tool calling with an explicitly reported success rate (including failures). Any unmet item must be marked incomplete in TASKS.md.
