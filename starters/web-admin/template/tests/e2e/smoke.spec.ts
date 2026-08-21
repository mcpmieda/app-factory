import { expect, test } from "@playwright/test";

test("renders the clean web-admin foundation without console errors", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("console", (message) => {
    if (message.type() === "error") errors.push(message.text());
  });

  await page.goto("/");

  await expect(
    page.getByRole("heading", {
      name: "Comece pelo domínio, não pela infraestrutura.",
    }),
  ).toBeVisible();
  await expect(page.getByText("Starter limpo e componível")).toBeVisible();
  expect(errors).toEqual([]);
});
