# App Factory — Plano consolidado

## Visão

Manter um sistema operacional portátil e **general-purpose** de desenvolvimento com IA que transforma intenção em software funcional, recuperável e verificável, com pouca intervenção manual e sem depender de agente, fornecedor ou domínio de negócio específico.

Sistemas escolares são um caso importante de uso, não o limite da Factory. O mesmo Core deve servir software administrativo, SaaS, e-commerce, logística, integrações, automações, produtos públicos, sistemas internos e software crítico quando os contratos proporcionais forem satisfeitos.

## Problemas que a Factory deve resolver

- projetos começando sem padrão;
- contexto perdido entre chats/computadores/agentes;
- excesso de microtarefas/cliques;
- código sem teste real ou sem prova da intenção;
- especificações ambíguas/contraditórias tratadas como verdade;
- testes escritos pela mesma IA sem evidência externa proporcional;
- demos locais apresentadas como sistemas completos;
- APIs sem contrato/compatibilidade/segurança proporcional;
- migrations arriscadas, arquitetura degradada, CI inseguro ou performance/resiliência não comprovadas quando materiais;
- bibliotecas/componentes reinventados;
- interfaces inconsistentes;
- executores pesados usados sem necessidade;
- dificuldade para recuperar versão segura;
- regras importantes apenas em documentação manual;
- divergência entre intenção, domínio, especificação, arquitetura, contratos, verificação e implementação.

## Arquitetura atual

Camadas complementares com responsabilidades separadas:

1. **Core** — princípios, interação humana, escala, risco, workflow e Definition of Done.
2. **System Engineering** — profundidade mínima da arquitetura; impede falsa persistência/completude.
3. **API Engineering** — governa APIs/integrações/eventos/webhooks somente quando existe fronteira real.
4. **Semantic Assurance** — qualidade da especificação: `scenario`/`domain`/`formal`, domínio, consistência, cobertura, semantic diff e geração/modelagem condicional.
5. **Independent Verification** — matriz `free-only` por classes de falha, independente do raciocínio implementador.
6. **Context Engine** — recuperação incremental do repositório.
7. **Autonomy Engine** — estado e próxima ação técnica.
8. **Semantic Verification** — critérios observáveis, rastreabilidade e revisão desacoplada.
9. **Execution Fabric** — executor por capacidade/disponibilidade; CI para prova determinística.
10. **Learning Engine** — otimização local somente entre candidatos já elegíveis.
11. **Skills** — conhecimento especializado sob demanda.
12. **Profiles/starters/templates** — defaults comprovados, sem stack universal congelada.
13. **UI system** — design system, Living UI e Semantic Motion.
14. **Scripts/CI** — guardrails executáveis/regressão.
15. **Research/audits** — evidência antes de promover padrões novos.

## Relação entre contratos

```text
objetivo
  ├─ PROJECT_SCALE ─ profundidade do processo
  ├─ RISK_MODEL ─── risco/gates
  └─ SYSTEM_ENGINEERING ─ profundidade mínima do produto
          └─ API/integração relevante? → API_ENGINEERING

intenção funcional
  ├─ SEMANTIC_ASSURANCE
  │    qualidade da spec
  │    domínio / propriedades / combinações / formalização
  └─ SEMANTIC_VERIFICATION
       critérios → evidência → revisão

risco + sistema + API + superfícies técnicas
  └─ INDEPENDENT_VERIFICATION
       menor matriz diversa free-only
       required / advisory / exception

EXECUTION_FABRIC
  └─ escolhe onde cada prova roda

DEFINITION_OF_DONE
  └─ fecha somente quando gates aplicáveis passaram
```

Security Review continua dono do threat model. Semantic Assurance não substitui decisão humana. Independent Verification não duplica API Engineering nem Semantic Verification.

## Estratégia de execução

Não existe divisão fixa “ChatGPT faz X / Codex faz Y”. A Execution Fabric decide por capacidade:

1. `current_agent`;
2. `github_ci`;
3. `sandbox` quando disponível/suficiente;
4. `local_full` quando capacidade local/interativa for necessária.

