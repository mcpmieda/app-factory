import { notFound } from "next/navigation"
import { updateItemAction } from "@/app/admin/items/actions"
import { ItemForm } from "@/components/item-form"
import { Card, CardContent, CardDescription, CardHeader } from "@/components/ui/card"
import { getItem } from "@/lib/items"

export default async function EditItemPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const item = await getItem(id)
  if (!item) notFound()
  const action = updateItemAction.bind(null, id)
  return (
    <main className="mx-auto w-full max-w-3xl p-4 py-8 sm:p-8">
      <Card>
        <CardHeader>
          <h1 className="font-heading text-xl font-medium">Editar registro</h1>
          <CardDescription>
            Atualize os dados e preserve o histórico de modificação.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ItemForm action={action} item={item} />
        </CardContent>
      </Card>
    </main>
  )
}
