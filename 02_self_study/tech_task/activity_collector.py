from __future__ import annotations

import argparse
import csv
import ctypes
from ctypes import wintypes
from dataclasses import dataclass
from datetime import datetime
import importlib
from pathlib import Path
import time
from typing import Any


# ---------------------------------------------------------------------------
# Win32 API
# ---------------------------------------------------------------------------

user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

# 64비트 Windows에서 HWND/HANDLE 값이 잘리지 않도록 반환형을 명시한다.
user32.GetForegroundWindow.restype = wintypes.HWND
user32.GetWindowTextLengthW.argtypes = [wintypes.HWND]
user32.GetWindowTextLengthW.restype = ctypes.c_int
user32.GetWindowTextW.argtypes = [
    wintypes.HWND,
    wintypes.LPWSTR,
    ctypes.c_int,
]
user32.GetWindowTextW.restype = ctypes.c_int
user32.GetWindowThreadProcessId.argtypes = [
    wintypes.HWND,
    ctypes.POINTER(wintypes.DWORD),
]
user32.GetWindowThreadProcessId.restype = wintypes.DWORD
user32.IsWindowVisible.argtypes = [wintypes.HWND]
user32.IsWindowVisible.restype = wintypes.BOOL
user32.IsIconic.argtypes = [wintypes.HWND]
user32.IsIconic.restype = wintypes.BOOL
user32.GetWindowRect.argtypes = [
    wintypes.HWND,
    ctypes.POINTER(wintypes.RECT),
]
user32.GetWindowRect.restype = wintypes.BOOL

kernel32.OpenProcess.argtypes = [
    wintypes.DWORD,
    wintypes.BOOL,
    wintypes.DWORD,
]
kernel32.OpenProcess.restype = wintypes.HANDLE
kernel32.QueryFullProcessImageNameW.argtypes = [
    wintypes.HANDLE,
    wintypes.DWORD,
    wintypes.LPWSTR,
    ctypes.POINTER(wintypes.DWORD),
]
kernel32.QueryFullProcessImageNameW.restype = wintypes.BOOL
kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
kernel32.CloseHandle.restype = wintypes.BOOL

EnumWindowsProc = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,
    wintypes.LPARAM,
)
user32.EnumWindows.argtypes = [EnumWindowsProc, wintypes.LPARAM]
user32.EnumWindows.restype = wintypes.BOOL


# ---------------------------------------------------------------------------
# 공통 데이터 구조
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class WindowInfo:
    hwnd: int
    pid: int
    process_name: str
    window_title: str
    x: int
    y: int
    width: int
    height: int


# ---------------------------------------------------------------------------
# Win32 창 정보 수집
# ---------------------------------------------------------------------------

def get_process_name(pid: int) -> str:
    """PID를 실행 파일 이름(ex: Code.exe)으로 변환한다."""
    handle = kernel32.OpenProcess(
        PROCESS_QUERY_LIMITED_INFORMATION,
        False,
        pid,
    )

    if not handle:
        return "<unknown>"

    try:
        size = wintypes.DWORD(32768)
        buffer = ctypes.create_unicode_buffer(size.value)

        ok = kernel32.QueryFullProcessImageNameW(
            handle,
            0,
            buffer,
            ctypes.byref(size),
        )

        if not ok:
            return "<unknown>"

        return Path(buffer.value).name

    finally:
        kernel32.CloseHandle(handle)


def get_window_title(hwnd: int) -> str:
    """HWND에서 현재 창 제목을 읽는다."""
    title_length = user32.GetWindowTextLengthW(hwnd)

    if title_length <= 0:
        return ""

    buffer = ctypes.create_unicode_buffer(title_length + 1)
    user32.GetWindowTextW(hwnd, buffer, len(buffer))
    return buffer.value.strip()


def get_window_info(hwnd: int) -> WindowInfo | None:
    """HWND 하나를 모델이 쓰기 쉬운 WindowInfo로 변환한다."""
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

    if pid.value == 0:
        return None

    rect = wintypes.RECT()

    if not user32.GetWindowRect(hwnd, ctypes.byref(rect)):
        return None

    return WindowInfo(
        hwnd=int(hwnd),
        pid=pid.value,
        process_name=get_process_name(pid.value),
        window_title=get_window_title(hwnd),
        x=rect.left,
        y=rect.top,
        width=max(0, rect.right - rect.left),
        height=max(0, rect.bottom - rect.top),
    )


