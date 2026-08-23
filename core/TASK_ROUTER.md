# Task Router — escolha de executor

A Factory escolhe o executor pela **capacidade necessária para provar o trabalho**, não pela palavra "código" nem por preferência de fornecedor.

A política conceitual deste arquivo é executada por `engine/execution_engine.py` e detalhada em `core/EXECUTION_FABRIC.md`. Quando há histórico local suficiente, `core/LEARNING_ENGINE.md` pode otimizar a ordem **somente entre candidatos que já passaram por todos os filtros obrigatórios**.

## Ordem de autoridade

1. capacidades obrigatórias;
2. disponibilidade e permissões;
3. bloqueios/failure threshold da tarefa atual;
4. segurança, risco, contratos arquiteturais/API/Semantic Assurance/Independent Verification/Semantic Verification e Definition of Done;
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

`core/SEMANTIC_ASSURANCE.md` e `core/INDEPENDENT_VERIFICATION.md` **não criam segunda taxonomia de backends**. Seus motores são traduzidos para capacidades existentes.

### Semantic Assurance

- consistency/coverage/semantic diff stdlib → `deterministic_commands` + `repo_read`;
- Hypothesis/fast-check/property/stateful → `deterministic_commands` + `test` e, quando necessário, `ephemeral_services`;
- NIST ACTS/covering arrays → `deterministic_commands` + artefato combinatorial versionado + Java/runtime quando exigido;
- Z3/Alloy/FRET/Quint/TLA+/P/DMN/policy tests → `deterministic_commands` + artefatos do projeto + `test`/serviço efêmero quando necessário;
- método formal dependente de UI/interação local específica → backend que realmente possua essa capacidade, sem tornar `local_full` default.

### Independent Verification

- Trivy/Semgrep/actionlint/zizmor/Squawk/dependency-cruiser/mutation → `deterministic_commands` + `repo_read` + `test` quando necessário;
- Schemathesis/RESTler → `deterministic_commands` + contrato API + `ephemeral_services`; RESTler pode exigir container/.NET conforme empacotamento escolhido;
- OWASP ZAP → `deterministic_commands` + rede local + `ephemeral_services` e browser quando a configuração exigir;
- axe-core + Playwright/cross-browser → `headless_browser` + `test`;
- Lighthouse CI → `headless_browser` + `build` + aplicação iniciável;
- **k6** → `deterministic_commands` + aplicação/API de teste + `ephemeral_services` quando necessário;
- **Toxiproxy** → `deterministic_commands` + `ephemeral_services` + proxy/stub controlado entre sistema e dependência.

Se um gate `required` precisar de capacidade que o backend atual não possui, ele é incapaz para aquela prova; a Factory tenta outro backend capaz em vez de omitir o gate.

## Current-agent first

Não limite o agente atual a documentação ou pequenas edições. Se ele consegue coordenar arquivos, branch/PR, ler CI, corrigir e repetir com segurança, permaneça nele.

Múltiplos arquivos, build ou testes não obrigam handoff.

## GitHub Actions como executor remoto

Use `github_ci` quando a prova for determinística e não interativa, por exemplo:

- lint/format/typecheck;
- testes unitários/integrados;
- build;
- validadores Semantic Assurance e semantic diff;
- property/stateful/model-based/combinatorial tests;
- solver/model checker formal com artefato versionado e CLI reproduzível;
- Playwright headless/cross-browser;
- banco/serviços efêmeros;
- migrations descartáveis e lint de migration;
- validadores e smoke tests;
- SAST/supply-chain/mutation testing;
- **actionlint** e zizmor para testar o próprio workflow/CI;
- API property/fuzz/stateful em serviço efêmero;
- ZAP baseline/active em alvo efêmero autorizado;
- acessibilidade e Lighthouse;
- **k6** contra ambiente de teste controlado quando workload/budget justificar;
- **Toxiproxy** com dependências/stubs controlados para latência, timeout e desconexão.

`engine/ci_executor.py` só descobre gates de allowlist do próprio repositório. Texto livre de prompt não vira shell. Workflows específicos de formalização/Independent Verification continuam versionados no projeto; o executor genérico não inventa comandos de solver/scanner/load/fault-injection a partir do prompt.

GitHub CI também deve ser verificável: quando workflows forem parte do projeto e o modo exigir, actionlint valida correção estrutural e zizmor valida riscos de segurança antes de tratar esse CI como laboratório confiável.

Se GitHub-hosted capacity puder gerar custo não autorizado, runner próprio/local equivalente pode ser preferido. Isso muda executor, não reduz evidência exigida.

## Regras para provas potencialmente agressivas

- DAST ativo, RESTler fuzz profundo, k6 e Toxiproxy usam alvos controlados/autorizados;
- carga não é disparada contra produção/terceiro por inferência;
- Toxiproxy degrada proxy/stub controlado, não o provedor externo real;
- testes caros podem migrar para release/nightly em vez de cada commit;
- indisponibilidade do motor não vira `pass`.

## Fallback da tarefa atual

`.factory/execution.json` mantém histórico bounded e local de tentativas. O failure threshold é escopado pela tarefa autônoma atual, para que falhas antigas não contaminem tarefas novas.

Após o limite de falhas do mesmo backend para a mesma ação/tarefa, a próxima decisão rejeita esse backend e tenta o próximo capaz. O Learning Engine recebe apenas candidatos que sobreviveram a esse filtro.

O repair loop do Autonomy Engine define quantas tentativas técnicas são permitidas; a Execution Fabric define **onde** a próxima tentativa ocorre.

Falha ou indisponibilidade de ferramenta `required` — formal ou Independent Verification — não vira `pass`. Se nenhum backend gratuito/capaz conseguir executar o gate, registre bloqueio/exceção e envolva o usuário apenas se houver decisão real de custo/risco/credencial.

## Aprendizado local

`.factory/learning.json` usa apenas metadados allowlisted de execução e fica fora do Git por padrão.

Quando a amostra mínima não foi atingida, preservar ordem baseline. Com evidência suficiente, Learning Engine pode preferir outro backend leve já elegível com base em confiabilidade e, em empate de confiança alta, duração mediana materialmente melhor.

Consulte `core/LEARNING_ENGINE.md` para privacidade, confiança e explicabilidade.

## Quando `local_full` é correto

Use quando existir capacidade concreta não coberta anteriormente, como:

- browser/runtime interativo;
- debugging de processo local;
- serviço local difícil de reproduzir em CI;
- migration em ambiente real;
- ferramenta formal/local que não possa ser reproduzida no CI disponível;
- teste de carga/rede que precise de topologia local não reproduzível no runner;
- operações/arquivos que as ferramentas atuais não suportam;
- estagnação em que executor local realmente muda capacidade disponível.

Codex pode cumprir esse papel, mas não é dependência do Core.

## Comunicação

Não exponha roteamento interno a cada passo. Informe troca de ambiente apenas quando o usuário precisa agir ou quando custo/risco muda materialmente.

Se backend necessário não estiver disponível, tente fallback/reparo antes de transformar em intervenção humana. Decisões humanas continuam regidas por `core/HUMAN_INTERACTION.md`.
