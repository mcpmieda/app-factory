"use server"

import { revalidatePath } from "next/cache"
import { redirect } from "next/navigation"
import { parseItemForm } from "@/lib/item-validation"
import { createItem, getItem, permanentlyDeleteItem, setItemActive, updateItem } from "@/lib/items"
import { requireSession } from "@/lib/session"

export type ItemFormState = {
  message?: string
  errors?: Record<string, string[]>
}

function invalidState(result: ReturnType<typeof parseItemForm>): ItemFormState {
  if (result.success) return {}
  return {
    message: "Revise os campos destacados.",
    errors: result.error.flatten().fieldErrors,
  }
}

export async function createItemAction(
  _previous: ItemFormState,
  formData: FormData,
): Promise<ItemFormState> {
  await requireSession()
  const result = parseItemForm(formData)
  if (!result.success) return invalidState(result)
  await createItem(result.data)
  revalidatePath("/admin")
  redirect("/admin?notice=created")
}

export async function updateItemAction(
  id: string,
  _previous: ItemFormState,
  formData: FormData,
): Promise<ItemFormState> {
  await requireSession()
  const result = parseItemForm(formData)
  if (!result.success) return invalidState(result)
  const existing = await getItem(id)
  if (!existing) return { message: "O registro não existe mais." }
  await updateItem(id, result.data)
  revalidatePath("/admin")
  redirect("/admin?notice=updated")
}

export async function toggleItemAction(id: string, active: boolean) {
  await requireSession()
  const existing = await getItem(id)
  if (!existing) return
  await setItemActive(id, active)
  revalidatePath("/admin")
}

export async function deleteItemAction(id: string) {
  await requireSession()
  const existing = await getItem(id)
  if (!existing || existing.active) return
  await permanentlyDeleteItem(id)
  revalidatePath("/admin")
}
