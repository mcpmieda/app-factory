# Git Policy

Git registra estado técnico; Issues registram trabalho; PRs registram proposta, diff e revisão; CI registra evidência automática.

## Projeto novo

- `main` representa estado integrado.
- Funcionalidades relevantes preferem branch/worktree própria.
- PR quando risco, colaboração ou revisão justificar.
- Evitar commits genéricos quando uma intenção clara puder ser registrada.

## Manutenção

- identificar baseline seguro antes de mudança relevante;
- revisar preferencialmente por diff;
- não misturar alterações independentes no mesmo commit sem motivo.

## Commits

Conventional Commits podem ser usados quando agregarem clareza: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `security`.

## Branch protection

Projetos de produção ou maior criticidade devem avaliar rulesets/checks obrigatórios. Protótipos não precisam copiar automaticamente a mesma governança.

## Continuidade

Ao trocar de agente, aponte para branch/PR, Issue, `PROJECT_STATE.md` e critérios de conclusão.