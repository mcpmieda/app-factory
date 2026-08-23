import { Card } from "@heroui/react";

import {
  SHIFT_LABELS,
  STATUS_LABELS,
  formatDate,
  formatDateTime,
} from "@/features/students/components/student-ui";
import type {
  StudentSort,
  StudentStatusFilter,
} from "@/features/students/domain/student-operations";
import type { StudentRecord } from "@/features/students/schemas/student-schema";

type Props = {
  hydrated: boolean;
  students: StudentRecord[];
  visibleStudents: StudentRecord[];
  resultLabel: string;
  classrooms: string[];
  query: string;
  statusFilter: StudentStatusFilter;
  classroomFilter: string;
  sort: StudentSort;
  expandedId: string | null;
  onQueryChange: (value: string) => void;
  onStatusFilterChange: (value: StudentStatusFilter) => void;
  onClassroomFilterChange: (value: string) => void;
  onSortChange: (value: StudentSort) => void;
  onToggleExpanded: (id: string) => void;
  onEdit: (student: StudentRecord) => void;
  onToggleArchive: (student: StudentRecord) => void;
  onDelete: (student: StudentRecord) => void;
};

export function StudentListCard({
  hydrated,
  students,
  visibleStudents,
  resultLabel,
  classrooms,
  query,
  statusFilter,
  classroomFilter,
  sort,
  expandedId,
  onQueryChange,
  onStatusFilterChange,
  onClassroomFilterChange,
  onSortChange,
  onToggleExpanded,
  onEdit,
  onToggleArchive,
  onDelete,
}: Props) {
  return (
    <Card className="student-panel shadow-sm" variant="secondary">
      <Card.Header className="flex flex-col gap-5 px-5 pt-5 sm:px-7 sm:pt-7">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
          <div>
            <Card.Title id="students-heading">Alunos cadastrados</Card.Title>
            <Card.Description>
              Pesquise, filtre e administre os registros deste dispositivo.
            </Card.Description>
          </div>
          <span className="student-result-count">
            {hydrated ? resultLabel : "Carregando…"}
          </span>
        </div>

        <div className="student-toolbar" aria-label="Filtros da lista">
          <label className="student-search">
            <span className="sr-only">Pesquisar alunos</span>
            <input
              aria-label="Pesquisar alunos"
              placeholder="Buscar por nome, matrícula, turma, curso ou contato"
              type="search"
              value={query}
              onChange={(event) => onQueryChange(event.target.value)}
            />
          </label>

          <label className="student-filter">
            <span>Status</span>
            <select
              aria-label="Filtrar por status"
              value={statusFilter}
              onChange={(event) =>
                onStatusFilterChange(
                  event.target.value as StudentStatusFilter,
                )
              }
            >
              <option value="all">Todos</option>
              <option value="active">Ativos</option>
              <option value="inactive">Arquivados</option>
              <option value="transferred">Transferidos</option>
            </select>
          </label>

          <label className="student-filter">
            <span>Turma</span>
            <select
              aria-label="Filtrar por turma"
              value={classroomFilter}
              onChange={(event) => onClassroomFilterChange(event.target.value)}
            >
              <option value="all">Todas</option>
              {classrooms.map((classroom) => (
                <option key={classroom} value={classroom}>
                  {classroom}
                </option>
              ))}
            </select>
          </label>

          <label className="student-filter">
            <span>Ordenar</span>
            <select
              aria-label="Ordenar alunos"
              value={sort}
              onChange={(event) =>
                onSortChange(event.target.value as StudentSort)
              }
            >
              <option value="recent">Atualizados recentemente</option>
              <option value="name">Nome</option>
              <option value="classroom">Turma</option>
            </select>
          </label>
        </div>
      </Card.Header>

      <Card.Content className="px-5 pb-5 pt-5 sm:px-7 sm:pb-7">
        {!hydrated ? (
          <p className="student-empty">Carregando cadastros…</p>
        ) : students.length === 0 ? (
          <div className="student-empty">
            <p className="font-medium text-slate-900">
              Nenhum aluno cadastrado ainda
            </p>
            <p className="mt-1 text-sm text-slate-500">
              Use “Novo aluno” ou o formulário ao lado para começar.
            </p>
          </div>
        ) : visibleStudents.length === 0 ? (
          <div className="student-empty">
            <p className="font-medium text-slate-900">
              Nenhum cadastro encontrado
            </p>
            <p className="mt-1 text-sm text-slate-500">
              Ajuste a busca ou os filtros para ver outros alunos.
            </p>
          </div>
        ) : (
          <div className="flex flex-col gap-3">
            {visibleStudents.map((student) => {
              const isExpanded = expandedId === student.id;

              return (
                <article
                  key={student.id}
                  className="student-row rounded-2xl border border-slate-200/80 bg-white/80 p-4"
                >
                  <div className="flex flex-col gap-4">
                    <div className="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
                      <div className="min-w-0">
                        <div className="flex flex-wrap items-center gap-2">
                          <h2 className="truncate text-base font-semibold text-slate-950">
                            {student.name}
                          </h2>
                          <span
                            className="student-status"
                            data-status={student.status}
                          >
                            {STATUS_LABELS[student.status]}
                          </span>
                        </div>
                        <p className="mt-1 text-sm text-slate-500">
                          Matrícula {student.registration} · {student.course} ·{" "}
                          {student.classroom} · {SHIFT_LABELS[student.shift]}
                        </p>
                        <p className="mt-2 break-all text-sm text-slate-600">
                          {student.email}
                          {student.phone ? ` · ${student.phone}` : ""}
                        </p>
                      </div>

                      <div className="student-row-actions">
                        <button
                          type="button"
                          onClick={() => onToggleExpanded(student.id)}
                        >
                          {isExpanded ? "Ocultar" : "Detalhes"}
                        </button>
                        <button type="button" onClick={() => onEdit(student)}>
                          Editar
                        </button>
                        <button
                          type="button"
                          onClick={() => onToggleArchive(student)}
                        >
                          {student.status === "active"
                            ? "Arquivar"
                            : "Reativar"}
                        </button>
                        <button
                          className="student-danger-action"
                          type="button"
                          onClick={() => onDelete(student)}
                        >
                          Excluir
                        </button>
                      </div>
                    </div>

                    {isExpanded && (
                      <div className="student-details">
                        <dl>
                          <div>
                            <dt>Nascimento</dt>
                            <dd>{formatDate(student.birthDate)}</dd>
                          </div>
                          <div>
                            <dt>Responsável</dt>
                            <dd>{student.guardianName || "Não informado"}</dd>
                          </div>
                          <div>
                            <dt>Contato do responsável</dt>
                            <dd>{student.guardianPhone || "Não informado"}</dd>
                          </div>
                          <div>
                            <dt>Última atualização</dt>
                            <dd>{formatDateTime(student.updatedAt)}</dd>
                          </div>
                        </dl>
                        <div className="student-notes">
                          <strong>Observações</strong>
                          <p>
                            {student.notes || "Nenhuma observação registrada."}
                          </p>
                        </div>
                      </div>
                    )}
                  </div>
                </article>
              );
            })}
          </div>
        )}
      </Card.Content>
    </Card>
  );
}
