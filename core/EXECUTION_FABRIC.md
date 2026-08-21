# Execution Fabric

A Execution Fabric separa **o que precisa ser executado** de **qual agente/ferramenta executa**.

## Objetivo

Evitar dependência arquitetural de Codex, ChatGPT ou qualquer executor específico. A Factory descreve capacidades necessárias e escolhe o backend mais leve que consiga executar e provar o trabalho.

Ordem padrão:

1. `current_agent` — agente atual + ferramentas conectadas;
2. `github_ci` — GitHub Actions/CI para execução determinística;
3. `sandbox` — shell leve quando realmente disponível;
4. `local_full` — executor local/interativo completo (Codex ou equivalente).

Essa ordem é preferência, não dogma. Um backend incapaz nunca pode ser escolhido só por ser mais barato/leve.

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
- um gate falho interrompe a sequência para preservar evidência clara.

## Fallback

`engine/execution_engine.py` mantém histórico bounded em `.factory/execution.json`.

Depois do limite de falhas configurado para uma mesma ação/backend, aquele backend é temporariamente rejeitado na próxima decisão e a Factory tenta o próximo backend capaz disponível.

Isso é diferente do repair loop do Autonomy Engine:

- **repair loop** decide quantas vezes o trabalho pode ser corrigido antes de bloquear;
- **Execution Fabric** decide qual backend deve executar a próxima tentativa.

Os dois mecanismos se complementam.

## Interface interna

```text
python scripts/factory.py route implement
python scripts/factory.py route verify
python scripts/factory.py --backends current_agent,github_ci,sandbox route verify
python scripts/factory.py record-execution verify github_ci failure --need test
python scripts/factory.py execution-status
python scripts/factory.py gates
python scripts/factory.py run-gates
```

`next`, `resume` e `record` também retornam uma decisão `execution` automaticamente.

O usuário não deve precisar executar esses comandos manualmente; são o protocolo portátil entre agentes.

## Limites de segurança

A Fabric nunca deve:

- conceder secrets/permissões por inferência;
- executar texto livre de prompt como shell;
- escolher backend sem todas as capacidades obrigatórias;
- reduzir testes/Definition of Done para economizar recursos;
- transformar falha técnica comum em pergunta ao usuário antes de tentar reparo/fallback.
