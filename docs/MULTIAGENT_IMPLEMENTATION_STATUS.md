# Multiagent Execution — estado de implementação

Atualizado em 27 de agosto de 2026.

## Classificação atual

A App Factory multiagente já possui prova operacional real para os blocos centrais:

- fundação provider-neutral;
- Jules API-first comprovado em execução real;
- OpenCode/Ollama comprovado e homologado em execução real;
- Factory Run mista Jules + OpenCode/Ollama comprovada de ponta a ponta;
- paralelismo real com `max_parallel=2` e task dependente liberada somente depois dos dois merges;
- protocolo durável baseado em GitHub;
- takeover entre executores comprovado depois da expiração de lease;
- branches/PRs isolados, CI por SHA exato e final PR draft/humano;
- GitHub Actions comprovadamente capaz de criar worker PRs e o PR final draft no repositório consumidor;
- Semgrep real integrado e fail-closed;
- CodeRabbit manual acionável, sujeito a rate limit externo;
- runtime Antigravity implementado/testado, ainda sem piloto live por depender de runner/profile externo;
- Sonar preparado no Merge Train, mas ainda dependente de configuração real do serviço.

A visão automática normal já funciona com Jules + OpenCode/Ollama. A declaração de “100% pronta” continua condicionada ao fechamento do Merge Train real com Sonar e à homologação live do Antigravity.

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

O PR consolidado `#93` foi posteriormente mesclado por decisão humana. Isso não amplia a autoridade automática da Factory sobre `main`.

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

### OpenCode/Ollama standalone

A homologação live v16, issue `#110` do `app-factory`, concluiu com sucesso no run `33125439929`.

Evidência principal:

- provider real: OpenCode `1.18.23` + Ollama `0.33.1` + `qwen3:0.6b`;
- inference real via Ollama native `POST /api/chat`;
- exatamente um `write` estruturado aceito e encaminhado;
- audit do bridge sem rejeições/upstream errors;
- arquivo validado byte a byte contra fixture imutável definida antes da execução;
- exatamente um path alterado;
- commit/push controlado e SHA remoto confirmado;
- CI por `workflow_dispatch` no SHA exato: run `33125552090` — `success`;
- nenhum merge no target, ativação de produção, ampliação de permissão ou execução Codex.

As versões v13–v15 permanecem como evidência do repair loop fail-closed e nunca foram reclassificadas retroativamente como sucesso.

### Factory Run real Jules + OpenCode/Ollama

A homologação final multi-provider foi executada no `mcpmieda/ecossistema-escola` pela parent issue `#112`, run id `multi-provider-hosted-pilot-002`.

Topologia real:

```text
#113 OpenCode/Ollama ─┐
                     ├─> #115 Jules verifier
#114 Jules API-first ─┘
```

Contrato:

- `max_parallel=2`;
- OpenCode e Jules independentes liberados simultaneamente;
- task `verify` bloqueada até os dois resultados estarem materialmente integrados;
- integração isolada `factory/multi-provider-hosted-pilot-002`;
- target `main` fora da autoridade automática;
- produção, Banco de Notas e Codex fora do escopo.

Evidência OpenCode `#113`:

- executor GitHub-hosted;
- probe real saudável;
- branch durável sibling sem colisão de namespace;
- lease bot-authored;
- provider result `success`;
- commit/push `25adb91a9bfa86c3f60002e78e12976c22f7412e`;
- exatamente um path alterado;
- exact-SHA CI `33133753826` — `success`;
- worker PR `#116` squash-merged somente na integration branch.

Evidência Jules `#114`:

- sessão Jules REST real;
- worker PR `#117` passou CI obrigatório;
- squash merge somente na mesma integration branch.

Evidência dependente `#115`:

- permaneceu `waiting` até #113 e #114 estarem integradas;
- sessão Jules criada somente após a liberação das dependências;
- worker PR `#119` passou CI obrigatório;
- merge SHA da integration branch `1de720f36729b0c36b3f459242a6312286d6a92e`.

Fechamento da run:

- job multi-provider `33133633332` concluiu `success`;
- integration CI final `33134149253` concluiu `success`;
- o bot criou o PR final `#120`, `factory/multi-provider-hosted-pilot-002 -> main`;
- PR `#120` permanece **DRAFT**, rotulado `factory:final`;
- o corpo registra explicitamente que é o human gate e que a Factory não fará o merge no target.

Isto encerra a antiga pendência “provar uma Factory Run com mais de um provider automático”.

## Repair loop do hosted OpenCode no Ecossistema

A prova mista também encontrou e corrigiu, sem relaxar guardrails:

