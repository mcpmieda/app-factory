# Task Router — escolha de executor

A Factory escolhe o executor pela **capacidade necessária para provar o trabalho**, não pela palavra "código" nem por preferência de fornecedor.

A política conceitual deste arquivo é executada por `engine/execution_engine.py` e detalhada em `core/EXECUTION_FABRIC.md`. Quando há histórico local suficiente, `core/LEARNING_ENGINE.md` pode otimizar a ordem **somente entre candidatos que já passaram por todos os filtros obrigatórios**.

## Ordem de autoridade

1. capacidades obrigatórias;
2. disponibilidade e permissões;
3. bloqueios/failure threshold da tarefa atual;
4. segurança, risco, contratos arquiteturais/API/Independent Verification/Semantic Verification e Definition of Done;
5. evidência aprendida local, quando suficiente;
6. ordem baseline entre candidatos restantes.

Aprendizado nunca cria capacidade, concede permissão, reduz verificação ou ressuscita backend rejeitado.

## Ordem baseline

1. **`current_agent`** — agente atual + ferramentas diretas de raciocínio, arquivos, GitHub e conectores;
2. **`github_ci`** — GitHub Actions/CI para comandos determinísticos, testes, build e prova reproduzível;
3. **`sandbox`** — executor leve quando realmente disponível;
4. **`local_full`** — executor local/interativo completo, como Codex ou equivalente.

A ordem só vale entre backends capazes. Com dados suficientes, o Learning Engine pode reordenar backends leves elegíveis; `local_full` não é promovido sobre um backend leve capaz somente por score histórico.

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

`core/INDEPENDENT_VERIFICATION.md` **não cria uma segunda taxonomia de backends**. Seus motores são traduzidos para estas capacidades existentes, por exemplo:

- Trivy/Semgrep/mutation testing → `deterministic_commands` + `repo_read` + `test` quando necessário;
- Schemathesis → `deterministic_commands` + `ephemeral_services` + contrato/API de teste;
- OWASP ZAP → `deterministic_commands` + `headless_browser`/rede local + `ephemeral_services`;
- axe-core + Playwright → `headless_browser` + `test`;
- Lighthouse CI → `headless_browser` + `build` + aplicação iniciável.

Se um check `required` precisar de uma capacidade que o backend atual não possui, ele é incapaz para aquela prova; a Factory tenta outro backend capaz em vez de simplesmente omitir o check.

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
- validadores e smoke tests;
- SAST/supply-chain/mutation testing;
- API property/fuzz testing em serviço efêmero;
- ZAP baseline/active em alvo efêmero autorizado;
- acessibilidade e Lighthouse quando selecionados.

`engine/ci_executor.py` só descobre gates de uma allowlist de IDs do próprio repositório. Texto livre de prompt não vira shell. Workflows específicos de Independent Verification continuam versionados no projeto e seguem `core/INDEPENDENT_VERIFICATION.md`; o executor genérico não inventa comandos de scanner a partir do prompt.

Se GitHub-hosted capacity puder gerar custo não autorizado, um runner próprio/local equivalente pode ser preferido. Isso é mudança de executor, não redução da evidência exigida.

## Fallback da tarefa atual

`.factory/execution.json` mantém histórico bounded e local de tentativas. O failure threshold é escopado pela tarefa autônoma atual, para que falhas antigas não contaminem tarefas novas.

Após o limite de falhas do mesmo backend para a mesma ação/tarefa, a próxima decisão rejeita esse backend e tenta o próximo capaz. O Learning Engine recebe apenas os candidatos que sobreviveram a esse filtro.

O repair loop do Autonomy Engine continua definindo quantas tentativas técnicas são permitidas; a Execution Fabric define **onde** a próxima tentativa ocorre.

Falha ou indisponibilidade de ferramenta Independent Verification não vira `pass`. Se nenhum backend gratuito/capaz conseguir executar um check `required`, registre o bloqueio/exceção conforme política e envolva o usuário apenas se houver decisão real de custo/risco/credencial.

## Aprendizado local

`.factory/learning.json` usa apenas metadados allowlisted de execução e fica fora do Git por padrão.

Quando a amostra mínima não foi atingida, preservar a ordem baseline. Quando há evidência suficiente, o Learning Engine pode preferir outro backend leve já elegível com base em confiabilidade e, em empate de confiança alta, duração mediana materialmente melhor.

Consulte `core/LEARNING_ENGINE.md` para privacidade, confiança e explicabilidade.

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
