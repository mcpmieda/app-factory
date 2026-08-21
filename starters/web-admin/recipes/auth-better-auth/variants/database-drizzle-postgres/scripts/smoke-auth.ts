import { config } from "dotenv";

async function main() {
  config({ path: ".env.local" });
  const { auth } = await import("../src/lib/auth");
  const { sqlClient } = await import("../src/db/client");
  const baseURL = process.env.BETTER_AUTH_URL ?? "http://127.0.0.1:3000";

  try {
    const login = await auth.handler(
      new Request(`${baseURL}/api/auth/sign-in/email`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          email: process.env.SEED_ADMIN_EMAIL ?? "admin@example.com",
          password: process.env.SEED_ADMIN_PASSWORD ?? "local-admin-password",
        }),
      }),
    );
    if (!login.ok) {
      throw new Error(`Better Auth login smoke failed with ${login.status}`);
    }

    const cookies = login.headers
      .getSetCookie()
      .map((value) => value.split(";", 1)[0]);
    const session = await auth.handler(
      new Request(`${baseURL}/api/auth/get-session`, {
        headers: { cookie: cookies.join("; ") },
      }),
    );
    const payload = (await session.json()) as { user?: { email?: string } };
    if (!session.ok || payload.user?.email !== process.env.SEED_ADMIN_EMAIL) {
      throw new Error(
        "Better Auth session smoke did not recover the seeded user",
      );
    }
    console.log("Better Auth PostgreSQL login/session smoke passed.");
  } finally {
    await sqlClient.end({ timeout: 5 });
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
