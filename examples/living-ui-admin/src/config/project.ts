import { z } from "zod";

const projectConfigSchema = z.object({
  name: z.string().min(2),
  description: z.string().min(10),
  profile: z.literal("web-admin"),
  factoryBaseline: z.string().min(1),
});

export const projectConfig = projectConfigSchema.parse({
  name: "Pulse Desk",
  description:
    "Uma central fictícia para acompanhar filas operacionais e revisar exceções.",
  profile: "web-admin",
  factoryBaseline: "v0.7",
});
