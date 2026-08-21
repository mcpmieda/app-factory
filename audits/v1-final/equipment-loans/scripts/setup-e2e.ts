import { rmSync } from "node:fs";
import { resolve } from "node:path";

import { migrate } from "drizzle-orm/better-sqlite3/migrator";

process.env.DATABASE_URL = "e2e.db";
const target = resolve(process.cwd(), "data", "e2e.db");
rmSync(target, { force: true });
rmSync(`${target}-shm`, { force: true });
rmSync(`${target}-wal`, { force: true });

const { db } = await import("../src/db/client");
migrate(db, { migrationsFolder: "./drizzle" });
console.log("Fresh fictitious E2E database ready.");
