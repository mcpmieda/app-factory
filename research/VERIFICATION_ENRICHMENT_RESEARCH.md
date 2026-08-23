# Verification Enrichment Research

Pesquisa consolidada para ampliar a diversidade de prova da App Factory sem transformar o repositório em um catálogo de scanners.

## Objetivo

Cobrir classes de falha que a matriz anterior ainda tratava de forma parcial:

- correção e segurança do próprio GitHub Actions;
- regras de domínio com espaço grande de entradas/estados;
- combinações de configuração;
- segurança de migrations PostgreSQL;
- conformidade arquitetural;
- carga/concorrência/performance de backend;
- falhas de rede e dependências externas;
- compatibilidade entre engines de navegador;
- fuzzing REST stateful mais profundo quando a API realmente justificar.

A seleção é geral para software. Sistemas escolares são apenas um dos possíveis domínios; os mesmos mecanismos servem SaaS, e-commerce, logística, automação, integrações, sistemas internos, produtos públicos e software crítico.

## Critério de adoção

Um motor entra como default condicional somente se:

1. cobre uma classe de falha materialmente diferente;
2. pode rodar gratuitamente/open source ou ser substituído por equivalente gratuito;
3. é automatizável em CI/runner controlado;
4. possui condição objetiva de ativação;
5. não duplica um motor já preferido sem ganho suficiente.

Ferramenta madura mas redundante fica como escalonamento/alternativa, não como execução paralela automática.

## Adotados como defaults condicionais

### actionlint — GitHub Actions correctness

Fonte: https://github.com/rhysd/actionlint

Papel: lint específico de workflows, expressões, referências, shell/Python quando integrados e erros estruturais do GitHub Actions.

Decisão: `required` a partir de `independent` quando o projeto possui `.github/workflows`. Antes de confiar no GitHub CI como executor, o próprio mecanismo de execução precisa de validação.

### zizmor — GitHub Actions security

Fonte: https://github.com/zizmorcore/zizmor

Papel: segurança do CI/CD, incluindo template injection, credenciais, permissões excessivas e referências Git perigosas.

Decisão: complementar ao actionlint; `required` em `adversarial/release`, sem exigir GitHub Advanced Security. Usar modo que funcione também em repositório privado sem produto pago quando necessário.

### Hypothesis / fast-check — property/stateful testing de domínio

Fontes:

- https://hypothesis.readthedocs.io/
- https://fast-check.dev/

Papel: gerar entradas/estados e reduzir contraexemplos a partir de propriedades/invariantes. Diferente de Schemathesis: aqui o alvo principal é lógica/domínio, não o contrato HTTP.

Decisão: derivar de Semantic Assurance quando existirem invariantes, ranges, restrições ou estados. Hypothesis é default Python; fast-check é default JS/TS. `formal` ou release de alto risco pode torná-los obrigatórios; não entram em lógica trivial.

### NIST ACTS — combinatorial / covering arrays

Fontes:

- https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software/
- https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software/downloadable-tools
- https://www.nist.gov/publications/combinatorial-testing-building-reliable-systems

Papel: cobrir interações t-way entre múltiplos parâmetros/configurações sem explosão exaustiva. O programa ACTS é disponibilizado gratuitamente pelo NIST.

Decisão: Semantic Assurance identifica domínios candidatos; o gate só fica obrigatório quando existir um modelo combinatorial versionado. Caso contrário permanece advisory. Não usar apenas porque há muitos campos.

### Squawk — PostgreSQL migration safety

Fonte: https://squawkhq.com/docs/

Papel: detectar padrões de migration PostgreSQL com risco de lock, indisponibilidade ou alteração insegura.

Decisão: selecionar somente quando PostgreSQL + migrations SQL existirem. Em alto risco/multiusuário/release, o lint de migration pode bloquear; não aplicar a bancos não suportados.

### dependency-cruiser — architecture conformance JS/TS

Fonte: https://github.com/sverweij/dependency-cruiser

Papel: transformar limites arquiteturais em regras executáveis e detectar dependências proibidas/cíclicas.

Decisão: default JS/TS quando regras arquiteturais forem materializadas. Em outros ecossistemas usar equivalente. Se não houver configuração declarada, pode ser recomendação advisory em sistemas maiores, não gate inventado.

