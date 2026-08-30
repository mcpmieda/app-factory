# Multiagent Execution — estado final

Atualizado em 30 de agosto de 2026.

## Estado

A automação multiagente da App Factory está **finalizada no escopo suportado Jules + OpenCode/Ollama**.

Não existem novas homologações obrigatórias, pilotos pendentes ou passos futuros necessários para declarar este escopo concluído.

## Componentes preservados

O estado comprovado e mantido inclui:

- execução provider-neutral no escopo suportado;
- Jules API-first remoto;
- OpenCode/Ollama em execução controlada;
- paralelismo com `max_parallel` entre 1 e 3;
- dependências entre tasks;
- branches e PRs isolados;
- CI por SHA exato;
- retomada após restart;
- leases/resultados duráveis no GitHub;
- takeover entre executores quando aplicável;
- integração automática somente na integration branch;
- PR final draft e merge no target exclusivamente humano;
- Semgrep e CodeRabbit como evidências independentes já integradas ao Control Plane existente;
- Codex preservado somente como escalonamento manual/premium, nunca automático.

## Escopo encerrado

### Antigravity

A expansão para Antigravity foi encerrada sem homologação live. Ela não integra o escopo automático final e não deve ser selecionada por `scripts/factory_run.py`.

Artefatos internos antigos podem permanecer apenas por compatibilidade histórica enquanto não forem alcançáveis pela superfície suportada. Eles não representam funcionalidade pendente nem compromisso futuro.

### SonarQube Cloud

A homologação externa adicional de SonarQube Cloud deixou de ser requisito de conclusão da automação multiagente. A infraestrutura já existente pode permanecer como defesa adicional onde estiver configurada, mas não há passo futuro aberto associado à conclusão deste projeto.

## Provas canônicas preservadas

A Factory Run `jules-api-pilot-002` comprovou Jules remoto, paralelismo, dependências, retomada, branches/PRs isolados, CI exato e PR final humano.

A homologação OpenCode/Ollama v16 comprovou execução real, escrita limitada, commit/push controlado, confirmação do SHA remoto e CI exato.

A run `multi-provider-hosted-pilot-002` comprovou Jules + OpenCode/Ollama executando tasks independentes em paralelo e liberando uma task dependente após integração dos dois resultados.

Essas provas são históricas e não criam novos passos de trabalho.

## Contrato final

Providers automáticos suportados:

1. `opencode_ollama` — preferência zero-cost quando disponível;
2. `jules` — provider remoto suportado.

Escalonamento não automático:

- `codex` — manual, metered e explicitamente fora do fallback automático.

Provider retirado do escopo automático:

- `antigravity`.

## Regra operacional

A automação deve continuar usando as proteções existentes:

- escopo de arquivos fechado;
- paths protegidos fora do alcance de workers;
- branch de integração isolada;
- CI ligado ao SHA exato;
- nenhuma ativação de produção por worker;
- nenhuma ampliação automática de permissões;
- nenhuma fusão automática no target;
- estado durável no GitHub.

## Encerramento

O projeto de automação multiagente não possui roadmap residual. Novos providers, reviewers ou expansões futuras serão tratados como projetos novos, somente se houver nova decisão explícita.
