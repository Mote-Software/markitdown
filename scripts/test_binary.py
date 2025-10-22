#!/usr/bin/env python3
"""
test_binary.py - Test markitdown binary functionality

This script:
1. Locates the binary for the current platform
2. Tests basic conversion functionality with output redirection
3. Validates output correctness
"""

import os
import sys
import subprocess
import tempfile
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


def get_binary_path(root_dir, plat):
    """Get the path to the binary for the current platform."""
    binary_name = "markitdown.exe" if plat == "win32" else "markitdown"
    binary_path = root_dir / "bin" / plat / binary_name
    return binary_path


def run_command_with_redirect(binary_path, args, output_file, shell=False):
    """Run the binary with output redirected to a file."""
    try:
        if shell:
            # Use shell redirection for stdin tests
            cmd = f"{binary_path} {' '.join(args)} > {output_file}"
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
        else:
            # Run command and redirect stdout to file
            with open(output_file, 'w') as f:
                result = subprocess.run(
                    [str(binary_path)] + args,
                    stdout=f,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=30
                )
        return result
    except subprocess.TimeoutExpired:
        print(f"  Error: Command timed out")
        return None
    except Exception as e:
        print(f"  Error running command: {e}")
        return None


def test_html_conversion(binary_path):
    """Test HTML file conversion with output redirection."""
    print("Testing HTML file conversion...")

    # Create a temporary HTML file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Test HTML</title>
</head>
<body>
    <h1>Hello, World!</h1>
    <p>This is a <strong>test</strong> HTML file.</p>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
    </ul>
</body>
</html>"""
        f.write(html_content)
        temp_html = f.name

    # Create temp output file
    output_file = temp_html.replace('.html', '.md')

    try:
        # Convert HTML to markdown with output redirection
        result = run_command_with_redirect(binary_path, [temp_html], output_file)

        if result is None:
            return False

        if result.returncode != 0:
            print(f"  FAILED: Conversion returned non-zero exit code {result.returncode}")
            print(f"  stderr: {result.stderr}")
            return False

        # Check if output file was created
        if not os.path.exists(output_file):
            print(f"  FAILED: Output file was not created at {output_file}")
            return False

        # Read and verify output content
        with open(output_file, 'r') as f:
            output = f.read()

        # Check for expected markdown content
        if "# Hello, World!" not in output:
            print(f"  FAILED: Output doesn't contain expected heading")
            print(f"  Output: {output[:200]}")
            return False

        if "**test**" not in output:
            print(f"  FAILED: Output doesn't contain expected bold text")
            print(f"  Output: {output[:200]}")
            return False

        if "* Item 1" not in output and "- Item 1" not in output:
            print(f"  FAILED: Output doesn't contain expected list items")
            print(f"  Output: {output[:200]}")
            return False

        print(f"  Output preview: {output[:100]}")
        print("  PASSED")
        return True

    finally:
        # Clean up temporary files
        try:
            os.unlink(temp_html)
            if os.path.exists(output_file):
                os.unlink(output_file)
        except Exception:
            pass


def test_text_conversion(binary_path):
    """Test text file conversion with output redirection."""
    print("Testing text file conversion...")

    # Create a temporary text file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        test_content = "Hello, World!\nThis is a test file.\nLine 3 of text."
        f.write(test_content)
        temp_txt = f.name

    # Create temp output file
    output_file = temp_txt.replace('.txt', '.md')

    try:
        # Convert text to markdown with output redirection
        result = run_command_with_redirect(binary_path, [temp_txt], output_file)

        if result is None:
            return False

        if result.returncode != 0:
            print(f"  FAILED: Conversion returned non-zero exit code {result.returncode}")
            print(f"  stderr: {result.stderr}")
            return False

        # Check if output file was created
        if not os.path.exists(output_file):
            print(f"  FAILED: Output file was not created at {output_file}")
            return False

        # Read and verify output content
        with open(output_file, 'r') as f:
            output = f.read()

        if "Hello, World!" not in output:
            print(f"  FAILED: Output doesn't contain expected text")
            print(f"  Output: {output[:200]}")
            return False

        print(f"  Output preview: {output[:100]}")
        print("  PASSED")
        return True

    finally:
        # Clean up temporary files
        try:
            os.unlink(temp_txt)
            if os.path.exists(output_file):
                os.unlink(output_file)
        except Exception:
            pass


def test_stdin_conversion(binary_path):
    """Test conversion from stdin with output redirection."""
    print("Testing stdin conversion...")

    # Create temp output file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        output_file = f.name

    try:
        # Test stdin using subprocess.PIPE (cross-platform)
        test_content = "Test content from stdin"

        with open(output_file, 'w') as outf:
            result = subprocess.run(
                [str(binary_path)],
                input=test_content,
                stdout=outf,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30
            )

        if result.returncode != 0:
            print(f"  FAILED: Stdin conversion returned non-zero exit code {result.returncode}")
            print(f"  stderr: {result.stderr}")
            return False

        # Check if output file was created
        if not os.path.exists(output_file):
            print(f"  FAILED: Output file was not created at {output_file}")
            return False

        # Read and verify output content
        with open(output_file, 'r') as f:
            output = f.read()

        if "Test content from stdin" not in output:
            print(f"  FAILED: Output doesn't contain expected text")
            print(f"  Output: {output}")
            return False

        print(f"  Output preview: {output[:100]}")
        print("  PASSED")
        return True

    except Exception as e:
        print(f"  EXCEPTION: {e}")
        return False
    finally:
        # Clean up temporary file
        try:
            if os.path.exists(output_file):
                os.unlink(output_file)
        except Exception:
            pass


def main():
    # Get paths
    script_dir = Path(__file__).parent.resolve()
    root_dir = script_dir.parent

    # Detect platform and get binary path
    plat = get_platform()
    binary_path = get_binary_path(root_dir, plat)

    print(f"=== Testing markitdown binary for {plat} ===")
    print(f"Binary path: {binary_path}")
    print()

    # Check if binary exists
    if not binary_path.exists():
        print(f"Error: Binary not found at {binary_path}")
        print("Please run 'python scripts/build.py' first")
        sys.exit(1)

    # Check if binary is executable
    if not os.access(binary_path, os.X_OK):
        print(f"Warning: Binary is not executable, attempting to fix...")
        os.chmod(binary_path, 0o755)

    # Run tests
    tests = [
        ("HTML file conversion", lambda: test_html_conversion(binary_path)),
        ("Text file conversion", lambda: test_text_conversion(binary_path)),
        ("Stdin conversion", lambda: test_stdin_conversion(binary_path)),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  EXCEPTION: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
        print()

    # Print summary
    total = passed + failed
    print("=== Test Summary ===")
    print(f"Total tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print()

    if failed > 0:
        print("Some tests failed. Please review the output above.")
        sys.exit(1)
    else:
        print("All tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
