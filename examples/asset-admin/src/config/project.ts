import { z } from "zod";

const projectConfigSchema = z.object({
  name: z.string().min(2),
  description: z.string().min(10),
  profile: z.literal("web-admin"),
  factoryBaseline: z.string().min(1),
});

export const projectConfig = projectConfigSchema.parse({
  name: "Patrimônio Escolar",
  description:
    "Inventário escolar fictício criado para validar o starter web-admin reutilizável.",
  profile: "web-admin",
  factoryBaseline: "v0.5",
});
