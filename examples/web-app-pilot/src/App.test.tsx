import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";
import App from "./App";
describe("booking journey", () => {
  it("shows and recovers from empty search", async () => {
    const user = userEvent.setup();
    render(<App />);
    await user.type(screen.getByLabelText("Buscar espaço"), "inexistente");
    expect(
      screen.getByRole("heading", { name: "Nenhum espaço encontrado" }),
    ).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "Limpar busca" }));
    expect(
      screen.getByRole("heading", { name: "Sala Aurora" }),
    ).toBeInTheDocument();
  });
  it("validates contact fields", async () => {
    const user = userEvent.setup();
    render(<App />);
    await user.click(
      screen.getAllByRole("button", { name: /Ver horários/ })[0],
    );
    await user.click(screen.getByRole("button", { name: "Continuar" }));
    await user.click(screen.getByRole("button", { name: "Confirmar reserva" }));
    expect(screen.getByText("Informe seu nome.")).toBeInTheDocument();
    expect(screen.getByText("Informe um e-mail válido.")).toBeInTheDocument();
  });
});
