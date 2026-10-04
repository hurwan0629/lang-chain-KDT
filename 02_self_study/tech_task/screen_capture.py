# Python의 타입 힌트를 런타임에 바로 평가하지 않고 문자열처럼 지연 평가하게 한다.
# 예: Path 같은 타입을 더 유연하게 참조할 수 있고, 최신 타입 힌트 문법 사용 시 호환성이 좋아진다.
from __future__ import annotations

# 명령행 인자(command-line argument)를 처리하기 위한 파이썬 표준 라이브러리이다.
# 이 파일에서는 --output-dir, --interval 같은 옵션을 읽는 데 사용한다.
import argparse

# 파이썬에서 C 라이브러리와 C 자료형/함수를 직접 호출할 수 있게 해주는 표준 라이브러리이다.
# Windows의 user32.dll, gdi32.dll 함수를 호출하기 위해 사용한다.
import ctypes

# Windows API에서 자주 사용하는 DWORD, LONG, WORD 같은 C 타입을 파이썬 타입으로 제공한다.
from ctypes import wintypes

# 현재 날짜와 시간을 얻기 위해 사용한다.
# 스크린샷 파일 이름에 촬영 시간을 넣는 데 사용한다.
from datetime import datetime

# 문자열 경로 대신 객체 형태로 파일/폴더 경로를 다루기 위한 표준 라이브러리이다.
from pathlib import Path

# 파이썬 값을 C 구조체/바이너리 형식으로 변환하기 위한 표준 라이브러리이다.
# BMP 파일 헤더를 직접 바이너리로 만들기 위해 사용한다.
import struct

# 일정 시간 동안 프로그램 실행을 멈추는 sleep() 함수를 사용하기 위한 모듈이다.
import time


# user32.dll을 현재 프로세스에 로드한다.
# user32.dll에는 화면, 창, 키보드, 마우스 같은 Windows 사용자 인터페이스 관련 API가 들어 있다.
# use_last_error=True를 사용하면 Windows API 호출 실패 후 GetLastError 값을 ctypes가 보존해준다.
user32 = ctypes.WinDLL("user32", use_last_error=True)

# gdi32.dll을 현재 프로세스에 로드한다.
# GDI(Graphics Device Interface)는 Windows의 전통적인 2D 그래픽 처리 API이다.
# 화면을 복사하고 비트맵을 생성하는 BitBlt, CreateCompatibleBitmap 같은 함수가 여기 들어 있다.
gdi32 = ctypes.WinDLL("gdi32", use_last_error=True)


# BitBlt 함수에서 사용하는 Raster Operation 코드이다.
# SRCCOPY는 "원본(source)의 픽셀을 목적지(destination)에 그대로 복사하라"는 뜻이다.
# 값 0x00CC0020은 Windows SDK에 정의된 상수값이다.
SRCCOPY = 0x00CC0020

# GetDIBits 함수에서 색상 테이블을 RGB 값으로 해석하라는 의미이다.
# 값 0은 Windows의 DIB_RGB_COLORS 상수와 같다.
DIB_RGB_COLORS = 0

# BMP 데이터가 압축되지 않은 일반 RGB 형식이라는 뜻이다.
# BITMAPINFOHEADER의 biCompression 필드에 사용한다.
BI_RGB = 0


