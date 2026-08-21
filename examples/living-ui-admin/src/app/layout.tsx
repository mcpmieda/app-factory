import type { Metadata } from "next";
import { Geist } from "next/font/google";
import type { ReactNode } from "react";

import { projectConfig } from "@/config/project";
import { cn } from "@/lib/utils";
import "./globals.css";

const geist = Geist({ subsets: ["latin"], variable: "--font-geist-sans" });

export const metadata: Metadata = {
  title: projectConfig.name,
  description: projectConfig.description,
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html className={cn("font-sans", geist.variable)} lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
