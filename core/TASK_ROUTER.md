# Task Router — escolha de executor

A Factory escolhe o executor pela **capacidade necessária para provar o trabalho**, não pela palavra "código" nem por preferência de fornecedor.

A política conceitual deste arquivo é executada por `engine/execution_engine.py` e detalhada em `core/EXECUTION_FABRIC.md`.

## Ordem padrão

1. **`current_agent`** — agente atual + ferramentas diretas de raciocínio, arquivos, GitHub e conectores;
2. **`github_ci`** — GitHub Actions/CI para comandos determinísticos, testes, build e prova reproduzível;
3. **`sandbox`** — executor leve quando realmente disponível;
4. **`local_full`** — executor local/interativo completo, como Codex ou equivalente.

A ordem só vale entre backends capazes. Um backend sem alguma capacidade obrigatória é rejeitado.

## Capacidades antes de marcas

A tarefa é traduzida para necessidades como:

- `reasoning`;
- `repo_read` / `repo_write`;
- `github_api`;
- `deterministic_commands`;
- `build` / `test`;
- `headless_browser`;
- `interactive_shell` / `interactive_browser`;
- `ephemeral_services` / `local_services`;
- `live_migration`.

Assim o Core continua portátil mesmo quando os agentes disponíveis mudarem.

## Current-agent first

Não limite o agente atual a documentação ou pequenas edições. Se ele consegue coordenar arquivos, branch/PR, ler CI, corrigir e repetir com segurança, permaneça nele.

Múltiplos arquivos, build ou testes não obrigam handoff.

## GitHub Actions como executor remoto

Use `github_ci` quando a prova for determinística e não interativa, por exemplo:

- lint/format/typecheck;
- testes unitários/integrados;
- build;
- Playwright headless;
- banco/serviços efêmeros;
- migrations descartáveis;
- validadores e smoke tests.

`engine/ci_executor.py` só descobre gates de uma allowlist de IDs do próprio repositório. Texto livre de prompt não vira shell.

## Fallback

`.factory/execution.json` mantém histórico bounded de tentativas. Após o limite de falhas do mesmo backend para a mesma ação, a próxima decisão pode rejeitá-lo e escolher o próximo backend capaz.

O repair loop do Autonomy Engine continua definindo quantas tentativas técnicas são permitidas; a Execution Fabric define **onde** a próxima tentativa ocorre.

## Quando `local_full` é correto

Use quando existir capacidade concreta não coberta anteriormente, como:

- browser/runtime interativo;
- debugging de processo local;
- serviço local difícil de reproduzir em CI;
- migration em ambiente real;
- operações/arquivos que as ferramentas atuais não suportam;
- estagnação em que um executor local realmente muda a capacidade disponível.

Codex pode cumprir esse papel, mas não é uma dependência do Core.

## Comunicação

Não exponha roteamento interno a cada passo. Informe troca de ambiente apenas quando o usuário precisa agir ou quando custo/risco muda materialmente.

Se o backend necessário não estiver disponível, tente fallback/reparo antes de transformar a situação em intervenção humana. Decisões humanas continuam regidas por `core/HUMAN_INTERACTION.md`.
