const path = require("path");
const { execFileSync } = require("child_process");

// Lookup table for all platforms and binary distribution packages
const BINARY_DISTRIBUTION_PACKAGES = {
	"darwin-x64": "@motesoftware/markitdown-binary-darwin-x64",
	"darwin-arm64": "@motesoftware/markitdown-binary-darwin-arm64",
	"linux-x64": "@motesoftware/markitdown-binary-linux-x64",
	"win32-x64": "@motesoftware/markitdown-binary-win32-x64",
};

/**
 * Get the path to the markitdown binary for the current platform
 * @returns {string} The absolute path to the binary
 */
function getBinaryPath() {
	// Windows binaries end with .exe so we need to special case them.
	const binaryName =
		process.platform === "win32" ? "markitdown.exe" : "markitdown";

	// Determine package name for this platform
	const platformSpecificPackageName =
		BINARY_DISTRIBUTION_PACKAGES[`${process.platform}-${process.arch}`];

	if (!platformSpecificPackageName) {
		throw new Error(
			`Platform ${process.platform}-${process.arch} is not supported. ` +
				`Supported platforms: ${Object.keys(BINARY_DISTRIBUTION_PACKAGES).join(", ")}`,
		);
	}

	try {
		// Try to resolve from the platform-specific optional dependency
		return require.resolve(`${platformSpecificPackageName}/bin/${binaryName}`);
	} catch (e) {
		// Fall back to the binary downloaded by the postinstall script
		return path.join(__dirname, binaryName);
	}
}

/**
 * Execute the markitdown binary with the given arguments
 * @param {...string} args - Arguments to pass to the binary
 * @returns {Buffer} The output from the binary
 */
function runBinary(...args) {
	return execFileSync(getBinaryPath(), args, {
		stdio: "inherit",
	});
}

/**
 * Execute the markitdown binary with the given arguments and return output
 * @param {...string} args - Arguments to pass to the binary
 * @returns {string} The output from the binary as a string
 */
function runMarkitdown(...args) {
	return execFileSync(getBinaryPath(), args, {
		encoding: "utf-8",
	});
}

module.exports = {
	getBinaryPath,
	runBinary,
	runMarkitdown,
};
