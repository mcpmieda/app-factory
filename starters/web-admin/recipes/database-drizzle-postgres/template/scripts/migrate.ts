import { config } from "dotenv";
import { migrate } from "drizzle-orm/postgres-js/migrator";

async function main() {
  config({ path: ".env.local" });
  const { db, sqlClient } = await import("../src/db/client");
  try {
    await migrate(db, { migrationsFolder: "./drizzle" });
    console.log("PostgreSQL migrations applied.");
  } finally {
    await sqlClient.end({ timeout: 5 });
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
