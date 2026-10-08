# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules, copy_metadata


project_root = Path(SPECPATH).parents[1]
package_dir = project_root / "gru_activity_tracker"
assets_dir = package_dir / "bundle_assets"

checkpoint = assets_dir / "activity_gru.pt"
clip_dir = assets_dir / "clip"

if not checkpoint.exists():
    raise FileNotFoundError(f"Missing bundled checkpoint: {checkpoint}")
if not clip_dir.exists():
    raise FileNotFoundError(f"Missing bundled CLIP directory: {clip_dir}")


datas = [
    (str(checkpoint), "bundle_assets"),
    (str(clip_dir), "bundle_assets/clip"),
]

for distribution in ("transformers", "huggingface-hub", "tokenizers", "safetensors"):
    try:
        datas += copy_metadata(distribution)
    except Exception:
        pass

hiddenimports = collect_submodules("transformers.models.clip")
hiddenimports += [
    "PySide6.QtCore",
    "PySide6.QtGui",
    "PySide6.QtWidgets",
]


a = Analysis(
    [str(package_dir / "app.py")],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Training/data preparation only.
        "cv2",
        "pyarrow",
        "yt_dlp",
        "pandas",

        # Optional ML/scientific stacks pulled in by torch/transformers hooks
        # but not used by the CLIP + GRU runtime.
        "matplotlib",
        "scipy",
        "IPython",
        "ipykernel",
        "jupyter",
        "notebook",
        "datasets",
        "timm",
        "sklearn",
        "torchvision",
        "torchaudio",
        "tensorflow",
        "keras",
        "jax",
        "jaxlib",
        "flax",
        "librosa",
        "soundfile",
        "nbformat",
        "jedi",
        "zmq",
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="ActivityTracker",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="ActivityTracker",
)
