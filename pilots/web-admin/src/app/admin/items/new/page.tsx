import { createItemAction } from "@/app/admin/items/actions"
import { ItemForm } from "@/components/item-form"
import { Card, CardContent, CardDescription, CardHeader } from "@/components/ui/card"

export default function NewItemPage() {
  return (
    <main className="mx-auto w-full max-w-3xl p-4 py-8 sm:p-8">
      <Card>
        <CardHeader>
          <h1 className="font-heading text-xl font-medium">Novo registro</h1>
          <CardDescription>Cadastre um recurso para disponibilizá-lo no painel.</CardDescription>
        </CardHeader>
        <CardContent>
          <ItemForm action={createItemAction} />
        </CardContent>
      </Card>
    </main>
  )
}
