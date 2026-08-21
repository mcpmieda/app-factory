import { MapPin, PackageOpen, UserRound } from "lucide-react";

import { AssetActions } from "@/components/asset-actions";
import { Badge } from "@/components/ui/badge";
import type { Asset } from "@/db/schema";
import {
  categoryLabels,
  statusLabels,
  statusStyles,
} from "@/features/assets/asset-labels";
import { cn } from "@/lib/utils";

export function AssetList({ records }: { records: Asset[] }) {
  if (records.length === 0) {
    return (
      <div className="grid min-h-64 place-items-center rounded-xl border border-dashed bg-background px-6 text-center">
        <div className="space-y-2">
          <PackageOpen
            aria-hidden="true"
            className="mx-auto size-8 text-muted-foreground"
          />
          <h2 className="font-semibold">Nenhum patrimônio encontrado</h2>
          <p className="max-w-md text-sm text-muted-foreground">
            Ajuste os filtros ou cadastre o primeiro item deste recorte
            fictício.
          </p>
        </div>
      </div>
    );
  }

  return (
    <>
      <div className="hidden overflow-hidden rounded-xl border bg-background md:block">
        <table className="w-full text-sm">
          <thead className="border-b bg-muted/55 text-left text-xs uppercase tracking-wide text-muted-foreground">
            <tr>
              <th className="px-4 py-3">Patrimônio</th>
              <th className="px-4 py-3">Localização</th>
              <th className="px-4 py-3">Situação</th>
              <th className="px-4 py-3 text-right">Ações</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {records.map((asset) => (
              <tr key={asset.id}>
                <td className="px-4 py-4">
                  <p className="font-semibold">{asset.code}</p>
                  <p className="mt-1 text-muted-foreground">
                    {asset.description} · {categoryLabels[asset.category]}
                  </p>
                </td>
                <td className="px-4 py-4">
                  <p>{asset.location}</p>
                  <p className="mt-1 text-muted-foreground">
                    {asset.custodian ?? "Sem responsável"}
                  </p>
                </td>
                <td className="px-4 py-4">
                  <Badge
                    className={cn("font-medium", statusStyles[asset.status])}
                    variant="outline"
                  >
                    {statusLabels[asset.status]}
                  </Badge>
                </td>
                <td className="px-4 py-4">
                  <div className="flex justify-end">
                    <AssetActions
                      active={asset.active}
                      assetId={asset.id}
                      code={asset.code}
                    />
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="grid gap-3 md:hidden">
        {records.map((asset) => (
          <article
            className="space-y-4 rounded-xl border bg-background p-4"
            key={asset.id}
          >
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="font-semibold">{asset.code}</p>
                <p className="mt-1 text-sm text-muted-foreground">
                  {asset.description}
                </p>
              </div>
              <Badge
                className={cn("shrink-0", statusStyles[asset.status])}
                variant="outline"
              >
                {statusLabels[asset.status]}
              </Badge>
            </div>
            <div className="grid gap-2 text-sm text-muted-foreground">
              <p className="flex items-center gap-2">
                <MapPin className="size-4" />
                {asset.location}
              </p>
              <p className="flex items-center gap-2">
                <UserRound className="size-4" />
                {asset.custodian ?? "Sem responsável"}
              </p>
            </div>
            <AssetActions
              active={asset.active}
              assetId={asset.id}
              code={asset.code}
            />
          </article>
        ))}
      </div>
    </>
  );
}
