import { describe, expect, it } from "vitest";
import { bookingSchema } from "./booking";
describe("booking validation", () => {
  it("accepts a complete future booking", () => {
    expect(
      bookingSchema.safeParse({
        name: "Ana Lima",
        email: "ana@example.test",
        date: "2026-08-25",
        period: "Manhã",
      }).success,
    ).toBe(true);
  });
  it("rejects invalid identity and past date", () => {
    const result = bookingSchema.safeParse({
      name: "A",
      email: "nope",
      date: "2026-08-20",
      period: "Tarde",
    });
    expect(result.success).toBe(false);
    if (!result.success) expect(result.error.issues).toHaveLength(3);
  });
});
