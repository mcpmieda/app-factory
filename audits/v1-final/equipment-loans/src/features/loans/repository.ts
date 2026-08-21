import type Database from "better-sqlite3";

import { sqlite } from "@/db/client";
import {
  classifyEquipmentStatus,
  LoanRuleError,
  type EquipmentStatus,
  type LoanInput,
  validateDueDate,
} from "./domain";

type EquipmentRow = {
  id: string;
  assetTag: string;
  name: string;
  category: string;
  loanId: string | null;
  responsibleName: string | null;
  dueDate: string | null;
  loanedAt: number | null;
};

export type EquipmentView = EquipmentRow & { status: EquipmentStatus };

export function listEquipment(database = sqlite): EquipmentView[] {
  const rows = database
    .prepare(
      `SELECT equipment.id,
              equipment.asset_tag AS assetTag,
              equipment.name,
              equipment.category,
              loans.id AS loanId,
              loans.responsible_name AS responsibleName,
              loans.due_date AS dueDate,
              loans.loaned_at AS loanedAt
       FROM equipment
       LEFT JOIN loans
         ON loans.equipment_id = equipment.id
        AND loans.returned_at IS NULL
       ORDER BY equipment.name`,
    )
    .all() as EquipmentRow[];

  return rows.map((row) => ({
    ...row,
    status: classifyEquipmentStatus(row.dueDate),
  }));
}

export function createLoan(
  input: LoanInput,
  id: string = crypto.randomUUID(),
  database: Database.Database = sqlite,
) {
  validateDueDate(input.dueDate);

  const transaction = database.transaction(() => {
    const item = database
      .prepare("SELECT id FROM equipment WHERE id = ?")
      .get(input.equipmentId);
    if (!item)
      throw new LoanRuleError("Equipamento não encontrado.", "NOT_FOUND");

    const activeLoan = database
      .prepare(
        "SELECT id FROM loans WHERE equipment_id = ? AND returned_at IS NULL",
      )
      .get(input.equipmentId);
    if (activeLoan) {
      throw new LoanRuleError(
        "Este equipamento já está emprestado.",
        "ALREADY_LOANED",
      );
    }

    database
      .prepare(
        `INSERT INTO loans (id, equipment_id, responsible_name, due_date)
         VALUES (?, ?, ?, ?)`,
      )
      .run(id, input.equipmentId, input.responsibleName.trim(), input.dueDate);
  });

  try {
    transaction();
  } catch (error) {
    if (
      error instanceof Error &&
      error.message.includes("UNIQUE constraint failed: loans.equipment_id")
    ) {
      throw new LoanRuleError(
        "Este equipamento já está emprestado.",
        "ALREADY_LOANED",
      );
    }
    throw error;
  }

  return id;
}

export function returnLoan(
  loanId: string,
  database: Database.Database = sqlite,
) {
  const result = database
    .prepare(
      `UPDATE loans
       SET returned_at = cast(unixepoch('subsecond') * 1000 as integer)
       WHERE id = ? AND returned_at IS NULL`,
    )
    .run(loanId);

  if (result.changes === 0) {
    const exists = database
      .prepare("SELECT id FROM loans WHERE id = ?")
      .get(loanId);
    throw new LoanRuleError(
      exists
        ? "Este empréstimo já foi devolvido."
        : "Empréstimo não encontrado.",
      exists ? "ALREADY_RETURNED" : "NOT_FOUND",
    );
  }
}

export function resetDemoData(database: Database.Database = sqlite) {
  database.transaction(() => {
    database.prepare("DELETE FROM loans").run();
    database
      .prepare(
        `INSERT INTO loans
          (id, equipment_id, responsible_name, due_date, loaned_at)
         VALUES
          ('loan-overdue-seed', 'eq-projector-01', 'Marina Lopes', date('now', '-2 day'), cast(unixepoch('subsecond', '-5 day') * 1000 as integer)),
          ('loan-active-seed', 'eq-notebook-01', 'João Ribeiro', date('now', '+3 day'), cast(unixepoch('subsecond', '-1 day') * 1000 as integer))`,
      )
      .run();
  })();
}