def get_foreground_window() -> WindowInfo | None:
    """현재 키보드/마우스 입력 포커스를 가진 foreground 창 하나를 가져온다."""
    hwnd = user32.GetForegroundWindow()

    if not hwnd:
        return None

    return get_window_info(hwnd)


def get_visible_windows() -> list[WindowInfo]:
    """
    Windows가 'visible'로 표시하고 있고 최소화되지 않은 최상위 창을 가져온다.

    주의:
    여기서 visible은 실제 픽셀이 다른 창에 가려지지 않았다는 뜻은 아니다.
    완전히 뒤에 가려진 창도 IsWindowVisible=True일 수 있다.
    """
    windows: list[WindowInfo] = []

    @EnumWindowsProc
    def callback(hwnd: int, _lparam: int) -> bool:
        if not user32.IsWindowVisible(hwnd):
            return True

        if user32.IsIconic(hwnd):
            return True

        info = get_window_info(hwnd)

        if info is None:
            return True

        # 제목이 없는 시스템용 보조 창은 행동 추론에 노이즈가 많아서 제외한다.
        if not info.window_title:
            return True

        # 크기가 0인 창도 실제 사용자 화면 정보가 거의 없어서 제외한다.
        if info.width <= 0 or info.height <= 0:
            return True

        windows.append(info)
        return True

    user32.EnumWindows(callback, 0)
    return windows


# ---------------------------------------------------------------------------
# CSV
# ---------------------------------------------------------------------------