### k6 — load/performance/reliability

Fonte: https://grafana.com/docs/k6/latest/

Papel: cenários de carga, concorrência e thresholds pass/fail ligados a SLO/baseline.

Decisão: nunca inventar número universal de usuários ou latência. Torna-se `required` quando o projeto já possui workload/threshold relevante e a release é de alto risco; em produção sem baseline pode começar advisory.

### Toxiproxy — network fault injection

Fonte: https://github.com/Shopify/toxiproxy

Papel: latência, timeout, desconexão, largura de banda e outros problemas de rede entre o sistema de teste e dependências controladas.

Decisão: somente quando integrações externas/rede forem materialmente relevantes. Falhas são injetadas em proxy/stub controlado; jamais degradar o serviço de terceiro em si.

### Playwright cross-browser matrix

Fonte: https://playwright.dev/docs/browsers

Papel: reutilizar o motor já presente para Chromium, Firefox e WebKit em fluxos críticos.

Decisão: não criar nova ferramenta. Ativar seletivamente em web app release/adversarial; extensões Chrome permanecem no engine compatível em vez de ganhar Firefox/WebKit artificialmente.

## Escalonamentos, não defaults paralelos

### Microsoft RESTler

Fontes:

- https://github.com/microsoft/restler-fuzzer
- https://www.microsoft.com/en-us/research/project/restler-fuzzing/

RESTler infere dependências produtor-consumidor de OpenAPI e explora sequências stateful profundas. Continua sob desenvolvimento ativo, mas possui custo operacional maior e sobreposição parcial com Schemathesis.

Decisão: Schemathesis continua default de API property/fuzz/stateful. RESTler só aparece em `governed` + OpenAPI + release/nightly; fica obrigatório apenas quando o projeto materializou configuração RESTler e o risco justificar. Fuzz agressivo usa ambiente descartável.

### Opengrep

Fonte: https://opengrep.dev/

É alternativa open source relevante ao Semgrep CE e compatível com grande parte do ecossistema de regras.

Decisão: não executar Semgrep e Opengrep juntos por padrão. Semgrep CE permanece default até piloto comparativo da Factory demonstrar ganho de cobertura/manutenção suficiente; Opengrep é substituto qualificado, não scanner adicional.

## Mantidos sem duplicação

- Trivy continua cobrindo supply chain/secrets/misconfiguration; não adicionar vários scanners equivalentes apenas para aumentar contagem.
- OWASP ZAP continua DAST principal; baseline e active são modos do mesmo motor.
- Schemathesis continua API fuzz/property/stateful principal.
- StrykerJS/mutmut continuam mutation testing; property-based testing tem objetivo diferente e não os substitui.
- axe-core e Lighthouse continuam suas funções específicas.
- Pact permanece governado por API Engineering quando consumer/provider independente justificar.

## Candidatos qualificados, mas fora do planner automático por enquanto

- OpenSSF Scorecard: útil para postura de supply chain/repositório, especialmente software público/distribuído; sobrepõe parcialmente verificações de repositório e pode depender de contexto GitHub externo. Avaliar quando houver fluxo de publicação relevante.
- Cosign/SLSA: alto valor para assinatura/proveniência de artefatos distribuídos; não é necessário para todo sistema interno. Deve entrar quando a Factory tiver uma política própria de release/artifact provenance.

## Arquitetura resultante

```text
Semantic Assurance
  -> invariantes/ranges/estados -> Hypothesis / fast-check
  -> múltiplas dimensões finitas -> NIST ACTS

System/API/Architecture
  -> limites de módulos -> dependency-cruiser/equivalente
  -> PostgreSQL migrations -> Squawk
  -> API contract -> Schemathesis
  -> REST governed complexo -> RESTler (escalonamento)
  -> integração externa -> Toxiproxy
  -> SLO/workload -> k6

Independent Verification
  -> Trivy / SAST / ZAP / mutation / axe / Lighthouse
  -> Playwright cross-browser quando aplicável

GitHub CI, que executa os gates
  -> actionlint (correção)
  -> zizmor (segurança)
```

## Regra final

A qualidade da Factory aumenta por **diversidade de método**, não por quantidade de nomes. O planner deve preferir a menor matriz que cubra as classes de risco reais do produto, independentemente do domínio de negócio.
