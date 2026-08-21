import { z } from "zod";

import { assetCategories, assetStatuses } from "@/db/schema";

const optionalText = z.preprocess(
  (value) =>
    typeof value === "string" && value.trim() === "" ? undefined : value,
  z.string().trim().max(240).optional(),
);

export const assetFormSchema = z.object({
  code: z
    .string()
    .trim()
    .min(3, "Informe um código com pelo menos 3 caracteres.")
    .max(24, "Use no máximo 24 caracteres.")
    .regex(
      /^[A-Za-z0-9._/-]+$/,
      "Use apenas letras, números, ponto, barra, hífen ou sublinhado.",
    )
    .transform((value) => value.toUpperCase()),
  description: z.string().trim().min(3, "Descreva o patrimônio.").max(120),
  category: z.enum(assetCategories, {
    message: "Selecione uma categoria válida.",
  }),
  location: z.string().trim().min(2, "Informe a localização.").max(80),
  custodian: optionalText,
  status: z.enum(assetStatuses, { message: "Selecione uma situação válida." }),
  notes: optionalText,
});

export type AssetFormInput = z.infer<typeof assetFormSchema>;

export function parseAssetForm(formData: FormData) {
  return assetFormSchema.safeParse({
    code: formData.get("code"),
    description: formData.get("description"),
    category: formData.get("category"),
    location: formData.get("location"),
    custodian: formData.get("custodian"),
    status: formData.get("status"),
    notes: formData.get("notes"),
  });
}
