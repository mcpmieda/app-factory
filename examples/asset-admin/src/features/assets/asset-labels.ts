import type { Asset } from "@/db/schema";

export const categoryLabels: Record<Asset["category"], string> = {
  technology: "Tecnologia",
  furniture: "Mobiliário",
  equipment: "Equipamento",
  other: "Outro",
};

export const statusLabels: Record<Asset["status"], string> = {
  available: "Disponível",
  "in-use": "Em uso",
  maintenance: "Manutenção",
  retired: "Baixado",
};

export const statusStyles: Record<Asset["status"], string> = {
  available: "border-emerald-200 bg-emerald-50 text-emerald-800",
  "in-use": "border-blue-200 bg-blue-50 text-blue-800",
  maintenance: "border-amber-200 bg-amber-50 text-amber-900",
  retired: "border-slate-200 bg-slate-100 text-slate-700",
};
