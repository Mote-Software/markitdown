#!/usr/bin/env node
const fs = require("fs");
const path = require("path");

// Ensure the binary has executable permissions
const binaryPath = path.join(__dirname, "bin", "markitdown");

try {
	if (fs.existsSync(binaryPath)) {
		fs.chmodSync(binaryPath, 0o755);
		console.log("✓ markitdown binary permissions set");
	}
} catch (error) {
	console.warn("Warning: Could not set executable permissions:", error.message);
	// Don't fail the installation if this doesn't work
}
