# Independent Verification Contract

Este contrato define como a App Factory obtém evidência **independente do raciocínio da IA que implementou o código**, usando motores determinísticos e preferencialmente open source executados em CI ou ambiente equivalente.

Ele não substitui `core/SEMANTIC_ASSURANCE.md`, `core/SEMANTIC_VERIFICATION.md`, `core/API_ENGINEERING.md`, `skills/security-review` nem `core/EXECUTION_FABRIC.md`:

- **Semantic Assurance** melhora a qualidade da própria especificação e deriva invariantes/espaços de teste quando aplicável;
- **Semantic Verification** define o que precisa ser provado contra a intenção;
- **API Engineering** define contratos e gates próprios de interfaces/APIs;
- **Security Review** define threat model e riscos relevantes;
- **Independent Verification** escolhe motores externos que tentam reprovar implementação, testes, migrations, arquitetura, performance e o próprio CI por métodos diferentes;
- **Execution Fabric** escolhe onde esses motores rodam, preferindo `github_ci` quando capaz.

## 1. Princípio

Testes escritos pela mesma IA que escreveu a implementação são evidência útil, mas não suficiente em todo nível de risco.

O objetivo não é rodar o maior número possível de scanners. É usar **diversidade de método** de forma proporcional e **não rodar ferramentas redundantes** apenas para aumentar contagem.

A Factory escolhe a menor matriz que cubra as classes de falha materiais do produto, seja ele escolar, administrativo, SaaS, e-commerce, automação, integração, serviço público, produto de consumo ou software crítico.

## 2. Política de custo

A camada é **free-only por padrão**:

- não exigir segunda API/modelo de IA pago;
- não ativar SaaS pago, plano premium ou scanner comercial por inferência;
- preferir ferramentas open source executáveis no GitHub Actions, runner próprio ou ambiente local já disponível;
- GitHub-hosted runners podem consumir franquia/minutos do plano; evitar surpresa de custo e preferir self-hosted/local quando necessário;
- ferramentas não devem enviar código privado a serviço externo pago por padrão.

Se uma ferramenta deixar de ser gratuita/open source para a função usada, ela deixa de ser default até nova validação.

## 3. Modos proporcionais

### `baseline`

Alteração simples/baixo risco.

- lint/typecheck/build/testes normais;
- nenhum scanner pesado obrigatório só porque existe código.

### `independent`

Trabalho funcional relevante, dependências, persistência, autenticação, dados compartilhados ou sistema com impacto real.

Adicionar verificadores independentes de baixo/médio custo quando aplicáveis.

### `adversarial`

`multi-user-system`, API compartilhada, autenticação/autorização sensível, alto risco ou superfície exposta.

Além de `independent`, usar métodos que tentam quebrar o sistema: mutation, property/stateful, DAST, cenários negativos, migrations/arquitetura quando materiais.

### `release`

Release de `production-system`/`critical-system` ou alteração de alto impacto.

Executar matriz adversarial aplicável em estado limpo; ampliar browser, load, fault injection, mutation, API fuzz e recovery somente quando o produto possuir essas superfícies.

## 4. Matriz principal de motores

Defaults são substituíveis por equivalentes gratuitos tecnicamente melhores. Fixe versão/commit reproduzível no projeto real.

### Supply chain / secrets / misconfiguration — Trivy

- vulnerabilidades de dependências;
- secrets acidentais;
- misconfiguration e artefatos suportados;
- combine com audit nativo da stack quando já existir.

Finding crítico/alto explorável em caminho de produção deve bloquear proporcionalmente; falso positivo vira exceção pequena, não desativação global.

### SAST — Semgrep Community Edition

Semgrep CE continua default de análise estática enquanto atender a stack. **Opengrep** é alternativa open source qualificada e deve ser pilotado como possível substituto; não rodar Semgrep + Opengrep juntos por padrão porque isso duplica classe de evidência.

Security Review continua dono do threat model; SAST fornece evidência, não prova segurança total.

### Mutation testing — StrykerJS / mutmut

Objetivo: verificar se os **próprios testes** percebem defeitos deliberadamente introduzidos.

- JavaScript/TypeScript: **StrykerJS**;
- Python: **mutmut** ou equivalente maduro;
- seletivo em PR e mais forte em release/alto risco;
- threshold nasce de baseline real, nunca `100%` universal.

### API property/fuzz/stateful — Schemathesis

Preferir **Schemathesis** para OpenAPI/GraphQL quando API Engineering indicar.

- gera inputs/sequências independentes dos exemplos manuais;
- usa dados isolados;
- fuzz destrutivo nunca aponta para produção por inferência.

### API stateful deep fuzzing — Microsoft RESTler

RESTler é **escalonamento**, não substituto automático do Schemathesis.

Use apenas quando:

- API mode `governed`;
- REST/OpenAPI;
- dependências produtor-consumidor/estado profundo justificarem;
- normalmente release/nightly;
- configuração RESTler estiver materializada para virar gate required.

`fuzz` agressivo pode degradar o alvo; use ambiente descartável/autorizado.

