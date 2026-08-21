"use server";

import { randomUUID } from "node:crypto";

import { eq } from "drizzle-orm";
import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { db } from "@/db/client";
import { assets } from "@/db/schema";
import { parseAssetForm } from "@/features/assets/asset-schema";
import { requireSession } from "@/lib/session";

export type AssetFormState = {
  message?: string;
  errors?: Record<string, string[]>;
};

function validationState(
  result: ReturnType<typeof parseAssetForm>,
): AssetFormState | undefined {
  if (result.success) return undefined;
  return {
    message: "Revise os campos destacados.",
    errors: result.error.flatten().fieldErrors,
  };
}

async function codeBelongsToAnotherAsset(code: string, currentId?: string) {
  const existing = db
    .select({ id: assets.id })
    .from(assets)
    .where(eq(assets.code, code))
    .get();
  return Boolean(existing && existing.id !== currentId);
}

export async function createAssetAction(
  _state: AssetFormState,
  formData: FormData,
): Promise<AssetFormState> {
  await requireSession();
  const parsed = parseAssetForm(formData);
  const invalid = validationState(parsed);
  if (invalid || !parsed.success)
    return invalid ?? { message: "Dados inválidos." };
  if (await codeBelongsToAnotherAsset(parsed.data.code)) {
    return {
      message: "Já existe um patrimônio com este código.",
      errors: { code: ["Código já utilizado."] },
    };
  }

  db.insert(assets)
    .values({ id: randomUUID(), ...parsed.data })
    .run();
  revalidatePath("/admin");
  redirect("/admin?notice=created");
}

export async function updateAssetAction(
  id: string,
  _state: AssetFormState,
  formData: FormData,
): Promise<AssetFormState> {
  await requireSession();
  const parsed = parseAssetForm(formData);
  const invalid = validationState(parsed);
  if (invalid || !parsed.success)
    return invalid ?? { message: "Dados inválidos." };
  if (await codeBelongsToAnotherAsset(parsed.data.code, id)) {
    return {
      message: "Já existe um patrimônio com este código.",
      errors: { code: ["Código já utilizado."] },
    };
  }

  const updated = db
    .update(assets)
    .set(parsed.data)
    .where(eq(assets.id, id))
    .run();
  if (updated.changes === 0) return { message: "Patrimônio não encontrado." };
  revalidatePath("/admin");
  redirect("/admin?notice=updated");
}

export async function archiveAssetAction(id: string) {
  await requireSession();
  db.update(assets).set({ active: false }).where(eq(assets.id, id)).run();
  revalidatePath("/admin");
}

export async function reactivateAssetAction(id: string) {
  await requireSession();
  db.update(assets).set({ active: true }).where(eq(assets.id, id)).run();
  revalidatePath("/admin");
}
