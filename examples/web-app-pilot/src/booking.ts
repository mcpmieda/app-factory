import { z } from "zod";
export const spaces = [
  {
    id: "aurora",
    name: "Sala Aurora",
    capacity: 8,
    feature: "TV + quadro",
    tone: "mint",
  },
  {
    id: "atelier",
    name: "Ateliê Norte",
    capacity: 12,
    feature: "Bancadas móveis",
    tone: "peach",
  },
  {
    id: "studio",
    name: "Estúdio Som",
    capacity: 4,
    feature: "Tratamento acústico",
    tone: "lilac",
  },
] as const;
export type Space = (typeof spaces)[number];
export const bookingSchema = z.object({
  name: z.string().trim().min(2, "Informe seu nome."),
  email: z.email("Informe um e-mail válido."),
  date: z
    .string()
    .refine((date) => date >= "2026-08-22", "Escolha uma data futura."),
  period: z.enum(["Manhã", "Tarde"]),
});
export type Booking = z.infer<typeof bookingSchema>;
