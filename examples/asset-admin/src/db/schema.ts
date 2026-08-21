import { sql } from "drizzle-orm";
import {
  integer,
  sqliteTable,
  text,
  uniqueIndex,
} from "drizzle-orm/sqlite-core";

const nowInMilliseconds = sql`(cast(unixepoch('subsecond') * 1000 as integer))`;

export const projectSettings = sqliteTable("project_settings", {
  key: text("key").primaryKey(),
  value: text("value").notNull(),
  updatedAt: integer("updated_at", { mode: "timestamp_ms" })
    .default(nowInMilliseconds)
    .notNull(),
});

export const assetCategories = [
  "technology",
  "furniture",
  "equipment",
  "other",
] as const;
export const assetStatuses = [
  "available",
  "in-use",
  "maintenance",
  "retired",
] as const;

export const assets = sqliteTable(
  "assets",
  {
    id: text("id").primaryKey(),
    code: text("code").notNull(),
    description: text("description").notNull(),
    category: text("category", { enum: assetCategories }).notNull(),
    location: text("location").notNull(),
    custodian: text("custodian"),
    status: text("status", { enum: assetStatuses })
      .notNull()
      .default("available"),
    notes: text("notes"),
    active: integer("active", { mode: "boolean" }).notNull().default(true),
    createdAt: integer("created_at", { mode: "timestamp_ms" })
      .default(nowInMilliseconds)
      .notNull(),
    updatedAt: integer("updated_at", { mode: "timestamp_ms" })
      .default(nowInMilliseconds)
      .$onUpdate(() => new Date())
      .notNull(),
  },
  (table) => [uniqueIndex("assets_code_uidx").on(table.code)],
);

export type Asset = typeof assets.$inferSelect;
export type NewAsset = typeof assets.$inferInsert;
