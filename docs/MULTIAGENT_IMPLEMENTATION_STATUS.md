# Multiagent Execution — estado de implementação

Atualizado em 27 de agosto de 2026.

## Classificação atual

A App Factory possui fundação provider-neutral, Control Plane Jules API-first comprovado em execução real e uma primeira implementação segura dos runtimes Antigravity/OpenCode-Ollama e do Merge Train.

A Factory multi-provider ainda não deve ser declarada 100% pronta.

## Comprovado em execução real

No `mcpmieda/ecossistema-escola`, a Factory Run `jules-api-pilot-002` comprovou:

- materialização durável em GitHub;
- dispatch Jules por REST API;
- dois workers paralelos;
- dependência liberada após merges;
- branches/PRs isolados;
- escopo por arquivos;
- CI obrigatório por `workflow_dispatch` e `head_sha` exato;
- retomada de task em `factory:ci` após restart;
- ausência de sessão duplicada;
- squash merge somente na integration branch;
- CI final completo;
- PR final draft e humano;
- deploy de produção pulado.

Evidência: `docs/JULES_API_FIRST_PILOT_EVIDENCE.md`.

## Implementado no Core

### Planner

- grafo de tarefas e dependências;
- waves paralelas;
- serialização por conflito de path;
- política `zero -> free_quota -> included -> metered`;
- `max_parallel` obrigatório entre 1 e 3;
- Codex `automatic=false`;
- human gates;
- CLI de template, validação, registry e plano.

### Provider Runtime

- request frozen/validado;
- health `healthy/degraded/unavailable/unknown`;
- seleção com fallback por health;
- ambiente sanitizado;
- profiles dedicados;
- saída machine-readable e prompt redigido;
- escopos protegidos fail-closed;
- Git config/hooks/remote/refs protegidos;
- histórico linear;
- commit controlado;
- push somente da worker branch;
- confirmação remota do SHA;
- telemetria sanitizada.

### Antigravity adapter

- CLI headless real com JSON;
- model/effort/agent opcionais;
- profile isolado obrigatório;
- probe de binary/auth/model;
- nenhuma flag de bypass de permissões.

### OpenCode/Ollama adapter

- CLI `opencode run` não interativa;
- apenas Ollama loopback;
- modelo explícito;
- profile isolado obrigatório;
- permission config por path/comando;
- web/external directory/subagents/skills negados;
- Git mutável negado;
- repo-provided OpenCode config recusada;
- plugins/configs externas desabilitados.

### Merge Train

- worker PR limitado à integration branch;
- CI exato por SHA/evento;
- escopo obrigatório;
- CodeRabbit, Semgrep e Sonar requeridos no mesmo SHA;
- revisão bloqueadora impede merge;
- PR final draft;
- target auto-merge sempre proibido.

## Validação automatizada

A suíte multiagent cobre 50 regressões, incluindo:

- limite 1–3;
- zero-first e fallback remoto;
- Codex manual-only;
- escopos protegidos;
- comandos perigosos;
- redaction;
- profiles isolados;
- configuração OpenCode bounded;
- health probes;
- execução Git local end-to-end;
- commit e push da worker branch;
- confirmação do SHA remoto;
- recusa de arquivo fora do escopo;
- recusa de modificação em Git config, hooks, remote e refs;
- Merge Train por SHA/reviews;
- final gate draft/humano.

O workflow `Validate Multiagent Execution` executa compile, regressões estruturais, Execution Fabric e o gate multiagent.

## Ainda não homologado live

1. Antigravity executando uma task real em profile/host isolado.
2. OpenCode/Ollama executando uma task real com modelo local.
3. Worker local durável/efêmero que continue sem o computador inicial.
4. Health/fallback conectado ao Control Plane do `ecossistema-escola`.
5. Telemetria persistida automaticamente em GitHub.
6. CodeRabbit, Semgrep e Sonar conectados como checks reais do Merge Train.
7. Piloto live de integração multi-provider.
8. Escalonamento excepcional Codex auditado, sempre manual.

## Dependência administrativa conhecida

No `ecossistema-escola`, GitHub Actions ainda não pode criar/aprovar PRs. A permissão administrativa precisa ser habilitada para que o runner crie sozinho o PR final draft. O merge final continuará humano mesmo depois disso.

## Próxima ordem de trabalho

1. piloto Antigravity;
2. piloto OpenCode/Ollama;
3. persistência de provider health/telemetria;
4. wiring real CodeRabbit/Semgrep/Sonar;
5. Merge Train multi-provider;
6. fallback operacional entre providers;
7. Codex apenas para exceção premium/manual.

## Regra de declaração

- **Implementado**: código e testes existem.
- **Comprovado**: passou em execução real com evidência durável.
- **Homologado**: passou repetidamente com CI, segurança e recovery.
- **Pronto**: todos os providers/gates necessários estão homologados e as dependências administrativas foram resolvidas.

Hoje, Jules API-first está comprovado; os novos adapters estão implementados/testados; a Factory inteira ainda não está pronta.
