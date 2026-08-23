# Agent Conformance Corpus

Este corpus mede se um executor/agente produz **estado observável compatível com a App Factory**. Ele não avalia chain-of-thought e não confia em afirmações do agente.

## Arquitetura

```text
case JSON
  ├─ prompt
  ├─ reference_actions (gold/reference executor)
  └─ assertions
          ↓
worktree produzido
          ↓
scorer determinístico
```

O mesmo scorer pode avaliar:

1. o executor de referência stdlib no CI;
2. um worktree produzido manualmente;
3. no futuro, um agente real rodado por Inspect AI, Codex CLI, Claude Code ou executor equivalente.

## Por que existe executor de referência

Antes de medir agentes, a Factory precisa provar que o próprio caso é solucionável e que o scorer reconhece uma solução conhecida. Isso segue a disciplina de harnesses como SWE-bench: benchmark quebrado não deve produzir score confiável.

## Segurança

`reference_actions` não executam shell arbitrário. Tipos permitidos:

- `write_text`;
- `write_json`;
- `factory_cli` — somente `scripts/factory.py` com argv estruturado;
- `attach_evidence` — altera somente o verification plan do workspace.

Paths absolutos, `..` e `.git` são rejeitados.

## Assertions atuais

- `file_exists` / `file_absent`;
- `text_contains`;
- `json_equals` via JSON Pointer;
- `semantic_spec_valid`;
- `verification_plan_valid`;
- `semantic_ready`;
- `declared_gate_passes`.

Todo caso precisa de pelo menos uma assertion que vá além de presença/ausência de arquivo.

## Comandos

```bash
python scripts/agent_conformance.py validate-corpus
python scripts/agent_conformance.py run-reference
python scripts/agent_conformance.py score --case functional-spec-and-plan --workspace /path/to/worktree
```

## Agente real

A avaliação com agente real é propositalmente opcional/adapter-based. Um runner externo recebe `prompt`, entrega um worktree e chama o comando `score`. Inspect AI é uma opção especialmente adequada porque suporta coding agents externos, sandbox e scorers que inspecionam arquivos; ele não é dependência universal da App Factory.