# Windows API에서 사용하는 BITMAPINFOHEADER C 구조체를 파이썬에서 똑같이 정의한다.
# 이 구조체에는 비트맵의 너비, 높이, 색 깊이, 압축 방식 등의 메타데이터가 들어간다.
class BITMAPINFOHEADER(ctypes.Structure):

    # ctypes.Structure는 _fields_ 목록을 보고 실제 C 구조체 메모리 배치를 만든다.
    _fields_ = [

        # 구조체 자체의 크기(byte)를 저장한다.
        # DWORD는 Windows의 32비트 unsigned integer 타입이다.
        ("biSize", wintypes.DWORD),

        # 비트맵의 가로 픽셀 수이다.
        # LONG은 Windows의 32비트 signed integer 타입이다.
        ("biWidth", wintypes.LONG),

        # 비트맵의 세로 픽셀 수이다.
        # 양수이면 BMP 픽셀 데이터가 아래쪽 행부터 저장되는 bottom-up 형식이다.
        ("biHeight", wintypes.LONG),

        # BMP에서 사용하는 color plane 수이다.
        # Windows BMP에서는 항상 1이어야 한다.
        # WORD는 16비트 unsigned integer 타입이다.
        ("biPlanes", wintypes.WORD),

        # 픽셀 하나를 표현하는 비트 수이다.
        # 이 코드에서는 RGB 각 8비트씩 사용하므로 24비트가 된다.
        ("biBitCount", wintypes.WORD),

        # 압축 방식이다.
        # 이 코드에서는 압축하지 않으므로 BI_RGB(0)를 넣는다.
        ("biCompression", wintypes.DWORD),

        # 실제 픽셀 데이터의 전체 크기(byte)이다.
        ("biSizeImage", wintypes.DWORD),

        # 가로 방향 해상도를 pixels-per-meter 단위로 표현하는 값이다.
        # 이 코드에서는 따로 설정하지 않으므로 기본값 0으로 남는다.
        ("biXPelsPerMeter", wintypes.LONG),

        # 세로 방향 해상도를 pixels-per-meter 단위로 표현하는 값이다.
        # 이 코드에서는 따로 설정하지 않으므로 기본값 0으로 남는다.
        ("biYPelsPerMeter", wintypes.LONG),

        # 색상 테이블에서 실제 사용되는 색의 개수이다.
        # 24비트 RGB에서는 보통 0으로 둔다.
        ("biClrUsed", wintypes.DWORD),

        # 중요한 색상 개수를 나타낸다.
        # 보통 0으로 두면 모든 색상이 중요하다는 의미로 처리된다.
        ("biClrImportant", wintypes.DWORD),
    ]


# Windows의 BITMAPINFO 구조체를 파이썬에서 정의한다.
# BITMAPINFOHEADER와 색상 테이블 정보를 함께 담는 구조체이다.
class BITMAPINFO(ctypes.Structure):

    # 실제 C 구조체와 동일한 필드 구성을 정의한다.
    _fields_ = [

        # 앞에서 정의한 BITMAPINFOHEADER 구조체가 들어간다.
        ("bmiHeader", BITMAPINFOHEADER),

        # 색상 테이블 영역을 확보한다.
        # 이 코드의 24비트 RGB에서는 사실상 색상 테이블을 사용하지 않지만,
        # Windows BITMAPINFO 구조체 형태를 맞추기 위해 공간을 둔다.
        ("bmiColors", wintypes.DWORD * 3),
    ]


