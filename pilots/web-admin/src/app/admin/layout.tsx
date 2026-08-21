import { AdminShell } from "@/components/admin-shell"
import { requireSession } from "@/lib/session"

export default async function AdminLayout({ children }: { children: React.ReactNode }) {
  const session = await requireSession()
  return <AdminShell userName={session.user.name}>{children}</AdminShell>
}
