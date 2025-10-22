# Markitdown Binaries

Standalone NPM package for [Markitdown](https://github.com/microsoft/markitdown) - Convert various file formats to Markdown.

This repository builds and distributes markitdown as:
- **Standalone binaries** for Windows, macOS, and Linux
- **npm package** (`@mote-software/markitdown`) with platform-specific binaries

_Intended for Node JS use - web is not supported, though could be explored._

## Quick Start

### npm Installation

```bash
# Install globally
npm install -g @mote-software/markitdown

# Or use with npx
npx @mote-software/markitdown input.pdf > output.md
```

### Download Binary

- **macOS**: Intel (x64) and Apple Silicon (arm64)
- **Linux**: x64
- **Windows**: x64

Download pre-built binaries from the [Releases](https://github.com/mote-software/markitdown-binaries/releases) page.

## Usage

### Command Line

```bash
# Convert a file to markdown
markitdown input.pdf > output.md
markitdown document.docx > output.md
markitdown presentation.pptx > output.md
```

### Programmatic API (Node.js)

```javascript
const { getBinaryPath, runMarkitdown } = require('@mote-software/markitdown')

// Run markitdown and get output
const markdown = runMarkitdown('input.pdf')
console.log(markdown)
```

## Credits

Wrapper of the excellent [markitdown](https://github.com/microsoft/markitdown) project by Microsoft.