# 현재 Windows의 주 모니터(primary display)를 캡처해서 BMP 파일로 저장하는 함수이다.
# output_path에는 저장할 최종 파일 경로를 Path 객체로 전달한다.
def capture_primary_screen(output_path: Path) -> None:

    # 함수 역할을 설명하는 docstring이다.
    """Windows 주 모니터 화면을 캡처하여 BMP 파일로 저장한다."""

    user32.SetProcessDPIAware()
    
    # GetSystemMetrics(0)은 주 모니터의 화면 가로 크기를 픽셀 단위로 반환한다.
    # Windows SDK에서 0은 SM_CXSCREEN 상수를 의미한다.
    width = user32.GetSystemMetrics(0)

    # GetSystemMetrics(1)은 주 모니터의 화면 세로 크기를 픽셀 단위로 반환한다.
    # Windows SDK에서 1은 SM_CYSCREEN 상수를 의미한다.
    height = user32.GetSystemMetrics(1)

    print(width, height)

    # GetDC(None)은 전체 화면에 해당하는 Device Context(DC)를 얻는다.
    # DC는 Windows GDI가 화면이나 프린터 같은 출력 장치에 그릴 때 사용하는 "그래픽 작업 대상 핸들"이다.
    # None을 넘기면 특정 창이 아니라 전체 화면에 대한 DC를 가져온다.
    screen_dc = user32.GetDC(None)

    # GetDC가 실패하면 0/NULL 값이 반환되므로 이를 검사한다.
    if not screen_dc:

        # ctypes.get_last_error()로 Windows API의 마지막 오류 코드를 가져온다.
        # ctypes.WinError(...)는 오류 코드를 사람이 읽을 수 있는 Windows 예외로 바꿔서 발생시킨다.
        raise ctypes.WinError(ctypes.get_last_error())

    # 화면 DC와 호환되는 메모리 DC(memory device context)를 생성한다.
    # 화면에서 바로 파일로 저장하는 대신,
    # 먼저 화면 내용을 메모리 DC에 복사한 뒤 픽셀 데이터를 읽는 방식으로 사용한다.
    memory_dc = gdi32.CreateCompatibleDC(screen_dc)

    # 메모리 DC 생성에 실패했는지 확인한다.
    if not memory_dc:

        # 앞에서 얻은 screen_dc는 OS 자원이므로 실패 시 반드시 반환한다.
        # ReleaseDC의 첫 번째 인자 None은 GetDC(None)으로 얻은 전체 화면 DC라는 의미이다.
        user32.ReleaseDC(None, screen_dc)

        # Windows API 오류를 파이썬 예외로 변환해서 발생시킨다.
        raise ctypes.WinError(ctypes.get_last_error())

    # 화면과 호환되는 비트맵 객체를 만든다.
    # width와 height를 현재 화면 해상도로 지정하므로 화면 전체 크기의 비트맵이 만들어진다.
    bitmap = gdi32.CreateCompatibleBitmap(screen_dc, width, height)

    # 비트맵 생성에 실패했는지 확인한다.
    if not bitmap:

        # 이미 생성한 메모리 DC를 삭제한다.
        gdi32.DeleteDC(memory_dc)

        # 화면 DC도 운영체제에 반환한다.
        user32.ReleaseDC(None, screen_dc)

        # 실패 원인을 Windows 예외로 발생시킨다.
        raise ctypes.WinError(ctypes.get_last_error())

    # 생성한 bitmap을 memory_dc에 선택(select)한다.
    # GDI에서는 BitBlt의 목적지로 사용하려는 비트맵을 먼저 DC에 선택해야 한다.
    # SelectObject는 기존에 선택돼 있던 객체를 반환하므로 나중에 원상복구할 수 있다.
    old_bitmap = gdi32.SelectObject(memory_dc, bitmap)

    # 아래 작업 중 예외가 발생해도 GDI 객체와 DC를 반드시 정리하기 위해 try/finally를 사용한다.
    try:

        # BitBlt는 한 DC의 픽셀 영역을 다른 DC로 복사하는 Windows GDI 함수이다.
        # 여기서는 실제 화면(screen_dc)을 메모리(memory_dc)로 복사한다.
        if not gdi32.BitBlt(

            # 첫 번째 인자는 목적지 DC이다.
            # 즉, 화면 복사 결과를 memory_dc에 저장한다.
            memory_dc,

            # 목적지의 시작 X 좌표이다.
            # 0이면 메모리 비트맵의 가장 왼쪽부터 쓴다.
            0,

            # 목적지의 시작 Y 좌표이다.
            # 0이면 가장 위쪽부터 쓴다.
            0,

            # 복사할 영역의 가로 길이이다.
            # 화면 전체 너비를 복사한다.
            width,

            # 복사할 영역의 세로 길이이다.
            # 화면 전체 높이를 복사한다.
            height,

            # 원본 DC이다.
            # 실제 모니터 화면의 픽셀을 의미한다.
            screen_dc,

            # 원본 영역의 시작 X 좌표이다.
            0,

            # 원본 영역의 시작 Y 좌표이다.
            0,

            # 픽셀 복사 방식이다.
            # SRCCOPY는 화면 픽셀을 그대로 목적지로 복사한다.
            SRCCOPY,
        ):

            # BitBlt가 실패하면 현재 Windows 오류 코드를 예외로 발생시킨다.
            raise ctypes.WinError(ctypes.get_last_error())

        # BMP의 각 행(scanline)은 4바이트 경계에 맞춰 정렬되어야 한다.
        # width * 24는 한 행의 전체 비트 수이고,
        # +31 후 //32를 하면 32비트 단위로 올림한 뒤,
        # *4를 해서 실제 바이트 크기로 바꾼다.
        row_size = ((width * 24 + 31) // 32) * 4

        # 전체 이미지 픽셀 데이터 크기는 "한 행의 바이트 수 × 세로 행 개수"이다.
        image_size = row_size * height

        # 앞에서 정의한 BITMAPINFO C 구조체의 인스턴스를 생성한다.
        # ctypes 구조체의 숫자 필드는 기본적으로 0으로 초기화된다.
        bitmap_info = BITMAPINFO()

        # BITMAPINFOHEADER 구조체의 크기를 biSize에 기록한다.
        # GetDIBits가 구조체 버전을 판단할 때 필요한 값이다.
        bitmap_info.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)

        # 캡처할 비트맵의 가로 픽셀 수를 설정한다.
        bitmap_info.bmiHeader.biWidth = width

        # 캡처할 비트맵의 세로 픽셀 수를 설정한다.
        # 양수이므로 BMP 데이터는 bottom-up 방식으로 저장된다.
        bitmap_info.bmiHeader.biHeight = height

        # BMP의 plane 수는 규격상 반드시 1이어야 한다.
        bitmap_info.bmiHeader.biPlanes = 1

        # 한 픽셀을 24비트, 즉 B/G/R 각각 8비트로 저장한다.
        bitmap_info.bmiHeader.biBitCount = 24

        # 픽셀 데이터에 압축을 사용하지 않는다는 뜻이다.
        bitmap_info.bmiHeader.biCompression = BI_RGB

        # 픽셀 데이터 전체 크기를 구조체에 기록한다.
        bitmap_info.bmiHeader.biSizeImage = image_size

        # C 함수 GetDIBits가 픽셀 데이터를 써 넣을 수 있도록
        # image_size만큼의 연속된 바이트 버퍼를 파이썬 메모리에 생성한다.
        pixels = ctypes.create_string_buffer(image_size)

        # GetDIBits는 GDI 비트맵 객체의 픽셀 데이터를
        # 우리가 준비한 메모리 버퍼로 복사하는 Windows API 함수이다.
        scan_lines = gdi32.GetDIBits(

            # 비트맵과 호환되는 DC를 전달한다.
            memory_dc,

            # 픽셀을 읽어올 GDI bitmap 핸들을 전달한다.
            bitmap,

            # 첫 번째로 읽을 scan line 번호이다.
            # 0이면 첫 행부터 읽는다.
            0,

            # 읽어올 scan line 개수이다.
            # 전체 화면 높이만큼 읽는다.
            height,

            # 픽셀 데이터가 저장될 메모리 버퍼이다.
            pixels,

            # BITMAPINFO 구조체의 주소(pointer)를 C 함수에 전달한다.
            # ctypes.byref()는 파이썬 객체 자체가 아니라 메모리 주소를 넘긴다.
            ctypes.byref(bitmap_info),

            # bmiColors를 RGB 값으로 해석하도록 지정한다.
            DIB_RGB_COLORS,
        )

        # GetDIBits의 반환값은 실제로 복사한 scan line 수이다.
        # 요청한 height와 다르면 전체 이미지 데이터를 읽지 못한 것이다.
        if scan_lines != height:

            # 실패한 Windows API 오류를 예외로 변환한다.
            raise ctypes.WinError(ctypes.get_last_error())

        # 저장할 파일의 상위 폴더가 없으면 생성한다.
        # parents=True이면 중간 폴더까지 전부 만들고,
        # exist_ok=True이면 이미 폴더가 존재해도 오류를 내지 않는다.
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # BMP 파일의 BITMAPFILEHEADER 크기는 규격상 14바이트이다.
        file_header_size = 14

        # 우리가 정의한 BITMAPINFOHEADER C 구조체의 실제 바이트 크기를 구한다.
        # 일반적인 BITMAPINFOHEADER는 40바이트이다.
        info_header_size = ctypes.sizeof(BITMAPINFOHEADER)

        # BMP 파일 시작점에서 실제 픽셀 데이터가 시작되는 위치(byte offset)를 계산한다.
        # 파일 헤더 14바이트 + 정보 헤더 크기 이후부터 픽셀 데이터가 시작된다.
        pixel_offset = file_header_size + info_header_size

        # 최종 BMP 파일 전체 크기를 계산한다.
        # 헤더 부분과 실제 픽셀 데이터 크기를 더한다.
        file_size = pixel_offset + image_size

        # output_path에 파일을 바이너리 쓰기 모드("wb")로 연다.
        # 이미지 데이터는 텍스트가 아닌 raw byte이므로 반드시 바이너리 모드를 사용해야 한다.
        with output_path.open("wb") as file:

            # BMP의 첫 번째 헤더인 BITMAPFILEHEADER를 파일에 기록한다.
            file.write(

                # struct.pack은 여러 파이썬 값을 지정된 C 바이너리 구조로 묶어 bytes를 만든다.
                struct.pack(

                    # "<"는 little-endian 형식을 의미한다.
                    # 2s = 2바이트 문자열, I = 4바이트 unsigned int,
                    # H = 2바이트 unsigned short, H = 2바이트 unsigned short,
                    # I = 4바이트 unsigned int를 의미한다.
                    "<2sIHHI",

                    # BMP 파일은 맨 앞 두 바이트가 ASCII 문자 "BM"이어야 한다.
                    b"BM",

                    # BMP 파일 전체 크기(byte)를 기록한다.
                    file_size,

                    # BMP 규격의 예약 필드(reserved1)이다.
                    # 일반적으로 0으로 둔다.
                    0,

                    # BMP 규격의 예약 필드(reserved2)이다.
                    # 일반적으로 0으로 둔다.
                    0,

                    # 파일 시작점에서 실제 픽셀 데이터가 시작되는 위치를 기록한다.
                    pixel_offset,
                )
            )

            # BITMAPINFOHEADER 구조체의 실제 메모리 내용을 bytes로 변환해서 파일에 쓴다.
            file.write(bytes(bitmap_info.bmiHeader))

            # GetDIBits가 채운 실제 화면 픽셀 raw 데이터를 파일에 쓴다.
            # create_string_buffer의 .raw는 전체 바이트 버퍼를 반환한다.
            file.write(pixels.raw)

    # try 내부에서 성공/실패 여부와 관계없이 반드시 실행되는 정리 영역이다.
    finally:

        # memory_dc에 우리가 넣었던 bitmap 대신 원래 들어 있던 old_bitmap을 다시 선택한다.
        # GDI 객체를 삭제하기 전에 DC에서 분리하는 것이 안전한 정리 방식이다.
        gdi32.SelectObject(memory_dc, old_bitmap)

        # CreateCompatibleBitmap으로 생성한 GDI 비트맵 객체를 삭제한다.
        # 삭제하지 않으면 반복 캡처 시 GDI 리소스 누수가 발생할 수 있다.
        gdi32.DeleteObject(bitmap)

        # CreateCompatibleDC로 만든 메모리 DC를 삭제한다.
        gdi32.DeleteDC(memory_dc)

        # GetDC(None)으로 얻은 화면 DC를 Windows에 반환한다.
        user32.ReleaseDC(None, screen_dc)


