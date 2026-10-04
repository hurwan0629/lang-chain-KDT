from __future__ import annotations

import argparse
import csv
import ctypes
from ctypes import wintypes
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import time


# Win32 API - c로 만든 함수나 자료형을 접근할 수 있음
# Dinamic Link Library - .dll -> 실행 파일은 아니고 다른 프로그램이 필요할 때 불러서 쓰는 부품 파일들
# api 구현체가 있음
# user32는 키보드, 마우스같은 
user32 = ctypes.WinDLL("user32", use_last_error=True)
# 프로세스, 메모리 파일같은 핵심 dll
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

# 권한 플래그값 -> 제한된 기본 정보만 조회한다는 뜻
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000


@dataclass(frozen=True)
class WindowState:
    pid: int
    process_name: str
    window_title: str


def get_foreground_window_state() -> WindowState | None:
    """맨 앞에 활성화된 윈도우 창을 가져오는 프로세스를 가져오는 함수"""
    # handle to a window
    # Window에서 정의한 handle 타입 (정확히는 참조값이 됨)
    hwnd = user32.GetForegroundWindow()

    if not hwnd:
        return None

    # 참조주소를 주소를 줘서 그 창의 이름을 가져오기 (w는 유니코드 버전이라는 뜻)
    # A: ancii
    # W: unicode-utf16
    title_length = user32.GetWindowTextLengthW(hwnd)
    # 파이썬 프로세스 메모리 공간에 유니코드를 넣을 버퍼를 만들기
    # 유니코드라는 이름이 들어간 이유는 일반 바이트가 아닌 wchar_t값이 들어가는 버퍼 타입을 만들기
    title_buffer = ctypes.create_unicode_buffer(title_length + 1)
    # 프로세스가져오기 -> 써줄 공간 -> 쓸 길이
    user32.GetWindowTextW(hwnd, title_buffer, len(title_buffer))
    window_title = title_buffer.value.strip()

    # windows의 DWORD(32비트의 부호없는 정수타입)
    # PID를 받을 그릇
    pid = wintypes.DWORD()
    # 결과를 2개 돌려줌 (프로세스ID를 포인터 주소에 줌)
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

    process_name = get_process_name(pid.value)

    return WindowState(
        pid=pid.value,
        process_name=process_name,
        window_title=window_title,
    )


def get_process_name(pid: int) -> str:
    """Resolve a PID to an executable name using Win32 only."""
    # 프로세스 정보에 접근 가능한 객체
    handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not handle:
        return "<unknown>"

    try:
        # 32비트 정수 하나를 채워주기 (버퍼의 크기나 문자의 개수)
        size = wintypes.DWORD(32768)
        buffer = ctypes.create_unicode_buffer(size.value)

        # 프로세스 핸들을 넘겨서 
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


def ensure_csv_header(csv_path: Path) -> None:
    """CSV 파일이 비어 있으면 foreground 세션용 헤더를 작성한다."""
    if csv_path.exists() and csv_path.stat().st_size > 0:
        return

    with csv_path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "start_time",
                "end_time",
                "duration_seconds",
                "pid",
                "process_name",
                "window_title",
            ]
        )


def append_session(
    csv_path: Path,
    state: WindowState,
    started_at: datetime,
    ended_at: datetime,
) -> None:
    """하나의 foreground 창 사용 세션을 CSV 한 행으로 저장한다."""
    duration_seconds = (ended_at - started_at).total_seconds()

    with csv_path.open("a", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                started_at.isoformat(timespec="seconds"),
                ended_at.isoformat(timespec="seconds"),
                round(duration_seconds, 3),
                state.pid,
                state.process_name,
                state.window_title,
            ]
        )


def main() -> None:
    # parser 정의하기
    parser = argparse.ArgumentParser(
        description="Track the currently focused Windows application."
    )

    # 확인하는 간격
    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Polling interval in seconds. Default: 1.0",
    )

    # foreground 창 사용 세션을 저장할 CSV 파일 경로
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("foreground_activity_log.csv"),
        help="CSV output path. Default: foreground_activity_log.csv",
    )

    args = parser.parse_args()

    # 파일 작성
    ensure_csv_header(args.output)

    # 현재 사용 중인 foreground 창과 그 세션의 시작 시간을 기억한다.
    previous_state: WindowState | None = None
    session_started_at: datetime | None = None

    print("Tracking active window sessions. Press Ctrl+C to stop.")
    print(f"CSV: {args.output.resolve()}")

    try:
        while True:
            state = get_foreground_window_state()
            now = datetime.now()

            if state is not None:
                # 첫 번째 foreground 창을 발견하면 세션 시작 시각만 기록한다.
                if previous_state is None:
                    previous_state = state
                    session_started_at = now

                    print(
                        f"[{now.strftime('%H:%M:%S')}] START | "
                        f"{state.process_name} | "
                        f"PID={state.pid} | "
                        f"{state.window_title}"
                    )

                # 프로세스나 창 제목이 달라졌다면 이전 세션이 끝난 것으로 본다.
                elif state != previous_state:
                    assert session_started_at is not None

                    append_session(
                        args.output,
                        previous_state,
                        session_started_at,
                        now,
                    )

                    duration = (now - session_started_at).total_seconds()
                    print(
                        f"[{now.strftime('%H:%M:%S')}] END   | "
                        f"{previous_state.process_name} | "
                        f"{duration:.1f}s | "
                        f"{previous_state.window_title}"
                    )
                    print(
                        f"[{now.strftime('%H:%M:%S')}] START | "
                        f"{state.process_name} | "
                        f"PID={state.pid} | "
                        f"{state.window_title}"
                    )

                    previous_state = state
                    session_started_at = now

            time.sleep(max(args.interval, 0.1))

    except KeyboardInterrupt:
        # 프로그램을 끌 때 현재 진행 중인 마지막 세션도 CSV에 저장한다.
        if previous_state is not None and session_started_at is not None:
            append_session(
                args.output,
                previous_state,
                session_started_at,
                datetime.now(),
            )

        print("\nStopped.")


if __name__ == "__main__":
    # ctypes에 윈도우가 제공하는 라이브러리를 쓸 수 있는지 확인하기
    # 윈도우용 파이썬 런타임이 아니라면 에러를 터트려주기
    if not hasattr(ctypes, "WinDLL"):
        raise SystemExit("This script only supports Windows.")

    main()
