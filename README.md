# App Factory

Sistema portátil para construir e manter software com agentes de IA de forma consistente, verificável, autônoma e com mínimo trabalho manual do usuário.

Versão estável dos engines/plugin: **`1.4.0` — App Factory V1.4**. System Engineering, API Engineering, Semantic Assurance e Independent Verification são governance hardenings sobre essa baseline; não inventam uma V1.5.

## Objetivo

Transformar uma ideia em software funcional usando um método reutilizável por ChatGPT, Codex, Claude Code, Cursor ou outro agente compatível, sem tornar nenhum executor, fornecedor ou domínio de negócio obrigatório.

A Factory é **general-purpose**. Sistemas escolares são um caso importante de uso, mas o mesmo Core atende SaaS, e-commerce, automação, logística, sistemas internos, integrações, produtos públicos e outros tipos de software.

A App Factory combina:

- entrada universal por intenção de software;
- **System Engineering Contract** para arquitetura/persistência/segurança proporcionais;
- **API Engineering Contract** para APIs/integrações somente quando existe fronteira real;
- **Semantic Assurance Contract** para qualidade da própria especificação;
- **Semantic Verification** para provar implementação contra intenção/spec;
- **Independent Verification Contract** para evidência técnica externa ao raciocínio implementador;
- **Context Engine** incremental;
- **Autonomy Engine** para estado/próxima ação;
- **Execution Fabric** para escolher executor por capacidade;
- GitHub Actions/CI como executor determinístico preferido quando capaz;
- **Learning Engine** local/conservador;
- **19 Skills** especializadas carregadas sob demanda;
- profiles/starters/templates reutilizáveis;
- Living UI / Semantic Motion quando houver interface;
- repair/fallback limitados;
- GitHub como fonte técnica de verdade.

## Experiência desejada

O usuário descreve apenas o resultado:

> Quero criar um sistema de patrimônio.

ou:

> Quero criar uma plataforma SaaS de atendimento.

Ele não precisa escolher framework, executor, scanner, solver, método formal ou fase interna.

```text
pedido
→ recuperar contexto/estado
→ classificar escala/risco/sistema
→ API Engineering quando houver fronteira real
→ decidir Semantic Verification
→ semantic depth: scenario / domain / formal
→ Semantic Assurance proporcional
→ planejar
→ implementar
→ Independent Verification proporcional
→ Execution Fabric escolhe onde provar
→ CI/testes/gates
→ repair/fallback
→ review desacoplado quando exigido
→ Definition of Done
→ entrega
```

## System Engineering

`core/SYSTEM_ENGINEERING.md` classifica:

- `website`;
- `local-app`;
- `persistent-app`;
- `multi-user-system`;
- `production-system`;
- `critical-system`.

Um sistema compartilhado não pode ser tratado como pronto se seus dados autoritativos ainda estiverem apenas em `localStorage`, mocks ou JSON estático. Backend, persistência, identidade, autorização, migrations, recovery e observabilidade entram somente no nível exigido pelo produto real.

## API Engineering

`core/API_ENGINEERING.md` só entra quando existe interface relevante entre consumidores/sistemas.

Modos:

- `none`;
- `lightweight`;
- `contract`;
- `governed`.

A Factory não força REST/OpenAPI em todo backend. Pode selecionar HTTP/OpenAPI, GraphQL, gRPC/Protobuf, AsyncAPI ou Arazzo conforme o comportamento. Redocly CLI, oasdiff, Schemathesis e Pact são ferramentas condicionais, não dependências universais.

## Semantic Assurance

`core/SEMANTIC_ASSURANCE.md` responde:

> A especificação está suficientemente clara, coerente, completa, modelada e rastreável para ser implementada com segurança?

Profundidades:

- `scenario` — regra isolada; critérios/invariantes normalmente bastam;
- `domain` — conceitos, papéis, relações, estados e regras interagem;
- `formal` — temporalidade, concorrência/distribuição, safety/liveness, policy/combinatória complexa ou criticidade justificam técnica formal.

Em `domain/formal`, `specs/semantic-assurance.json` complementa `specs/semantic-contract.json` com vocabulário, entidades, relações, estados, restrições, requisitos normalizados e referências.

O engine detecta, de forma determinística quando o modelo permite:

- IDs/referências quebradas;
- cardinalidades/ranges impossíveis;
- enums inviáveis;
- dependências contraditórias;
- requisito `must` sem critério;
- critério `must` sem origem;
- pergunta `blocking`;
- assurance stale em relação à spec.

