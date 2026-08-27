import { spawn } from "node:child_process";
import { once } from "node:events";
import { get } from "node:http";
import { resolve } from "node:path";

const port = 3200;
const nextBinary = resolve("node_modules", "next", "dist", "bin", "next");
const server = spawn(
  process.execPath,
  [nextBinary, "start", "--hostname", "127.0.0.1", "--port", String(port)],
  { env: process.env, stdio: ["ignore", "pipe", "pipe"] },
);

let output = "";
server.stdout.on("data", (chunk) => (output += chunk));
server.stderr.on("data", (chunk) => (output += chunk));

function requestLoopback() {
  return new Promise((resolveRequest, rejectRequest) => {
    const request = get(
      { hostname: "127.0.0.1", port, path: "/", protocol: "http:" },
      (response) => {
        const chunks = [];
        response.on("data", (chunk) => chunks.push(chunk));
        response.on("end", () => {
          resolveRequest({
            ok: response.statusCode >= 200 && response.statusCode < 300,
            text: Buffer.concat(chunks).toString("utf8"),
          });
        });
      },
    );
    request.on("error", rejectRequest);
    request.setTimeout(5_000, () =>
      request.destroy(new Error("loopback smoke request timed out")),
    );
  });
}

try {
  const deadline = Date.now() + 60_000;
  let response;
  while (Date.now() < deadline) {
    if (server.exitCode !== null) {
      throw new Error(`Production server exited early.\n${output}`);
    }
    try {
      response = await requestLoopback();
      if (response.ok) break;
    } catch {}
    await new Promise((resolveDelay) => setTimeout(resolveDelay, 500));
  }
  if (!response?.ok) {
    throw new Error(`Production smoke timed out.\n${output}`);
  }
  if (!response.text.includes("<main")) {
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
