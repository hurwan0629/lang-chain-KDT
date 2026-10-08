param(
    [switch]$Run
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$VenvDir = Join-Path $ProjectRoot ".venv"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
$RuntimeRequirements = Join-Path $ScriptDir "requirements-runtime.txt"
$SpecFile = Join-Path $ScriptDir "packaging\ActivityTracker.spec"
$DistRoot = Join-Path $ProjectRoot "dist"
$BuildRoot = Join-Path $ProjectRoot "build"
$ReleaseDir = Join-Path $DistRoot "ActivityTracker"
$ReleaseExe = Join-Path $ReleaseDir "ActivityTracker.exe"
$ReleaseZip = Join-Path $DistRoot "ActivityTracker-windows.zip"

if (-not (Test-Path $VenvPython)) {
    $PyLauncher = Get-Command py -ErrorAction SilentlyContinue
    if (-not $PyLauncher) {
        throw "Windows py launcher를 찾을 수 없습니다. Python 3.12를 설치해 주세요."
    }

    Write-Host ""
    Write-Host "Creating clean Python 3.12 environment: $VenvDir" -ForegroundColor Yellow
    & $PyLauncher.Source -3.12 -m venv $VenvDir
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path $VenvPython)) {
        throw "py -3.12로 .venv 생성에 실패했습니다."
    }
}

$Python = $VenvPython

# Keep the release build reproducible: this local environment must be Python 3.12.
$PreviousErrorActionPreference = $ErrorActionPreference
$ErrorActionPreference = "SilentlyContinue"
& $Python -c "import sys; raise SystemExit(0 if sys.version_info[:2] == (3, 12) else 1)" *> $null
$PythonVersionExitCode = $LASTEXITCODE
$ErrorActionPreference = $PreviousErrorActionPreference
if ($PythonVersionExitCode -ne 0) {
    throw "$VenvDir 가 Python 3.12 환경이 아닙니다. 이 배포용 .venv를 지운 뒤 다시 실행해 주세요."
}

Write-Host ""
Write-Host "=== ActivityTracker Windows Release Build ===" -ForegroundColor Cyan
Write-Host "Project root : $ProjectRoot"
Write-Host "Python       : $Python"

Push-Location $ProjectRoot
try {
    Write-Host ""
    Write-Host "[1/5] Checking runtime packages..." -ForegroundColor Yellow

    # PowerShell 5 can promote stderr from a native command to a terminating
    # NativeCommandError when ErrorActionPreference is Stop. Missing imports are
    # expected here, so probe them quietly and inspect the process exit code.
    $PreviousErrorActionPreference = $ErrorActionPreference
    $ErrorActionPreference = "SilentlyContinue"
    & $Python -c "import torch, transformers, PIL, numpy, PySide6, PyInstaller" *> $null
    $ImportExitCode = $LASTEXITCODE
    $ErrorActionPreference = $PreviousErrorActionPreference

    if ($ImportExitCode -ne 0) {
        Write-Host "Installing runtime/build packages..."
        & $Python -m pip install -r $RuntimeRequirements
        if ($LASTEXITCODE -ne 0) {
            throw "패키지 설치에 실패했습니다."
        }
    }

    Write-Host ""
    Write-Host "[2/5] Preparing checkpoint + offline CLIP assets..." -ForegroundColor Yellow
    & $Python -m gru_activity_tracker.packaging.prepare_assets
    if ($LASTEXITCODE -ne 0) {
        throw "배포 asset 준비에 실패했습니다."
    }

    Write-Host ""
    Write-Host "[3/5] Cleaning previous build..." -ForegroundColor Yellow
    if (Test-Path $BuildRoot) {
        Remove-Item $BuildRoot -Recurse -Force
    }
    if (Test-Path $ReleaseDir) {
        Remove-Item $ReleaseDir -Recurse -Force
    }
    if (Test-Path $ReleaseZip) {
        Remove-Item $ReleaseZip -Force
    }

    Write-Host ""
    Write-Host "[4/5] Building EXE with PyInstaller..." -ForegroundColor Yellow
    & $Python -m PyInstaller --noconfirm --clean $SpecFile
    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller 빌드에 실패했습니다."
    }
    if (-not (Test-Path $ReleaseExe)) {
        throw "빌드는 끝났지만 EXE를 찾을 수 없습니다: $ReleaseExe"
    }

    Write-Host ""
    Write-Host "[5/5] Creating ZIP..." -ForegroundColor Yellow
    Compress-Archive -Path (Join-Path $ReleaseDir "*") -DestinationPath $ReleaseZip -Force

    Write-Host ""
    Write-Host "Build complete." -ForegroundColor Green
    Write-Host "EXE : $ReleaseExe"
    Write-Host "ZIP : $ReleaseZip"
    Write-Host "Log : %LOCALAPPDATA%\GRUActivityTracker\gru_activity_log.csv"

    if ($Run) {
        Write-Host ""
        Write-Host "Launching ActivityTracker..." -ForegroundColor Cyan
        Start-Process -FilePath $ReleaseExe -WorkingDirectory $ReleaseDir
    }
}
finally {
    Pop-Location
}
