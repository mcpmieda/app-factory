# Multiagent Execution — estado de implementação

Atualizado em 28 de agosto de 2026.

## Classificação atual

A App Factory multiagente já é operacional com **Jules + OpenCode/Ollama** e possui prova real de:

- execução provider-neutral;
- paralelismo (`max_parallel=2`);
- dependências entre tasks;
- branches e PRs isolados;
- CI por SHA exato;
- recuperação após restart;
- takeover entre executores após expiração de lease;
- integração automática somente na integration branch;
- PR final draft e decisão humana no target;
- criação autônoma de worker PRs e PR final pelo GitHub Actions;
- Semgrep real e fail-closed;
- CodeRabbit vinculado ao SHA exato, inclusive no formato real de zero findings;
- Control Plane confiável executando autoridade a partir de `main` e tratando o worker como dado não confiável.

A visão ampliada ainda não deve ser declarada 100% homologada porque faltam somente duas provas externas:

1. SonarQube Cloud real fechando o Merge Train completo;
2. Antigravity live em runner Linux x64 efêmero com profile autenticado isolado.

## Provas concluídas

### Jules API-first

No `mcpmieda/ecossistema-escola`, a Factory Run `jules-api-pilot-002` comprovou duas tasks Jules paralelas, task dependente, branches/PRs isolados, retomada de `factory:ci`, ausência de sessão duplicada, CI exato e PR final humano. O PR consolidado `#93` foi posteriormente mesclado por decisão humana.

### Takeover entre executores

A issue `mcpmieda/app-factory#72` comprovou:

- Lease A exclusiva do executor A;
- rejeição de B enquanto A estava válida;
- heartbeat sem extensão implícita;
- expiração real da Lease A;
- Lease B para executor B com os mesmos fingerprints imutáveis;
- rejeição posterior de A;
- continuidade baseada em estado durável do GitHub, sem cache/local session.

### OpenCode/Ollama

A homologação live v16 (`app-factory#110`) concluiu com sucesso:

- OpenCode `1.18.23`;
- Ollama `0.33.1`;
- `qwen3:0.6b`;
- inferência real via `/api/chat`;
- exatamente um `write` estruturado;
- validação byte a byte;
- um único path alterado;
- commit/push controlado;
- SHA remoto confirmado;
- exact-SHA CI verde;
- zero Codex, zero merge no target e zero ativação de produção.

### Factory Run real Jules + OpenCode/Ollama

A run `multi-provider-hosted-pilot-002` no `ecossistema-escola` comprovou:

```text
OpenCode/Ollama ─┐
                 ├─> Jules verifier
Jules API-first ─┘
```

- `max_parallel=2`;
- workers independentes liberados simultaneamente;
- verifier bloqueado até os dois resultados estarem integrados;
- hosted OpenCode e Jules reais;
- exact-SHA CI por worker;
- squash somente na integration branch;
- CI consolidado da integration branch;
- PR final `#120` criado automaticamente como **DRAFT** para `main`;
- target merge permanece humano.

Isso encerra a antiga pendência “provar uma Factory Run com mais de um provider automático”.

## Runtime e autoridade

### Planner

- DAG de tasks/dependências;
- waves paralelas;
- serialização por conflito de path;
- `max_parallel` entre 1 e 3;
- política de provider `zero -> free_quota -> included -> metered`;
- Codex `automatic=false`;
- human gates.

### Durable provider runtime

- request/manifesto imutáveis e validados;
- fingerprint portátil;
- lease bot-authored ligada a run/task/issue/provider/executor/branches/hashes;
- expiração/takeover fail-closed;
- heartbeat sem renovar autoridade;
- resultado terminal vinculado à lease;
- ambiente sanitizado e profiles dedicados;
- proteção de paths/Git metadata;
- commit/push apenas da worker branch;
- confirmação remota do SHA;
- workers sem autoridade sobre target/produção.

## Merge Train confiável

Contrato vigente no `mcpmieda/ecossistema-escola`:

- worker PR aponta somente para uma integration branch Factory;
- CI obrigatório por SHA exato;
- Semgrep + Sonar + CodeRabbit precisam validar o mesmo SHA;
- evidência stale ou ausente falha fechado;
- autoridade do gate vem de código confiável de `main`;
- PR final permanece draft/humano;
- target auto-merge é proibido.

### Estado real dos reviewers

**Semgrep**

- integrado e executado de verdade;
- já encontrou findings reais durante o desenvolvimento;
- repair loop corrigiu as causas sem `nosemgrep`/suppressions;
- evidence SHA-bound está operacional.

**CodeRabbit**

- integração real comprovada;
- o gate reconhece review submissions com findings/zero findings;
- também reconhece o comportamento real em que CodeRabbit atualiza seu comentário `recent_review` sem criar nova review submission quando existem zero actionable comments;
- essa forma alternativa só é aceita se for bot-authored, contiver a seção limitada `recent_review`, declarar zero actionable comments e terminar no SHA exato esperado;
- skip, indisponibilidade, rate limit, SHA errado e findings continuam falhando fechado.

**SonarQube Cloud**

A infraestrutura confiável foi concluída no `ecossistema-escola`:

- PR `#132` foi mesclado no commit `52beeaace9a4ee673c057bdc25f78c791e94e32c`;
- `infra/factory/configure-sonar-merge-train.ps1` automatiza criação/validação do projeto, repository variables, secret, baseline de `main`, Sonar do worker e o CI final da Factory;
- `sonar-main-baseline.yml` fixa a primeira análise em um SHA atual de `main`;
- `merge-train-sonar.yml` valida o worker SHA real e usa a baseline estável de `main`;
- SonarScanner CLI é pinado por versão e SHA-256;
- PowerShell, actionlint, policy, zizmor, Semgrep e CI geral ficaram verdes antes do merge.

