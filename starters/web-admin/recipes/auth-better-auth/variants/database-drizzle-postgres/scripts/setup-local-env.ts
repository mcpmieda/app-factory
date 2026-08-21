import { config } from "dotenv";

config({ path: ".env.local" });

const required = ["DATABASE_URL", "BETTER_AUTH_SECRET"] as const;
for (const name of required) {
  if (!process.env[name]) {
    throw new Error(
      `${name} is required. Copy .env.example to .env.local for local use or inject it in the deployment environment.`,
    );
  }
}

const protocol = new URL(process.env.DATABASE_URL!).protocol;
if (protocol !== "postgres:" && protocol !== "postgresql:") {
  throw new Error(
    "DATABASE_URL must use the postgres:// or postgresql:// protocol",
  );
}
if (process.env.BETTER_AUTH_SECRET!.length < 32) {
  throw new Error("BETTER_AUTH_SECRET must contain at least 32 characters");
}

console.log("PostgreSQL and Better Auth environment validated.");
