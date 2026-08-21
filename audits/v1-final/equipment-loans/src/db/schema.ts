import { sql } from "drizzle-orm";
import { integer, sqliteTable, text } from "drizzle-orm/sqlite-core";

const nowInMilliseconds = sql`(cast(unixepoch('subsecond') * 1000 as integer))`;

export const equipment = sqliteTable("equipment", {
  id: text("id").primaryKey(),
  assetTag: text("asset_tag").notNull().unique(),
  name: text("name").notNull(),
  category: text("category").notNull(),
  createdAt: integer("created_at", { mode: "timestamp_ms" })
    .default(nowInMilliseconds)
    .notNull(),
});

export const loans = sqliteTable("loans", {
  id: text("id").primaryKey(),
  equipmentId: text("equipment_id")
    .notNull()
    .references(() => equipment.id, { onDelete: "restrict" }),
  responsibleName: text("responsible_name").notNull(),
  dueDate: text("due_date").notNull(),
  loanedAt: integer("loaned_at", { mode: "timestamp_ms" })
    .default(nowInMilliseconds)
    .notNull(),
  returnedAt: integer("returned_at", { mode: "timestamp_ms" }),
});
