@echo off
setlocal
set "EXE=%~dp0..\dist\ActivityTracker\ActivityTracker.exe"
if not exist "%EXE%" (
    echo Release EXE not found.
    echo Run build_release.bat first.
    pause
    exit /b 1
)
start "" "%EXE%"
