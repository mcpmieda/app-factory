import { config } from "dotenv"

async function main() {
  config({ path: ".env.local" })

  const email = process.env.SEED_ADMIN_EMAIL
  const password = process.env.SEED_ADMIN_PASSWORD
  const name = process.env.SEED_ADMIN_NAME ?? "Admin Pilot"

  if (!email || !password) {
    throw new Error("SEED_ADMIN_EMAIL and SEED_ADMIN_PASSWORD are required")
  }

  const { createAuth } = await import("../src/lib/auth")
  const { eq } = await import("drizzle-orm")
  const { db } = await import("../src/db/client")
  const { account, items, user } = await import("../src/db/schema")

  let existingUser = await db.query.user.findFirst({ where: eq(user.email, email) })
  if (existingUser) {
    const credential = await db.query.account.findFirst({
      where: eq(account.userId, existingUser.id),
    })
    if (!credential) {
      await db.delete(user).where(eq(user.id, existingUser.id))
      existingUser = undefined
    }
  }
  if (!existingUser) {
    await createAuth({ allowSignUp: true }).api.signUpEmail({ body: { email, password, name } })
    console.log(`Seeded local administrator: ${email}`)
  } else {
    console.log(`Local administrator already exists: ${email}`)
  }

  const existingItem = await db.query.items.findFirst()
  if (!existingItem) {
    const now = new Date()
    await db.insert(items).values([
      {
        id: crypto.randomUUID(),
        name: "Notebook de demonstração",
        category: "Equipamentos",
        status: "available",
        location: "Escritório central",
        notes: "Registro inicial para explorar o painel.",
        active: true,
        createdAt: now,
        updatedAt: now,
      },
      {
        id: crypto.randomUUID(),
        name: "Projetor da sala 2",
        category: "Audiovisual",
        status: "maintenance",
        location: "Filial norte",
        notes: "Troca da lâmpada programada.",
        active: true,
        createdAt: now,
        updatedAt: now,
      },
    ])
    console.log("Seeded demonstration resources.")
  }
}

main().catch((error) => {
  console.error(error)
  process.exit(1)
})
