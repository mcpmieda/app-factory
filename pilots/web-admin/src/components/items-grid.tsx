"use client"

import { type ColumnDef, useTable } from "@tanstack/react-table"
import { ItemActions } from "@/components/item-actions"
import type { DataGridFeatures } from "@/components/reui/data-grid/data-grid"
import {
  DataGrid,
  DataGridContainer,
  dataGridFeatures,
} from "@/components/reui/data-grid/data-grid"
import { DataGridPagination } from "@/components/reui/data-grid/data-grid-pagination"
import { DataGridTable } from "@/components/reui/data-grid/data-grid-table"
import { Badge } from "@/components/ui/badge"

export type ItemRow = {
  id: string
  name: string
  category: string
  status: "available" | "maintenance" | "allocated"
  location: string
  notes: string | null
  active: boolean
  updatedAt: string
}

const labels = { available: "Disponível", maintenance: "Manutenção", allocated: "Alocado" }
const columns: ColumnDef<DataGridFeatures, ItemRow>[] = [
  {
    accessorKey: "name",
    header: "Nome",
    cell: ({ row }) => (
      <div>
        <p className="font-medium">{row.original.name}</p>
        <p className="text-muted-foreground max-w-64 truncate text-xs">
          {row.original.notes || "Sem observações"}
        </p>
      </div>
    ),
    meta: { autoSize: true },
  },
  {
    accessorKey: "category",
    header: "Categoria",
    meta: { headerClassName: "hidden md:table-cell", cellClassName: "hidden md:table-cell" },
  },
  {
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => (
      <Badge variant={row.original.status === "maintenance" ? "secondary" : "outline"}>
        {labels[row.original.status]}
      </Badge>
    ),
  },
  {
    accessorKey: "location",
    header: "Localização",
    meta: { headerClassName: "hidden lg:table-cell", cellClassName: "hidden lg:table-cell" },
  },
  {
    accessorKey: "updatedAt",
    header: "Atualizado",
    meta: { headerClassName: "hidden xl:table-cell", cellClassName: "hidden xl:table-cell" },
  },
  {
    id: "actions",
    header: "",
    cell: ({ row }) => (
      <ItemActions id={row.original.id} active={row.original.active} name={row.original.name} />
    ),
    size: 90,
  },
]

export function ItemsGrid({ data }: { data: ItemRow[] }) {
  const table = useTable({
    features: dataGridFeatures,
    columns,
    data,
    initialState: { pagination: { pageIndex: 0, pageSize: 10 } },
  })
  return (
    <DataGrid
      table={table}
      recordCount={data.length}
      emptyMessage="Nenhum registro corresponde aos filtros."
      tableLayout={{ headerBackground: true, rowBorder: true }}
    >
      <DataGridContainer className="rounded-lg border">
        <DataGridTable />
      </DataGridContainer>
      {data.length > 0 ? (
        <DataGridPagination
          sizes={[5, 10, 25]}
          rowsPerPageLabel="Linhas"
          info="{from}–{to} de {count}"
        />
      ) : null}
    </DataGrid>
  )
}
