import { and, asc, eq, like, or, sql } from "drizzle-orm"
import { db } from "@/db/client"
import { items } from "@/db/schema"
import type { ItemInput } from "@/lib/item-validation"

export type ItemFilters = {
  query?: string
  status?: string
  activity?: "active" | "inactive" | "all"
}

export async function listItems(filters: ItemFilters = {}) {
  const clauses = []
  const query = filters.query?.trim()
  if (query) {
    const pattern = `%${query}%`
    clauses.push(
      or(like(items.name, pattern), like(items.category, pattern), like(items.location, pattern)),
    )
  }
  if (filters.status && filters.status !== "all") {
    clauses.push(eq(items.status, filters.status as (typeof items.status.enumValues)[number]))
  }
  if (filters.activity !== "all") {
    clauses.push(eq(items.active, filters.activity !== "inactive"))
  }

  return db
    .select()
    .from(items)
    .where(clauses.length ? and(...clauses) : undefined)
    .orderBy(asc(items.name))
}

export async function getItem(id: string) {
  return db.query.items.findFirst({ where: eq(items.id, id) })
}

export async function getItemMetrics() {
  const rows = await db
    .select({
      total: sql<number>`count(*)`,
      active: sql<number>`sum(case when ${items.active} = 1 then 1 else 0 end)`,
      maintenance: sql<number>`sum(case when ${items.status} = 'maintenance' and ${items.active} = 1 then 1 else 0 end)`,
    })
    .from(items)
  return rows[0] ?? { total: 0, active: 0, maintenance: 0 }
}

export function createItem(input: ItemInput) {
  const now = new Date()
  return db.insert(items).values({
    id: crypto.randomUUID(),
    ...input,
    createdAt: now,
    updatedAt: now,
  })
}

export function updateItem(id: string, input: ItemInput) {
  return db
    .update(items)
    .set({ ...input, updatedAt: new Date() })
    .where(eq(items.id, id))
}

export function setItemActive(id: string, active: boolean) {
  return db.update(items).set({ active, updatedAt: new Date() }).where(eq(items.id, id))
}

export function permanentlyDeleteItem(id: string) {
  return db.delete(items).where(and(eq(items.id, id), eq(items.active, false)))
}
