import { spawn } from "node:child_process";
import { once } from "node:events";
import { resolve } from "node:path";

const port = 3200;
const url = `http://127.0.0.1:${port}`;
const nextBinary = resolve("node_modules", "next", "dist", "bin", "next");
const server = spawn(
  process.execPath,
  [nextBinary, "start", "--hostname", "127.0.0.1", "--port", String(port)],
  { env: process.env, stdio: ["ignore", "pipe", "pipe"] },
);

let output = "";
server.stdout.on("data", (chunk) => (output += chunk));
server.stderr.on("data", (chunk) => (output += chunk));

try {
  const deadline = Date.now() + 60_000;
  let response;
  while (Date.now() < deadline) {
    if (server.exitCode !== null) {
      throw new Error(`Production server exited early.\n${output}`);
    }
    try {
      response = await fetch(url);
      if (response.ok) break;
    } catch {}
    await new Promise((resolveDelay) => setTimeout(resolveDelay, 500));
  }
  if (!response?.ok) throw new Error(`Production smoke timed out.\n${output}`);
  const html = await response.text();
  if (!html.includes("<main")) {
    throw new Error("Production response did not contain application content");
  }
  console.log("Production next start smoke passed.");
} finally {
  if (server.exitCode === null) {
    server.kill("SIGTERM");
    await Promise.race([
      once(server, "exit"),
      new Promise((resolveDelay) => setTimeout(resolveDelay, 5_000)),
    ]);
  }
}
