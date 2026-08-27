# Multiagent Execution — estado de implementação

Atualizado em 27 de agosto de 2026.

## Classificação atual

A App Factory possui:

- fundação provider-neutral;
- Jules API-first comprovado em execução real;
- OpenCode/Ollama comprovado em execução real, com `write`, commit, push, SHA remoto e CI exato;
- runtime Antigravity implementado/testado, ainda sem piloto live por depender de runner/profile externo;
- protocolo de executor durável baseado em GitHub;
- takeover entre executores comprovado em execução real depois da expiração de lease;
- contrato de Merge Train por SHA exato;
- Semgrep real em fase de integração e CodeRabbit manual comprovadamente acionável;
- Sonar ainda não conectado como evidência real.

A Factory multi-provider ainda não deve ser declarada 100% pronta. O que falta está concentrado na homologação Antigravity, no fechamento do Merge Train real e em um piloto final usando mais de um provider.

## Comprovado em execução real

### Jules API-first

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
- PR final draft e humano.

O PR consolidado `#93` foi posteriormente mesclado por decisão humana e o pipeline normal do repositório ficou verde. Isso não amplia a autoridade automática da Factory sobre `main`.

### Takeover entre executores

A issue `#72` (`durable-takeover-proof-001`) comprovou com dois runners GitHub-hosted distintos:

- fingerprints imutáveis idênticos nos dois executores;
- Lease A válida somente para executor A;
- rejeição de B enquanto A mantinha lease ativa;
- heartbeat sem extensão da expiração;
- expiração real da Lease A;
- nova Lease B para executor B com as mesmas identidades de run/task/request/manifest/branches;
- rejeição de A contra Lease B;
- autorização de B contra Lease B;
- estado durável vindo de GitHub, não de cache, stdout ou sessão local.

### OpenCode/Ollama

A homologação live v16, issue `#110`, concluiu com sucesso no run `33125439929`.

Evidência principal:

- trusted `main` SHA de origem: `4ba942bd80ad2adfa866573da886456d32f6bcce`;
- provider real: OpenCode `1.18.23` + Ollama `0.33.1` + `qwen3:0.6b`;
- inference real via Ollama native `POST /api/chat`;
- exatamente um `write` estruturado aceito e encaminhado;
- audit do bridge: `accepted=1`, `forwarded=1`, `upstream_tool_calls=1`, `responses_normalized=1`, `post_tool_requests=1`, `post_tool_completions=1`, `rejected=0`, `upstream_errors=0`;
- arquivo do provider validado byte a byte contra fixture imutável definida antes da execução;
- exatamente um path alterado: `pilots/live/opencode-ollama/run-33125439929-1.md`;
- branch publicada: `factory/opencode-ollama-live-33125439929-1`;
- commit/SHA remoto exato: `766b14a8e4a133a431902fdc355125648adb837a`;
- CI por `workflow_dispatch` no SHA exato: run `33125552090` — `success`;
- artifact sanitizado: `opencode-ollama-live-pilot-33125439929-1`, digest `sha256:4acd3c21ada29c45673023abe286cd10a480f16c66428ef6c67e53362371ee46`;
- nenhum merge no target, ativação de produção, ampliação de permissão ou execução Codex ocorreu.

As versões anteriores v13–v15 permanecem como evidência do repair loop fail-closed. V13 já havia provado `write + commit + push`, mas divergira somente no newline terminal do fixture; v14 não produziu tool call; v15 produziu uma moldura literal no conteúdo. Nenhuma dessas tentativas foi reclassificada retroativamente como sucesso.

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

O piloto live está materializado na issue `#65`, mas permanece bloqueado até existir runner efêmero self-hosted e profile Antigravity autenticado dedicado. A ausência desses pré-requisitos deve continuar falhando fechado, sem fallback silencioso.

### OpenCode/Ollama adapter

- CLI `opencode run` não interativa;
- apenas Ollama loopback;
- modelo explícito;
- profile isolado obrigatório;
- permission config por path/comando;
- web/external directory/subagents/skills negados;
- Git mutável negado;
- repo-provided OpenCode config recusada;
- plugins/configs externas desabilitados;
- bridge native single-write bounded, com auditoria sanitizada;
- homologação live v16 concluída.

### Merge Train

Contrato Core vigente:

- worker PR limitado à integration branch;
- CI exato por SHA/evento;
- escopo obrigatório;
- CodeRabbit, Semgrep e Sonar requeridos no mesmo SHA;
- revisão bloqueadora impede merge;
- PR final draft;
- target auto-merge sempre proibido.

Estado operacional em 27/08/2026:

- Semgrep: workflow/check real criado e executado; primeiro scan encontrou findings reais e o repair loop corrigiu as causas sem suppressions. Integração final ainda deve ficar verde e ser propagada ao repositório consumidor;
- CodeRabbit: comando manual `@coderabbitai full review` foi aceito e iniciou revisão real; está sendo testado também o disparo por `github-actions[bot]`;
- Sonar: ainda sem check real conectado;
- o Control Plane consumidor ainda precisa exigir os reviewers reais antes do squash na integration branch; hoje o gate operacional comprovado é o CI exato.

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

1. Antigravity executando uma task real em profile/host isolado.
2. Sonar conectado como check real do Merge Train.
3. Merge Train operacional do Control Plane exigindo todos os reviewers previstos no contrato.
4. Piloto live de integração multi-provider, usando mais de um provider na mesma Factory Run.
5. Escalonamento excepcional Codex auditado, se algum dia necessário; continua manual e não é requisito para o caminho automático normal.

## Dependências externas conhecidas

No `ecossistema-escola`, a documentação vigente registra que GitHub Actions não pode criar/aprovar PRs. Enquanto a configuração administrativa não for alterada, criação autônoma de worker/final PR pode falhar fechada; o merge final continuará humano mesmo depois da habilitação.

Antigravity depende de um runner efêmero e profile autenticado dedicados, descritos na issue `#65`. Credenciais desse profile nunca devem ir para issue, workflow input ou chat.

Sonar ainda precisa de conexão/configuração real antes de poder fornecer evidência de reviewer no Merge Train.

## Próxima ordem de trabalho

1. concluir e integrar Semgrep real no Core e no `ecossistema-escola`;
2. provar se CodeRabbit aceita solicitação feita pelo `github-actions[bot]` e automatizar o disparo quando possível;
3. implementar no Control Plane a cobrança dos reviewers por SHA exato;
4. conectar Sonar;
5. homologar Antigravity no runner/profile externo exigido;
6. executar uma Factory Run multi-provider final;
7. manter Codex somente para exceção premium/manual.

## Regra de declaração

- **Implementado**: código e testes existem.
- **Comprovado**: passou em execução real com evidência durável.
- **Homologado**: passou no contrato live definido, com CI e guardrails preservados.
- **Pronto**: todos os providers/gates necessários estão homologados e as dependências administrativas foram resolvidas.

Hoje, Jules API-first e OpenCode/Ollama estão comprovados em execução real; takeover entre executores está comprovado; o runtime multi-provider e o protocolo durável estão integrados. A Factory inteira ainda não está pronta por causa de Antigravity, Sonar, enforcement operacional completo do Merge Train e do piloto multi-provider final.
