import assert from "node:assert/strict";
import { mkdtemp, readFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { spawnSync } from "node:child_process";

const temporaryDirectory = await mkdtemp(
  join(tmpdir(), "better-auth-schema-check-"),
);
const generatedSchema = join(temporaryDirectory, "auth-schema.ts");
const committedSchema = resolve("src", "db", "auth-schema.ts");

function contract(source) {
  const provider = source.match(/drizzle-orm\/(sqlite-core|pg-core)/)?.[1];
  const tables = [
    ...source.matchAll(
      /export const (\w+) = (?:sqlite|pg)Table\(\s*"([^"]+)"/g,
    ),
  ].map(([, symbol, table]) => `${symbol}:${table}`);
  const fields = [
    ...source.matchAll(
      /\b(?:text|integer|timestamp|boolean|varchar|index|uniqueIndex)\("([^"]+)"/g,
    ),
  ].map(([, field]) => field);
  return { provider, tables: tables.sort(), fields: fields.sort() };
}

try {
  const cli = resolve("node_modules", "auth", "dist", "index.mjs");
  const generated = spawnSync(
    process.execPath,
    [
      cli,
      "generate",
      "--config",
      "src/lib/auth.ts",
      "--output",
      generatedSchema,
      "--yes",
    ],
    {
      cwd: process.cwd(),
      encoding: "utf8",
      env: { ...process.env, BETTER_AUTH_TELEMETRY_DISABLED: "1" },
    },
  );
  if (generated.status !== 0) {
    throw new Error(
      generated.stderr || generated.stdout || "schema generation failed",
    );
  }

  const [expected, actual] = await Promise.all([
    readFile(generatedSchema, "utf8"),
    readFile(committedSchema, "utf8"),
  ]);
  assert.deepEqual(
    contract(actual),
    contract(expected),
    "Versioned Better Auth schema differs from the pinned CLI contract",
  );
  console.log("Better Auth schema contract matches the pinned CLI.");
} finally {
  await rm(temporaryDirectory, { recursive: true, force: true });
}