A única dependência Sonar restante é externa: existir uma organização SonarQube Cloud e um token válido. O token nunca deve ir para issue, workflow input ou chat.

Execução prevista no repositório consumidor:

```powershell
pwsh ./infra/factory/configure-sonar-merge-train.ps1 -Organization '<SONAR_ORG>'
```

O script solicita `SONAR_TOKEN` de forma não exibida e executa as provas restantes. Se o serviço/plano não suportar a análise exigida, o gate deve continuar falhando fechado.

## Antigravity

O adapter e o fluxo live estão implementados/testados. A prova canônica é `app-factory#115` (`antigravity-live-pilot-002`); a antiga issue `#65` foi superseded porque o par original de refs colidia no namespace Git.

### Workflow live preparado

`.github/workflows/live-antigravity-pilot.yml` separa credenciais em dois estágios:

**Provider stage — self-hosted efêmero**

- labels obrigatórias `self-hosted`, `Linux`, `X64`, `factory-antigravity`, `ephemeral`;
- job permissions `{}`;
- checkout público sem credential helper;
- `GITHUB_TOKEN`, `GH_TOKEN` e `FACTORY_GITHUB_TOKEN` proibidos no ambiente do provider;
- `ANTIGRAVITY_PROFILE_HOME` autenticado, dedicado e fora do worktree;
- `agy` roda pelo provider runtime bounded;
- nenhuma publicação GitHub;
- artifact contém somente `provider.bundle` + `stage-record.json` sanitizado.

**Trusted publisher — GitHub-hosted**

- começa somente depois do provider terminar;
- confere digest, contexto, histórico, ancestry, path scope e credential patterns;
- cria refs isoladas somente após validação;
- publica worker commit;
- exact-SHA CI do worker;
- squash somente na integration branch;
- exact-SHA CI da integration branch;
- cria PR final **DRAFT** para `main`;
- para antes de qualquer merge no target ou produção.

### Bootstrap PowerShell do runner

Este estado adiciona `scripts/bootstrap-antigravity-runner.ps1`, feito para um host/VM/WSL Linux x64 dedicado e descartável. O script:

- rejeita root, plataforma/arquitetura erradas e homes com credenciais GitHub persistentes conhecidas;
- exige `ptrace_scope >= 1` quando Yama está disponível;
- valida `agy`, Git e Python;
- cria/valida profile Antigravity isolado e `chmod 700`;
- pode abrir o login interativo do `agy` somente no profile dedicado;
- autentica `gh` em `GH_CONFIG_DIR` temporário;
- registra runner **ephemeral** com labels obrigatórias;
- usa GitHub Actions runner oficial `v2.337.0` pinado por SHA-256 `70920811a4f8ad4328818682bca5c6469c1c942fab52448868071d0063816613`;
- recusa runner `factory-antigravity` concorrente/stale;
- grava somente a variável `ANTIGRAVITY_PROFILE_HOME` no repositório;
- dispara `/run-antigravity-v2` somente quando solicitado;
- destrói a credencial temporária do GitHub **antes** de iniciar o runner/provider;
- inicia o runner com HOME/XDG temporários e sem tokens GitHub do bootstrap;
- espera apenas o provider-stage efêmero;
- depois disso o publisher continua duravelmente no GitHub-hosted runner;
- restaura o shell local e remove o diretório temporário do runner no cleanup.

A CI `validate-factory.yml` valida a sintaxe desse PowerShell com o parser real do `pwsh`, mas não executa o bootstrap nem cria runner durante CI.

### Dependência externa ainda necessária

O piloto live continua dependendo de um host Linux x64 realmente disponível e de login interativo do Antigravity. Isso não pode ser fabricado pelo GitHub-hosted Control Plane sem quebrar a separação de credenciais.

No host dedicado, a execução prevista é:

```powershell
pwsh ./scripts/bootstrap-antigravity-runner.ps1 -AuthenticateProfile -RunPilot
```

O usuário conclui apenas os logins interativos. Depois que o provider-stage termina, o computador local deixa de ser necessário e o publisher segue pelo GitHub.

## Dependências que NÃO são mais bloqueadores

- criação autônoma de worker PRs;
- criação do PR final draft;
- Jules live;
- OpenCode/Ollama live;
- paralelismo multi-provider;
- recovery/restart;
- cross-executor takeover;
- Semgrep real;
- hardening confiável do Merge Train (`ecossistema-escola#118` mesclado);
- comportamento CodeRabbit zero-findings (`ecossistema-escola#131` mesclado);
- infraestrutura Sonar/PowerShell (`ecossistema-escola#132` mesclado).

## Ainda não homologado live

1. SonarQube Cloud fornecendo evidence real e o Merge Train completo Semgrep + Sonar + CodeRabbit passando no worker #126 (ou novo head equivalente).
2. Antigravity executando a task real de `app-factory#115` no runner/profile isolado exigido.

Esses são bloqueios externos de homologação, não lacunas fundamentais da arquitetura.

## Regra de declaração

- **Implementado**: código e testes existem.
- **Comprovado**: passou em execução real com evidência durável.
- **Homologado**: passou no contrato live definido, com CI e guardrails preservados.
- **Pronto**: todos os providers/gates obrigatórios da visão ampliada estão homologados; o merge final no target continua humano por design.

Hoje a Factory é operacional com **Jules + OpenCode/Ollama**. Para declarar a visão ampliada 100% homologada faltam apenas **Sonar real + Antigravity live**.
