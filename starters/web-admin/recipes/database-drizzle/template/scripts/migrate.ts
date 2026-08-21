import { config } from "dotenv";
import { migrate } from "drizzle-orm/better-sqlite3/migrator";

async function main() {
  config({ path: ".env.local" });
  const { db } = await import("../src/db/client");
  migrate(db, { migrationsFolder: "./drizzle" });
  console.log("Database migrations applied.");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
