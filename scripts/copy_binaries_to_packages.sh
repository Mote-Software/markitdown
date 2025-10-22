#!/bin/bash
set -e

# Script to copy built binaries to npm package directories
# This should be run after the binaries are built

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Copying binaries to npm packages ==="

# Detect platform
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PLATFORM="linux"
    BINARY_NAME="markitdown"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="darwin"
    BINARY_NAME="markitdown"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    PLATFORM="win32"
    BINARY_NAME="markitdown.exe"
else
    echo "Error: Unsupported platform $OSTYPE"
    exit 1
fi

# Detect architecture
ARCH=$(uname -m)
if [[ "$ARCH" == "x86_64" ]]; then
    ARCH="x64"
elif [[ "$ARCH" == "aarch64" ]] || [[ "$ARCH" == "arm64" ]]; then
    ARCH="arm64"
else
    echo "Error: Unsupported architecture $ARCH"
    exit 1
fi

PLATFORM_ARCH="${PLATFORM}-${ARCH}"
SOURCE_BINARY="${ROOT_DIR}/bin/${PLATFORM}/${BINARY_NAME}"
DEST_DIR="${ROOT_DIR}/packages/markitdown-binary-${PLATFORM_ARCH}/bin"

echo "Platform: ${PLATFORM_ARCH}"
echo "Source: ${SOURCE_BINARY}"
echo "Destination: ${DEST_DIR}"

# Check if source binary exists
if [ ! -f "$SOURCE_BINARY" ]; then
    echo "Error: Binary not found at ${SOURCE_BINARY}"
    exit 1
fi

# Create destination directory
mkdir -p "$DEST_DIR"

# Copy binary
cp "$SOURCE_BINARY" "${DEST_DIR}/${BINARY_NAME}"

# Make executable on Unix
if [[ "$PLATFORM" != "win32" ]]; then
    chmod +x "${DEST_DIR}/${BINARY_NAME}"
fi

# Get binary size
SIZE=$(du -h "${DEST_DIR}/${BINARY_NAME}" | cut -f1)

echo "✓ Binary copied successfully"
echo "  Size: ${SIZE}"
echo "  Location: ${DEST_DIR}/${BINARY_NAME}"
