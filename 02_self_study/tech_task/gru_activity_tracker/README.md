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

Development run:

```bash
python -m gru_activity_tracker.run_tracker --interval 1
```

The tracker captures the full screen, updates the GRU hidden state continuously, and writes activity sessions to CSV.

## Windows GUI / EXE Release

The EXE entry point now launches the PySide6 dark dashboard under `gui/`.
Actual CLIP + GRU inference runs in a background `QThread`, so the UI remains responsive while screen activity is classified and logged.

The packaged runtime is separated under `runtime/`, while training and dataset code stays outside the EXE import path.
The release builder uses a project-local `.venv/`. If it does not exist, it is created automatically with `py -3.12 -m venv .venv`, then only `requirements-runtime.txt` is installed.
The PyInstaller spec excludes training/data-science packages that are not used by the GUI + CLIP + GRU runtime.

The build copies the trained checkpoint and saves CLIP locally so the release can run without downloading a model on the target PC.

From Windows Explorer, double-click:

```text
gru_activity_tracker/build_release.bat
```

This produces both:

```text
dist/ActivityTracker/ActivityTracker.exe
dist/ActivityTracker-windows.zip
```

To build, zip, and immediately launch the tracker, double-click:

```text
gru_activity_tracker/build_and_run.bat
```

After a release already exists, `run_release.bat` launches it without rebuilding.
Runtime logs are written to:

```text
%LOCALAPPDATA%/GRUActivityTracker/gru_activity_log.csv
```

The first release build may download `openai/clip-vit-base-patch32`. Later builds reuse `bundle_assets/clip/`.
The trained `checkpoints/activity_gru.pt` is automatically copied into the release assets during each build when needed.

## Project Structure

```text
gru_activity_tracker/
├─ gui/
│  ├─ main_window.py      # application shell / sidebar / lifecycle
│  ├─ dashboard.py        # live dashboard composition
│  ├─ tracker_worker.py   # background inference QThread
│  ├─ current_panel.py
│  ├─ timeline_widget.py
│  ├─ activity_table.py
│  ├─ donut_chart.py
│  └─ theme.py
├─ runtime/
│  ├─ predictor.py        # stateful CLIP + GRU inference
│  ├─ tracker.py          # console runtime kept for development
│  └─ paths.py            # source/PyInstaller/user-data paths
├─ packaging/
│  ├─ prepare_assets.py   # checkpoint + offline CLIP preparation
│  └─ ActivityTracker.spec
├─ app.py                 # PySide6 EXE entry point
├─ build_release.ps1      # build + zip automation
├─ build_release.bat      # double-click build
├─ build_and_run.bat      # double-click build + launch
├─ run_release.bat        # launch existing release
├─ requirements-runtime.txt
├─ prepare_pie2f.py       # training/data preparation
├─ prepare_videocua.py
├─ prepare_dataset.py
├─ train.py
├─ test.py
├─ run_tracker.py
├─ clip_encoder.py
├─ model.py
├─ dataset.py
├─ activity_store.py
└─ screen_capture.py
```
