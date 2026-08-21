import { config } from "dotenv";
import { eq } from "drizzle-orm";

async function main() {
  config({ path: ".env.local" });
  const { user } = await import("../src/db/auth-schema");
  const { db } = await import("../src/db/client");
  const { assets } = await import("../src/db/schema");
  const { createAuth } = await import("../src/lib/auth");

  const email = process.env.SEED_ADMIN_EMAIL ?? "admin@example.com";
  const existingAdmin = db
    .select({ id: user.id })
    .from(user)
    .where(eq(user.email, email))
    .get();

  if (!existingAdmin) {
    const auth = createAuth({ allowSignUp: true });
    await auth.api.signUpEmail({
      body: {
        name: process.env.SEED_ADMIN_NAME ?? "Gestora de Exemplo",
        email,
        password: process.env.SEED_ADMIN_PASSWORD ?? "local-admin-password",
      },
    });
    console.log("Fictitious local administrator created.");
  } else {
    console.log("Local administrator already exists.");
  }

  db.insert(assets)
    .values([
      {
        id: "asset-example-001",
        code: "PAT-001",
        description: "Notebook do laboratório",
        category: "technology",
        location: "Laboratório de informática",
        custodian: "Equipe de tecnologia",
        status: "in-use",
        notes: "Registro totalmente fictício.",
      },
      {
        id: "asset-example-002",
        code: "PAT-002",
        description: "Projetor multimídia",
        category: "equipment",
        location: "Sala de recursos",
        custodian: "Coordenação pedagógica",
        status: "maintenance",
      },
      {
        id: "asset-example-003",
        code: "PAT-003",
        description: "Armário de aço",
        category: "furniture",
        location: "Secretaria fictícia",
        status: "available",
      },
    ])
    .onConflictDoNothing({ target: assets.code })
    .run();
  console.log("Fictitious asset seed completed without duplicates.");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
