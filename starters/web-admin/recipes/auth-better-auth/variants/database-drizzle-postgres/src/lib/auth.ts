import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";

import * as authSchema from "@/db/auth-schema";
import { db } from "@/db/client";
import { projectConfig } from "@/config/project";

export function createAuth(options: { allowSignUp?: boolean } = {}) {
  const baseURL = process.env.BETTER_AUTH_URL ?? "http://localhost:3000";

  return betterAuth({
    appName: projectConfig.name,
    baseURL,
    secret: process.env.BETTER_AUTH_SECRET,
    trustedOrigins: [baseURL, "http://127.0.0.1:3000"],
    database: drizzleAdapter(db, { provider: "pg", schema: authSchema }),
    emailAndPassword: {
      enabled: true,
      disableSignUp: !options.allowSignUp,
      minPasswordLength: 8,
    },
    session: { cookieCache: { enabled: true, maxAge: 5 * 60 } },
  });
}

export const auth = createAuth();
