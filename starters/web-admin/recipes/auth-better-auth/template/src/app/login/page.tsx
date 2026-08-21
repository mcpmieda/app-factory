import { Boxes } from "lucide-react";
import { redirect } from "next/navigation";

import { LoginForm } from "@/components/auth/login-form";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
} from "@/components/ui/card";
import { projectConfig } from "@/config/project";
import { getCurrentSession } from "@/lib/session";

export default async function LoginPage() {
  if (await getCurrentSession()) redirect("/");

  return (
    <main className="grid min-h-screen place-items-center bg-muted/40 px-4 py-10">
      <div className="w-full max-w-md space-y-6">
        <div className="flex items-center justify-center gap-3 text-sm font-semibold">
          <span className="grid size-10 place-items-center rounded-xl bg-primary text-primary-foreground">
            <Boxes aria-hidden="true" />
          </span>
          {projectConfig.name}
        </div>
        <Card>
          <CardHeader>
            <h1 className="text-2xl font-semibold tracking-tight">
              Acesse o painel
            </h1>
            <CardDescription>
              Use a conta criada pelo setup local.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <LoginForm />
          </CardContent>
        </Card>
      </div>
    </main>
  );
}
