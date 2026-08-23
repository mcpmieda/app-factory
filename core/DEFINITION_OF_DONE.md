# Definition of Done

Uma funcionalidade não está pronta porque o código foi escrito.

A Factory deve adaptar esta lista ao tipo de projeto e risco, mas por padrão verificar:

## Qualidade da especificação — Semantic Assurance

Quando `core/SEMANTIC_ASSURANCE.md` selecionar profundidade `domain` ou `formal`:

- `specs/semantic-assurance.json` corresponde ao fingerprint do `semantic-contract.json` atual;
- requisitos `must` possuem origem/estrutura clara e estão ligados a critérios de aceite;
- critérios `must` possuem requisito de origem rastreável ou exceção explícita e justificada;
- conceitos, entidades, relações, estados e restrições referenciados existem e são coerentes;
- não há cardinalidade/range/enum impossível ou dependência estruturada simultaneamente exigida e proibida;
- perguntas `blocking` foram resolvidas antes da implementação;
- cobertura semântica é **cobertura estrutural de rastreabilidade**, nunca percentual de correção da intenção humana;
- semantic diff foi considerado quando baseline de requisitos/domínio mudou e ACs/invariantes/gates impactados foram reverificados;
- property/stateful/model-based testing foi derivado quando invariantes, ranges ou estados justificarem exploração além de exemplos manuais;
- combinatorial/t-way testing foi considerado quando múltiplas dimensões finitas interagirem; modelo ACTS/covering-array só vira gate quando materializado/versionado;
- formalizações `required` possuem artefato, referências de origem e gate executado;
- métodos formais registram pressupostos/limites e não são tratados como prova de interpretação humana perfeita.

Em `scenario`, não exigir `semantic-assurance.json` apenas para preencher processo.

## Correspondência com a intenção

Quando a mudança exigir Semantic Verification:

- `specs/semantic-contract.json` representa objetivo/regras atuais antes da implementação;
- critérios obrigatórios são observáveis (`given / when / then`);
- todo critério `must` está ligado em `specs/verification-plan.json` a evidência executável/gate;
- gates foram realmente executados; rastreabilidade textual não substitui execução;
- `specs/review-evidence.json` corresponde a spec, plano e conteúdo atual;
- risco médio/alto recebeu revisão desacoplada (`independent-agent` ou `clean-context`);
- mudança posterior em código/spec/plano invalida revisão anterior até nova verificação;
- mudança semântica material indicada por Semantic Assurance invalida evidência dependente.

Docs/chore/refactor pequeno sem mudança observável permanecem leves.

## Adequação da arquitetura

Quando `core/SYSTEM_ENGINEERING.md` se aplicar:

- nível do produto foi classificado/registrado;
- `persistent-app` ou superior possui fonte autoritativa durável;
- `multi-user-system` ou superior não usa `localStorage`/mocks/JSON estático como persistência final compartilhada;
- identidade/autenticação existe quando necessária;
- **autorização é aplicada server-side** quando escopos diferem;
- mutações protegidas possuem validação server-side;
- schema persistente usa migrations/versionamento equivalente;
- concorrência, idempotência e recovery foram considerados quando materiais;
- protótipo/demo não é rotulado produção só porque UI/CRUD funcionam.

## APIs e integrações

Quando `core/API_ENGINEERING.md` se aplicar:

- API mode foi classificado sem formalização desnecessária;
- `contract`/`governed` tem fonte machine-readable versionada;
- contrato e implementação representam o mesmo fluxo crítico;
- lint/validação passou quando suportado;
- breaking changes foram comparadas contra baseline quando necessário;
- autenticação/autorização protegida possui allow/deny evidence;
- inputs inválidos/erros esperados são controlados e não viram 500 acidental;
- paginação, idempotência, concorrência, operações longas e rate limiting foram tratados quando materiais;
- integrações externas têm timeout e retry/falha limitada;
- webhooks tratam autenticidade, replay/duplicidade e idempotência quando necessário;
- testes negativos/property/fuzz/consumer-provider foram executados quando modo/risco exigir;
- docs/SDK não prometem comportamento divergente.

Redocly CLI, oasdiff, Schemathesis, Pact, AsyncAPI e Arazzo são defaults/opções condicionais, não gates universais.

## Independent Verification

Quando `core/INDEPENDENT_VERIFICATION.md` selecionar acima de `baseline`:

