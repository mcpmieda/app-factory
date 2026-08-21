import { existsSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

const target = resolve(process.cwd(), ".env.local");

if (existsSync(target)) {
  console.log("Local environment already exists; keeping it unchanged.");
  process.exit(0);
}

writeFileSync(target, "DATABASE_URL=local.db\n", {
  encoding: "utf8",
  mode: 0o600,
});
console.log("Created .env.local for local SQLite validation.");
