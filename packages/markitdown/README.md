# @motesoftware/markitdown

Convert various file formats to Markdown with ease.

## Installation

```bash
npm install @motesoftware/markitdown
```

Or with pnpm:

```bash
pnpm add @motesoftware/markitdown
```

## Usage

### Command Line

```bash
# Convert a file to markdown
markitdown input.pdf > output.md

# Or use npx without installing
npx @motesoftware/markitdown input.docx > output.md
```

### Programmatic API

```javascript
const { runMarkitdown, getBinaryPath } = require('@motesoftware/markitdown')

// Run markitdown and get output
const markdown = runMarkitdown('input.pdf')
console.log(markdown)
```

## Supported Formats

- PDF documents (.pdf)
- Word documents (.docx)
- PowerPoint presentations (.pptx)
- HTML files (.html)
- Images (various formats)
- Audio files (with transcription)
- And more!

## Platform Support

This package includes pre-built binaries for:

- macOS (Intel x64 and Apple Silicon arm64)
- Linux (x64)
- Windows (x64)

The correct binary for your platform will be automatically installed.

## How It Works

This package uses platform-specific optional dependencies to install the correct binary for your system. If the optional dependency installation fails (e.g., due to network issues), the postinstall script will download the binary from npm as a fallback.

## License

MIT

## Credits

Wrapper of the excellent [markitdown](https://github.com/microsoft/markitdown) project by Microsoft.