# 스크린샷을 저장할 고유 파일 경로를 만드는 함수이다.
# 같은 초에 여러 번 캡처되어도 이름이 겹치지 않게 마이크로초까지 사용한다.
def make_output_path(output_dir: Path) -> Path:

    # 현재 시간을 "연월일_시분초_마이크로초" 문자열로 만든다.
    # 예: 20261004_101530_123456
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    # pathlib의 / 연산자는 경로를 이어붙이는 기능으로 오버로드되어 있다.
    # 예: Path("screenshots") / "screen_....bmp"
    return output_dir / f"screen_{timestamp}.bmp"


# 프로그램 실행의 시작점 역할을 하는 메인 함수이다.
# 명령행 옵션을 읽고, 한 번 또는 반복적으로 화면을 캡처한다.
def main() -> None:

    # ArgumentParser 객체를 생성한다.
    # 터미널에서 -h 또는 --help를 입력했을 때 description 내용도 함께 출력된다.
    parser = argparse.ArgumentParser(

        # 이 프로그램이 무엇을 하는지 설명하는 도움말 문구이다.
        description="Capture the primary Windows screen without external packages."
    )

    # --output-dir 명령행 옵션을 추가한다.
    # 사용자가 스크린샷 저장 폴더를 지정할 수 있게 한다.
    parser.add_argument(

        # 실제 터미널에서 사용할 옵션 이름이다.
        "--output-dir",

        # 문자열로 입력된 경로를 자동으로 pathlib.Path 객체로 변환한다.
        type=Path,

        # 옵션을 생략했을 때 기본 저장 폴더는 screenshots이다.
        default=Path("screenshots"),

        # python screen_capture.py --help 실행 시 표시할 도움말이다.
        help="Directory for screenshots. Default: screenshots",
    )

    # --interval 명령행 옵션을 추가한다.
    # 반복 캡처할 경우 몇 초 간격인지 지정한다.
    parser.add_argument(

        # 실제 터미널에서 사용할 옵션 이름이다.
        "--interval",

        # 0.5초 같은 소수점 값도 받을 수 있도록 float 타입으로 변환한다.
        type=float,

        # 기본값은 0.0이다.
        # 0 이하이면 한 번만 캡처하고 프로그램을 종료한다.
        default=0.0,

        # --help에서 보여줄 옵션 설명이다.
        help="Repeat capture every N seconds. 0 means capture once.",
    )

    # 실제 명령행 인자를 파싱해서 args 객체로 만든다.
    # 예: args.output_dir, args.interval 형태로 사용할 수 있다.
    args = parser.parse_args()

    # 사용자가 Ctrl+C를 눌렀을 때 KeyboardInterrupt를 잡아서 깔끔하게 종료하기 위한 try 블록이다.
    try:

        # 반복 캡처를 지원하기 위해 무한 반복문을 시작한다.
        while True:

            # 현재 시각을 사용해서 이번 스크린샷의 파일 경로를 만든다.
            output_path = make_output_path(args.output_dir)

            # 실제 화면을 캡처하고 위에서 만든 경로에 BMP 파일로 저장한다.
            capture_primary_screen(output_path)

            # 저장된 파일의 절대 경로를 터미널에 출력한다.
            # resolve()는 상대 경로를 가능한 한 절대 경로로 변환한다.
            print(f"Captured: {output_path.resolve()}")

            # interval 값이 0 이하이면 반복하지 않고 한 번만 캡처한다.
            if args.interval <= 0:

                # while 반복문을 종료한다.
                break

            # 다음 캡처까지 지정된 시간만큼 기다린다.
            # max(..., 0.1)을 사용해서 반복 간격이 최소 0.1초보다 작아지지 않게 한다.
            time.sleep(max(args.interval, 0.1))

    # 터미널에서 Ctrl+C를 누르면 파이썬이 KeyboardInterrupt 예외를 발생시킨다.
    except KeyboardInterrupt:

        # 강제 traceback을 보여주는 대신 사용자가 중단했다는 메시지만 출력한다.
        print("\nStopped.")


# 현재 파일이 다른 파일에서 import된 것이 아니라 직접 실행되었는지 확인한다.
# python screen_capture.py처럼 직접 실행한 경우에만 아래 코드가 실행된다.
if __name__ == "__main__":

    # ctypes에 WinDLL이 존재하는지 확인한다.
    # WinDLL은 Windows에서만 제공되므로 Linux/macOS에서 실행되는 것을 방지한다.
    if not hasattr(ctypes, "WinDLL"):

        # Windows가 아닌 환경에서는 명확한 오류 메시지를 출력하고 프로그램을 종료한다.
        raise SystemExit("This script only supports Windows.")

    # 위의 검사를 통과하면 실제 프로그램 로직을 실행한다.
    main()
