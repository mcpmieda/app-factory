import { mkdirSync } from "node:fs"
import { basename, dirname, resolve } from "node:path"
import Database from "better-sqlite3"
import { drizzle } from "drizzle-orm/better-sqlite3"
import * as schema from "./schema"

const databaseFile = basename(process.env.DATABASE_URL ?? "web-admin.db")
const databasePath = resolve(process.cwd(), "data", databaseFile)
mkdirSync(dirname(databasePath), { recursive: true })

const globalDatabase = globalThis as unknown as { sqlite?: Database.Database }
const sqlite = globalDatabase.sqlite ?? new Database(databasePath)
sqlite.pragma("journal_mode = WAL")
sqlite.pragma("foreign_keys = ON")

if (process.env.NODE_ENV !== "production") {
  globalDatabase.sqlite = sqlite
}

export const db = drizzle(sqlite, { schema })
export { sqlite }
