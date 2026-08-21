"use client"

import { MoreHorizontal, Pencil, Power, RotateCcw, Trash2 } from "lucide-react"
import Link from "next/link"
import { useState, useTransition } from "react"
import { deleteItemAction, toggleItemAction } from "@/app/admin/items/actions"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog"
import { Button } from "@/components/ui/button"

export function ItemActions({ id, active, name }: { id: string; active: boolean; name: string }) {
  const [open, setOpen] = useState(false)
  const [pending, startTransition] = useTransition()
  const destructive = !active
  const run = () =>
    startTransition(async () => {
      if (destructive) await deleteItemAction(id)
      else await toggleItemAction(id, false)
      setOpen(false)
    })

  return (
    <div className="flex justify-end gap-1">
      <Button asChild variant="ghost" size="icon-sm">
        <Link href={`/admin/items/${id}/edit`} aria-label={`Editar ${name}`}>
          <Pencil />
        </Link>
      </Button>
      {!active ? (
        <Button
          variant="ghost"
          size="icon-sm"
          aria-label={`Reativar ${name}`}
          onClick={() => startTransition(() => toggleItemAction(id, true))}
        >
          <RotateCcw />
        </Button>
      ) : null}
      <AlertDialog open={open} onOpenChange={setOpen}>
        <AlertDialogTrigger asChild>
          <Button
            variant="ghost"
            size="icon-sm"
            aria-label={active ? `Desativar ${name}` : `Excluir ${name}`}
          >
            <MoreHorizontal />
          </Button>
        </AlertDialogTrigger>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>
              {destructive ? "Excluir permanentemente?" : "Desativar este registro?"}
            </AlertDialogTitle>
            <AlertDialogDescription>
              {destructive
                ? `“${name}” será removido. Essa ação não pode ser desfeita.`
                : `“${name}” deixará as listas ativas, mas poderá ser reativado depois.`}
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancelar</AlertDialogCancel>
            <AlertDialogAction
              variant={destructive ? "destructive" : "default"}
              disabled={pending}
              onClick={run}
            >
              {destructive ? <Trash2 /> : <Power />}
              {pending ? "Processando…" : destructive ? "Excluir" : "Desativar"}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}
