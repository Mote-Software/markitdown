#!/bin/bash
set -e

# Test script for local npm package testing
# This simulates the full workflow without publishing

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  Markitdown NPM Package - Local Test Script                   ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo

# Step 1: Check if binary exists
echo "Step 1/6: Checking for binary..."
if [ ! -f "$ROOT_DIR/bin/darwin/markitdown" ] && [ ! -f "$ROOT_DIR/bin/linux/markitdown" ] && [ ! -f "$ROOT_DIR/bin/win32/markitdown.exe" ]; then
    echo "❌ No binary found. Building..."

    if [ ! -d "$ROOT_DIR/venv" ]; then
        echo "   Running install_deps.sh..."
        cd "$ROOT_DIR"
        chmod +x scripts/install_deps.sh
        ./scripts/install_deps.sh
    fi

    echo "   Building binary..."
    cd "$ROOT_DIR"
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate
    python scripts/build.py
else
    echo "✓ Binary found"
fi

# Step 2: Copy binary to npm package
echo
echo "Step 2/6: Copying binary to npm package..."
cd "$ROOT_DIR"
chmod +x scripts/copy_binaries_to_packages.sh
./scripts/copy_binaries_to_packages.sh

# Step 3: Install dependencies (skip postinstall for local testing)
echo
echo "Step 3/6: Installing npm dependencies..."
cd "$ROOT_DIR/packages/markitdown"

# Temporarily disable postinstall script for local testing
echo "   Disabling postinstall script for local testing..."
jq 'del(.scripts.postinstall)' package.json > package.json.tmp
mv package.json.tmp package.json

if command -v pnpm &> /dev/null; then
    echo "   Using pnpm..."
    pnpm install
else
    echo "   Using npm..."
    npm install
fi

# Restore postinstall script
echo "   Restoring postinstall script..."
git checkout package.json 2>/dev/null || true

# Manually link the platform-specific package (simulate what optionalDependencies does)
echo "   Linking platform-specific package..."
PLATFORM=$(node -e "console.log(process.platform)")
ARCH=$(node -e "console.log(process.arch)")
PLATFORM_PKG="../markitdown-binary-${PLATFORM}-${ARCH}"

if [ -d "$PLATFORM_PKG" ]; then
    mkdir -p node_modules/@mote-software
    ln -sf "$ROOT_DIR/packages/markitdown-binary-${PLATFORM}-${ARCH}" "node_modules/@mote-software/markitdown-binary-${PLATFORM}-${ARCH}"
    echo "   ✓ Linked $PLATFORM_PKG"
else
    echo "   ⚠ Platform package $PLATFORM_PKG not found (this is okay for testing)"
fi

# Step 4: Link package globally
echo
echo "Step 4/6: Linking package globally..."
if command -v pnpm &> /dev/null; then
    pnpm link --global
else
    npm link
fi

# Step 5: Test CLI
echo
echo "Step 5/6: Testing CLI..."
echo "   Running: markitdown --help"
markitdown --help > /dev/null 2>&1 && echo "   ✓ CLI works!" || echo "   ❌ CLI failed"

# Create test file
echo "Hello from markitdown test!" > /tmp/test-markitdown.txt
echo "   Running: markitdown /tmp/test-markitdown.txt"
markitdown /tmp/test-markitdown.txt > /tmp/test-output.md
if [ -s /tmp/test-output.md ]; then
    echo "   ✓ File conversion works!"
    rm /tmp/test-markitdown.txt /tmp/test-output.md
else
    echo "   ❌ File conversion failed"
fi

# Step 6: Test programmatic API
echo
echo "Step 6/6: Testing programmatic API..."

# Test from the package directory where it's linked
cd "$ROOT_DIR/packages/markitdown"

cat > test-api-temp.js << 'EOF'
const { getBinaryPath, runMarkitdown } = require('./index.js');

try {
  // Test getBinaryPath
  const path = getBinaryPath();
  console.log('   ✓ getBinaryPath():', path);

  // Test runMarkitdown
  const output = runMarkitdown('--help');
  if (output.includes('markitdown') || output.includes('usage')) {
    console.log('   ✓ runMarkitdown() works');
  } else {
    console.log('   ❌ runMarkitdown() returned unexpected output');
  }
} catch (e) {
  console.log('   ❌ API test failed:', e.message);
  process.exit(1);
}
EOF

node test-api-temp.js
rm test-api-temp.js

cd "$ROOT_DIR"

echo
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  ✓ All tests passed!                                          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo
echo "The package is now globally linked. You can test it with:"
echo "  markitdown <file>"
echo
echo "To unlink when done:"
if command -v pnpm &> /dev/null; then
    echo "  pnpm unlink --global @mote-software/markitdown"
else
    echo "  npm unlink -g @mote-software/markitdown"
fi
echo
echo "For more detailed testing, see: LOCAL_TEST.md"
