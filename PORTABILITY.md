# Portability

A App Factory pertence ao repositório, não a um modelo específico.

## Núcleo neutro

Estes elementos devem continuar independentes do agente:

- princípios;
- workflow;
- risco;
- Definition of Done;
- Skills no padrão aberto quando possível;
- Context/Autonomy/Execution/Learning contracts;
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

O handoff durável entre agentes usa GitHub:

`repo + branch/PR + PROJECT_STATE + Issue + testes`.

Memória ou histórico de chat pode complementar, mas não é a fonte de verdade.

## Dados operacionais locais

A V1.3 diferencia continuidade durável de otimização local:

- `.factory/context/` — cache regenerável;
- `.factory/execution.json` — histórico bounded da execução local;
- `.factory/learning.json` — aprendizado técnico local allowlisted;
- `.factory/state.json` — pode ser versionado em handoffs importantes quando útil.

Context/execution/learning ficam fora do Git por padrão. Portanto, ao trocar de computador, um agente pode não receber o histórico aprendido. Isso não bloqueia o projeto: a Factory volta para o roteamento baseline seguro da Execution Fabric e aprende novamente a partir de novas execuções.

O Learning Engine é otimização e nunca requisito para correção, segurança ou continuidade.