Coverage é **rastreabilidade estrutural**, nunca “percentual de verdade”. Semantic Diff propaga impacto por IDs/fingerprints.

Métodos condicionais:

- **Hypothesis** / **fast-check** — property/stateful testing do domínio;
- **NIST ACTS** / covering arrays — combinações t-way quando múltiplas dimensões finitas interagem;
- **Z3/SMT** — restrições/satisfatibilidade;
- **Alloy** — relações/cardinalidades;
- **NASA FRET/FRETish** — requisitos temporais/reativos;
- **P ou Quint/TLA+** — estados/concorrência/distribuído;
- **DMN** — decisões tabulares;
- **OPA/Rego ou Cedar** — policies/autorização complexa.

Nenhum entra em todo projeto. Formalização/modelo só conta como prova quando existe artefato versionado, origem rastreável e gate real quando `required`.

## Semantic Verification

`core/SEMANTIC_VERIFICATION.md` responde:

> A implementação atual satisfaz a especificação atual?

Para trabalho funcional relevante, a Factory usa:

```text
specs/semantic-contract.json
specs/verification-plan.json
specs/review-evidence.json
```

Critérios `must` precisam apontar para evidência executável. Mudanças em spec/plano/conteúdo tornam review evidence stale quando afetam o fingerprint.

Risco médio/alto exige revisão desacoplada por `independent-agent` quando disponível ou `clean-context` provider-neutral. Scanner determinístico não conta como reviewer semântico.

## Independent Verification

`core/INDEPENDENT_VERIFICATION.md` obtém evidência **independente do raciocínio da IA implementadora**.

Modos:

- `baseline` — alteração simples;
- `independent` — evidências externas de baixo/médio custo;
- `adversarial` — tenta quebrar sistemas reais/alto risco;
- `release` — amplia provas antes de release importante.

Política: **`free-only` por padrão**. Nenhuma segunda IA paga ou SaaS comercial é requisito.

### Princípio central

**Diversidade de método > quantidade de scanners.**

A Factory prefere uma ferramenta principal por classe de falha e evita equivalentes redundantes sem ganho.

### Base preservada

- **Trivy** — supply chain/secrets/misconfiguration;
- **Semgrep Community Edition** — SAST;
- **StrykerJS / mutmut** — mutation testing;
- **Schemathesis** — API property/fuzz/stateful;
- **OWASP ZAP** — DAST;
- **axe-core + Playwright** — acessibilidade;
- **Lighthouse CI** — page quality/performance com baseline.

### Enriquecimento estratégico

- **actionlint** — correção do próprio GitHub Actions;
- **zizmor** — segurança do próprio GitHub Actions;
- **Hypothesis / fast-check** — property/stateful do domínio derivado da semântica;
- **NIST ACTS** — combinatorial/t-way quando há espaço finito relevante;
- **Squawk** — segurança de migrations PostgreSQL;
- **dependency-cruiser** ou equivalente — conformidade de limites arquiteturais declarados;
- **k6** — load/concurrency quando workload/SLO/baseline justificar;
- **Toxiproxy** ou equivalente — resiliência de rede em integrações materiais usando proxy/stub controlado;
- **Playwright Chromium + Firefox + WebKit** — compatibilidade quando o produto promete suporte multi-engine.

### Escalonamentos, não duplicação

- **Microsoft RESTler** pode ampliar Schemathesis em REST/OpenAPI `governed` com estado profundo, normalmente release/nightly;
- **Opengrep** é alternativa SAST qualificada após piloto, não execução paralela padrão com Semgrep CE;
- Pact continua pertencendo a API Engineering;
- OpenSSF Scorecard e Cosign/SLSA ficam candidatos para uma futura política de provenance/distribuição, não são adicionados sem esse problema existir.

`engine/independent_verification.py` usa sinais objetivos — linguagem, UI, API, workflows, semantic depth, migrations, arquitetura, load tests, RESTler config e integrações externas — para montar a menor matriz aplicável.

### Segurança dos testes agressivos

ZAP ativo, RESTler fuzz profundo, Schemathesis destrutivo, k6 e Toxiproxy **nunca inferem produção ou serviço de terceiro como alvo**. Use ambiente local/preview/efêmero e dados fictícios, salvo autorização explícita adequada.

Thresholds de mutation, Lighthouse, k6 e força t-way vêm de requisito, SLO ou baseline real; não há número universal.

## Execution Fabric