Codex pode ser `local_full`, mas não é dependência. Independent Verification e métodos formais são gates executados por backends, não novos agentes de raciocínio.

## Estratégia de arquitetura do produto

- arquitetura mais simples que satisfaça o produto real;
- `local-app` pode usar persistência local quando legítimo;
- `persistent-app`+ exige fonte autoritativa durável;
- `multi-user-system`+ exige compartilhamento/server-side, autorização e validação proporcionais;
- produção/criticidade elevam recovery, observabilidade, auditoria, segurança e rollout quando materiais;
- perfis não podem reduzir contratos centrais.

## Estratégia de Semantic Assurance

- `scenario` quando invariantes + `given/when/then` bastarem;
- `domain` quando conceitos/relações/papéis/estados/regras interagirem;
- `formal` somente para temporalidade, concorrência/distribuição, safety/liveness, policy/combinatória complexa ou criticidade;
- `specs/semantic-assurance.json` ligado por fingerprint ao contrato semântico em `domain/formal`;
- requisitos inspirados em EARS/FRET sem impor runtime Cucumber/FRET universal;
- consistência determinística, cobertura estrutural e semantic diff por IDs/fingerprints;
- coverage nunca é “percentual de verdade”;
- **Hypothesis**/ **fast-check** entram quando invariantes/ranges/estados justificarem property/stateful testing;
- **NIST ACTS**/covering arrays entram quando múltiplas dimensões finitas interagirem; só bloqueiam com modelo versionado e força t-way justificada;
- Z3/SMT, Alloy, FRET, P, Quint/TLA+, DMN, OPA/Rego/Cedar permanecem métodos formais condicionais;
- formalização `required` exige artefato + `source_refs` + gate executado;
- finding probabilístico da IA permanece hipótese/advisory até resolução estruturada/formal/humana.

## Estratégia de APIs e integrações

- backend não implica API formal;
- governança: `none`, `lightweight`, `contract`, `governed`;
- `contract/governed` usa fonte machine-readable adequada;
- HTTP/OpenAPI é forte default HTTP, não universal;
- GraphQL, gRPC/Protobuf, AsyncAPI e Arazzo são condicionais;
- OWASP API Security é referência de ameaça;
- integrações materiais recebem timeout/retry/rate-limit/idempotência/recovery proporcionais;
- breaking changes viram gate quando consumidores dependem de estabilidade;
- Redocly CLI, oasdiff, Schemathesis e Pact são condicionais/substituíveis;
- Independent Verification executa fuzz/DAST/deep state sem duplicar o contrato da API.

## Estratégia de Independent Verification

Princípio: **diversidade de método > quantidade de ferramentas**.

A política é `free-only` por padrão e classifica `baseline`, `independent`, `adversarial` ou `release`.

### Base preservada

- Trivy — supply chain/secrets/misconfiguration;
- Semgrep Community Edition — SAST;
- StrykerJS/mutmut — mutation testing;
- Schemathesis — API property/fuzz/stateful;
- OWASP ZAP — DAST;
- axe-core + Playwright — acessibilidade;
- Lighthouse CI — page quality com baseline.

### Lacunas agora cobertas estrategicamente

- **actionlint** — correção do próprio GitHub Actions;
- **zizmor** — segurança do próprio GitHub Actions;
- **Hypothesis / fast-check** — property/stateful do domínio derivado da semântica;
- **NIST ACTS** — combinatorial/t-way quando há dimensões finitas relevantes;
- **Squawk** — segurança de migrations PostgreSQL;
- **dependency-cruiser** ou equivalente — conformidade de limites arquiteturais declarados;
- **k6** — load/concurrency quando workload/SLO/baseline justificar;
- **Toxiproxy** ou equivalente — resiliência de rede para integrações materiais em proxy/stub controlado;
- **Playwright Chromium + Firefox + WebKit** — compatibilidade quando suporte multi-engine for requisito.

### Escalonamentos, não duplicação

