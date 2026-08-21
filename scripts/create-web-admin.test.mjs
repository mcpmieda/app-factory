import assert from "node:assert/strict";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";

const repositoryRoot = resolve(import.meta.dirname, "..");
const generator = join(repositoryRoot, "scripts", "create-web-admin.mjs");

test("generator creates a named clean project and refuses a non-empty destination", async () => {
  const temporaryRoot = await mkdtemp(join(tmpdir(), "app-factory-web-admin-"));
  const destination = join(temporaryRoot, "school-assets");

  try {
    const firstRun = spawnSync(
      process.execPath,
      [generator, destination, "Patrimônio Escolar"],
      {
        cwd: repositoryRoot,
        encoding: "utf8",
      },
    );
    assert.equal(firstRun.status, 0, firstRun.stderr);

    const packageJson = JSON.parse(
      await readFile(join(destination, "package.json"), "utf8"),
    );
    const manifest = JSON.parse(
      await readFile(join(destination, ".app-factory.json"), "utf8"),
    );
    assert.equal(packageJson.name, "patrimonio-escolar");
    assert.deepEqual(manifest.recipes, []);
    assert.equal(manifest.profile, "web-admin");
    assert.match(
      await readFile(join(destination, "PROJECT_STATE.md"), "utf8"),
      /Patrimônio Escolar/,
    );

    await writeFile(join(destination, "keep.txt"), "do not overwrite", "utf8");
    const secondRun = spawnSync(
      process.execPath,
      [generator, destination, "Outro Projeto"],
      {
        cwd: repositoryRoot,
        encoding: "utf8",
      },
    );
    assert.notEqual(secondRun.status, 0);
    assert.equal(
      await readFile(join(destination, "keep.txt"), "utf8"),
      "do not overwrite",
    );
  } finally {
    await rm(temporaryRoot, { recursive: true, force: true });
  }
});
