#!/usr/bin/env python3
"""
build.py - Build markitdown binaries using PyInstaller

This script:
1. Detects the current platform
2. Runs PyInstaller with the spec file
3. Copies the binary to the appropriate bin/<platform>/ directory
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path


def get_platform():
    """Detect the current platform and return platform identifier."""
    system = platform.system().lower()
    if system == "windows":
        return "win32"
    elif system == "darwin":
        return "darwin"
    elif system == "linux":
        return "linux"
    else:
        raise RuntimeError(f"Unsupported platform: {system}")


def get_binary_name(plat):
    """Get the appropriate binary name for the platform."""
    if plat == "win32":
        return "markitdown.exe"
    else:
        return "markitdown"


def main():
    # Get paths
    script_dir = Path(__file__).parent.resolve()
    root_dir = script_dir.parent
    spec_file = root_dir / "build" / "specs" / "markitdown.spec"
    build_dir = root_dir / "build"
    dist_dir = build_dir / "dist"

    # Detect platform
    plat = get_platform()
    binary_name = get_binary_name(plat)

    print(f"=== Building markitdown binary for {plat} ===")
    print(f"Root directory: {root_dir}")
    print(f"Spec file: {spec_file}")
    print(f"Platform: {plat}")
    print(f"Binary name: {binary_name}")
    print()

    # Check if spec file exists
    if not spec_file.exists():
        print(f"Error: Spec file not found at {spec_file}")
        sys.exit(1)

    # Change to root directory
    os.chdir(root_dir)

    # Clean previous build artifacts
    print("Cleaning previous build artifacts...")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    work_dir = build_dir / "build"
    if work_dir.exists():
        shutil.rmtree(work_dir)
    print()

    # Run PyInstaller
    print("Running PyInstaller...")
    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--clean",
        "--distpath", str(dist_dir),
        "--workpath", str(work_dir),
        str(spec_file)
    ]

    print(f"Command: {' '.join(cmd)}")
    print()

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: PyInstaller failed with exit code {e.returncode}")
        sys.exit(1)

    print()
    print("PyInstaller completed successfully")
    print()

    # Find the built binary
    built_binary = dist_dir / binary_name
    if not built_binary.exists():
        print(f"Error: Built binary not found at {built_binary}")
        print(f"Contents of {dist_dir}:")
        if dist_dir.exists():
            for item in dist_dir.iterdir():
                print(f"  - {item}")
        sys.exit(1)

    # Create output directory
    output_dir = root_dir / "bin" / plat
    output_dir.mkdir(parents=True, exist_ok=True)

    # Copy binary to output directory
    output_binary = output_dir / binary_name
    print(f"Copying binary to {output_binary}...")
    shutil.copy2(built_binary, output_binary)

    # Make binary executable on Unix-like systems
    if plat in ["darwin", "linux"]:
        os.chmod(output_binary, 0o755)

    # Get binary size
    size_mb = output_binary.stat().st_size / (1024 * 1024)

    print()
    print("=== Build complete ===")
    print(f"Binary location: {output_binary}")
    print(f"Binary size: {size_mb:.2f} MB")
    print()
    print("You can now test the binary with:")
    print(f"  python scripts/test_binary.py")
    print()
    print("Or run it directly:")
    print(f"  {output_binary} --help")
    print()


if __name__ == "__main__":
    main()