- existe matriz proporcional por **classe de falha**, sem instalar scanners só para checklist;
- política permanece `free-only` salvo gasto autorizado;
- checks `required` passaram ou possuem exceção explícita, pequena e versionada;
- ferramenta indisponível/não executada não virou `pass`;
- não foram executados equivalentes redundantes apenas para aumentar quantidade;
- SAST/supply-chain/accessibility foram aplicados quando selecionados;
- mutation testing foi usado quando modo/risco exigir;
- Hypothesis/fast-check/property-stateful foi usado quando Semantic Assurance derivou propriedade relevante e matriz tornou o gate aplicável;
- NIST ACTS/covering-array foi executado quando modelo combinatorial versionado e check `required` existirem;
- Schemathesis foi usado quando API Engineering/matriz selecionarem;
- RESTler só foi escalado em REST/OpenAPI `governed` complexo, com configuração materializada e alvo descartável;
- OWASP ZAP baseline/active foi executado apenas contra ambiente efêmero/autorizado;
- workflows GitHub selecionados foram validados por actionlint e, em risco maior, zizmor antes de tratar CI como laboratório confiável;
- migrations PostgreSQL materiais passaram por Squawk/equivalente quando selecionado;
- limites arquiteturais materializados passaram por dependency-cruiser/equivalente quando selecionado;
- cross-browser Playwright cobriu Chromium/Firefox/WebKit somente quando o produto promete suporte multi-engine;
- Lighthouse CI só bloqueia com baseline/budget estável;
- k6 só bloqueia por workload/SLO/threshold definido e alvo autorizado;
- Toxiproxy/fault injection usa proxy/stub controlado e prova timeout/retry/idempotência/degradação sem atacar provedor externo;
- findings críticos/altos materiais não foram silenciados por suppression global;
- logs/artefatos não expõem secrets/dados pessoais reais;
- ferramentas/actions usadas como gate possuem versão/commit reproduzível.

Defaults principais incluem Semgrep CE, Trivy, StrykerJS/mutmut, Schemathesis, OWASP ZAP, axe-core, Lighthouse CI, actionlint, zizmor, Hypothesis/fast-check, NIST ACTS, Squawk, dependency-cruiser, k6 e Toxiproxy conforme pré-condições. Opengrep/RESTler são substituição/escalonamento, não duplicação automática.

Independent Verification não substitui revisão semântica desacoplada nem Semantic Assurance.

## Implementação

- comportamento solicitado existe;
- requisitos relevantes foram atendidos;
- funcionalidades fora do escopo não foram removidas;
- solução reutiliza padrões existentes quando adequado;
- não há dependências/abstrações desnecessárias conhecidas.

## Qualidade executável

Quando suportado:

- lint passa;
- typecheck passa;
- testes relacionados passam;
- build passa;
- erros novos de console não são ignorados.

Typecheck/build defendem imports/assinaturas inexistentes. Integrações pouco tipadas/runtime ganham smoke/integration test quando falha de API for risco material.

## Comportamento

- fluxo principal foi exercitado;
- loading/vazio/sucesso/erro considerados quando aplicáveis;
- regressão direta verificada;
- operações repetíveis não duplicam quando idempotência é requisito;
- `persistent-app` ou superior exercita persistência real/equivalente, não só estado do navegador;
- fluxos protegidos cobrem acesso permitido/negado quando autorização material.

## UI

Quando houver interface:

- desktop verificado;
- mobile/responsividade verificada;
- interação real no navegador quando possível;
- acessibilidade básica considerada;
- design system respeitado;
- não há mistura visual sem justificativa;
- visual regression entra apenas com baseline estável e risco material;
- compatibilidade cross-browser entra somente quando parte do suporte prometido.

## Segurança e dados

Quando relevante:

- autenticação/autorização verificadas;
- inputs validados;
- segredos não foram adicionados;
- migrations/alterações de dados têm recovery;
- `production-system` ou superior tem backup/restore compatível quando perda material;
- logs/auditoria/observabilidade existem no nível necessário.

API Security fica em API Engineering + security-review; Independent Verification executa gates sem duplicar catálogo de ameaças. Policies complexas podem usar OPA/Rego/Cedar quando Semantic Assurance justificar.

## Entrega

- diff revisado proporcionalmente ao risco;
- estado do projeto recuperável pelo Git;
- PROJECT_STATE atualizado quando estado vigente mudou;
- nível do sistema/persistência/identidade/recovery recuperáveis quando relevantes;
- API mode/contrato/baseline recuperáveis quando `contract/governed`;
- semantic depth, assurance, diff e formalizações recuperáveis em `domain/formal`;
- modelos property/combinatorial/load/resilience ficam versionados quando virarem gates;
- modo/checks/exceções de Independent Verification ficam recuperáveis em `VERIFICATION.md`/workflows;
- limitações/testes impossíveis são declarados.

## Regra final

Nunca declarar "pronto" com erro conhecido que invalide objetivo principal. Distinguir: implementado, testado, validado e pronto para produção.

Spec `domain/formal` inconsistente ou com pergunta `blocking` não está pronta.

Trabalho funcional com spec aplicável não termina em `lint + typecheck + build + testes verdes` sem rastreabilidade/revisão atual.

`multi-user-system` ou superior não termina em UI + CRUD + dados locais sem arquitetura compartilhada.

API `contract/governed` não termina em endpoint funcionando sem contrato/compatibilidade/gates aplicáveis.

Independent Verification `adversarial/release` não termina com testes primários verdes se check `required` selecionado ainda não passou.
