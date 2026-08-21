"use client"

import { AlertCircle, LoaderCircle } from "lucide-react"
import Link from "next/link"
import { useActionState } from "react"
import type { ItemFormState } from "@/app/admin/items/actions"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import type { Item } from "@/db/schema"

type Action = (state: ItemFormState, data: FormData) => Promise<ItemFormState>

function FieldError({ errors }: { errors?: string[] }) {
  return errors?.[0] ? (
    <p className="text-destructive text-xs" role="alert">
      {errors[0]}
    </p>
  ) : null
}

export function ItemForm({ action, item }: { action: Action; item?: Item }) {
  const [state, formAction, pending] = useActionState(action, {})
  return (
    <form action={formAction} className="space-y-6" noValidate>
      {state.message ? (
        <Alert variant="destructive">
          <AlertCircle />
          <AlertTitle>Não foi possível salvar</AlertTitle>
          <AlertDescription>{state.message}</AlertDescription>
        </Alert>
      ) : null}
      <div className="grid gap-5 sm:grid-cols-2">
        <div className="space-y-2 sm:col-span-2">
          <Label htmlFor="name">Nome</Label>
          <Input
            id="name"
            name="name"
            defaultValue={item?.name}
            aria-invalid={Boolean(state.errors?.name)}
          />
          <FieldError errors={state.errors?.name} />
        </div>
        <div className="space-y-2">
          <Label htmlFor="category">Categoria</Label>
          <Input
            id="category"
            name="category"
            defaultValue={item?.category}
            aria-invalid={Boolean(state.errors?.category)}
          />
          <FieldError errors={state.errors?.category} />
        </div>
        <div className="space-y-2">
          <Label htmlFor="status">Status</Label>
          <select
            id="status"
            name="status"
            defaultValue={item?.status ?? "available"}
            className="border-input bg-background focus-visible:border-ring focus-visible:ring-ring/50 h-9 w-full rounded-md border px-3 text-sm outline-none focus-visible:ring-[3px]"
          >
            <option value="available">Disponível</option>
            <option value="allocated">Alocado</option>
            <option value="maintenance">Em manutenção</option>
          </select>
          <FieldError errors={state.errors?.status} />
        </div>
        <div className="space-y-2 sm:col-span-2">
          <Label htmlFor="location">Localização</Label>
          <Input
            id="location"
            name="location"
            defaultValue={item?.location}
            aria-invalid={Boolean(state.errors?.location)}
          />
          <FieldError errors={state.errors?.location} />
        </div>
        <div className="space-y-2 sm:col-span-2">
          <Label htmlFor="notes">
            Observações <span className="text-muted-foreground">(opcional)</span>
          </Label>
          <Textarea
            id="notes"
            name="notes"
            rows={5}
            defaultValue={item?.notes ?? ""}
            aria-invalid={Boolean(state.errors?.notes)}
          />
          <FieldError errors={state.errors?.notes} />
        </div>
      </div>
      <div className="flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
        <Button asChild variant="outline">
          <Link href="/admin">Cancelar</Link>
        </Button>
        <Button type="submit" disabled={pending}>
          {pending ? <LoaderCircle className="animate-spin" /> : null}
          {pending ? "Salvando…" : "Salvar registro"}
        </Button>
      </div>
    </form>
  )
}
