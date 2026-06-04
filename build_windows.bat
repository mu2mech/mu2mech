@echo off
REM Build script for mu2mech — Windows x86_64
REM Produces a self-contained folder at dist\mu2mech\
REM
REM Prerequisites (install before running this script):
REM   1. Python 3.9 or 3.10  (https://python.org) — PySide2 does NOT support 3.11+
REM   2. MinGW-w64 GCC       (https://winlibs.com or via MSYS2)
REM   3. FFTW3 for Windows   (https://fftw.org/install/windows.html)
REM       - Download fftw-3.3.x-dll64.zip, extract to C:\fftw3
REM       - Run: lib /machine:x64 /def:libfftw3-3.def  (creates libfftw3-3.lib)
REM       - Copy libfftw3-3.dll into Sources\
REM   4. Add MinGW bin directory to PATH (e.g. C:\mingw64\bin)

setlocal enabledelayedexpansion

cd /d "%~dp0"

REM ── Python version check ──────────────────────────────────────────────────
for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo Python version: %PYVER%
for /f "tokens=1,2 delims=." %%a in ("%PYVER%") do (
    set PY_MAJ=%%a
    set PY_MIN=%%b
)
if %PY_MAJ% NEQ 3 (
    echo ERROR: Python 3.9 or 3.10 required. Found %PYVER%.
    exit /b 1
)
if %PY_MIN% GTR 10 (
    echo ERROR: PySide2 requires Python 3.8-3.10. Found %PYVER%.
    echo Install Python 3.10 from https://python.org
    exit /b 1
)

REM ── Compile C sources ─────────────────────────────────────────────────────
echo.
echo Compiling C sources...
cd Sources
if not exist "C:\fftw3\libfftw3-3.dll" (
    echo WARNING: C:\fftw3\libfftw3-3.dll not found.
    echo Download FFTW3 Windows DLLs from https://fftw.org/install/windows.html
    echo and place them in C:\fftw3\
    pause
)
mingw32-make -f Makefile.win all
if errorlevel 1 (
    echo ERROR: C compilation failed. Check MinGW and FFTW3 installation.
    exit /b 1
)
cd ..
echo C sources compiled.

REM ── Python dependencies ───────────────────────────────────────────────────
echo.
echo Installing Python dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller

REM ── PyInstaller build ─────────────────────────────────────────────────────
echo.
echo Running PyInstaller...
pyinstaller mu2mech.spec --clean --noconfirm
if errorlevel 1 (
    echo ERROR: PyInstaller build failed.
    exit /b 1
)

echo.
echo ===================================================
echo  Build complete!
echo  Executable: dist\mu2mech\mu2mech.exe
echo  Distribute the entire dist\mu2mech\ folder.
echo ===================================================
pause
