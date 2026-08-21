import { describe, expect, it } from "vitest";

import {
  classifyEquipmentStatus,
  LoanRuleError,
  validateDueDate,
} from "./domain";

describe("loan domain", () => {
  it("classifies available, active and overdue equipment", () => {
    expect(classifyEquipmentStatus(null, "2026-08-21")).toBe("available");
    expect(classifyEquipmentStatus("2026-08-21", "2026-08-21")).toBe("loaned");
    expect(classifyEquipmentStatus("2026-08-20", "2026-08-21")).toBe("overdue");
  });

  it("rejects a due date in the past", () => {
    expect(() => validateDueDate("2026-08-20", "2026-08-21")).toThrowError(
      LoanRuleError,
    );
  });
});
