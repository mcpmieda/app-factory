import { config } from "dotenv";
import { eq } from "drizzle-orm";

async function main() {
  config({ path: ".env.local" });
  const { db, sqlClient } = await import("../src/db/client");
  const { projectSettings } = await import("../src/db/schema");

  try {
    await db
      .insert(projectSettings)
      .values({ key: "factory-smoke", value: "postgres-ready" })
      .onConflictDoUpdate({
        target: projectSettings.key,
        set: { value: "postgres-ready", updatedAt: new Date() },
      });
    const [stored] = await db
      .select({ value: projectSettings.value })
      .from(projectSettings)
      .where(eq(projectSettings.key, "factory-smoke"))
      .limit(1);
    if (stored?.value !== "postgres-ready") {
      throw new Error("PostgreSQL persistence smoke did not read its write");
    }
    console.log("PostgreSQL write/read smoke passed.");
  } finally {
    await sqlClient.end({ timeout: 5 });
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
