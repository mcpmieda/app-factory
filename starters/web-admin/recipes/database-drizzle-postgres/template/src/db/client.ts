import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";

import * as schema from "./schema";

const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) throw new Error("DATABASE_URL is required");

const globalDatabase = globalThis as unknown as {
  postgresClient?: ReturnType<typeof postgres>;
};
const sqlClient =
  globalDatabase.postgresClient ?? postgres(databaseUrl, { prepare: false });

if (process.env.NODE_ENV !== "production") {
  globalDatabase.postgresClient = sqlClient;
}

export const db = drizzle(sqlClient, { schema });
export { sqlClient };
