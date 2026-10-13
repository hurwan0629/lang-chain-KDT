# Milestones — Codex-managed checklist

Codex: update checkboxes only after running relevant tests/smoke commands. Include actual evidence in each completion note. Implement sequentially. If a phase is blocked, document why.

## M0 — Project skeleton & acceptance tests
- [x] Create Python packaging, src layout, pytest config, .gitignore, initial README.
- [x] Print CPU/GPU environment and establish deterministic seeds.
- [x] Make `python -m pytest -q` work, even before adding substantive tests.

### M0 verification — 2026-10-09 (Asia/Seoul)

- Scope: `pyproject.toml`, `.gitignore`, `src/mini_moe/` package skeleton,
  `environment.py`, `tests/test_environment.py`, and updated README. The six
  responsibility packages contain docstrings only; M1–M7 remain incomplete.
- Installation: created a project-local environment with `py -3.12 -m venv .venv`,
  installed `torch==2.5.1` from the official CPU wheel index, then ran
  `.\.venv\Scripts\python.exe -m pip install -e ".[dev]"` successfully.
  Direct dependencies: PyTorch 2.5.1+cpu, NumPy 2.1.3, pytest 8.3.5.
- Dependency check: `.\.venv\Scripts\python.exe -m pip check`
  → `No broken requirements found.` (exit 0).
- Tests: `.\.venv\Scripts\python.exe -m pytest -q`
  → **9 passed in 1.52s**, no warnings (exit 0). Covers Python/NumPy/PyTorch CPU
  RNG replay, different seeds, invalid seed values, environment JSON, CPU smoke,
  and CLI error reporting. This is `python -m pytest -q` using the local venv.
- CPU smoke: `.\.venv\Scripts\python.exe -m mini_moe.environment --seed 42`
  → exit 0; `device=cpu`, `seed_reproducible=true`,
  `deterministic_algorithms=true`, `cpu_matmul=[[1.0,3.0],[3.0,13.0]]`.
  CPU sample: `[0.8822692633, 0.9150039554, 0.3828637600, 0.9593056440]`.
- Runtime: Windows 11 (10.0.26200), CPython 3.12.10, x86-64
  `Intel64 Family 6 Model 198 Stepping 2, GenuineIntel`, 24 logical CPUs,
  24 PyTorch threads. CPU-only build reports `cuda_build=null`,
  `cuda_available=false`, `gpu_names=[]`; this does not establish physical GPU absence.
  Smoke tensor shape is `[2,2]`; training batch/sequence length are not applicable.
- Debugging: the PATH Python was MSYS without pip/PyTorch; used CPython via `py`.
  Sandbox pip setup/download and pytest cache access required approved execution.
  Initial run passed with warnings; adding NumPy resolved PyTorch's missing-array
  bridge warning and rerunning pytest with normal cache permissions removed cache
  warnings. `.gitignore` explicitly preserves source `src/mini_moe/data/` against
  the parent repository's `**/data/` rule while excluding local experiment data.
- Limits: Windows CPU path verified only; GPU, Linux/macOS, training, generation,
  and tool use not run. No external LLM APIs, pretrained weights, or external
  datasets used. First dependency installation needs network or pre-cached wheels;
  tests/smoke themselves need no network. Direct dependency versions are pinned,
  but the full transitive environment is not locked. No commit made.
- Next milestone: M1 — deterministic synthetic dataset split and train-only tokenizer.

## M1 — Dataset & tokenizer
- [x] Deterministic synthetic generator with hold-out split and a generated dataset card.
- [x] Train tokenizer on train only; serialize and reload.
- [x] Tokenizer and split tests pass; print 3 encode/decode examples.

### M1 verification — 2026-10-09 (Asia/Seoul)

- Changed: `data/synthetic.py` (authored patterns and family-stratified split),
  `tokenizer/character.py` (train-fitted Unicode character vocabulary),
  `data/prepare.py` (offline generation CLI), the two package docstrings,
  three M1 test modules, `.gitignore`, README, and this checklist. No new dependencies.
- Full suite: `.\.venv\Scripts\python.exe -m pytest -q`
  → **46 passed in 1.48s**, no warnings, exit 0 (9 M0 + 37 M1 cases).
  Checks include reproducible/disjoint splits, invalid inputs, small-family
  holdouts, unchanged global RNG, Unicode/whitespace roundtrip, fixed special IDs,
  unknown characters, save/load, invalid tokenizer schemas, artifact hashes,
  byte-identical outputs in different directories, a validation-only character
  leakage trap, and three actual saved-data encode/decode examples.
