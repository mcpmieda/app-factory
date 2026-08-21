import { config } from "dotenv";

config({ path: ".env.local" });

const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) {
  throw new Error(
    "DATABASE_URL is required. Copy .env.example to .env.local for local use or inject it in the deployment environment.",
  );
}

const protocol = new URL(databaseUrl).protocol;
if (protocol !== "postgres:" && protocol !== "postgresql:") {
  throw new Error(
    "DATABASE_URL must use the postgres:// or postgresql:// protocol",
  );
}

console.log(
  "PostgreSQL environment validated; no local database file created.",
);
