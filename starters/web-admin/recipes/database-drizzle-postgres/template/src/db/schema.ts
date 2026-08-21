import { pgTable, text, timestamp } from "drizzle-orm/pg-core";

export const projectSettings = pgTable("project_settings", {
  key: text("key").primaryKey(),
  value: text("value").notNull(),
  updatedAt: timestamp("updated_at", { withTimezone: true })
    .defaultNow()
    .notNull(),
});
