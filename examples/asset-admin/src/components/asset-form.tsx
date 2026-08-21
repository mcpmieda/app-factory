"use client";

import { ArrowLeft, LoaderCircle, Save } from "lucide-react";
import Link from "next/link";
import { useActionState } from "react";

import type { AssetFormState } from "@/app/admin/assets/actions";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import type { Asset } from "@/db/schema";
import { categoryLabels, statusLabels } from "@/features/assets/asset-labels";

type AssetAction = (
  state: AssetFormState,
  formData: FormData,
) => Promise<AssetFormState>;

function FieldError({ errors }: { errors?: string[] }) {
  return errors?.length ? (
    <p className="text-sm text-destructive">{errors[0]}</p>
  ) : null;
}

export function AssetForm({
  action,
  asset,
}: {
  action: AssetAction;
  asset?: Asset;
}) {
  const [state, formAction, pending] = useActionState(action, {});

  return (
    <form action={formAction} className="space-y-7">
      {state.message ? (
        <div
          className="rounded-lg border border-destructive/30 bg-destructive/5 px-4 py-3 text-sm text-destructive"
          role="alert"
        >
          {state.message}
        </div>
      ) : null}
      <div className="grid gap-5 sm:grid-cols-2">
        <div className="space-y-2">
          <Label htmlFor="code">Código patrimonial</Label>
          <Input
            aria-invalid={Boolean(state.errors?.code)}
            defaultValue={asset?.code}
            id="code"
            name="code"
            placeholder="PAT-001"
            required
          />
          <FieldError errors={state.errors?.code} />
        </div>
        <div className="space-y-2">
          <Label htmlFor="category">Categoria</Label>
          <select
            className="h-9 w-full rounded-lg border bg-transparent px-3 text-sm outline-none focus-visible:ring-3 focus-visible:ring-ring/50"
            defaultValue={asset?.category ?? "technology"}
            id="category"
            name="category"
            required
          >
            {Object.entries(categoryLabels).map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
          <FieldError errors={state.errors?.category} />
        </div>
      </div>
      <div className="space-y-2">
        <Label htmlFor="description">Descrição</Label>
        <Input
          aria-invalid={Boolean(state.errors?.description)}
          defaultValue={asset?.description}
          id="description"
          name="description"
          placeholder="Ex.: Notebook para laboratório"
          required
        />
        <FieldError errors={state.errors?.description} />
      </div>
      <div className="grid gap-5 sm:grid-cols-2">
        <div className="space-y-2">
          <Label htmlFor="location">Localização / setor</Label>
          <Input
            aria-invalid={Boolean(state.errors?.location)}
            defaultValue={asset?.location}
            id="location"
            name="location"
            placeholder="Laboratório 1"
            required
          />
          <FieldError errors={state.errors?.location} />
        </div>
        <div className="space-y-2">
          <Label htmlFor="custodian">Responsável (opcional)</Label>
          <Input
            defaultValue={asset?.custodian ?? ""}
            id="custodian"
            name="custodian"
            placeholder="Equipe ou pessoa fictícia"
          />
          <FieldError errors={state.errors?.custodian} />
        </div>
      </div>
      <div className="space-y-2">
        <Label htmlFor="status">Situação</Label>
        <select
          className="h-9 w-full rounded-lg border bg-transparent px-3 text-sm outline-none focus-visible:ring-3 focus-visible:ring-ring/50"
          defaultValue={asset?.status ?? "available"}
          id="status"
          name="status"
          required
        >
          {Object.entries(statusLabels).map(([value, label]) => (
            <option key={value} value={value}>
              {label}
            </option>
          ))}
        </select>
        <FieldError errors={state.errors?.status} />
      </div>
      <div className="space-y-2">
        <Label htmlFor="notes">Observações</Label>
        <Textarea
          defaultValue={asset?.notes ?? ""}
          id="notes"
          name="notes"
          placeholder="Informações adicionais fictícias"
          rows={4}
        />
        <FieldError errors={state.errors?.notes} />
      </div>
      <div className="flex flex-col-reverse gap-3 border-t pt-6 sm:flex-row sm:justify-between">
        <Button asChild type="button" variant="outline">
          <Link href="/admin">
            <ArrowLeft aria-hidden="true" />
            Voltar
          </Link>
        </Button>
        <Button disabled={pending} type="submit">
          {pending ? (
            <LoaderCircle aria-hidden="true" className="animate-spin" />
          ) : (
            <Save aria-hidden="true" />
          )}
          {pending ? "Salvando…" : "Salvar patrimônio"}
        </Button>
      </div>
    </form>
  );
}
