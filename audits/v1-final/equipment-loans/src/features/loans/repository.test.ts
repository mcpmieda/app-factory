import Database from "better-sqlite3";
import { afterEach, beforeEach, describe, expect, it } from "vitest";

import { localIsoDate, LoanRuleError } from "./domain";
import { createLoan, listEquipment, returnLoan } from "./repository";

let database: Database.Database;

beforeEach(() => {
  database = new Database(":memory:");
  database.exec(`
    PRAGMA foreign_keys = ON;
    CREATE TABLE equipment (
      id text PRIMARY KEY,
      asset_tag text NOT NULL UNIQUE,
      name text NOT NULL,
      category text NOT NULL,
      created_at integer NOT NULL DEFAULT 0
    );
    CREATE TABLE loans (
      id text PRIMARY KEY,
      equipment_id text NOT NULL REFERENCES equipment(id) ON DELETE RESTRICT,
      responsible_name text NOT NULL,
      due_date text NOT NULL,
      loaned_at integer NOT NULL DEFAULT 0,
      returned_at integer
    );
    CREATE UNIQUE INDEX one_active_loan_per_equipment
      ON loans (equipment_id) WHERE returned_at IS NULL;
    INSERT INTO equipment (id, asset_tag, name, category, created_at)
      VALUES ('item-1', 'TEST-001', 'Projetor de teste', 'Audiovisual', 0);
  `);
});

afterEach(() => database.close());

describe("loan persistence", () => {
  it("persists a loan and makes the item available after return", () => {
    const id = createLoan(
      {
        equipmentId: "item-1",
        responsibleName: "Pessoa Fictícia",
        dueDate: localIsoDate(),
      },
      "loan-1",
      database,
    );

    expect(id).toBe("loan-1");
    expect(listEquipment(database)[0]).toMatchObject({
      responsibleName: "Pessoa Fictícia",
      status: "loaned",
    });

    returnLoan("loan-1", database);
    expect(listEquipment(database)[0]).toMatchObject({
      responsibleName: null,
      status: "available",
    });
  });

  it("blocks a second active loan for the same item", () => {
    const input = {
      equipmentId: "item-1",
      responsibleName: "Pessoa Fictícia",
      dueDate: localIsoDate(),
    };
    createLoan(input, "loan-1", database);
    expect(() => createLoan(input, "loan-2", database)).toThrowError(
      new LoanRuleError(
        "Este equipamento já está emprestado.",
        "ALREADY_LOANED",
      ),
    );
    expect(
      database.prepare("SELECT count(*) AS count FROM loans").get(),
    ).toEqual({ count: 1 });
  });
});
