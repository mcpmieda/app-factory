import { and, desc, eq, like, or, type SQL } from "drizzle-orm";

import { db } from "@/db/client";
import { assets, type Asset } from "@/db/schema";

export type AssetFilters = {
  query?: string;
  category?: string;
  status?: string;
  location?: string;
  archived?: boolean;
};

export async function listAssets(filters: AssetFilters = {}) {
  const conditions: SQL[] = [eq(assets.active, !filters.archived)];
  const query = filters.query?.trim();

  if (query) {
    const pattern = `%${query}%`;
    const searchCondition = or(
      like(assets.code, pattern),
      like(assets.description, pattern),
      like(assets.location, pattern),
      like(assets.custodian, pattern),
    );
    if (searchCondition) conditions.push(searchCondition);
  }
  if (filters.category)
    conditions.push(eq(assets.category, filters.category as Asset["category"]));
  if (filters.status)
    conditions.push(eq(assets.status, filters.status as Asset["status"]));
  if (filters.location)
    conditions.push(like(assets.location, `%${filters.location.trim()}%`));

  return db
    .select()
    .from(assets)
    .where(and(...conditions))
    .orderBy(desc(assets.updatedAt))
    .all();
}

export async function getAsset(id: string) {
  return db.select().from(assets).where(eq(assets.id, id)).get();
}

export async function getAssetStats() {
  const records = db
    .select({ status: assets.status, active: assets.active })
    .from(assets)
    .all();
  return {
    active: records.filter((asset) => asset.active).length,
    available: records.filter(
      (asset) => asset.active && asset.status === "available",
    ).length,
    maintenance: records.filter(
      (asset) => asset.active && asset.status === "maintenance",
    ).length,
    archived: records.filter((asset) => !asset.active).length,
  };
}
