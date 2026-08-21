"use client"

import { AlertTriangle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export default function AdminError({ reset }: { reset: () => void }) {
  return (
    <main className="grid min-h-[70vh] place-items-center p-4">
      <Card className="max-w-md">
        <CardHeader>
          <AlertTriangle className="text-destructive mb-2" />
          <CardTitle>Não foi possível carregar o painel</CardTitle>
          <CardDescription>
            O erro foi contido. Tente novamente; seus dados não foram alterados.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button onClick={reset}>Tentar novamente</Button>
        </CardContent>
      </Card>
    </main>
  )
}
