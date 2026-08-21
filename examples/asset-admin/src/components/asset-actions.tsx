"use client";

import { Archive, ArchiveRestore, LoaderCircle, Pencil } from "lucide-react";
import Link from "next/link";
import { useTransition } from "react";

import {
  archiveAssetAction,
  reactivateAssetAction,
} from "@/app/admin/assets/actions";
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
} from "@/components/ui/alert-dialog";
import { Button } from "@/components/ui/button";

export function AssetActions({
  active,
  assetId,
  code,
}: {
  active: boolean;
  assetId: string;
  code: string;
}) {
  const [pending, startTransition] = useTransition();

  if (!active) {
    return (
      <Button
        aria-label={`Reativar ${code}`}
        disabled={pending}
        onClick={() => startTransition(() => reactivateAssetAction(assetId))}
        size="sm"
        variant="outline"
      >
        {pending ? (
          <LoaderCircle className="animate-spin" />
        ) : (
          <ArchiveRestore />
        )}
        Reativar
      </Button>
    );
  }

  return (
    <div className="flex flex-wrap gap-2">
      <Button asChild size="sm" variant="outline">
        <Link
          aria-label={`Editar ${code}`}
          href={`/admin/assets/${assetId}/edit`}
        >
          <Pencil />
          Editar
        </Link>
      </Button>
      <AlertDialog>
        <AlertDialogTrigger asChild>
          <Button
            aria-label={`Arquivar ${code}`}
            disabled={pending}
            size="sm"
            variant="outline"
          >
            <Archive />
            Arquivar
          </Button>
        </AlertDialogTrigger>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Arquivar este patrimônio?</AlertDialogTitle>
            <AlertDialogDescription>
              O registro {code} sairá da lista ativa, mas poderá ser reativado
              sem perda de histórico.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancelar</AlertDialogCancel>
            <AlertDialogAction
              onClick={() => startTransition(() => archiveAssetAction(assetId))}
            >
              Confirmar arquivamento
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}