### DAST — OWASP ZAP

- baseline/passive scan pode rodar em PR em aplicação iniciável;
- active/full scan somente release/alto risco;
- nunca apontar scan ativo automaticamente para produção, intranet alheia ou serviço de terceiro.

Baseline e active são modos do mesmo motor, não “dois scanners independentes”.

### Acessibilidade — axe-core + Playwright

Rodar em páginas/estados importantes. Automação não prova acessibilidade total, mas detecta violações objetivas que testes funcionais não enxergam.

### Performance/qualidade da página — Lighthouse CI

Use somente com aplicação web e baseline estável. Budgets são específicos do produto; não impor score universal arbitrário.

### Browser/E2E — Playwright

Playwright continua base para fluxos reais, screenshots e axe.

Para releases web relevantes, considerar matriz **Chromium + Firefox + WebKit**. Não aplicar essa matriz artificialmente a extensão específica de Chromium/Chrome ou plataforma deliberadamente restrita.

## 5. Verificar o próprio GitHub CI

GitHub Actions é frequentemente o laboratório que executa os demais motores. Por isso ele também precisa de prova independente.

### actionlint — correção do workflow

Quando `.github/workflows` existir e o projeto estiver acima de `baseline`:

- validar sintaxe;
- expressões `${{ }}`;
- referências/inputs/outputs;
- integração com checks de shell/Python quando suportada.

`actionlint` é `required` a partir de `independent` porque um CI inválido não é executor confiável.

### zizmor — segurança do workflow

Usar **zizmor** para riscos específicos de GitHub Actions, como template injection, credenciais, permissões excessivas e referências perigosas.

- `advisory` em contexto menor quando apropriado;
- `required` em `adversarial/release` quando workflows existirem;
- não exigir GitHub Advanced Security; usar modo console/CI gratuito quando necessário.

## 6. Domínio: property/stateful testing

Semantic Assurance pode identificar invariantes, ranges, restrições e máquinas de estado que merecem geração automática de casos.

### Python — Hypothesis

Use **Hypothesis** para gerar valores/estados e reduzir um finding ao menor contraexemplo reproduzível.

### JavaScript/TypeScript — fast-check

Use **fast-check** com a mesma finalidade em JS/TS.

Regras:

- não duplicam Schemathesis: o foco aqui é domínio/lógica, não a interface HTTP;
- `domain` normalmente começa advisory;
- `formal` ou release de alto risco pode tornar required;
- contraexemplo encontrado vira regressão determinística quando útil.

## 7. Combinações de configuração — NIST ACTS

Use **NIST ACTS** ou covering-array generator equivalente quando houver múltiplas dimensões finitas e o teste exaustivo explodir.

Exemplos gerais:

- planos × permissões × feature flags × regiões;
- navegador × autenticação × configuração;
- tipos de usuário × estados × políticas;
- qualquer domínio com interação combinatória relevante.

Regras:

- Semantic Assurance identifica candidato a combinatorial testing;
- não basta “ter muitos campos”;
- o check fica `required` somente quando um modelo combinatorial versionado existir (`specs/combinatorial-model.json` ou equivalente);
- sem modelo, permanece `advisory` para o agente materializar apenas se trouxer ganho real.

## 8. Banco e migrations — Squawk

Para **PostgreSQL com migrations SQL**, preferir **Squawk** ou equivalente compatível para detectar padrões que podem causar locks, indisponibilidade ou mudanças perigosas.

- não aplicar a banco não suportado;
- `independent`: pode iniciar advisory;
- `adversarial/release`: required quando migrations PostgreSQL forem parte da mudança/entrega.

Isso complementa testes de migration: “SQL executou” não prova que a migration é segura em produção.

## 9. Arquitetura executável — dependency-cruiser

Para JS/TS, **dependency-cruiser** é default forte quando o projeto materializa limites de módulos/camadas.

Use para regras como:

- frontend não importa módulo server-only;
- domínio não depende de infraestrutura proibida;
- evitar ciclos;
- limites entre bounded contexts/módulos.

Se config arquitetural existir, o gate pode ser required. Sem config, sistemas maiores podem receber recomendação advisory; não invente fronteiras que a arquitetura não declarou.

Outras linguagens podem usar equivalente de architecture test/import boundary.

## 10. Carga e concorrência — k6

Use **k6** para validar workload, concorrência e performance de backend/API.

- thresholds devem vir de SLO, requisito ou baseline estável;
- produção/release sem baseline pode começar advisory;
- se o projeto já possui testes de carga e a release é de alto risco, o gate pode ser required;
- não gerar carga contra produção ou serviço externo sem autorização explícita.

Lighthouse e k6 não são redundantes: Lighthouse observa qualidade/performance da experiência/página; k6 testa capacidade e comportamento sob carga.

## 11. Resiliência de rede — Toxiproxy

Quando integrações externas/rede forem materiais, use **Toxiproxy** ou fault proxy equivalente para simular:

- latência/jitter;
- timeout;
- desconexão;
- conexão lenta/limitada;
- degradação transitória.

