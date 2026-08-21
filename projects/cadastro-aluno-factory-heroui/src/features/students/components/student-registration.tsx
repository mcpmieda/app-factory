"use client";

import {
  Alert,
  Button,
  Card,
  FieldError,
  Input,
  Label,
  TextField,
} from "@heroui/react";
import { useEffect, useMemo, useState } from "react";

import {
  studentSchema,
  type StudentFormValues,
  type StudentRecord,
} from "@/features/students/schemas/student-schema";
import {
  hasRegistration,
  readStudents,
  writeStudents,
} from "@/features/students/data/student-storage";

const INITIAL_FORM: StudentFormValues = {
  name: "",
  registration: "",
  birthDate: "",
  email: "",
  phone: "",
  course: "",
  classroom: "",
};

type FieldName = keyof StudentFormValues;
type FieldErrors = Partial<Record<FieldName, string>>;

type Feedback =
  | {
      status: "success" | "danger";
      title: string;
      description: string;
    }
  | null;

function formatPhone(value: string) {
  const digits = value.replace(/\D/g, "").slice(0, 11);

  if (digits.length <= 2) return digits;
  if (digits.length <= 6) return digits.replace(/(\d{2})(\d+)/, "($1) $2");
  if (digits.length <= 10) {
    return digits.replace(/(\d{2})(\d{4})(\d{0,4})/, "($1) $2-$3");
  }

  return digits.replace(/(\d{2})(\d{5})(\d{0,4})/, "($1) $2-$3");
}

function issueMap(issues: { path: PropertyKey[]; message: string }[]) {
  const errors: FieldErrors = {};

  for (const issue of issues) {
    const key = issue.path[0];

    if (
      typeof key === "string" &&
      key in INITIAL_FORM &&
      !errors[key as FieldName]
    ) {
      errors[key as FieldName] = issue.message;
    }
  }

  return errors;
}

