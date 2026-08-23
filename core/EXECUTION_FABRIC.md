# Execution Fabric

A Execution Fabric separa **o que precisa ser executado** de **qual agente/ferramenta executa**.

## Objetivo

Evitar dependência arquitetural de Codex, ChatGPT ou qualquer executor específico. A Factory descreve capacidades necessárias e escolhe um backend capaz, verificável e tão leve quanto possível.

Ordem baseline:

1. `current_agent` — agente atual + ferramentas conectadas;
2. `github_ci` — GitHub Actions/CI para execução determinística;
3. `sandbox` — shell leve quando realmente disponível;
4. `local_full` — executor local/interativo completo (Codex ou equivalente).

Essa ordem é preferência, não dogma. Backend incapaz nunca pode ser escolhido só por ser mais barato/leve. Learning Engine pode otimizar a ordem apenas entre candidatos já elegíveis.

## Capacidades

O núcleo trabalha com capacidades como:

- `reasoning`;
- `repo_read` / `repo_write`;
- `github_api`;
- `deterministic_commands`;
- `build` / `test`;
- `headless_browser`;
- `ephemeral_services`;
- `interactive_shell` / `interactive_browser`;
- `local_services`;
- `live_migration`.

Adaptadores futuros podem mapear essas capacidades para qualquer ferramenta sem mudar o Core.

## Current-agent first

Múltiplos arquivos, build e testes não são motivo suficiente para handoff.

Se o agente atual consegue editar/revisar pelo GitHub e o CI consegue provar o resultado, ele deve permanecer responsável pelo ciclo:

`editar → CI → ler falha → corrigir → CI → revisar → entregar`.

## GitHub Actions como executor

`github_ci` é um backend real para trabalho reproduzível e não interativo.

Pode cobrir:

- lint/format/typecheck;
- unit/integration tests;
- builds;
- Playwright headless/cross-browser;
- serviços efêmeros de teste;
- migrations em ambiente descartável e migration-safety lint;
- validadores do repositório;
- property/stateful/combinatorial tests;
- scanners de segurança/supply-chain;
- mutation testing;
- API fuzz/stateful testing;
- DAST em alvo efêmero;
- load testing em alvo controlado;
- fault-injection por proxy/stub controlado;
- solvers/model checkers formais reproduzíveis.

O adaptador em `engine/ci_executor.py` descobre apenas gates declarados no repositório e pertencentes a uma allowlist. O conteúdo de prompt nunca vira comando de shell.

Por padrão:

- `shell=False` no executor Python;
- nenhuma credencial/secret é necessária;
- comandos são construídos a partir de IDs conhecidos, não do texto livre do usuário;
- instalação de dependências só é proposta quando existe lockfile compatível;
- um gate falho interrompe a sequência para preservar evidência clara.

## Independent Verification

`core/INDEPENDENT_VERIFICATION.md` usa esta Fabric para separar implementação de prova.

Quando a matriz selecionar `independent`, `adversarial` ou `release`, `github_ci` é executor preferido porque pode iniciar ambiente limpo e rodar motores determinísticos independentes do julgamento da IA atual.

A matriz pode incluir, somente quando houver pré-condição real:

- Trivy / Semgrep CE ou substituto validado;
- StrykerJS/mutmut;
- Schemathesis e, como escalonamento, RESTler;
- OWASP ZAP;
- axe-core/Playwright e matriz Chromium/Firefox/WebKit;
- Lighthouse CI;
- actionlint / zizmor para verificar o próprio GitHub Actions;
- Hypothesis / fast-check;
- NIST ACTS ou covering-array equivalent;
- Squawk;
- dependency-cruiser/equivalente;
- k6;
- Toxiproxy/equivalente.

Esses motores são **gates do projeto**, não novos backends de raciocínio. A Execution Fabric escolhe onde executá-los; `engine/independent_verification.py` decide quais são proporcionais ao risco e às superfícies do projeto.

O CI que executa os outros gates também deve ser verificável: actionlint cobre correção estrutural do workflow e zizmor cobre riscos de segurança do GitHub Actions quando selecionados.

Se GitHub-hosted capacity não estiver disponível ou puder gerar custo não autorizado, a Factory pode usar runner self-hosted/local equivalente. Não deve contratar scanner/SaaS pago nem reduzir gate silenciosamente.

Scanner/fuzzer/solver determinístico não conta como `independent-agent` de Semantic Verification. Produz evidência técnica, mas não entende sozinho a intenção.

## Provas agressivas e alvos seguros

- ZAP ativo, RESTler fuzz profundo, Schemathesis destrutivo, k6 e Toxiproxy nunca inferem produção/terceiro como alvo;
- load usa preview/test env controlado, salvo autorização explícita para outro alvo;
- Toxiproxy degrada conexão via proxy/stub controlado, não o provedor externo;
- checks caros podem migrar para release/nightly;
- ferramenta required indisponível não vira `pass`.

## Fallback da tarefa

`engine/execution_engine.py` mantém histórico bounded em `.factory/execution.json`, cache operacional local fora do Git por padrão.

O fallback é escopado pela tarefa atual (`task_key`). Depois do limite de falhas para tarefa + ação + backend, aquele backend é temporariamente rejeitado e a Factory tenta o próximo capaz. Falhas antigas não penalizam tarefa nova.

Isso difere do repair loop:

- **repair loop** decide quantas correções são permitidas antes de bloquear;
- **Execution Fabric** decide qual backend executa a próxima tentativa.

## Learning Engine

Depois de capacidade, disponibilidade, fallback e guardrails de segurança/risco, a Factory pode consultar `engine/learning_engine.py`.

O aprendizado:

- usa somente metadados técnicos locais/allowlisted;
- exige amostra mínima antes de alterar baseline;
- reordena somente backends já elegíveis;
- não ressuscita backend rejeitado;
- não promove `local_full` sobre backend leve capaz só por score;
- retorna explicação e permite comparar com `--no-learning`.

Consulte `core/LEARNING_ENGINE.md`.

## Interface interna

```text
python scripts/factory.py route implement
python scripts/factory.py route verify
python scripts/factory.py route verify --no-learning
python scripts/factory.py --backends current_agent,github_ci,sandbox route verify
python scripts/factory.py record-execution verify github_ci failure
python scripts/factory.py execution-status
python scripts/factory.py learning-status
python scripts/factory.py learning-recommend verify
python scripts/factory.py gates
python scripts/factory.py run-gates
python scripts/independent_verification.py --root <projeto> --risk high --system-level multi-user-system
```

Quando integrações externas forem materialmente relevantes, o agente pode acrescentar `--external-integrations` ao planner de Independent Verification.

`next`, `resume` e `record` também retornam decisão `execution` automaticamente. A CLI deriva `task_key` do estado do Autonomy Engine quando disponível.

O usuário não precisa executar esses comandos manualmente; são protocolo portátil entre agentes.

## Limites de segurança

A Fabric nunca deve:

- conceder secrets/permissões por inferência;
- executar texto livre de prompt como shell;
- escolher backend sem capacidades obrigatórias;
- deixar aprendizado ultrapassar incapacidade/fallback/risco;
- reduzir testes/Definition of Done para economizar recursos;
- transformar falha técnica comum em pergunta ao usuário antes de tentar reparo/fallback;
- tratar scanner/fuzzer/model checker não executado como sucesso;
- apontar fuzz/DAST/load/fault injection para produção ou terceiro por inferência.
