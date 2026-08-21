import { config } from "dotenv";
import { eq } from "drizzle-orm";

async function main() {
  config({ path: ".env.local" });
  const { user } = await import("../src/db/auth-schema");
  const { db, sqlClient } = await import("../src/db/client");
  const { createAuth } = await import("../src/lib/auth");

  try {
    const email = process.env.SEED_ADMIN_EMAIL ?? "admin@example.com";
    const [existing] = await db
      .select({ id: user.id })
      .from(user)
      .where(eq(user.email, email))
      .limit(1);
    if (existing) {
      console.log(
        "PostgreSQL administrator already exists; seed is idempotent.",
      );
      return;
    }

    const auth = createAuth({ allowSignUp: true });
    await auth.api.signUpEmail({
      body: {
        name: process.env.SEED_ADMIN_NAME ?? "Local Admin",
        email,
        password: process.env.SEED_ADMIN_PASSWORD ?? "local-admin-password",
      },
    });
    console.log("PostgreSQL administrator created.");
  } finally {
    await sqlClient.end({ timeout: 5 });
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