- Schemathesis continua API fuzz principal; **Microsoft RESTler** entra somente em REST/OpenAPI `governed` com estado profundo, normalmente release/nightly;
- Semgrep CE continua SAST default; **Opengrep** é substituto qualificado após piloto, não scanner paralelo;
- Pact continua governado por API Engineering;
- OpenSSF Scorecard e Cosign/SLSA permanecem candidatos para futura política de provenance/distribuição, não entram automaticamente sem esse problema existir.

### Regras de ativação

- actionlint/zizmor: workflows GitHub;
- property testing: invariantes/ranges/estados materiais;
- ACTS: múltiplas dimensões finitas interativas e modelo versionado para virar required;
- Squawk: PostgreSQL + migrations compatíveis;
- architecture check: limites materializados;
- k6: workload/SLO/baseline;
- Toxiproxy: integração externa material;
- RESTler: API governed/OpenAPI profunda;
- cross-browser: suporte multi-engine prometido.

Nenhum motor entra só porque “produção deve ter tudo”.

## Segurança dos próprios testes

- GitHub CI é laboratório preferido quando capaz, mas actionlint/zizmor verificam o próprio workflow;
- ZAP ativo, RESTler fuzz profundo, Schemathesis destrutivo, k6 e Toxiproxy nunca inferem produção/terceiro;
- Toxiproxy degrada proxy/stub controlado, não o provedor;
- thresholds de mutation/Lighthouse/k6/t-way vêm de requisito/SLO/baseline, não números universais;
- check `required` não executado não vira `pass`;
- suppressions/exceções são pequenas, justificadas e versionadas;
- versões/commits de ferramentas/actions são fixados no CI real.

## Estratégia de UI

- web-admin/dashboard: shadcn como base validada, ReUI seletivo; HeroUI permanece alternativa;
- não misturar design systems sem ganho;
- reuse-first para componentes/blocos;
- motion transversal via `ui/MOTION_POLICY.md`;
- `ambient` pode ser atenuado para `subtle` em telas densas;
- `prefers-reduced-motion` obrigatório para movimento não essencial;
- axe/Lighthouse/visual regression/cross-browser entram por risco/suporte, não como estética universal.

## Estratégia de trabalho

- GitHub é fonte técnica de verdade;
- recuperar contexto antes de depender de chat;
- fatias funcionais completas;
- preservar baseline/diff/rollback em manutenção;
- semantic diff quando domínio/spec mudar;
- máximo seguro antes de pedir intervenção;
- governança proporcional a risco/sistema/custo de incompatibilidade;
- pesquisar/reutilizar antes de criar equivalente;
- transformar regras repetitivas em teste/lint/policy/solver/CI quando houver retorno;
- fonte comum para cada contrato; templates/perfis apontam para ela em vez de duplicar catálogo;
- `SEMANTICS.md`/assurance somente em `domain/formal`;
- `VERIFICATION.md` quando Independent Verification estiver acima de `baseline`.

## Linha evolutiva consolidada

- **V1.0** — baseline estável, starters/pilotos/portabilidade/validação final.
- **V1.1** — Context Engine + Autonomy Engine.
- **V1.2** — Execution Fabric + CI Executor.
- **V1.3** — Learning Engine local/conservador.
- **V1.4** — Semantic Verification + revisão desacoplada.
- **Governance hardenings sobre V1.4** — System Engineering + API Engineering + Semantic Assurance + Independent Verification e enriquecimento por classes de falha, sem alterar engines V1.1–V1.4 nem inventar versão nova.

Novas capacidades viram defaults/perfis estáveis somente após evidência/pilotos suficientes.

## Critério principal de sucesso

O usuário descreve objetivo em linguagem simples. A Factory recupera estado, classifica arquitetura/risco/interface/semântica/verificação, escolhe ferramentas e executor, melhora a especificação quando necessário, implementa a maior fatia segura possível e prova o resultado com testes primários + evidência independente proporcional — sem exigir que o usuário conheça frameworks, protocolos, solvers, scanners, Skills ou fases internas.
