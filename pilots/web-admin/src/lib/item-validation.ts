import { z } from "zod"
import { itemStatuses } from "@/db/schema"

const optionalNotes = z.preprocess(
  (value) => (typeof value === "string" && value.trim() === "" ? null : value),
  z.string().trim().max(500, "Use no máximo 500 caracteres.").nullable(),
)

export const itemInputSchema = z.object({
  name: z.string().trim().min(2, "Informe um nome com pelo menos 2 caracteres.").max(100),
  category: z.string().trim().min(2, "Informe a categoria.").max(60),
  status: z.enum(itemStatuses, { error: "Escolha um status válido." }),
  location: z.string().trim().min(2, "Informe a localização.").max(100),
  notes: optionalNotes,
})

export type ItemInput = z.infer<typeof itemInputSchema>

export function parseItemForm(formData: FormData) {
  return itemInputSchema.safeParse({
    name: formData.get("name"),
    category: formData.get("category"),
    status: formData.get("status"),
    location: formData.get("location"),
    notes: formData.get("notes"),
  })
}
