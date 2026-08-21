import { randomBytes } from "node:crypto"
import { existsSync, writeFileSync } from "node:fs"
import { resolve } from "node:path"

const target = resolve(process.cwd(), ".env.local")

if (existsSync(target)) {
  console.log("Local environment already exists; keeping it unchanged.")
  process.exit(0)
}

const secret = randomBytes(32).toString("base64url")
const content = [
  "DATABASE_URL=./data/web-admin.db",
  "BETTER_AUTH_URL=http://localhost:3000",
  `BETTER_AUTH_SECRET=${secret}`,
  "SEED_ADMIN_NAME=Admin Pilot",
  "SEED_ADMIN_EMAIL=admin@example.com",
  "SEED_ADMIN_PASSWORD=local-pilot-password",
  "",
].join("\n")

writeFileSync(target, content, { encoding: "utf8", mode: 0o600 })
console.log("Created .env.local with a random Better Auth secret.")
