# Execution Fabric

A Execution Fabric separa **o que precisa ser executado** de **qual agente/ferramenta executa**.

## Objetivo

Evitar dependência arquitetural de Codex, ChatGPT ou qualquer executor específico. A Factory descreve capacidades necessárias e escolhe um backend capaz, verificável e tão leve quanto possível.

Ordem baseline:

1. `current_agent` — agente atual + ferramentas conectadas;
2. `github_ci` — GitHub Actions/CI para execução determinística;
3. `sandbox` — shell leve quando realmente disponível;
4. `local_full` — executor local/interativo completo (Codex ou equivalente).

Essa ordem é preferência, não dogma. Um backend incapaz nunca pode ser escolhido só por ser mais barato/leve. Na V1.3, o Learning Engine pode otimizar a ordem apenas entre candidatos já elegíveis.

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
- Playwright headless;
- serviços efêmeros de teste;
- migrations em ambiente descartável;
- validadores do repositório.

O adaptador em `engine/ci_executor.py` descobre apenas gates declarados no repositório e pertencentes a uma allowlist. O conteúdo de prompt nunca vira comando de shell.

Por padrão:

- `shell=False` no executor Python;
- nenhuma credencial/secret é necessária;
- comandos são construídos a partir de IDs conhecidos, não do valor textual de scripts recebido do usuário;
- instalação de dependências só é proposta quando existe lockfile compatível; `package.json` sem lockfile não recebe `npm install` permissivo como fallback;
- um gate falho interrompe a sequência para preservar evidência clara.

## Independent Verification

`core/INDEPENDENT_VERIFICATION.md` usa esta Fabric para separar ainda mais implementação de prova.

Quando a matriz selecionar `independent`, `adversarial` ou `release`, `github_ci` é o executor preferido porque pode iniciar um ambiente limpo e rodar motores determinísticos que não dependem do julgamento da IA atual, por exemplo:

- Semgrep Community Edition e Trivy;
- StrykerJS/mutmut;
- Schemathesis;
- OWASP ZAP em alvo efêmero/autorizado;
- axe-core/Playwright;
- Lighthouse CI quando houver baseline estável.

Esses motores continuam sendo **gates do projeto**, não novos backends de raciocínio. A Execution Fabric escolhe onde executá-los; `engine/independent_verification.py` decide quais são proporcionais ao risco/arquitetura.

Se GitHub-hosted capacity não estiver disponível ou puder gerar custo não autorizado, a Factory pode usar runner self-hosted/local equivalente. Não deve contratar scanner/SaaS pago ou reduzir o gate silenciosamente para economizar recursos.

Um scanner determinístico não conta como `independent-agent` de Semantic Verification. Ele produz evidência técnica independente, mas não entende sozinho a intenção do produto.

## Fallback da tarefa

`engine/execution_engine.py` mantém histórico bounded em `.factory/execution.json`. Esse arquivo é cache operacional local e fica fora do Git por padrão.

O fallback é escopado pela tarefa autônoma atual (`task_key`). Depois do limite de falhas configurado para uma mesma tarefa + ação + backend, aquele backend é temporariamente rejeitado e a Factory tenta o próximo backend capaz disponível. Falhas de uma tarefa antiga não penalizam uma tarefa nova.

Isso é diferente do repair loop do Autonomy Engine:

- **repair loop** decide quantas vezes o trabalho pode ser corrigido antes de bloquear;
- **Execution Fabric** decide qual backend deve executar a próxima tentativa.

## Learning Engine

Depois de capacidade, disponibilidade, fallback da tarefa e guardrails de segurança/risco, a V1.3 pode consultar `engine/learning_engine.py`.

O aprendizado:

- usa apenas metadados técnicos allowlisted e locais;
- exige amostra mínima antes de alterar a ordem baseline;
- pode reordenar somente backends já elegíveis;
- não ressuscita backend rejeitado;
- não promove `local_full` sobre backend leve capaz somente por score;
- retorna explicação e permite comparar com `--no-learning`.

Consulte `core/LEARNING_ENGINE.md` para o contrato completo.

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

`next`, `resume` e `record` também retornam uma decisão `execution` automaticamente. A CLI deriva `task_key` do estado atual do Autonomy Engine quando disponível.

A decisão automática usa as capacidades padrão da fase. Quando a tarefa tiver exigência adicional conhecida — como browser interativo ou migration real — o agente deve refinar a rota com essas capacidades antes de executar.

O usuário não deve precisar executar esses comandos manualmente; são o protocolo portátil entre agentes.

## Limites de segurança

A Fabric nunca deve:

- conceder secrets/permissões por inferência;
- executar texto livre de prompt como shell;
- escolher backend sem todas as capacidades obrigatórias;
- deixar aprendizado ultrapassar incapacidade/fallback/risco;
- reduzir testes/Definition of Done para economizar recursos;
- transformar falha técnica comum em pergunta ao usuário antes de tentar reparo/fallback;
- tratar scanner não executado como sucesso;
- apontar fuzz/DAST ativo para produção por inferência.
