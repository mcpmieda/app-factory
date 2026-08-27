# Multiagent Execution — estado de implementação

Atualizado em 27 de agosto de 2026.

## Classificação atual

A App Factory possui:

- fundação provider-neutral;
- Jules API-first comprovado em execução real;
- runtimes Antigravity e OpenCode/Ollama implementados e testados;
- protocolo de executor durável baseado em GitHub;
- contrato de Merge Train por SHA exato.

A Factory multi-provider ainda não deve ser declarada 100% pronta. Os componentes locais/headless precisam ser conectados ao Control Plane operacional e homologados em hosts reais.

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

### Durable Provider Agent

- fingerprint portátil do request, independente do diretório local;
- fingerprint do manifesto imutável;
- lease vinculada a run/task/issue/provider/executor/branches/hashes;
- confiança somente em lease cuja autoria real é verificada como `github-actions[bot]`;
- expiração e takeover fail-closed;
- heartbeat sanitizado sem renovação implícita;
- resultado terminal vinculado à lease;
- sucesso somente após commit, push e confirmação do SHA remoto;
- validação de escopo novamente no resultado;
- seleção de exatamente uma lease ativa compatível;
- CLI para fingerprint, validação, heartbeat e execução publicada;
- resultados locais tratados somente como candidatos até validação pelo Control Plane.

Detalhes: `core/DURABLE_PROVIDER_AGENT.md`.

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

A suíte multiagent cobre, entre outros:

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
- fingerprints canônicos;
- leases confiáveis, expiradas e conflitantes;
- takeover depois da expiração;
- heartbeat e resultado sanitizados;
- recusa de identidade/hash/SHA divergente;
- CLI durável machine-readable;
- Merge Train por SHA/reviews;
- final gate draft/humano.

O workflow `Validate Multiagent Execution` executa compile, regressões estruturais, Execution Fabric e o gate multiagent.

## Ainda não homologado live

1. Gateway do Durable Provider Agent integrado ao Control Plane do `ecossistema-escola`.
2. Antigravity executando uma task real em profile/host isolado.
3. OpenCode/Ollama executando uma task real com modelo local.
4. Recovery real em outro executor depois de expiração de lease.
5. Health/fallback persistido automaticamente no GitHub.
6. CodeRabbit, Semgrep e Sonar conectados como checks reais do Merge Train.
7. Piloto live de integração multi-provider.
8. Escalonamento excepcional Codex auditado, sempre manual.

## Dependências externas conhecidas

No `ecossistema-escola`, GitHub Actions ainda não pode criar/aprovar PRs. A permissão administrativa precisa ser habilitada para que o runner crie sozinho futuros PRs finais draft. O merge final continuará humano mesmo depois disso.

CodeRabbit também informou que a revisão automática está desabilitada no repositório enquanto ele tiver menos de dez estrelas. Essa limitação externa não reduz os gates do Core; o Merge Train deve permanecer fail-closed até haver evidência real dos revisores exigidos ou uma política formal aprovada para o repositório.

## Próxima ordem de trabalho

1. integrar o gateway de leases/heartbeat/resultados no Control Plane;
2. homologar Antigravity;
3. homologar OpenCode/Ollama;
4. comprovar takeover entre executores;
5. persistir provider health/telemetria;
6. conectar CodeRabbit/Semgrep/Sonar reais;
7. executar piloto multi-provider;
8. manter Codex somente para exceção premium/manual.

## Regra de declaração

- **Implementado**: código e testes existem.
- **Comprovado**: passou em execução real com evidência durável.
- **Homologado**: passou repetidamente com CI, segurança e recovery.
- **Pronto**: todos os providers/gates necessários estão homologados e as dependências administrativas foram resolvidas.

Hoje, Jules API-first está comprovado; o runtime multi-provider e o protocolo durável estão implementados/testados; a Factory inteira ainda não está pronta.
