@echo off
setlocal
cd /d "%~dp0"

set "VENV_PYTHON=.venv\Scripts\python.exe"

echo ========================================
echo Book crawler setup
echo ========================================
echo.

if exist "%VENV_PYTHON%" goto :check_packages

py -3.12 --version > nul 2>&1
if not errorlevel 1 (
  set "PYTHON_COMMAND=py -3.12"
  goto :create_venv
)

py -c "import sys; raise SystemExit(sys.version_info < (3, 10))" > nul 2>&1
if not errorlevel 1 (
  set "PYTHON_COMMAND=py"
  goto :create_venv
)

python -c "import sys; raise SystemExit(sys.version_info < (3, 10))" > nul 2>&1
if errorlevel 1 goto :python_error
set "PYTHON_COMMAND=python"

:create_venv
echo [SETUP] Creating a virtual environment with %PYTHON_COMMAND%...
%PYTHON_COMMAND% -m venv .venv
if errorlevel 1 goto :venv_error

:check_packages
"%VENV_PYTHON%" -c "import pandas, openpyxl, requests, selenium" > nul 2>&1
if not errorlevel 1 goto :collect_input

echo [SETUP] Installing required packages...
"%VENV_PYTHON%" -m pip install -r requirements.txt
if errorlevel 1 goto :install_error
goto :collect_input

:collect_input
echo.
set /p "CRAWL_KEYWORD=Search keyword: "
set /p "YES_PAGES=YES24 page count: "
set /p "KYOBO_PAGES=Kyobo page count: "
set /p "ALADIN_PAGES=Aladin page count: "

:path_mode
echo.
echo Select the image path format.
echo   1. Absolute path
echo   2. Relative path
set "PATH_MODE_SELECT="
set /p "PATH_MODE_SELECT=Select [1]: "

if not defined PATH_MODE_SELECT set "PATH_MODE_SELECT=1"

if "%PATH_MODE_SELECT%"=="1" (
  set "PATH_MODE=absolute"
) else if "%PATH_MODE_SELECT%"=="2" (
  set "PATH_MODE=relative"
) else (
  echo [ERROR] Enter 1 or 2.
  goto :path_mode
)

echo.
echo ========================================
echo Book crawler start
echo ========================================
echo.

"%VENV_PYTHON%" exec.py "%CRAWL_KEYWORD%" "%YES_PAGES%" "%KYOBO_PAGES%" "%ALADIN_PAGES%" "%PATH_MODE%"
set "EXIT_CODE=%errorlevel%"

echo.
if not "%EXIT_CODE%"=="0" (
  echo [ERROR] Execution failed. Exit code: %EXIT_CODE%
)
goto :finish

:python_error
echo [ERROR] Python 3.10 or newer was not found.
echo Install Python 3.10 or newer, then try again.
set "EXIT_CODE=1"
goto :finish

:venv_error
echo [ERROR] Failed to create the virtual environment.
set "EXIT_CODE=1"
goto :finish

:install_error
echo [ERROR] Failed to install required packages.
set "EXIT_CODE=1"
goto :finish

:finish
echo.
pause
exit /b %EXIT_CODE%