1. **Schema do health probe** — o provider real reportava `provider`, enquanto o executor lia somente `provider_id`. PR `#109` normalizou a fronteira confiável mantendo provider/status estritos.
2. **Namespace de Git refs** — `factory/<run>` não pode coexistir com `factory/<run>/<task>`. PR `#110` adotou workers sibling `factory/<run>-<task>` com regressão.
3. **Fixture Markdown da v1** — o provider escreveu o conteúdo pedido, mas Prettier rejeitou apenas newline terminal ausente. O resultado não foi adulterado nem reclassificado; a v2 definiu previamente um fixture `.txt`, fora do domínio do formatter, e passou todos os gates.

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

### Provider Runtime / Durable Agent

- request e manifesto frozen/validados;
- fingerprint portátil;
- health `healthy/degraded/unavailable/unknown`;
- ambiente sanitizado e profiles dedicados;
- lease vinculada a run/task/issue/provider/executor/branches/hashes;
- confiança somente em lease bot-authored válida;
- expiração/takeover fail-closed;
- heartbeat sem renovação implícita;
- resultado terminal vinculado à lease;
- provider sem autoridade para merge no target;
- escopo protegido e Git mutável fail-closed;
- commit/push apenas de worker branch;
- confirmação remota do SHA;
- telemetria sanitizada.

### Antigravity

O adapter está implementado/testado com CLI headless, profile isolado obrigatório e sem bypass de permissões.

O piloto live continua materializado na issue `#65`, mas depende de:

- runner efêmero/fresh Linux x64 dedicado;
- labels `self-hosted`, `Linux`, `X64`, `factory-antigravity`, `ephemeral`;
- `agy`, Git e Python instalados;
- `ANTIGRAVITY_PROFILE_HOME` autenticado e dedicado, fora de qualquer worktree;
- destruição/reprovisionamento do runner depois da prova.

A ausência desses pré-requisitos deve continuar falhando fechado.

## Merge Train

Contrato lógico vigente:

- worker PR limitado à integration branch;
- CI exato por SHA/evento;
- escopo obrigatório;
- Semgrep, Sonar e CodeRabbit no mesmo SHA;
- revisão bloqueadora impede merge;
- evidência stale é inválida;
- PR final draft;
- target auto-merge sempre proibido.

Estado real:

- **Semgrep**: real, integrado, já encontrou findings reais e comprovou repair loop;
- **CodeRabbit**: comando manual funciona, mas o serviço pode responder `rate limited`; isso deve falhar fechado;
- **Sonar**: workflow fail-closed preparado, ainda precisa das credenciais/configuração reais do serviço;
- **Control Plane consumidor**: hardening do gate confiável está sendo fechado no PR `mcpmieda/ecossistema-escola#118`, após o CodeRabbit ter corretamente rejeitado o desenho anterior em que o worker executava o código de sua própria aprovação.

O desenho seguro do PR `#118` move a autoridade para código de `main`, usa reviewer evidence bot-authored por SHA e trata o worker como dado não confiável.

## Dependências externas restantes

### Antigravity

Runner/profile descritos na issue `#65`. Credenciais nunca devem ir para issue, workflow input ou chat.

### Sonar

O repositório consumidor precisa de configuração real de SonarQube Cloud:

- repository variable `SONAR_PROJECT_KEY`;
- repository variable `SONAR_ORGANIZATION`;
- repository secret `SONAR_TOKEN`.

O gate deve falhar, e não pular Sonar, enquanto esses valores não existirem.

### CodeRabbit

O mecanismo manual foi comprovado, mas disponibilidade/rate limit é controlada pelo serviço externo. O gate não deve fabricar sucesso quando o reviewer estiver indisponível.

## Dependências que NÃO são mais bloqueadores

A antiga documentação dizia que GitHub Actions não podia criar/aprovar PRs. Essa afirmação não é mais válida para a criação de PRs:

- hosted OpenCode criou worker PR `#116`;
- Jules criou worker PRs `#117` e `#119`;
- o bot criou o PR final draft `#120`.

Portanto, criação autônoma de PR está comprovadamente habilitada. O **merge final em `main` continua humano por design**, não por limitação administrativa.

## Ainda não homologado live

1. Antigravity executando uma task real no runner/profile isolado exigido.
2. Sonar fornecendo evidence real no Merge Train.
3. Merge Train completo Semgrep + Sonar + CodeRabbit passando em um worker real depois do hardening confiável do Control Plane.

O piloto multi-provider já não pertence a esta lista: está concluído.

## Regra de declaração

- **Implementado**: código e testes existem.
- **Comprovado**: passou em execução real com evidência durável.
- **Homologado**: passou no contrato live definido, com CI e guardrails preservados.
- **Pronto**: todos os providers/gates considerados obrigatórios para a visão completa estão homologados e dependências externas resolvidas.

Hoje a Factory é operacional com **Jules + OpenCode/Ollama**, inclusive em uma mesma run durável com paralelismo, dependências, recovery, CI por SHA exato e PR final humano. O que impede a declaração de 100% da visão ampliada está concentrado em **Antigravity live + Sonar real + fechamento do Merge Train completo**.