`core/EXECUTION_FABRIC.md` escolhe executor por capacidade.

Ordem baseline:

1. `current_agent`;
2. `github_ci`;
3. `sandbox`;
4. `local_full`.

GitHub CI pode rodar testes, builds, browsers headless, bancos/serviços efêmeros, scanners, property/combinatorial tests, migration/architecture checks, load/fault testing controlado e model checkers reproduzíveis.

O próprio CI também pode ser verificado por **actionlint + zizmor** quando a matriz exigir.

`engine/ci_executor.py` usa gates declarados/allowlisted, `shell=False`, sem transformar prompt em comando livre.

## Context + Autonomy + Learning

### Context Engine

`engine/context_engine.py` mantém mapa incremental, SHA-256 e delta `added/changed/removed` sem substituir arquivos reais.

### Autonomy Engine

`engine/autonomy_engine.py` mantém `.factory/state.json` e próxima ação/repair loop.

### Learning Engine

`engine/learning_engine.py` aprende apenas com metadados técnicos locais/allowlisted. Não armazena prompt, código, conteúdo de arquivos, secrets ou URLs privadas; não envia telemetria externa.

Aprendizado nunca cria capacidade, reduz gate ou promove backend incapaz.

## UI

Living UI / Semantic Motion permanece transversal quando há interface.

- design system adequado ao produto;
- reuse-first;
- motion contextual;
- `prefers-reduced-motion` obrigatório para movimento não essencial;
- visual regression, axe, Lighthouse e cross-browser entram apenas quando risco/baseline/suporte justificarem.

## Comandos internos

O usuário normalmente não precisa executá-los:

```text
python scripts/factory.py --root <projeto> resume
python scripts/factory.py --root <projeto> next
python scripts/factory.py --root <projeto> spec-validate
python scripts/factory.py --root <projeto> verification-plan-init
python scripts/factory.py --root <projeto> review-packet --base main
python scripts/semantic_assurance.py --root <projeto> analyze
python scripts/semantic_assurance.py --root <projeto> diff --baseline <arquivo>
python scripts/independent_verification.py --root <projeto> --risk high --system-level multi-user-system --api-mode contract
python scripts/factory.py --root <projeto> route verify
python scripts/factory.py --root <projeto> gates
```

Quando integrações externas forem materiais, o planner pode receber `--external-integrations` internamente.

## Comece por aqui

1. `AGENTS.md`
2. `PROJECT_STATE.md`
3. `core/ENTRYPOINT.md`
4. `core/SYSTEM_ENGINEERING.md`
5. `core/API_ENGINEERING.md`
6. `core/SEMANTIC_ASSURANCE.md`
7. `core/SEMANTIC_VERIFICATION.md`
8. `core/INDEPENDENT_VERIFICATION.md`
9. `core/EXECUTION_FABRIC.md`
10. `core/DEFINITION_OF_DONE.md`
11. `PORTABILITY.md`
12. Skills/perfis/templates somente quando aplicáveis.

## Perfis

`web-admin` permanece estável (`v1`). `website`, `web-app`, `chrome-extension` e `automation` permanecem `validated`. Perfis são evidência/defaults, não tecnologias universais congeladas.

## Estrutura central

```text
app-factory/
├── AGENTS.md
├── PROJECT_STATE.md
├── core/
│   ├── SYSTEM_ENGINEERING.md
│   ├── API_ENGINEERING.md
│   ├── SEMANTIC_ASSURANCE.md
│   ├── SEMANTIC_VERIFICATION.md
│   ├── INDEPENDENT_VERIFICATION.md
│   ├── EXECUTION_FABRIC.md
│   └── ...
├── engine/
│   ├── semantic_assurance.py
│   ├── semantic_verification.py
│   ├── independent_verification.py
│   ├── execution_engine.py
│   ├── ci_executor.py
│   └── ...
├── skills/              # 19 Skills portáteis
├── profiles/
├── templates/
├── starters/
├── ui/
├── audits/
├── research/
└── scripts/
```

## Estado

**V1.4 / `1.4.0`** continua sendo a baseline estável dos engines/plugin.

Governance hardenings atuais:

- System Engineering;
- API Engineering;
- Semantic Assurance;
- Independent Verification enriquecida por classes de falha.

O objetivo final não é maximizar complexidade. É fazer com que cada sistema receba **a menor arquitetura e a menor matriz de prova capazes de sustentar com evidência aquilo que o produto realmente precisa fazer**.
