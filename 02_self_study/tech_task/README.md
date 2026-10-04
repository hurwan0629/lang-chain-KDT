# PC Activity Tracking

Windows PC의 사용 행동을 수집하고, 스크린샷 묶음으로 현재 작업 상태를 추론하는 실험 프로젝트입니다.

## active_window_tracker.py
- 입력: `--interval`, `--output`
- 수집: foreground 창의 PID, 프로세스명, window title
- 출력: foreground 사용 세션 CSV
- 구조: 창이 바뀌면 이전 세션의 시작/종료/지속 시간을 기록
- 특이사항: Win32 API 직접 사용, Windows 전용

## activity_collector.py
- 입력: `--foreground`, `--visible-windows`, `--system-usage`, `--all`
- 수집: foreground 창, visible 창, 프로세스별 CPU/RAM
- 출력: `foreground.csv`, `visible_windows.csv`, `process_usage.csv`
- 구조: 각 수집기를 서로 다른 주기로 선택 실행
- 특이사항: CPU/RAM 수집은 `psutil` 필요, Windows 전용

## screen_capture.py
- 입력: `--output-dir`, `--interval`
- 처리: Win32 GDI로 주 화면 캡처
- 출력: `screenshots/screen_*.bmp`
- 구조: 1회 캡처 또는 지정 간격 반복 캡처
- 특이사항: 외부 캡처 라이브러리 없이 BMP 직접 저장, Windows 전용

## clip_activity_classifier.py
- 입력: `--folder`, `--offset`, `--limit`
- 처리: 여러 이미지 → CLIP embedding → 정규화 → 평균 → 재정규화
- 출력: 행동 label별 cosine similarity와 최종 예측
- 구조: 평균 image embedding과 text embeddings를 내적해 가장 가까운 행동 선택
- 특이사항: `openai/clip-vit-base-patch32` 사용, 이후 이미지 목록 직접 입력 구조로 확장 가능
