// @vitest-environment jsdom
import { beforeEach, describe, expect, it } from "vitest";
import { mount, toggleFocus } from "./content";
describe("Focus Lens", () => {
  beforeEach(() => {
    document.head.innerHTML = "";
    document.body.innerHTML =
      "<article data-focus-item>One</article><article data-focus-item>Two</article>";
  });
  it("toggles every controlled item reversibly", () => {
    expect(toggleFocus()).toEqual({ active: true, count: 2 });
    expect(document.querySelectorAll(".focus-lens-active")).toHaveLength(2);
    expect(toggleFocus().active).toBe(false);
    expect(document.querySelectorAll(".focus-lens-active")).toHaveLength(0);
  });
  it("mounts one accessible control", () => {
    mount();
    mount();
    expect(document.querySelectorAll("#focus-lens-pilot")).toHaveLength(1);
    expect(document.querySelector("button")?.getAttribute("aria-pressed")).toBe(
      "false",
    );
  });
});
