# Independent Verification Contract

Este contrato define como a App Factory obtém evidência **independente do raciocínio da IA que implementou o código**, usando motores determinísticos e preferencialmente open source executados em CI ou ambiente equivalente.

Ele não substitui `core/SEMANTIC_VERIFICATION.md`, `core/API_ENGINEERING.md`, `skills/security-review` nem `core/EXECUTION_FABRIC.md`:

- **Semantic Verification** define o que precisa ser provado contra a intenção;
- **API Engineering** define contratos e gates próprios de interfaces/APIs;
- **Security Review** define o threat model e riscos relevantes;
- **Independent Verification** escolhe motores externos que tentam reprovar a implementação por métodos diferentes dos testes escritos pela IA;
- **Execution Fabric** escolhe onde esses motores rodam, preferindo `github_ci` quando capaz.

## 1. Princípio

Testes escritos pela mesma IA que escreveu a implementação são evidência útil, mas não suficiente em todo nível de risco. A Factory deve adicionar verificadores independentes quando eles puderem descobrir classes de falhas que a implementação/testes primários podem compartilhar.

O objetivo não é rodar o maior número possível de scanners. É usar **diversidade de método** de forma proporcional.

## 2. Política de custo

A camada é **free-only por padrão**:

- não exigir segunda API/modelo de IA pago;
- não ativar SaaS pago, plano premium ou scanner comercial por inferência;
- preferir ferramentas open source executáveis no GitHub Actions, runner próprio ou ambiente local já disponível;
- GitHub-hosted runners podem consumir a franquia/minutos incluídos do plano quando o repositório não tiver execução gratuita ilimitada; a Factory deve evitar surpresa de custo e pode preferir self-hosted quando necessário;
- ferramentas devem funcionar sem enviar código privado a um serviço externo pago por padrão.

Se uma ferramenta deixar de ser gratuita/open source ou exigir conta paga para a função usada, ela deixa de ser default até nova validação.

## 3. Modos proporcionais

### `baseline`

Para alteração simples/baixo risco.

- lint/typecheck/build/testes normais continuam sendo o núcleo;
- nenhum scanner pesado é obrigatório apenas por existir código.

### `independent`

Para trabalho funcional relevante, dependências, persistência, autenticação, dados compartilhados ou sistema com impacto real.

Adicionar verificadores independentes de baixo/médio custo quando aplicáveis, como:

- análise estática de segurança;
- vulnerabilidades/dependências/secrets;
- acessibilidade automatizada para UI relevante.

### `adversarial`

Para `multi-user-system`, APIs compartilhadas, autenticação/autorização sensível, alto risco ou superfície web/API exposta.

Além de `independent`, adicionar métodos que tentam quebrar o sistema:

- mutation testing seletivo;
- property/fuzz/stateful testing de API;
- DAST/baseline scan em ambiente efêmero;
- cenários negativos de autorização e validação.

### `release`

Para release de `production-system`/`critical-system` ou alteração de alto impacto.

Executar a matriz adversarial aplicável com escopo ampliado e, quando fizer sentido:

- mutation testing em domínios críticos;
- DAST ativo somente contra ambiente descartável/autorizado;
- budgets de performance/qualidade com baseline estável;
- prova de recovery/rollback quando exigida pelo System Engineering;
- reexecução dos gates críticos antes do merge/deploy.

O modo de verificação não substitui a classificação de risco/sistema. Ele deriva delas.

## 4. Matriz de motores preferidos

As ferramentas abaixo são defaults substituíveis por equivalentes gratuitos tecnicamente melhores. Sempre fixe versão/commit reproduzível no projeto real.

### Mutation testing

Objetivo: verificar se os **próprios testes** percebem erros deliberadamente introduzidos.

- JavaScript/TypeScript: **StrykerJS**;
- Python: **mutmut** ou equivalente maduro compatível com a stack;
- outras linguagens: usar ferramenta equivalente somente após validar maturidade/manutenção.

Regras:

- não rodar em todo commit por padrão;
- preferir PR de risco alto, módulos críticos e release;
- definir threshold por projeto depois de obter baseline real; não inventar `100%` universal;
- mutantes sobreviventes em regra crítica devem gerar teste/correção ou exceção documentada.

### API property/fuzz/stateful testing

Objetivo: gerar inputs e sequências que não dependem dos casos escritos manualmente.

- preferir **Schemathesis** para OpenAPI/GraphQL quando compatível;
- `core/API_ENGINEERING.md` continua sendo a autoridade sobre quando esse gate é necessário;
- nunca executar fuzz destrutivo contra produção por padrão;
- usar seed/ambiente isolado e autenticação de teste quando necessário.

### DAST / ataque externo

Objetivo: observar a aplicação de fora, como um cliente/atacante.

- preferir **OWASP ZAP**;
- baseline/passive scan pode rodar em PR quando houver aplicação web iniciável em ambiente efêmero;
- active/full scan é gate de release/alto risco e deve apontar apenas para ambiente descartável ou alvo explicitamente autorizado;
- nunca apontar scan ativo automaticamente para domínio de produção, intranet de terceiros ou sistema externo.

### SAST

Objetivo: encontrar padrões inseguros diretamente no código-fonte.

- preferir **Semgrep Community Edition** ou equivalente open source;
- `skills/security-review` define o risco/ameaça; o scanner fornece evidência, não substitui revisão de segurança;
- suppressions precisam ser pequenas, versionadas e justificadas.

### Supply chain / secrets / misconfiguration

Objetivo: verificar dependências vulneráveis, secrets acidentais e configuração insegura.

- preferir **Trivy** ou equivalente open source;
- combinar com audits nativos do ecossistema quando já existirem;
- findings `critical`/`high` exploráveis em caminho de produção devem bloquear proporcionalmente; falso positivo deve virar exceção explícita, não desativação global.

