import { defineConfig } from "drizzle-kit";

export default defineConfig({
  dialect: "sqlite",
  schema: "./src/db/**/*.ts",
  out: "./drizzle",
  dbCredentials: {
    url: `./data/${process.env.DATABASE_URL ?? "local.db"}`,
  },
  strict: true,
  verbose: true,
});
