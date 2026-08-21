import { sql } from "drizzle-orm";
import { integer, sqliteTable, text } from "drizzle-orm/sqlite-core";

const nowInMilliseconds = sql`(cast(unixepoch('subsecond') * 1000 as integer))`;

export const projectSettings = sqliteTable("project_settings", {
  key: text("key").primaryKey(),
  value: text("value").notNull(),
  updatedAt: integer("updated_at", { mode: "timestamp_ms" })
    .default(nowInMilliseconds)
    .notNull(),
});