- CPU smoke: `.\.venv\Scripts\python.exe -m mini_moe.data.prepare --output-dir data/synthetic --seed 42 --validation-fraction 0.2`
  → exit 0; generated `train.jsonl`, `validation.jsonl`, `manifest.json`,
  `tokenizer.json`, and `dataset_card.md` under ignored `data/synthetic/`.
- Corpus: 256 unique sequences, 128 descriptions and 128 counting patterns.
  Train=204, validation=52; per family train=102, validation=26.
  Validation was split before fitting and never passed into tokenizer fit.
- Tokenizer: 42 IDs (4 special + 38 learned characters); PAD=0, UNK=1, BOS=2,
  EOS=3; validation unknown character count=0. Saved/reloaded vocabulary matched.
  Printed examples all had `roundtrip=true`:
  `Count from 100: 100, 101, 102, 103.` (train),
  `The red bird is near the hill.` (validation),
  `The blue bird is near the river.` (validation).
- SHA-256 from the smoke manifest:
  - train: `6a32a84ec9a059ee613aad8b8ea615ef24ff99937d4a8561f5919dfb995b6abe`
  - validation: `e16548355c577cd8f1a90d03879818c6a46eafb1d9cd2c0bf43e297d1ed06a7e`
  - tokenizer: `9c20e8e0b3351e6568f5a5796a420f600418f8cc71a299c9baecf552d089f37d`
- Dependency check: `.\.venv\Scripts\python.exe -m pip check`
  → `No broken requirements found.`, exit 0.
- Runtime: same Windows 11 / CPython 3.12.10 / Intel x86-64 24-logical-CPU
  environment as M0. Data generation/tokenization use Python on CPU; no GPU,
  model, tensor batch, or training benchmark. Token IDs have shape `[T]`, where
  `T=len(text)+2` with BOS/EOS framing; batching remains for later milestones.
- Debugging: first test run found a tuple/list mismatch between returned and
  JSON-restored special-token metadata. Manifest now uses a JSON-native list;
  the full suite passed after the fix.
  Final Git check also caught the source-data exception unignoring Python bytecode;
  cache exclusions now follow that exception, and generated data/caches stay ignored.
- Limits: shared templates/words/numerical neighborhoods mean this is an
  in-distribution holdout, not unseen-template generalization. Unknown characters
  decode visibly as `<unk>` and cannot roundtrip. No public corpus or tool-use
  examples, external LLM API, pretrained vocabulary/weights, or network calls.
  GPU/other OS not tested; no commit made.
- Next milestone: M2 — from-scratch dense causal decoder and CPU overfit diagnostic.

## M2 — Dense GPT baseline
- [ ] Decoder-only causal model with attention, FFN, training loss.
- [ ] Causal masking, shape and gradient tests pass.
- [ ] CPU one-batch overfit run proves training works.

## M3 — Sparse MoE
- [ ] Replace FFN with top-2 router, 4 experts, actual selected-expert computation.
- [ ] Auxiliary balancing loss and per-expert routing histogram.
- [ ] Test sparse/reference output parity and gradient flow.
- [ ] Compare dense vs MoE under same corpus and controlled training budget.

## M4 — Training & inference
- [ ] Runnable pretrain CLI with config, held-out loss, checkpoint and resume.
- [ ] Sampling CLI, reproducible run example, README commands.
- [ ] Report observed output and limitations; no invented benchmark results.

## M5 — Tool runner & harness
- [ ] Allowed tool schemas, AST-safe calculator, local note lookup.
- [ ] Agent loop with bounded steps, strict call validation, tool result feedback and structured trace.
- [ ] Mock-model end-to-end tests for valid, invalid, failing and repeated tools.

## M6 — Learned tool-use experiment
- [ ] Synthetic tool-use examples and strict train/test split.
- [ ] SFT pipeline for model tool-call generation.
- [ ] Held-out evaluation with denominator, schema-validity rate and true end-to-end success rate.
- [ ] Compare mock/rule-based baseline vs model-selected tool calls, labeling them honestly.

## M7 — Final reproducibility & write-up
- [ ] Verify clean environment setup and CPU smoke path.
- [ ] Save dataset provenance, config, weights location, log sample and results table.
- [ ] Write concise architecture diagram and postmortem of failures and next steps.
