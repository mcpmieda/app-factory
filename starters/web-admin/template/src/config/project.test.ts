import { describe, expect, it } from "vitest";

import { projectConfig } from "./project";

describe("projectConfig", () => {
  it("records the reusable Factory profile and baseline", () => {
    expect(projectConfig).toMatchObject({
      profile: "web-admin",
      factoryBaseline: "v1.1.0",
    });
    expect(projectConfig.name.length).toBeGreaterThan(1);
  });
});