### Acessibilidade

Objetivo: detectar violações objetivas que testes funcionais não enxergam.

- preferir **axe-core** integrado a Playwright quando houver UI web;
- executar em páginas/estados importantes, não somente na home vazia;
- automação não substitui revisão manual de acessibilidade para casos críticos.

### Performance/qualidade web

Objetivo: detectar regressões de performance e qualidade da página.

- preferir **Lighthouse CI** quando houver aplicação web e baseline estável;
- usar budgets específicos do produto; não impor pontuação universal arbitrária;
- em UI exploratória, manter advisory até existir baseline confiável.

### Browser/E2E

**Playwright** continua como executor de fluxos reais e base para browser, screenshots e axe. Ele não é considerado adversarial sozinho; torna-se parte da camada quando executa cenários independentes/negativos, acessibilidade ou baseline visual.

## 5. Seleção automática

A Factory deve escolher a matriz a partir de sinais objetivos, não perguntar ao usuário por ferramenta.

Sinais importantes:

- nível do sistema (`SYSTEM_ENGINEERING`);
- risco da mudança;
- API mode (`none`/`lightweight`/`contract`/`governed`);
- presença de autenticação/autorização;
- entrada de dados não confiáveis/uploads/URLs remotas;
- dependências novas/alteradas;
- UI web;
- contrato OpenAPI/GraphQL;
- linguagem com mutation tooling maduro;
- existência de testes capazes de receber mutation testing;
- release/deploy de produção.

Não ativar ferramenta sem pré-condição técnica real.

## 6. Cadência

### Commit/iterações rápidas

- lint/typecheck/testes direcionados/build;
- scanners rápidos somente quando baratos e úteis.

### Pull request

- regressão completa aplicável;
- SAST/supply-chain/accessibility quando selecionados;
- Schemathesis/ZAP baseline/mutation seletivo conforme modo.

### Release

- matriz adversarial aplicável em estado limpo;
- DAST ativo somente em ambiente autorizado/efêmero;
- mutation testing de domínio crítico;
- Lighthouse/budgets quando estáveis;
- evidências de recovery/rollback quando o sistema exigir.

### Agendado

Para sistemas mantidos em produção, pode haver workflow semanal/mensal de dependências/DAST. Isso é opcional e deve respeitar custo de CI e disponibilidade do ambiente.

## 7. Segurança do próprio CI

Workflows de Independent Verification devem seguir, quando suportado:

- `permissions` mínimas, normalmente `contents: read`;
- ações/containers e CLIs com versão/commit fixado;
- nenhum secret entregue a fork PR por conveniência;
- ambiente de teste isolado e dados fictícios;
- `timeout-minutes` e limites explícitos;
- active scan sem acesso a produção por default;
- artefatos/logs sem tokens, credenciais ou dados pessoais reais;
- teardown `always()` de serviços efêmeros;
- suppressions/allowlists versionadas e revisáveis.

## 8. Evidência e bloqueio

Cada motor selecionado deve ter status claro:

- `required` — falha bloqueia o gate;
- `advisory` — registra finding/baseline, sem bloquear até haver política estável;
- `not-applicable` — pré-condição ausente;
- `exception` — exceção explícita, pequena, justificada e versionada.

Não converter indisponibilidade do scanner em `pass`.

Resultados úteis devem ficar recuperáveis via logs/artefatos/SARIF/relatório equivalente quando o toolchain suportar, sem transformar dados sensíveis em artifact público.

## 9. Independência real e seus limites

Esses motores são independentes do raciocínio da IA implementadora, mas **não entendem sozinhos a intenção do produto**.

Portanto:

- mutation testing prova força dos testes, não correção da regra de negócio;
- Semgrep/Trivy/ZAP procuram classes de falha, não provam segurança total;
- axe não prova acessibilidade total;
- Lighthouse não prova boa UX;
- Schemathesis não substitui critérios semânticos de negócio.

Para risco médio/alto, a revisão desacoplada de `core/SEMANTIC_VERIFICATION.md` continua obrigatória quando aplicável. Deterministic tooling não vira "segundo agente" artificialmente.

## 10. Integração com API Engineering

Evitar duplicação:

- API Engineering decide contrato, compatibilidade, erros, idempotência e necessidade de fuzz/contract testing;
- Independent Verification decide **como executar e combinar** Schemathesis/ZAP/segurança/mutation como prova externa;
- DoD exige que os gates selecionados tenham passado.

## 11. Integração com Security Review

Security Review produz threat model e prioridades. Independent Verification mapeia ameaças verificáveis para ferramentas apropriadas.

Exemplo:

- risco BOLA/autorização por objeto → testes negativos reais + Schemathesis quando útil;
- dependência vulnerável → Trivy/audit;
- padrão de código inseguro → Semgrep;
- superfície HTTP exposta → ZAP em ambiente de teste.

Scanner sem threat model não deve criar sensação de segurança completa.

## 12. Saída durável

Quando o modo for `independent`, `adversarial` ou `release`, o projeto deve manter decisões recuperáveis, preferencialmente em `VERIFICATION.md` e/ou workflow/config versionado:

- modo atual;
- motores selecionados e motivo;
- required vs advisory;
- frequência/trigger;
- ambiente/alvo de teste;
- thresholds/budgets quando existirem;
- suppressions/exceções;
- último baseline relevante quando necessário.

## 13. Regra final

A Factory não deve considerar um sistema robusto mais confiável apenas porque possui muitos testes escritos pela IA. Quando risco e arquitetura justificarem, deve haver pelo menos uma forma de **evidência independente do raciocínio implementador**, preferencialmente executada pelo GitHub Actions ou outro executor determinístico gratuito/equivalente.
