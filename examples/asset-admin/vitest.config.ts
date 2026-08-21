import { fileURLToPath } from "node:url";

import { defineConfig } from "vitest/config";

export default defineConfig({
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  test: {
    coverage: {
      provider: "v8",
      reporter: ["text", "json-summary"],
      include: ["src/config/project.ts", "src/features/assets/asset-schema.ts"],
    },
    exclude: ["tests/e2e/**", "node_modules/**", ".next/**"],
  },
});
