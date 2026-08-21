import { Card } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"

export default function AdminLoading() {
  return (
    <main className="mx-auto w-full max-w-7xl space-y-6 p-4 py-8 sm:p-8" aria-busy="true">
      <Skeleton className="h-10 w-72" />
      <div className="grid gap-4 sm:grid-cols-3">
        {[1, 2, 3].map((key) => (
          <Card key={key} className="p-6">
            <Skeleton className="h-16 w-full" />
          </Card>
        ))}
      </div>
      <Card className="space-y-4 p-6">
        <Skeleton className="h-9 w-full" />
        <Skeleton className="h-64 w-full" />
      </Card>
    </main>
  )
}
