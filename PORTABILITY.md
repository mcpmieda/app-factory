# Portability

A App Factory pertence ao repositório, não a um modelo específico.

## Núcleo neutro

Estes elementos devem continuar independentes do agente:

- princípios;
- workflow;
- risco;
- Definition of Done;
- Skills no padrão aberto quando possível;
- templates;
- scripts;
- testes;
- Issues/PRs/Git;
- documentação de produto e arquitetura.

## Adaptadores

### Codex

`AGENTS.md` deve funcionar como mapa do projeto e apontar para as Skills e documentos relevantes.

### Claude Code

Quando necessário, criar `CLAUDE.md` curto que aponte para o mesmo núcleo e Skills, evitando duplicar as regras.

### Cursor/outros

Criar regras/adaptadores mínimos apenas quando o cliente exigir formato próprio.

## Regra contra divergência

Nunca manter cópias completas e independentes das mesmas regras em `AGENTS.md`, `CLAUDE.md`, `.cursor/rules` etc. Os adaptadores devem apontar para uma fonte comum.

## Estado do trabalho

O handoff entre agentes usa GitHub:

`repo + branch/PR + PROJECT_STATE + Issue + testes`.

Memória ou histórico de chat pode complementar, mas não é a fonte de verdade.