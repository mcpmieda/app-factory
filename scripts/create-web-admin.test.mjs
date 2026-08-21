import assert from "node:assert/strict";
import {
  mkdtemp,
  mkdir,
  readFile,
  rm,
  stat,
  writeFile,
} from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";

const repositoryRoot = resolve(import.meta.dirname, "..");
const generator = join(repositoryRoot, "scripts", "create-web-admin.mjs");

function generate(destination, name, recipes = []) {
  return spawnSync(
    process.execPath,
    [
      generator,
      destination,
      name,
      ...recipes.flatMap((recipe) => ["--recipe", recipe]),
    ],
    { cwd: repositoryRoot, encoding: "utf8" },
  );
}

async function json(path) {
  return JSON.parse(await readFile(path, "utf8"));
}

test("generator resolves recipe providers, motion baseline, order and failures safely", async () => {
  const temporaryRoot = await mkdtemp(join(tmpdir(), "app-factory-web-admin-"));

  try {
    const base = join(temporaryRoot, "base");
    const baseRun = generate(base, "Patrimônio Escolar");
    assert.equal(baseRun.status, 0, baseRun.stderr);
    assert.equal(
      (await json(join(base, "package.json"))).name,
      "patrimonio-escolar",
    );
    const baseManifest = await json(join(base, ".app-factory.json"));
    assert.deepEqual(baseManifest.recipes, []);
    assert.equal(baseManifest.profile, "web-admin");
    assert.equal(baseManifest.factoryBaseline, "v0.7");
    assert.equal(baseManifest.motionProfile, "ambient");
    assert.match(
      await readFile(join(base, "PROJECT_STATE.md"), "utf8"),
      /Patrimônio Escolar/,
    );

    const databaseOnly = join(temporaryRoot, "database-only");
    const databaseRun = generate(databaseOnly, "Database Only", [
      "database-drizzle",
    ]);
    assert.equal(databaseRun.status, 0, databaseRun.stderr);
    assert.deepEqual(
      (await json(join(databaseOnly, ".app-factory.json"))).recipes,
      ["database-drizzle"],
    );

    const authOnly = join(temporaryRoot, "auth-only");
    const authRun = generate(authOnly, "Auth Only", ["auth-better-auth"]);
    assert.equal(authRun.status, 0, authRun.stderr);
    assert.deepEqual(
      (await json(join(authOnly, ".app-factory.json"))).recipes,
      ["database-drizzle", "auth-better-auth"],
    );

    const explicit = join(temporaryRoot, "explicit");
    const explicitRun = generate(explicit, "Explicit Combo", [
      "database-drizzle",
      "auth-better-auth",
    ]);
    assert.equal(explicitRun.status, 0, explicitRun.stderr);
    assert.deepEqual(
      (await json(join(explicit, ".app-factory.json"))).recipes,
      ["database-drizzle", "auth-better-auth"],
    );

    const postgresAuth = join(temporaryRoot, "postgres-auth");
    const postgresRun = generate(postgresAuth, "Postgres Auth", [
      "database-drizzle-postgres",
      "auth-better-auth",
    ]);
    assert.equal(postgresRun.status, 0, postgresRun.stderr);
    const postgresManifest = await json(
      join(postgresAuth, ".app-factory.json"),
    );
    assert.deepEqual(postgresManifest.recipes, [
      "database-drizzle-postgres",
      "auth-better-auth",
    ]);
    assert.equal(postgresManifest.factoryBaseline, "v0.7");
    assert.equal(postgresManifest.motionProfile, "ambient");
    const postgresPackage = await json(join(postgresAuth, "package.json"));
    assert.equal(postgresPackage.dependencies.postgres, "3.4.9");
    assert.equal(postgresPackage.dependencies["better-sqlite3"], undefined);
    assert.equal(
      postgresPackage.devDependencies["@types/better-sqlite3"],
      undefined,
    );
    assert.match(
      await readFile(join(postgresAuth, "src", "lib", "auth.ts"), "utf8"),
      /provider: "pg"/,
    );

    const conflicting = join(temporaryRoot, "conflicting");
    const conflictingRun = generate(conflicting, "Conflicting Providers", [
      "database-drizzle",
      "database-drizzle-postgres",
    ]);
    assert.notEqual(conflictingRun.status, 0);
    await assert.rejects(stat(conflicting), { code: "ENOENT" });

    const unknown = join(temporaryRoot, "unknown");
    const unknownRun = generate(unknown, "Unknown Recipe", ["not-a-recipe"]);
    assert.notEqual(unknownRun.status, 0);
    await assert.rejects(stat(unknown), { code: "ENOENT" });

    const occupied = join(temporaryRoot, "occupied");
    await mkdir(occupied);
    await writeFile(join(occupied, "keep.txt"), "do not overwrite", "utf8");
    const occupiedRun = generate(occupied, "Other Project");
    assert.notEqual(occupiedRun.status, 0);
    assert.equal(
      await readFile(join(occupied, "keep.txt"), "utf8"),
      "do not overwrite",
    );
  } finally {
    await rm(temporaryRoot, { recursive: true, force: true });
  }
});
