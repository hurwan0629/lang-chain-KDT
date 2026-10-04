# X-CLIP Activity Tracker

Lightweight desktop activity tracker using **X-CLIP**.

```text
Screen Capture → Frame Queue → X-CLIP → Activity Label → CSV
```

## Features

- Full-screen capture at a fixed interval
- Sliding frame queue in memory
- Zero-shot activity classification
- Consecutive predictions merged into time ranges
- CSV output

## Model

`microsoft/xclip-base-patch32`

The model is downloaded automatically from Hugging Face on first run.

## Installation

```bash
pip install torch transformers pillow numpy
```

## Usage

Run from the `tech_task` directory:

```bash
python -m xclip_activity_tracker.activity_tracker
```

Default: 0.5s capture interval, 2s inference interval, 8-frame queue.

Custom example:

```bash
python -m xclip_activity_tracker.activity_tracker --capture-interval 0.5 --infer-interval 2 --frames 8
```

Stop with `Ctrl + C`.

## Project Structure

```text
xclip_activity_tracker/
├─ activity_tracker.py   # Main loop
├─ screen_capture.py     # Full-screen capture
├─ activity_model.py     # X-CLIP inference
├─ activity_store.py     # Session + CSV storage
└─ README.md
```

## Output

```csv
start_time,end_time,duration_seconds,predicted_label,user_label,score
2026-10-04T16:00:00,2026-10-04T16:10:00,600,coding,,0.73
```