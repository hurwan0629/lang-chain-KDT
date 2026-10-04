# GRU Activity Tracker

A small desktop activity tracker that learns temporal context from screen frames.

```text
Screen → CLIP image embedding → GRU hidden state → activity representation
                                               ↓
                                  CLIP text label similarity
```

## Activities

`gaming`, `entertainment_video`, `educational_video`, `python_coding`,
`java_coding`, `email`, `documentation`, `reading`.

## Setup

Run from the `tech_task` directory.

```bash
pip install -r gru_activity_tracker/requirements.txt
```

## Data

### PIE2F-LongHorizon (recommended)

Keep the PIE2F index files under `data/PIE2F/indexes/`. Training can then download one session video at a time, convert it to CLIP sequences, delete the video, and continue.

```bash
python -m gru_activity_tracker.train --dataset pie2f
```

Small trial:

```bash
python -m gru_activity_tracker.train --dataset pie2f --max-prepare-sessions 10
```

Processed sequences are stored in `data/pie2f_processed/`. Re-running resumes completed sessions.

### VideoCUA

Download the VideoCUA `raw_data` zip files, then extract only the task videos and minimal timelines:

```bash
python -m gru_activity_tracker.prepare_videocua --source D:\VideoCUA\raw_data
```

For a small trial:

```bash
python -m gru_activity_tracker.prepare_videocua --source D:\VideoCUA\raw_data --limit-per-label 50
```

Output:

```text
data/videocua/
├─ videos/       # selected task videos
├─ timelines/    # timestamp + action_type only
└─ tasks.csv     # task/platform/instruction/weak label
```

The original mouse coordinates, key parameters, and GroundCUA fields are not copied.

### Local videos

You can also place labeled videos under `data/raw/<label>/`.

```text
data/raw/python_coding/sample.mp4
data/raw/gaming/sample.mp4
```

## Train

```bash
python -m gru_activity_tracker.train
```

If no processed dataset exists, training automatically runs dataset preparation first.

Model output:

```text
gru_activity_tracker/checkpoints/activity_gru.pt
```

## Test

```bash
python -m gru_activity_tracker.test
```

## Live Tracker

```bash
python -m gru_activity_tracker.run_tracker --interval 1
```

The tracker captures the full screen, updates the GRU hidden state continuously, and writes activity sessions to CSV.

## Project Structure

```text
gru_activity_tracker/
├─ prepare_pie2f.py     # PIE2F index → download/process/delete
├─ prepare_videocua.py  # VideoCUA → video + minimal timeline
├─ prepare_dataset.py   # local/videoCUA → CLIP embedding sequences
├─ train.py             # GRU training
├─ test.py              # test split evaluation
├─ run_tracker.py       # real-time tracker
├─ clip_encoder.py      # frozen CLIP encoder
├─ model.py             # GRU + projection
├─ dataset.py
├─ activity_store.py
├─ screen_capture.py
└─ data/
   └─ sources.csv
```