def ensure_csv(
    path: Path,
    header: list[str],
) -> None:
    """CSV가 없거나 비어 있을 때만 헤더를 작성한다."""
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists() and path.stat().st_size > 0:
        return

    with path.open(
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        csv.writer(file).writerow(header)


def append_csv(
    path: Path,
    rows: list[list[Any]],
) -> None:
    """여러 행을 한 번에 CSV 뒤에 추가한다."""
    if not rows:
        return

    with path.open(
        "a",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        csv.writer(file).writerows(rows)


# ---------------------------------------------------------------------------
# Foreground 수집
# ---------------------------------------------------------------------------

class ForegroundCollector:
    def __init__(self, output_path: Path) -> None:
        self.output_path = output_path
        self.previous_key: tuple[int, str] | None = None
        self.state_started_at: float | None = None

        ensure_csv(
            output_path,
            [
                "sample_id",
                "timestamp",
                "active_duration_seconds",
                "hwnd",
                "pid",
                "process_name",
                "window_title",
                "x",
                "y",
                "width",
                "height",
            ],
        )

    def collect(
        self,
        sample_id: int,
        timestamp: str,
        monotonic_now: float,
    ) -> None:
        window = get_foreground_window()

        if window is None:
            return

        current_key = (
            window.pid,
            window.window_title,
        )

        # foreground 프로세스 또는 창 제목이 바뀌면 새로운 작업 상태로 본다.
        if current_key != self.previous_key:
            self.previous_key = current_key
            self.state_started_at = monotonic_now

        assert self.state_started_at is not None

        active_duration = monotonic_now - self.state_started_at

        append_csv(
            self.output_path,
            [[
                sample_id,
                timestamp,
                round(active_duration, 3),
                window.hwnd,
                window.pid,
                window.process_name,
                window.window_title,
                window.x,
                window.y,
                window.width,
                window.height,
            ]],
        )


# ---------------------------------------------------------------------------
# 화면에 표시 가능한 창 목록 수집
# ---------------------------------------------------------------------------

class VisibleWindowCollector:
    def __init__(self, output_path: Path) -> None:
        self.output_path = output_path

        ensure_csv(
            output_path,
            [
                "sample_id",
                "timestamp",
                "z_order_index",
                "is_foreground",
                "hwnd",
                "pid",
                "process_name",
                "window_title",
                "x",
                "y",
                "width",
                "height",
            ],
        )

    def collect(
        self,
        sample_id: int,
        timestamp: str,
    ) -> None:
        windows = get_visible_windows()
        foreground = user32.GetForegroundWindow()

        rows: list[list[Any]] = []

        for index, window in enumerate(windows):
            rows.append([
                sample_id,
                timestamp,
                index,
                int(window.hwnd == int(foreground or 0)),
                window.hwnd,
                window.pid,
                window.process_name,
                window.window_title,
                window.x,
                window.y,
                window.width,
                window.height,
            ])

        append_csv(self.output_path, rows)


# ---------------------------------------------------------------------------
# CPU / RAM 프로세스 수집
# ---------------------------------------------------------------------------

class ProcessUsageCollector:
    def __init__(
        self,
        output_path: Path,
        top_n: int,
    ) -> None:
        self.output_path = output_path
        self.top_n = top_n
        self.psutil = self._load_psutil()
        self.process_cache: dict[int, Any] = {}

        ensure_csv(
            output_path,
            [
                "sample_id",
                "timestamp",
                "rank",
                "pid",
                "process_name",
                "cpu_percent",
                "memory_mb",
                "memory_percent",
                "system_cpu_percent",
                "system_memory_percent",
            ],
        )

        # cpu_percent(None)은 이전 호출 시점과의 차이를 계산한다.
        # 따라서 시작할 때 기준점을 한 번 만들어 둔다.
        self.psutil.cpu_percent(None)
        self._prime_process_cpu_counters()

    @staticmethod
    def _load_psutil() -> Any:
        try:
            return importlib.import_module("psutil")
        except ModuleNotFoundError as exc:
            raise SystemExit(
                "CPU/RAM 수집에는 psutil이 필요합니다. "
                "먼저 'pip install psutil'을 실행하세요."
            ) from exc

    def _prime_process_cpu_counters(self) -> None:
        for pid in self.psutil.pids():
            try:
                process = self.psutil.Process(pid)
                process.cpu_percent(None)
                self.process_cache[pid] = process
            except (
                self.psutil.NoSuchProcess,
                self.psutil.AccessDenied,
                self.psutil.ZombieProcess,
            ):
                continue

    def collect(
        self,
        sample_id: int,
        timestamp: str,
    ) -> None:
        current_pids = set(self.psutil.pids())

        # 이미 종료된 프로세스는 캐시에서 제거한다.
        for pid in list(self.process_cache):
            if pid not in current_pids:
                self.process_cache.pop(pid, None)

        process_rows: list[dict[str, Any]] = []

        for pid in current_pids:
            try:
                process = self.process_cache.get(pid)

                if process is None:
                    process = self.psutil.Process(pid)
                    process.cpu_percent(None)
                    self.process_cache[pid] = process

                cpu_percent = process.cpu_percent(None)
                memory_info = process.memory_info()
                memory_percent = process.memory_percent()

                process_rows.append(
                    {
                        "pid": pid,
                        "name": process.name(),
                        "cpu_percent": cpu_percent,
                        "memory_mb": memory_info.rss / (1024 * 1024),
                        "memory_percent": memory_percent,
                    }
                )

            except (
                self.psutil.NoSuchProcess,
                self.psutil.AccessDenied,
                self.psutil.ZombieProcess,
            ):
                continue

        # CPU 사용량을 우선으로 정렬하고, 같으면 RAM 사용량을 보조 기준으로 쓴다.
        process_rows.sort(
            key=lambda item: (
                item["cpu_percent"],
                item["memory_mb"],
            ),
            reverse=True,
        )

        # top_n=0이면 전체 프로세스를 기록한다.
        if self.top_n > 0:
            process_rows = process_rows[: self.top_n]

        system_cpu = self.psutil.cpu_percent(None)
        system_memory = self.psutil.virtual_memory().percent

        rows: list[list[Any]] = []

        for rank, item in enumerate(process_rows, start=1):
            rows.append([
                sample_id,
                timestamp,
                rank,
                item["pid"],
                item["name"],
                round(item["cpu_percent"], 3),
                round(item["memory_mb"], 3),
                round(item["memory_percent"], 3),
                round(system_cpu, 3),
                round(system_memory, 3),
            ])

        append_csv(self.output_path, rows)


# ---------------------------------------------------------------------------
# 메인 루프
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Collect Windows user-activity features into separate CSV files."
        )
    )

    parser.add_argument(
        "--foreground",
        action="store_true",
        help="Collect the current foreground window.",
    )
    parser.add_argument(
        "--visible-windows",
        action="store_true",
        help="Collect visible, non-minimized top-level windows.",
    )
    parser.add_argument(
        "--system-usage",
        action="store_true",
        help="Collect per-process CPU/RAM usage.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Enable foreground, visible-windows and system-usage collectors.",
    )

    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Base foreground sampling interval in seconds. Default: 1.0",
    )
    parser.add_argument(
        "--visible-interval",
        type=float,
        default=2.0,
        help="Visible-window sampling interval in seconds. Default: 2.0",
    )
    parser.add_argument(
        "--system-interval",
        type=float,
        default=5.0,
        help="CPU/RAM sampling interval in seconds. Default: 5.0",
    )
    parser.add_argument(
        "--top-processes",
        type=int,
        default=5,
        help="Number of processes to keep by CPU usage. 0 means all. Default: 5",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("activity_data"),
        help="CSV output directory. Default: activity_data",
    )

    args = parser.parse_args()

    if args.all:
        args.foreground = True
        args.visible_windows = True
        args.system_usage = True

    if not (
        args.foreground
        or args.visible_windows
        or args.system_usage
    ):
        parser.error(
            "수집할 데이터를 하나 이상 선택하세요: "
            "--foreground / --visible-windows / --system-usage / --all"
        )

    if args.interval <= 0:
        parser.error("--interval은 0보다 커야 합니다.")

    if args.visible_interval <= 0:
        parser.error("--visible-interval은 0보다 커야 합니다.")

    if args.system_interval <= 0:
        parser.error("--system-interval은 0보다 커야 합니다.")

    if args.top_processes < 0:
        parser.error("--top-processes는 0 이상이어야 합니다.")

    foreground_collector = (
        ForegroundCollector(
            args.output_dir / "foreground.csv"
        )
        if args.foreground
        else None
    )

    visible_collector = (
        VisibleWindowCollector(
            args.output_dir / "visible_windows.csv"
        )
        if args.visible_windows
        else None
    )

    process_collector = (
        ProcessUsageCollector(
            args.output_dir / "process_usage.csv",
            args.top_processes,
        )
        if args.system_usage
        else None
    )

    sample_id = 0

    now_monotonic = time.monotonic()

    # visible/system 데이터는 각각 자신의 주기로 동작한다.
    # 시작하자마자 한 번 수집할 수 있도록 이전 시점을 interval만큼 뒤로 잡는다.
    last_visible_at = now_monotonic - args.visible_interval

    # process cpu_percent는 초기 기준점이 필요하므로
    # 첫 system sample은 system_interval 후부터 기록한다.
    last_system_at = now_monotonic

    print("Activity collector started. Press Ctrl+C to stop.")
    print(f"Output: {args.output_dir.resolve()}")

    try:
        while True:
            loop_started_at = time.monotonic()
            sample_id += 1

            timestamp = datetime.now().isoformat(
                timespec="milliseconds"
            )

            if foreground_collector is not None:
                foreground_collector.collect(
                    sample_id,
                    timestamp,
                    loop_started_at,
                )

            if (
                visible_collector is not None
                and loop_started_at - last_visible_at
                >= args.visible_interval
            ):
                visible_collector.collect(
                    sample_id,
                    timestamp,
                )
                last_visible_at = loop_started_at

            if (
                process_collector is not None
                and loop_started_at - last_system_at
                >= args.system_interval
            ):
                process_collector.collect(
                    sample_id,
                    timestamp,
                )
                last_system_at = loop_started_at

            elapsed = time.monotonic() - loop_started_at
            sleep_seconds = max(
                args.interval - elapsed,
                0.01,
            )
            time.sleep(sleep_seconds)

    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    if not hasattr(ctypes, "WinDLL"):
        raise SystemExit(
            "This script only supports Windows."
        )

    main()
