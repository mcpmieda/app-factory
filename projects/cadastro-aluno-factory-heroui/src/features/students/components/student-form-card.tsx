import {
  Alert,
  Button,
  Card,
  FieldError,
  Input,
  Label,
  TextField,
} from "@heroui/react";
import type { FormEvent } from "react";

import {
  SHIFT_LABELS,
  STATUS_LABELS,
  formatPhone,
  type Feedback,
  type FieldErrors,
  type FieldName,
} from "@/features/students/components/student-ui";
import type {
  StudentFormValues,
  StudentShift,
  StudentStatus,
} from "@/features/students/schemas/student-schema";

type Props = {
  form: StudentFormValues;
  errors: FieldErrors;
  editingId: string | null;
  editingStatus: StudentStatus;
  feedback: Feedback;
  storageError: string | null;
  onFieldChange: <K extends FieldName>(
    field: K,
    value: StudentFormValues[K],
  ) => void;
  onStatusChange: (status: StudentStatus) => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
  onCancel: () => void;
};

export function StudentFormCard({
  form,
  errors,
  editingId,
  editingStatus,
  feedback,
  storageError,
  onFieldChange,
  onStatusChange,
  onSubmit,
  onCancel,
}: Props) {
  return (
    <Card
      id="student-form-card"
      className="student-panel w-full scroll-mt-6 shadow-sm"
      variant="default"
    >
      <Card.Header className="flex flex-col items-start gap-1 px-5 pt-5 sm:px-7 sm:pt-7">
        <Card.Title>{editingId ? "Editar aluno" : "Novo aluno"}</Card.Title>
        <Card.Description>
          {editingId
            ? "Atualize os dados e salve as alterações."
            : "Inclua os dados essenciais e acadêmicos do aluno."}
        </Card.Description>
      </Card.Header>

      <Card.Content className="px-5 pb-2 pt-5 sm:px-7">
        <form
          id="student-form"
          className="grid grid-cols-1 gap-5 md:grid-cols-2"
          noValidate
          onSubmit={onSubmit}
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
              onChange={(event) => onFieldChange("name", event.target.value)}
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
                onFieldChange("registration", event.target.value)
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
                onFieldChange("birthDate", event.target.value)
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
              onChange={(event) => onFieldChange("email", event.target.value)}
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
                onFieldChange("phone", formatPhone(event.target.value))
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
            <Label>Curso / etapa</Label>
            <Input
              maxLength={80}
              placeholder="Ex.: Ensino Médio"
              value={form.course}
              variant="secondary"
              onChange={(event) => onFieldChange("course", event.target.value)}
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
                onFieldChange("classroom", event.target.value)
              }
            />
            <FieldError>{errors.classroom}</FieldError>
          </TextField>

          <label className="student-native-field">
            <span>Turno</span>
            <select
              aria-label="Turno"
              value={form.shift}
              onChange={(event) =>
                onFieldChange("shift", event.target.value as StudentShift)
              }
            >
              {Object.entries(SHIFT_LABELS).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </label>

          {editingId && (
            <label className="student-native-field">
              <span>Status</span>
              <select
                aria-label="Status do aluno"
                value={editingStatus}
                onChange={(event) =>
                  onStatusChange(event.target.value as StudentStatus)
                }
              >
                {Object.entries(STATUS_LABELS).map(([value, label]) => (
                  <option key={value} value={value}>
                    {label}
                  </option>
                ))}
              </select>
            </label>
          )}

          <TextField
            className={editingId ? "" : "md:col-span-2"}
            fullWidth
            isInvalid={Boolean(errors.guardianName)}
            name="guardianName"
          >
            <Label>Responsável</Label>
            <Input
              maxLength={120}
              placeholder="Nome do responsável"
              value={form.guardianName}
              variant="secondary"
              onChange={(event) =>
                onFieldChange("guardianName", event.target.value)
              }
            />
            <FieldError>{errors.guardianName}</FieldError>
          </TextField>

          <TextField
            className={editingId ? "md:col-span-2" : ""}
            fullWidth
            isInvalid={Boolean(errors.guardianPhone)}
            name="guardianPhone"
            type="tel"
          >
            <Label>Telefone do responsável</Label>
            <Input
              inputMode="tel"
              placeholder="(71) 99999-9999"
              type="tel"
              value={form.guardianPhone}
              variant="secondary"
              onChange={(event) =>
                onFieldChange(
                  "guardianPhone",
                  formatPhone(event.target.value),
                )
              }
            />
            <FieldError>{errors.guardianPhone}</FieldError>
          </TextField>

          <label className="student-native-field md:col-span-2" htmlFor="notes">
            <span>Observações</span>
            <textarea
              id="notes"
              maxLength={500}
              placeholder="Informações relevantes para consulta interna."
              rows={4}
              value={form.notes}
              onChange={(event) => onFieldChange("notes", event.target.value)}
            />
            {errors.notes && (
              <small className="student-native-error">{errors.notes}</small>
            )}
          </label>
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

      <Card.Footer className="flex flex-col items-stretch gap-3 px-5 pb-5 pt-5 sm:flex-row sm:items-center sm:justify-between sm:px-7 sm:pb-7">
        <p className="text-sm leading-5 text-slate-500">
          Os dados continuam armazenados apenas neste navegador.
        </p>
        <div className="flex flex-col gap-2 sm:flex-row">
          {editingId && (
            <button className="student-action" type="button" onClick={onCancel}>
              Cancelar
            </button>
          )}
          <Button
            className="min-w-40"
            form="student-form"
            size="lg"
            type="submit"
            variant="primary"
          >
            {editingId ? "Salvar alterações" : "Cadastrar aluno"}
          </Button>
        </div>
      </Card.Footer>
    </Card>
  );
}
