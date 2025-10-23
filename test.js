const { runMarkitdown } = require("@mote-software/markitdown");
const fs = require("node:fs");

async function run() {
	fs.writeFileSync(
		"test.html",
		await (await fetch("https://example.com")).text(),
	);

	const markdown = runMarkitdown("test.html");
	console.log(markdown);
}

run();
