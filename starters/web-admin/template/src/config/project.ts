import { z } from "zod";

const projectConfigSchema = z.object({
  name: z.string().min(2),
  description: z.string().min(10),
  profile: z.literal("web-admin"),
  factoryBaseline: z.string().min(1),
});

export const projectConfig = projectConfigSchema.parse({
  name: "Web Admin Starter",
  description:
    "Uma base administrativa enxuta para implementar a primeira fatia funcional.",
  profile: "web-admin",
  factoryBaseline: "v1.3.0",
});
