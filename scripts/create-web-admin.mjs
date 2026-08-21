#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import {
  cp,
  mkdir,
  readFile,
  readdir,
  rm,
  stat,
  writeFile,
} from "node:fs/promises";
import { dirname, isAbsolute, join, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDirectory = dirname(fileURLToPath(import.meta.url));
const repositoryRoot = resolve(scriptDirectory, "..");
const templateDirectory = join(
  repositoryRoot,
  "starters",
  "web-admin",
  "template",
);
const recipesDirectory = join(
  repositoryRoot,
  "starters",
  "web-admin",
  "recipes",
);
const factoryManifest = JSON.parse(
  await readFile(join(repositoryRoot, ".codex-plugin", "plugin.json"), "utf8"),
);
const templateMetadata = JSON.parse(
  await readFile(join(templateDirectory, ".factory-template.json"), "utf8"),
);
const factoryBaseline = `v${factoryManifest.version}`;
const templateBaseline = templateMetadata.factoryBaseline;
const motionProfile = "ambient";

function usage() {
  return [
    "Usage: node scripts/create-web-admin.mjs <destination> <name> [--recipe <id>]",
    "",
    "Recipes: auth-better-auth, database-drizzle, database-drizzle-postgres, advanced-ui-reui",
  ].join("\n");
}

function parseArguments(arguments_) {
  const positional = [];
  const recipes = [];

  for (let index = 0; index < arguments_.length; index += 1) {
    const argument = arguments_[index];
    if (argument === "--recipe") {
      const value = arguments_[index + 1];
      if (!value) throw new Error("--recipe requires an id");
      recipes.push(
        ...value
          .split(",")
          .map((recipe) => recipe.trim())
          .filter(Boolean),
      );
      index += 1;
    } else if (argument === "--help" || argument === "-h") {
      console.log(usage());
      process.exit(0);
    } else {
      positional.push(argument);
    }
  }

  if (positional.length !== 2) throw new Error(usage());
  return {
    destination: positional[0],
    name: positional[1].trim(),
    recipes: [...new Set(recipes)],
  };
}

function packageNameFrom(displayName) {
  const normalized = displayName
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");

  if (!normalized)
    throw new Error("Project name must contain letters or numbers");
  return normalized;
}

function shouldCopy(source) {
  const pathFromTemplate = relative(templateDirectory, source);
  if (!pathFromTemplate) return true;

  const segments = pathFromTemplate.split(sep);
  const excludedDirectories = new Set([
    "node_modules",
    ".next",
    "coverage",
    "playwright-report",
    "test-results",
    ".git",
  ]);
  if (segments.some((segment) => excludedDirectories.has(segment)))
    return false;

  const basename = segments.at(-1) ?? "";
  if (basename.startsWith(".env") && basename !== ".env.example") return false;
  if (/\.(?:db|sqlite|sqlite3)(?:-(?:shm|wal))?$/.test(basename)) return false;
  return true;
}

async function ensureSafeDestination(destination) {
  if (destination === repositoryRoot || destination === templateDirectory) {
    throw new Error(
      "Destination cannot overwrite the repository or starter template",
    );
  }

  try {
    const destinationStat = await stat(destination);
    if (!destinationStat.isDirectory())
      throw new Error("Destination exists and is not a directory");
    const entries = await readdir(destination);
    if (entries.length > 0)
      throw new Error(
        "Destination already contains files; nothing was changed",
      );
  } catch (error) {
    if (error?.code !== "ENOENT") throw error;
  }
}

async function readRecipe(id) {
  const recipeDirectory = join(recipesDirectory, id);
  const metadataPath = join(recipeDirectory, "recipe.json");

  try {
    const metadata = JSON.parse(await readFile(metadataPath, "utf8"));
    if (metadata.id !== id)
      throw new Error(`Recipe metadata id mismatch for ${id}`);
    return { ...metadata, directory: recipeDirectory };
  } catch (error) {
    if (error?.code === "ENOENT") throw new Error(`Unknown recipe: ${id}`);
    throw error;
  }
}

async function resolveRecipes(requestedIds) {
  const requested = await Promise.all(requestedIds.map(readRecipe));
  const resolved = [];
  const seen = new Set();

  function requestedProvider(requirement) {
    const providers = requested.filter(
      (recipe) =>
        recipe.id === requirement || recipe.provides?.includes(requirement),
    );
    if (providers.length > 1) {
      throw new Error(
        `Multiple requested recipes provide ${requirement}: ${providers
          .map((recipe) => recipe.id)
          .join(", ")}`,
      );
    }
    return providers[0];
  }

  async function visit(recipeOrId) {
    const recipe =
      typeof recipeOrId === "string"
        ? (requestedProvider(recipeOrId) ?? (await readRecipe(recipeOrId)))
        : recipeOrId;
    if (seen.has(recipe.id)) return;
    for (const requirement of recipe.requires ?? []) await visit(requirement);
    seen.add(recipe.id);
    resolved.push(recipe);
  }

  for (const recipe of requested) await visit(recipe);

  const resolvedIds = new Set(resolved.map((recipe) => recipe.id));
  for (const recipe of resolved) {
    const conflict = recipe.conflicts?.find((id) => resolvedIds.has(id));
    if (conflict) {
      throw new Error(`Recipe ${recipe.id} conflicts with ${conflict}`);
    }
  }

  return resolved;
}

async function updateJson(path, updater) {
  const value = JSON.parse(await readFile(path, "utf8"));
  await writeFile(path, `${JSON.stringify(updater(value), null, 2)}\n`, "utf8");
}

async function replaceInFile(path, replacements) {
  let contents = await readFile(path, "utf8");
  for (const [from, to] of replacements)
    contents = contents.replaceAll(from, to);
  await writeFile(path, contents, "utf8");
}

async function applyRecipeLayer(configuration, overlay, destination) {
  try {
    await cp(overlay, destination, { recursive: true, force: true });
  } catch (error) {
    if (error?.code !== "ENOENT") throw error;
  }

  await updateJson(join(destination, "package.json"), (packageJson) => ({
    ...packageJson,
    scripts: { ...packageJson.scripts, ...(configuration.scripts ?? {}) },
    dependencies: {
      ...packageJson.dependencies,
      ...(configuration.dependencies ?? {}),
    },
    devDependencies: {
      ...packageJson.devDependencies,
      ...(configuration.devDependencies ?? {}),
    },
  }));
}

async function applyRecipe(recipe, destination) {
  await applyRecipeLayer(
    recipe,
    join(recipe.directory, "template"),
    destination,
  );
}

async function applyRecipeVariants(recipes, destination) {
  const selectedIds = new Set(recipes.map((recipe) => recipe.id));
  for (const recipe of recipes) {
    for (const variant of recipe.variants ?? []) {
      if (!selectedIds.has(variant.when)) continue;
      await applyRecipeLayer(
        variant,
        join(recipe.directory, variant.template),
        destination,
      );
    }
  }
}

function refreshLockfile(destination) {
  const windows = process.platform === "win32";
  const executable = windows ? "cmd.exe" : "npx";
  const arguments_ = windows
    ? [
        "/d",
        "/s",
        "/c",
        "npx --yes npm@10.9.9 install --package-lock-only --ignore-scripts",
      ]
    : [
        "--yes",
        "npm@10.9.9",
        "install",
        "--package-lock-only",
        "--ignore-scripts",
      ];
  const result = spawnSync(executable, arguments_, {
    cwd: destination,
    stdio: "inherit",
  });
  if (result.status !== 0) {
    throw new Error(
      `Failed to create the npm 10.9.9 lockfile${result.error ? `: ${result.error.message}` : ""}`,
    );
  }
}

async function main() {
  const input = parseArguments(process.argv.slice(2));
  if (input.name.length < 2)
    throw new Error("Project name must contain at least two characters");

  const destination = resolve(process.cwd(), input.destination);
  const packageName = packageNameFrom(input.name);
  const recipes = await resolveRecipes(input.recipes);

  await ensureSafeDestination(destination);
  await mkdir(destination, { recursive: true });

  let completed = false;
  try {
    await cp(templateDirectory, destination, {
      recursive: true,
      filter: shouldCopy,
    });
    await rm(join(destination, ".factory-template.json"), { force: true });

    for (const recipe of recipes) await applyRecipe(recipe, destination);
    await applyRecipeVariants(recipes, destination);

    await updateJson(join(destination, "package.json"), (packageJson) => ({
      ...packageJson,
      name: packageName,
    }));

    const lockfilePath = join(destination, "package-lock.json");
    await updateJson(lockfilePath, (lockfile) => ({
      ...lockfile,
      name: packageName,
      packages: {
        ...lockfile.packages,
        "": { ...lockfile.packages[""], name: packageName },
      },
    }));

    const replacements = [
      ["Web Admin Starter", input.name],
      ["web-admin-starter", packageName],
      [templateBaseline, factoryBaseline],
    ];
    const recipeIds = recipes.map((recipe) => recipe.id);
    const formattedRecipeIds = `[${recipeIds.map((id) => JSON.stringify(id)).join(", ")}]`;
    for (const file of [
      "README.md",
      "AGENTS.md",
      "PROJECT_STATE.md",
      "PRODUCT.md",
      "src/config/project.ts",
      "src/config/project.test.ts",
    ]) {
      await replaceInFile(join(destination, file), replacements);
    }

    await replaceInFile(join(destination, "PROJECT_STATE.md"), [
      [
        "- authentication: not activated;",
        recipeIds.includes("auth-better-auth")
          ? "- authentication: Better Auth activated;"
          : "- authentication: not activated;",
      ],
      [
        "- persistence: not activated;",
        recipeIds.includes("database-drizzle-postgres")
          ? "- persistence: Drizzle + PostgreSQL activated;"
          : recipeIds.includes("database-drizzle")
            ? "- persistence: Drizzle + local SQLite activated;"
            : "- persistence: not activated;",
      ],
    ]);

    const manifest = [
      "{",
      '  "profile": "web-admin",',
      `  "motionProfile": ${JSON.stringify(motionProfile)},`,
      `  "factoryBaseline": ${JSON.stringify(factoryBaseline)},`,
      `  "generatedAt": ${JSON.stringify(new Date().toISOString())},`,
      '  "source": "starters/web-admin/template",',
      `  "recipes": ${formattedRecipeIds}`,
      "}",
      "",
    ].join("\n");
    await writeFile(join(destination, ".app-factory.json"), manifest, "utf8");

    if (recipes.length > 0) refreshLockfile(destination);
    completed = true;

    console.log(
      `Created ${input.name} at ${isAbsolute(input.destination) ? destination : input.destination}`,
    );
    console.log(`Profile: web-admin (${factoryBaseline})`);
    console.log(`Motion Profile: ${motionProfile}`);
    console.log(
      `Recipes: ${recipes.map((recipe) => recipe.id).join(", ") || "none"}`,
    );
  } finally {
    if (!completed) await rm(destination, { recursive: true, force: true });
  }
}

main().catch((error) => {
  console.error(`create-web-admin: ${error.message}`);
  process.exitCode = 1;
});
