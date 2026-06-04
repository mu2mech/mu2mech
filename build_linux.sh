#!/bin/bash
# Build script for mu2mech — Linux x86_64
# Produces a self-contained directory at dist/mu2mech/
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ── Python version check ──────────────────────────────────────────────────────
PY=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Python version: $PY"

# PySide6 (used here) requires Python 3.8+
PY_MAJOR=$(python3 -c "import sys; print(sys.version_info.major)")
PY_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")
if [ "$PY_MAJOR" -ne 3 ] || [ "$PY_MINOR" -lt 8 ]; then
    echo "ERROR: Python 3.8 or newer required. Found Python $PY."
    exit 1
fi

# ── Compile C sources ─────────────────────────────────────────────────────────
echo ""
echo "Compiling C sources..."
if ! command -v gcc &>/dev/null; then
    echo "ERROR: gcc not found. Install with: sudo apt install build-essential"
    exit 1
fi
if ! ldconfig -p | grep -q libfftw3; then
    echo "ERROR: libfftw3 not found. Install with: sudo apt install libfftw3-dev"
    exit 1
fi

cd Sources
make all
cd ..
echo "C sources compiled."

# ── Python dependencies ───────────────────────────────────────────────────────
echo ""
echo "Installing Python dependencies..."
pip3 install --upgrade pip
pip3 install PySide6 pyvista pyvistaqt numpy matplotlib Pillow PyYAML ffmpeg-python
pip3 install pyinstaller

# ── PyInstaller build ─────────────────────────────────────────────────────────
echo ""
echo "Running PyInstaller..."
pyinstaller mu2mech.spec --clean --noconfirm

# ── Launcher wrapper ──────────────────────────────────────────────────────────
# On Wayland desktops the app needs QT_QPA_PLATFORM=xcb for VTK rendering.
# Write a wrapper script alongside the executable.
cat > dist/mu2mech/run_mu2mech.sh << 'LAUNCHER'
#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export QT_QPA_PLATFORM=xcb
export LIBGL_ALWAYS_SOFTWARE="${LIBGL_ALWAYS_SOFTWARE:-0}"
export MESA_GL_VERSION_OVERRIDE=3.2
exec "$DIR/mu2mech" "$@"
LAUNCHER
chmod +x dist/mu2mech/run_mu2mech.sh

echo ""
echo "═══════════════════════════════════════════════════════════"
echo " Build complete!"
echo " Executable:    dist/mu2mech/mu2mech"
echo " Launch script: dist/mu2mech/run_mu2mech.sh  (recommended)"
echo " Distribute the entire dist/mu2mech/ folder."
echo ""
echo " Note: on Wayland desktops use run_mu2mech.sh so that"
echo " VTK renders correctly via the XCB (X11) backend."
echo "═══════════════════════════════════════════════════════════"
