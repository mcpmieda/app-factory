"use client";

import { useEffect, useMemo, useRef, useState } from "react";

import { StudentFormCard } from "@/features/students/components/student-form-card";
import { StudentListCard } from "@/features/students/components/student-list-card";
import {
  INITIAL_FORM,
  STATUS_LABELS,
  downloadTextFile,
  issueMap,
  type Feedback,
  type FieldErrors,
  type FieldName,
} from "@/features/students/components/student-ui";
import {
  createStudentBackup,
  hasRegistration,
  parseStudentBackup,
  readStudents,
  studentsToCsv,
  writeStudents,
} from "@/features/students/data/student-storage";
import {
  filterAndSortStudents,
  summarizeStudents,
  uniqueClassrooms,
  type StudentSort,
  type StudentStatusFilter,
} from "@/features/students/domain/student-operations";
import {
  studentSchema,
  type StudentFormValues,
  type StudentRecord,
  type StudentStatus,
} from "@/features/students/schemas/student-schema";

export function StudentRegistration() {
  const [form, setForm] = useState<StudentFormValues>(INITIAL_FORM);
  const [errors, setErrors] = useState<FieldErrors>({});
  const [students, setStudents] = useState<StudentRecord[]>([]);
  const [feedback, setFeedback] = useState<Feedback>(null);
  const [storageError, setStorageError] = useState<string | null>(null);
  const [hydrated, setHydrated] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editingStatus, setEditingStatus] = useState<StudentStatus>("active");
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [query, setQuery] = useState("");
  const [statusFilter, setStatusFilter] =
    useState<StudentStatusFilter>("all");
  const [classroomFilter, setClassroomFilter] = useState("all");
  const [sort, setSort] = useState<StudentSort>("recent");
  const backupInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    let cancelled = false;

    queueMicrotask(() => {
      if (cancelled) return;

      const result = readStudents();

      if (result.ok) {
        setStudents(result.students);
        if (result.migrated) {
          setFeedback({
            status: "success",
            title: "Cadastros atualizados",
            description:
              "Os dados da versão anterior foram migrados automaticamente.",
          });
        }
      } else {
        setStorageError(result.message);
      }

      setHydrated(true);
    });

    return () => {
      cancelled = true;
    };
  }, []);

  const stats = useMemo(() => summarizeStudents(students), [students]);
  const classrooms = useMemo(() => uniqueClassrooms(students), [students]);
  const visibleStudents = useMemo(
    () =>
      filterAndSortStudents(students, {
        query,
        status: statusFilter,
        classroom: classroomFilter,
        sort,
      }),
    [students, query, statusFilter, classroomFilter, sort],
  );

  const resultLabel = useMemo(() => {
    const count = visibleStudents.length;
    return `${count} ${count === 1 ? "resultado" : "resultados"}`;
  }, [visibleStudents.length]);

  function updateField<K extends FieldName>(
    field: K,
    value: StudentFormValues[K],
  ) {
    setForm((current) => ({ ...current, [field]: value }));
    setErrors((current) => ({ ...current, [field]: undefined }));

    if (feedback?.status === "danger") {
      setFeedback(null);
    }
  }

  function resetForm() {
    setForm(INITIAL_FORM);
    setErrors({});
    setEditingId(null);
    setEditingStatus("active");
  }

  function persistStudents(nextStudents: StudentRecord[]) {
    try {
      writeStudents(nextStudents);
      setStudents(nextStudents);
      setStorageError(null);
      return true;
    } catch {
      setFeedback({
        status: "danger",
        title: "Não foi possível salvar",
        description: "O navegador não permitiu gravar os dados localmente.",
      });
      return false;
    }
  }

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setFeedback(null);

    const parsed = studentSchema.safeParse(form);

    if (!parsed.success) {
      setErrors(issueMap(parsed.error.issues));
      setFeedback({
        status: "danger",
        title: "Revise os campos",
        description:
          "Há informações que precisam ser corrigidas antes de salvar.",
      });
      return;
    }

    if (
      hasRegistration(
        students,
        parsed.data.registration,
        editingId ?? undefined,
      )
    ) {
      setErrors({
        registration: "Esta matrícula já está cadastrada neste navegador.",
      });
      setFeedback({
        status: "danger",
        title: "Matrícula já cadastrada",
        description: "Use uma matrícula diferente para continuar.",
      });
      return;
    }

    const now = new Date().toISOString();

    if (editingId) {
      const current = students.find((student) => student.id === editingId);

      if (!current) {
        setFeedback({
          status: "danger",
          title: "Cadastro não encontrado",
          description: "Atualize a página e tente novamente.",
        });
        resetForm();
        return;
      }

      const updated: StudentRecord = {
        ...current,
        ...parsed.data,
        status: editingStatus,
        updatedAt: now,
      };

      const nextStudents = students.map((student) =>
        student.id === editingId ? updated : student,
      );

      if (persistStudents(nextStudents)) {
        resetForm();
        setFeedback({
          status: "success",
          title: "Cadastro atualizado",
          description: `${updated.name} foi atualizado com sucesso.`,
        });
      }
      return;
    }

    const record: StudentRecord = {
      ...parsed.data,
      id: globalThis.crypto?.randomUUID?.() ?? `${Date.now()}`,
      status: "active",
      createdAt: now,
      updatedAt: now,
    };

    if (persistStudents([record, ...students])) {
      resetForm();
      setFeedback({
        status: "success",
        title: "Aluno cadastrado",
        description: `${record.name} foi adicionado com sucesso.`,
      });
    }
  }

  function startNewStudent() {
    resetForm();
    setFeedback(null);
    document.getElementById("student-form-card")?.scrollIntoView({
      block: "start",
    });
  }

  function startEdit(student: StudentRecord) {
    setForm({
      name: student.name,
      registration: student.registration,
      birthDate: student.birthDate,
      email: student.email,
      phone: student.phone,
      course: student.course,
      classroom: student.classroom,
      shift: student.shift,
      guardianName: student.guardianName,
      guardianPhone: student.guardianPhone,
      notes: student.notes,
    });
    setEditingId(student.id);
    setEditingStatus(student.status);
    setErrors({});
    setFeedback(null);
    document.getElementById("student-form-card")?.scrollIntoView({
      block: "start",
    });
  }

  function toggleArchive(student: StudentRecord) {
    const nextStatus: StudentStatus =
      student.status === "active" ? "inactive" : "active";
    const now = new Date().toISOString();
    const nextStudents = students.map((item) =>
      item.id === student.id
        ? { ...item, status: nextStatus, updatedAt: now }
        : item,
    );

    if (persistStudents(nextStudents)) {
      setFeedback({
        status: "success",
        title: nextStatus === "active" ? "Aluno reativado" : "Aluno arquivado",
        description: `${student.name} agora está ${STATUS_LABELS[
          nextStatus
        ].toLocaleLowerCase("pt-BR")}.`,
      });
    }
  }

  function deleteStudent(student: StudentRecord) {
    const confirmed = window.confirm(
      `Excluir permanentemente o cadastro de ${student.name}?`,
    );
    if (!confirmed) return;

    const nextStudents = students.filter((item) => item.id !== student.id);

    if (persistStudents(nextStudents)) {
      if (editingId === student.id) resetForm();
      if (expandedId === student.id) setExpandedId(null);
      setFeedback({
        status: "success",
        title: "Cadastro excluído",
        description: `${student.name} foi removido deste dispositivo.`,
      });
    }
  }

  function exportCsv() {
    downloadTextFile(
      `alunos-${new Date().toISOString().slice(0, 10)}.csv`,
      `\uFEFF${studentsToCsv(students)}`,
      "text/csv;charset=utf-8",
    );
  }

  function exportBackup() {
    const backup = createStudentBackup(students);
    downloadTextFile(
      `backup-alunos-${new Date().toISOString().slice(0, 10)}.json`,
      `${JSON.stringify(backup, null, 2)}\n`,
      "application/json;charset=utf-8",
    );
  }

  async function restoreBackup(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    event.target.value = "";
    if (!file) return;

    const parsed = parseStudentBackup(await file.text());

    if (!parsed.ok) {
      setFeedback({
        status: "danger",
        title: "Backup inválido",
        description: parsed.message,
      });
      return;
    }

    const confirmed = window.confirm(
      `Restaurar ${parsed.students.length} cadastro(s)? Os dados atuais deste navegador serão substituídos.`,
    );
    if (!confirmed) return;

    if (persistStudents(parsed.students)) {
      resetForm();
      setExpandedId(null);
      setQuery("");
      setStatusFilter("all");
      setClassroomFilter("all");
      setFeedback({
        status: "success",
        title: "Backup restaurado",
        description: `${parsed.students.length} cadastro(s) foram restaurados.`,
      });
    }
  }

  const archivedCount = stats.inactive + stats.transferred;

  return (
    <main className="student-shell mx-auto w-full max-w-7xl px-4 py-7 sm:px-6 sm:py-10">
      <header className="mb-7 flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
        <div className="max-w-3xl">
          <div className="mb-3 inline-flex rounded-full border border-black/5 bg-white/70 px-3 py-1 text-xs font-semibold tracking-wide text-slate-600 backdrop-blur">
            Gestão acadêmica local
          </div>
          <h1 className="text-3xl font-semibold tracking-[-0.04em] text-slate-950 sm:text-4xl">
            Gestão de alunos
          </h1>
          <p className="mt-3 max-w-2xl text-base leading-7 text-slate-600">
            Cadastre, localize, atualize, arquive e faça backup dos alunos sem
            sair desta tela.
          </p>
        </div>

        <div className="flex flex-wrap gap-2">
          <button className="student-action" type="button" onClick={exportCsv}>
            Exportar CSV
          </button>
          <button
            className="student-action"
            type="button"
            onClick={exportBackup}
          >
            Fazer backup
          </button>
          <button
            className="student-action"
            type="button"
            onClick={() => backupInputRef.current?.click()}
          >
            Restaurar backup
          </button>
          <input
            ref={backupInputRef}
            className="sr-only"
            type="file"
            accept=".json,application/json"
            aria-label="Selecionar arquivo de backup"
            onChange={restoreBackup}
          />
          <button
            className="student-action student-action-primary"
            type="button"
            onClick={startNewStudent}
          >
            Novo aluno
          </button>
        </div>
      </header>

      <section
        className="mb-6 grid grid-cols-2 gap-3 lg:grid-cols-4"
        aria-label="Resumo dos cadastros"
      >
        <article className="student-stat">
          <span>Total</span>
          <strong>{hydrated ? stats.total : "—"}</strong>
          <small>cadastros no dispositivo</small>
        </article>
        <article className="student-stat">
          <span>Ativos</span>
          <strong>{hydrated ? stats.active : "—"}</strong>
          <small>alunos em acompanhamento</small>
        </article>
        <article className="student-stat">
          <span>Turmas ativas</span>
          <strong>{hydrated ? stats.classrooms : "—"}</strong>
          <small>com aluno ativo</small>
        </article>
        <article className="student-stat">
          <span>Arquivados</span>
          <strong>{hydrated ? archivedCount : "—"}</strong>
          <small>inativos ou transferidos</small>
        </article>
      </section>

      <div className="grid items-start gap-6 xl:grid-cols-[minmax(0,0.9fr)_minmax(0,1.45fr)]">
        <StudentFormCard
          form={form}
          errors={errors}
          editingId={editingId}
          editingStatus={editingStatus}
          feedback={feedback}
          storageError={storageError}
          onFieldChange={updateField}
          onStatusChange={setEditingStatus}
          onSubmit={handleSubmit}
          onCancel={resetForm}
        />

        <StudentListCard
          hydrated={hydrated}
          students={students}
          visibleStudents={visibleStudents}
          resultLabel={resultLabel}
          classrooms={classrooms}
          query={query}
          statusFilter={statusFilter}
          classroomFilter={classroomFilter}
          sort={sort}
          expandedId={expandedId}
          onQueryChange={setQuery}
          onStatusFilterChange={setStatusFilter}
          onClassroomFilterChange={setClassroomFilter}
          onSortChange={setSort}
          onToggleExpanded={(id) =>
            setExpandedId((current) => (current === id ? null : id))
          }
          onEdit={startEdit}
          onToggleArchive={toggleArchive}
          onDelete={deleteStudent}
        />
      </div>
    </main>
  );
}
