#!/bin/bash
# install_deps.sh - Install build dependencies for markitdown binaries
# This script sets up a virtual environment and installs all required dependencies

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=== Installing build dependencies for markitdown binaries ==="
echo "Root directory: $ROOT_DIR"

# Ensure we're in the root directory
cd "$ROOT_DIR"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "Using Python version: $PYTHON_VERSION"

# Check Python version is >= 3.10
PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f1)
PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f2)
if [ "$PYTHON_MAJOR" -lt 3 ] || { [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]; }; then
    echo "Error: Python 3.10 or higher is required (found $PYTHON_VERSION)"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install markitdown package from submodule with all optional dependencies
echo "Installing markitdown package from submodule with all extras..."
pip install -e "./markitdown/packages/markitdown[all]"

# Install PyInstaller and other build dependencies
echo "Installing PyInstaller and build dependencies..."
pip install -r requirements-build.txt

echo ""
echo "=== Installation complete ==="
echo "Virtual environment is active. You can now run:"
echo "  python scripts/build.py"
echo ""
echo "To activate the virtual environment in future sessions:"
echo "  source venv/bin/activate"