export function StudentRegistration() {
  const [form, setForm] = useState<StudentFormValues>(INITIAL_FORM);
  const [errors, setErrors] = useState<FieldErrors>({});
  const [students, setStudents] = useState<StudentRecord[]>([]);
  const [feedback, setFeedback] = useState<Feedback>(null);
  const [storageError, setStorageError] = useState<string | null>(null);
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    const result = readStudents();

    if (result.ok) {
      setStudents(result.students);
    } else {
      setStorageError(result.message);
    }

    setHydrated(true);
  }, []);

  const countLabel = useMemo(
    () => `${students.length} ${students.length === 1 ? "aluno" : "alunos"}`,
    [students.length],
  );

  function updateField(field: FieldName, value: string) {
    setForm((current) => ({ ...current, [field]: value }));
    setErrors((current) => ({ ...current, [field]: undefined }));

    if (feedback?.status === "danger") {
      setFeedback(null);
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
        description: "Há informações que precisam ser corrigidas antes do cadastro.",
      });
      return;
    }

    if (hasRegistration(students, parsed.data.registration)) {
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

    const record: StudentRecord = {
      ...parsed.data,
      id: globalThis.crypto?.randomUUID?.() ?? `${Date.now()}`,
      createdAt: new Date().toISOString(),
    };

    const nextStudents = [record, ...students];

    try {
      writeStudents(nextStudents);
      setStudents(nextStudents);
      setForm(INITIAL_FORM);
      setErrors({});
      setStorageError(null);
      setFeedback({
        status: "success",
        title: "Aluno cadastrado",
        description: `${record.name} foi adicionado com sucesso.`,
      });
    } catch {
      setFeedback({
        status: "danger",
        title: "Não foi possível salvar",
        description: "O navegador não permitiu gravar os dados localmente.",
      });
    }
  }

  return (
    <main className="student-shell mx-auto w-full max-w-5xl px-4 py-8 sm:px-6 sm:py-12">
      <header className="mb-7 max-w-2xl">
        <div className="mb-3 inline-flex rounded-full border border-black/5 bg-white/70 px-3 py-1 text-xs font-semibold tracking-wide text-slate-600 backdrop-blur">
          Cadastro em uma etapa
        </div>
        <h1 className="text-3xl font-semibold tracking-[-0.035em] text-slate-950 sm:text-4xl">
          Cadastro de aluno
        </h1>
        <p className="mt-3 max-w-xl text-base leading-7 text-slate-600">
          Preencha os dados abaixo e conclua o cadastro sem trocar de tela.
        </p>
      </header>

      <Card className="student-panel w-full shadow-sm" variant="default">
        <Card.Header className="flex flex-col items-start gap-1 px-5 pt-5 sm:px-7 sm:pt-7">
          <Card.Title>Dados do aluno</Card.Title>
          <Card.Description>
            Os campos marcados são necessários para concluir o cadastro.
          </Card.Description>
        </Card.Header>

        <Card.Content className="px-5 pb-2 pt-5 sm:px-7">
          <form
            id="student-form"
            className="grid grid-cols-1 gap-5 md:grid-cols-2"
            noValidate
            onSubmit={handleSubmit}
          >
            <TextField
              isRequired
              className="md:col-span-2"
              fullWidth
              isInvalid={Boolean(errors.name)}
              name="name"
            >
              <Label>Nome completo</Label>
              <Input
                autoComplete="name"
                maxLength={120}
                placeholder="Ex.: Ana Souza"
                value={form.name}
                variant="secondary"
                onChange={(event) => updateField("name", event.target.value)}
              />
              <FieldError>{errors.name}</FieldError>
            </TextField>

            <TextField
              isRequired
              fullWidth
              isInvalid={Boolean(errors.registration)}
              name="registration"
            >
              <Label>Matrícula</Label>
              <Input
                maxLength={30}
                placeholder="Ex.: 202600123"
                value={form.registration}
                variant="secondary"
                onChange={(event) =>
                  updateField("registration", event.target.value)
                }
              />
              <FieldError>{errors.registration}</FieldError>
            </TextField>

            <TextField
              isRequired
              fullWidth
              isInvalid={Boolean(errors.birthDate)}
              name="birthDate"
              type="date"
            >
              <Label>Data de nascimento</Label>
              <Input
                type="date"
                value={form.birthDate}
                variant="secondary"
                onChange={(event) =>
                  updateField("birthDate", event.target.value)
                }
              />
              <FieldError>{errors.birthDate}</FieldError>
            </TextField>

            <TextField
              isRequired
              fullWidth
              isInvalid={Boolean(errors.email)}
              name="email"
              type="email"
            >
              <Label>E-mail</Label>
              <Input
                autoComplete="email"
                placeholder="aluno@exemplo.com"
                type="email"
                value={form.email}
                variant="secondary"
                onChange={(event) => updateField("email", event.target.value)}
              />
              <FieldError>{errors.email}</FieldError>
            </TextField>

            <TextField
              fullWidth
              isInvalid={Boolean(errors.phone)}
              name="phone"
              type="tel"
            >
              <Label>Telefone</Label>
              <Input
                autoComplete="tel"
                inputMode="tel"
                placeholder="(71) 99999-9999"
                type="tel"
                value={form.phone}
                variant="secondary"
                onChange={(event) =>
                  updateField("phone", formatPhone(event.target.value))
                }
              />
              <FieldError>{errors.phone}</FieldError>
            </TextField>

            <TextField
              isRequired
              fullWidth
              isInvalid={Boolean(errors.course)}
              name="course"
            >
              <Label>Curso</Label>
              <Input
                maxLength={80}
                placeholder="Ex.: Ensino Médio"
                value={form.course}
                variant="secondary"
                onChange={(event) => updateField("course", event.target.value)}
              />
              <FieldError>{errors.course}</FieldError>
            </TextField>

            <TextField
              isRequired
              fullWidth
              isInvalid={Boolean(errors.classroom)}
              name="classroom"
            >
              <Label>Turma</Label>
              <Input
                maxLength={40}
                placeholder="Ex.: 3º A"
                value={form.classroom}
                variant="secondary"
                onChange={(event) =>
                  updateField("classroom", event.target.value)
                }
              />
              <FieldError>{errors.classroom}</FieldError>
            </TextField>
          </form>

          <div className="mt-5 space-y-3" aria-live="polite">
            {storageError && (
              <Alert status="danger">
                <Alert.Indicator />
                <Alert.Content>
                  <Alert.Title>Dados locais indisponíveis</Alert.Title>
                  <Alert.Description>{storageError}</Alert.Description>
                </Alert.Content>
              </Alert>
            )}

            {feedback && (
              <Alert status={feedback.status}>
                <Alert.Indicator />
                <Alert.Content>
                  <Alert.Title>{feedback.title}</Alert.Title>
                  <Alert.Description>{feedback.description}</Alert.Description>
                </Alert.Content>
              </Alert>
            )}
          </div>
        </Card.Content>

        <Card.Footer className="flex flex-col items-stretch gap-4 px-5 pb-5 pt-5 sm:flex-row sm:items-center sm:justify-between sm:px-7 sm:pb-7">
          <p className="text-sm leading-5 text-slate-500">
            Nesta versão de demonstração, os dados ficam somente neste navegador.
          </p>
          <Button
            className="min-w-40"
            form="student-form"
            size="lg"
            type="submit"
            variant="primary"
          >
            Cadastrar aluno
          </Button>
        </Card.Footer>
      </Card>

      <section className="mt-6" aria-labelledby="students-heading">
        <Card className="student-panel shadow-sm" variant="secondary">
          <Card.Header className="flex flex-row items-start justify-between gap-4 px-5 pt-5 sm:px-7 sm:pt-7">
            <div className="min-w-0">
              <Card.Title id="students-heading">Alunos cadastrados</Card.Title>
              <Card.Description>
                Registros disponíveis neste dispositivo.
              </Card.Description>
            </div>
            <span className="shrink-0 rounded-full border border-black/5 bg-white/70 px-3 py-1 text-sm font-medium text-slate-700">
              {hydrated ? countLabel : "Carregando…"}
            </span>
          </Card.Header>

          <Card.Content className="px-5 pb-5 pt-5 sm:px-7 sm:pb-7">
            {!hydrated ? (
              <p className="rounded-2xl border border-dashed border-slate-200 bg-white/55 p-7 text-center text-sm text-slate-500">
                Carregando cadastros…
              </p>
            ) : students.length === 0 ? (
              <div className="rounded-2xl border border-dashed border-slate-200 bg-white/55 p-7 text-center">
                <p className="font-medium text-slate-900">
                  Nenhum aluno cadastrado ainda
                </p>
                <p className="mt-1 text-sm text-slate-500">
                  O primeiro cadastro aparecerá aqui automaticamente.
                </p>
              </div>
            ) : (
              <div className="flex flex-col gap-3">
                {students.map((student) => (
                  <article
                    key={student.id}
                    className="student-row rounded-2xl border border-slate-200/80 bg-white/75 p-4"
                  >
                    <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                      <div className="min-w-0">
                        <h2 className="truncate font-semibold text-slate-950">
                          {student.name}
                        </h2>
                        <p className="mt-1 text-sm text-slate-500">
                          Matrícula {student.registration} · {student.course} ·{" "}
                          {student.classroom}
                        </p>
                      </div>
                      <p className="break-all text-sm text-slate-500">
                        {student.email}
                      </p>
                    </div>
                  </article>
                ))}
              </div>
            )}
          </Card.Content>
        </Card>
      </section>
    </main>
  );
}