O objetivo é provar timeout, retry seguro, idempotência, fallback e recuperação.

Falhas são injetadas **entre o sistema de teste e proxy/stub controlado**. Nunca degrade o provedor externo real.

Em release de alto risco com integração material, resilience test pode ser required.

## 12. Seleção automática

O planner considera sinais objetivos:

- nível do sistema;
- risco;
- API mode;
- UI/browser;
- autenticação/autorização;
- contrato OpenAPI/GraphQL;
- workflows GitHub;
- migrations PostgreSQL;
- limites arquiteturais materializados;
- invariantes/ranges/estados da Semantic Assurance;
- modelo combinatorial;
- testes de carga/SLO;
- integrações externas;
- release/deploy de produção.

Não ativar ferramenta sem pré-condição técnica real.

## 13. Cadência

### Commit/iterações rápidas

- lint/typecheck/testes direcionados/build;
- scanners rápidos somente quando baratos/úteis.

### Pull request

- regressão aplicável;
- actionlint/zizmor quando CI relevante;
- SAST/supply-chain/accessibility;
- migration/architecture checks;
- property/combinatorial/Schemathesis/ZAP/mutation seletivamente.

### Release

- matriz adversarial aplicável;
- cross-browser quando suportado;
- DAST ativo em alvo descartável;
- load/resilience quando material;
- mutation/domínio crítico;
- RESTler somente em REST governed complexo;
- recovery/rollback quando System Engineering exigir.

### Agendado/nightly

Pode hospedar checks caros: RESTler profundo, mutation ampliado, dependency/DAST recorrente, combinatorial ou load prolongado. Respeitar custo de CI.

## 14. Segurança do próprio CI

Workflows devem seguir, quando suportado:

- permissões mínimas;
- ações/containers/CLIs com versão/commit fixado;
- nenhum secret em fork PR por conveniência;
- dados fictícios;
- `timeout-minutes`;
- teardown `always()`;
- logs/artefatos sem tokens/dados pessoais;
- load/fuzz/DAST/fault injection somente em alvo controlado/autorizado.

## 15. Evidência e bloqueio

Cada motor selecionado recebe status:

- `required` — falha bloqueia;
- `advisory` — produz finding/baseline sem bloquear;
- `not-applicable` — pré-condição ausente;
- `exception` — exceção explícita, pequena, justificada e versionada.

Ferramenta indisponível **não vira pass**.

## 16. Independência real e limites

Esses motores são independentes do raciocínio implementador, mas **não entendem sozinhos a intenção**.

- mutation prova força dos testes, não regra correta;
- SAST/Trivy/ZAP/zizmor procuram classes de falha, não segurança total;
- axe não prova acessibilidade total;
- Lighthouse/k6 não provam boa UX/capacidade infinita;
- ACTS cobre combinações do modelo fornecido, não todas as interpretações humanas;
- property testing prova propriedades declaradas, não que escolhemos a propriedade correta;
- RESTler/Schemathesis não substituem critérios semânticos;
- Squawk não substitui estratégia de migration/rollback;
- dependency-cruiser só prova os limites que foram declarados.

Para risco médio/alto, revisão desacoplada de Semantic Verification continua separada. Ferramenta determinística não vira “segundo agente” artificialmente.

## 17. Relação com API Engineering

- API Engineering decide contrato, compatibilidade, erros, idempotência e necessidade de contract/fuzz testing;
- Independent Verification executa Schemathesis/ZAP/RESTler e outros gates selecionados;
- RESTler só escala casos REST stateful complexos;
- DoD exige que gates required tenham passado.

## 18. Relação com Semantic Assurance

- Semantic Assurance define domínio, invariantes, ranges, estados e combinações relevantes;
- Independent Verification transforma candidatos em Hypothesis/fast-check/ACTS somente quando executáveis e úteis;
- coverage semântica não é substituída por quantidade de casos gerados.

## 19. Relação com Security Review

Security Review produz threat model. Independent Verification mapeia ameaças automatizáveis para ferramentas apropriadas.

Exemplos:

- autorização por objeto → testes negativos + Schemathesis quando útil;
- dependência vulnerável → Trivy;
- código inseguro → Semgrep CE/Opengrep equivalente;
- HTTP exposto → ZAP;
- CI perigoso → zizmor;
- migration PostgreSQL arriscada → Squawk.

## 20. Saída durável

Acima de `baseline`, manter decisões recuperáveis em `VERIFICATION.md`/workflow/config:

- modo;
- motores e motivo;
- required/advisory;
- triggers;
- alvo/ambiente seguro;
- thresholds/budgets derivados de baseline/requisito;
- suppressions/exceções;
- modelo combinatorial/property/load quando houver;
- último baseline relevante.

## 21. Regra final

A Factory não fica melhor por ter “20 scanners”. Fica melhor quando **cada classe importante de erro possui pelo menos uma forma independente e proporcional de ser descoberta**.

Quando risco/arquitetura justificarem, use diversidade de método; quando não justificarem, preserve o projeto simples.
