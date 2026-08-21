import { betterAuth } from "better-auth"
import { drizzleAdapter } from "better-auth/adapters/drizzle"
import { db } from "@/db/client"
import * as schema from "@/db/schema"

export function createAuth(options: { allowSignUp?: boolean } = {}) {
  return betterAuth({
    appName: "App Factory Web Admin",
    baseURL: process.env.BETTER_AUTH_URL ?? "http://localhost:3000",
    secret: process.env.BETTER_AUTH_SECRET,
    trustedOrigins: ["http://localhost:3000", "http://127.0.0.1:3000"],
    database: drizzleAdapter(db, {
      provider: "sqlite",
      schema,
    }),
    emailAndPassword: {
      enabled: true,
      disableSignUp: !options.allowSignUp,
      minPasswordLength: 8,
    },
    session: {
      cookieCache: {
        enabled: true,
        maxAge: 5 * 60,
      },
    },
  })
}

export const auth = createAuth()
