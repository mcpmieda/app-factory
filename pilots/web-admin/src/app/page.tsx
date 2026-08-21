import { redirect } from "next/navigation"
import { getCurrentSession } from "@/lib/session"

export default async function HomePage() {
  const session = await getCurrentSession()
  redirect(session ? "/admin" : "/login")
}
