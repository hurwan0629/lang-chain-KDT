from __future__ import annotations

import argparse
from collections import deque
from datetime import datetime
from pathlib import Path
import time

from PIL import Image

from .activity_model import ActivityModel
from .activity_store import ActivityStore
from .screen_capture import capture_full_screen


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="최근 foreground 화면 sequence를 X-CLIP으로 분류합니다."
    )
    parser.add_argument(
        "--capture-interval",
        type=float,
        default=0.5,
        help="화면 캡처 간격(초). Default: 0.5",
    )
    parser.add_argument(
        "--infer-interval",
        type=float,
        default=2.0,
        help="X-CLIP 추론 간격(초). Default: 2.0",
    )
    parser.add_argument(
        "--frames",
        type=int,
        default=8,
        help="한 번 추론할 때 사용할 최근 frame 수. Default: 8",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("activity_log.csv"),
        help="결과 CSV 경로. Default: activity_log.csv",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.capture_interval <= 0:
        raise SystemExit("--capture-interval은 0보다 커야 합니다.")
    if args.infer_interval <= 0:
        raise SystemExit("--infer-interval은 0보다 커야 합니다.")
    if args.frames <= 0:
        raise SystemExit("--frames는 1 이상이어야 합니다.")

    model = ActivityModel()
    store = ActivityStore(args.output)

    frames: deque[Image.Image] = deque(maxlen=args.frames)
    last_inference_at = 0.0

    print("Activity tracker started. Press Ctrl+C to stop.")
    print(f"Output: {args.output.resolve()}")

    try:
        while True:
            loop_started_at = time.monotonic()

            frame = capture_full_screen()
            frames.append(frame)

            should_infer = (
                len(frames) == args.frames
                and loop_started_at - last_inference_at
                >= args.infer_interval
            )

            if should_infer:
                prediction = model.predict(list(frames))
                now = datetime.now()

                store.update(
                    prediction.label,
                    prediction.score,
                    now,
                )

                print(
                    f"[{now.strftime('%H:%M:%S')}] "
                    f"{prediction.label} "
                    f"({prediction.score:.3f})"
                )

                last_inference_at = loop_started_at

            elapsed = time.monotonic() - loop_started_at
            time.sleep(max(args.capture_interval - elapsed, 0.01))

    except KeyboardInterrupt:
        print("\nStopped.")

    finally:
        store.close()


if __name__ == "__main__":
    main()
