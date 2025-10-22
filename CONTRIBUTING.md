# Contributing to @motesoftware/markitdown

Contributions are very welcome.

This guide covers development, testing, and releasing of markitdown npm packages.

## Pre-reqs

- Python3
- Node JS

## Quick Start

```bash
# Build binary for your platform
./scripts/install_deps.sh
source venv/bin/activate
python scripts/build.py

# Copy to npm package and test
./scripts/copy_binaries_to_packages.sh
cd packages/markitdown
pnpm install
pnpm link --global
markitdown test.html # Should see markdown output
```

## Package Architecture

This is a pnpm monorepo with platform-specific binaries:

```
packages/
├── markitdown/                    # Main package (CLI + Node Lib)
├── markitdown-binary-darwin-x64/  # macOS Intel binary
├── markitdown-binary-darwin-arm64/# macOS ARM binary
├── markitdown-binary-linux-x64/   # Linux binary
└── markitdown-binary-win32-x64/   # Windows binary
```

**How it works:**
- User installs `@motesoftware/markitdown`
- npm tries to install the correct `optionalDependency` for their platform
- If that fails, the postinstall script downloads the binary from npm
- Result: User gets the right binary automatically

## Development

### Building Binaries

```bash
# Setup Python environment
./scripts/install_deps.sh
source venv/bin/activate  # Windows: venv/Scripts/activate

# Build for current platform
python scripts/build.py

# Copy to package directory
./scripts/copy_binaries_to_packages.sh
```

### Local Testing

**Test with npm link:**
```bash
cd packages/markitdown
pnpm install
pnpm link --global

# Test CLI
markitdown README.md

# Test Lib
node -e "console.log(require('@motesoftware/markitdown').getBinaryPath())"

# Cleanup
pnpm unlink --global
```

### Testing Checklist

- [ ] Binary builds successfully
- [ ] CLI command works (`markitdown test.html # Should see markdown output`)
- [ ] CLI can convert files
- [ ] Programmatic Lib works (`getBinaryPath()`, `runMarkitdown()`)
- [ ] Package structure is correct (`npm pack`)

## Commit Guidelines

We use [Conventional Commits](https://www.conventionalcommits.org/) for automated versioning:

| Commit Type | Version Bump | Example |
|-------------|--------------|---------|
| `feat:` | Minor (1.0.0 → 1.1.0) | `feat: add Excel support` |
| `fix:` | Patch (1.0.0 → 1.0.1) | `fix: handle corrupt PDFs` |
| `feat!:` or `BREAKING CHANGE:` | Major (1.0.0 → 2.0.0) | `feat!: redesign CLI` |

**Non-releasing commits:** `docs:`, `chore:`, `test:`, `ci:`, `refactor:`

**Examples:**
```bash
git commit -m "fix: correct binary error"
git commit -m "feat: updated binary version"
git commit -m "feat!: breaking binary update

BREAKING CHANGE: New binary version is considered breaking"
```

## Release Process

Releases are **automated** via GitHub Actions and will be run when a PR is accepted:

1. **Push to main** with conventional commit messages
2. **CI automatically:**
   - Builds binaries for all platforms (Linux, macOS x64/ARM, Windows)
   - Determines version from commits
   - Updates package.json files
   - Generates CHANGELOG.md
   - Creates GitHub release
   - Publishes all packages to npm
3. **Done!** New version is live on npm

### Prerequisites

### Monitoring

- **Actions**: Check workflow runs in Actions tab
- **Releases**: View GitHub Releases tab
- **npm**: Visit [npmjs.com/package/@motesoftware/markitdown](https://www.npmjs.com/package/@motesoftware/markitdown)
- **Changelog**: See CHANGELOG.md (auto-generated)

## Troubleshooting

## Scripts Reference

- `scripts/install_deps.sh` - Setup Python environment and install dependencies
- `scripts/build.py` - Build binary for current platform using PyInstaller
- `scripts/copy_binaries_to_packages.sh` - Copy binaries to npm package directories
- `packages/markitdown/install.js` - Postinstall script (downloads binary if needed)
- `packages/markitdown/index.js` - Main Lib (`getBinaryPath()`, `runMarkitdown()`)

## Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Release](https://semantic-release.gitbook.io/)
- [npm optionalDependencies](https://docs.npmjs.com/cli/v9/configuring-npm/package-json#optionaldependencies)
- [pnpm workspaces](https://pnpm.io/workspaces)
