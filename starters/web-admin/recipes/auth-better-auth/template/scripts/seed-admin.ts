import { config } from "dotenv";
import { eq } from "drizzle-orm";

async function main() {
  config({ path: ".env.local" });
  const { user } = await import("../src/db/auth-schema");
  const { db } = await import("../src/db/client");
  const { createAuth } = await import("../src/lib/auth");

  const email = process.env.SEED_ADMIN_EMAIL ?? "admin@example.com";
  const existing = db
    .select({ id: user.id })
    .from(user)
    .where(eq(user.email, email))
    .get();
  if (existing) {
    console.log("Local administrator already exists; seed is idempotent.");
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
  console.log("Local administrator created.");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
