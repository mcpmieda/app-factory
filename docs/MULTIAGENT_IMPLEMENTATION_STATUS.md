# Multiagent Execution — estado de implementação

## Fase atual

Implementada a fundação provider-neutral para planejamento de Factory Runs paralelos.

Entregue nesta fase:

- `engine/work_orchestrator.py`: grafo de tarefas, dependências, escopos, waves e roteamento de providers;
- política `zero -> free_quota -> included -> metered`;
- Codex registrado como `automatic=false`;
- human gates para produto, destrutivo, produção, privilégios e decisão legal/organizacional;
- serialização conservadora quando escopos de arquivos se sobrepõem ou são desconhecidos;
- `scripts/factory_run.py`: template, validação, registry e planner;
- testes unitários e integração CLI;
- workflow `Validate Multiagent Execution`;
- exemplo de piloto para Banco de Notas.

## Ainda não habilitado

Esta fase não instala, autentica nem dispara providers externos.

Permanecem para fases seguintes:

1. materialização de Factory Run no GitHub Control Plane;
2. criação de child tasks/issues tipadas;
3. conexão Jules;
4. conexão Antigravity headless;
5. conexão OpenCode/Ollama local;
6. reconciliation/merge train;
7. telemetria de cota, falha e fallback.

## Segurança

Nenhum prompt vira shell.

Nenhuma API key/secret pertence ao Factory Run.

Nenhuma ativação de produção é automática.

Nenhum provider pago é escolhido automaticamente.
