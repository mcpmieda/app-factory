import { defineConfig } from "@playwright/test";
export default defineConfig({
  testDir: "./tests/e2e",
  workers: 1,
  webServer: {
    command: "node tests/fixture-server.mjs",
    port: 4174,
    reuseExistingServer: !process.env.CI,
  },
});
