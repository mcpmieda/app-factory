# Independent Verification — tooling template

Use este diretório como referência para materializar workflows de verificação independente em projetos gerados/evoluídos pela App Factory.

## Regra central

Não copie todas as ferramentas para todo projeto. Rode primeiro o planner determinístico e materialize somente o que for aplicável:

```bash
python scripts/independent_verification.py \
  --root <projeto> \
  --risk medium \
  --system-level multi-user-system \
  --api-mode contract
```

Se integrações externas forem materialmente relevantes ao comportamento/recovery, o agente pode acrescentar `--external-integrations`. Isso é um sinal arquitetural, não uma opção que o usuário precise escolher manualmente.

Quando a CLI central não estiver disponível no repositório do produto, use `VERIFICATION.md` + `core/INDEPENDENT_VERIFICATION.md` como contrato de seleção.

## Defaults por classe de falha

Use **um motor principal por classe** salvo ganho documentado:

- supply chain/secrets/misconfiguration — Trivy;
- SAST — Semgrep Community Edition; Opengrep é substituto qualificado, não scanner paralelo padrão;
- mutation JS/TS — StrykerJS;
- mutation Python — mutmut;
- API property/fuzz/stateful — Schemathesis;
- REST stateful profundo — Microsoft RESTler somente como escalonamento de API `governed`/OpenAPI;
- DAST — OWASP ZAP;
- acessibilidade — axe-core + Playwright;
- page quality — Lighthouse CI;
- CI correctness — actionlint;
- CI security — zizmor;
- domain property Python — Hypothesis;
- domain property JS/TS — fast-check;
- combinatorial/t-way — NIST ACTS ou covering-array equivalent;
- PostgreSQL migration safety — Squawk;
- architecture conformance JS/TS — dependency-cruiser ou equivalente;
- load/concurrency — k6;
- network resilience — Toxiproxy ou equivalente;
- browser compatibility — Playwright Chromium + Firefox + WebKit quando o produto suportar os três engines.

Nem todos são scanners. Alguns geram casos, sabotam código, validam arquitetura, testam migrations, exercitam carga ou injetam falhas controladas. Essa diversidade é intencional.

## Pré-condições importantes

- actionlint/zizmor: somente quando há `.github/workflows`;
- Hypothesis/fast-check: quando Semantic Assurance possui invariantes/ranges/estados relevantes;
- NIST ACTS: quando há múltiplas dimensões finitas que realmente interagem; só bloqueia com modelo versionado;
- Squawk: somente PostgreSQL + migrations compatíveis;
- dependency-cruiser: bloqueia apenas quando limites arquiteturais estão declarados/configurados;
- k6: quando workload/SLO/baseline real existir ou precisar ser estabelecido;
- Toxiproxy: quando integração externa/rede for material;
- RESTler: somente API REST/OpenAPI `governed` com estado profundo e alvo descartável;
- cross-browser: somente quando o produto promete suporte multi-engine.

## Workflow real

Ao gerar `.github/workflows/independent-verification.yml`:

1. usar `permissions: contents: read` salvo necessidade explícita;
2. fixar versões/commits de actions e CLIs;
3. usar lockfile/instalação reproduzível;
4. não injetar secrets em fork PR;
5. iniciar app/banco com dados fictícios quando necessário;
6. usar `timeout-minutes`;
7. destruir serviços efêmeros com `if: always()`;
8. nunca inferir produção/terceiro para ZAP, Schemathesis destrutivo, RESTler fuzz, k6 ou Toxiproxy;
9. salvar apenas relatórios sem dados sensíveis;
10. separar `required` de `advisory`;
11. validar o próprio workflow com actionlint e, quando o risco justificar, zizmor;
12. não executar ferramentas equivalentes redundantes apenas para aumentar quantidade de checks.

## Cadência recomendada

- iteração rápida: testes primários e checks baratos;
- PR: actionlint, supply-chain/SAST/accessibility e gates específicos selecionados;
- PR seletivo: property/combinatorial/mutation/cross-browser/load/resilience quando o custo fizer sentido;
- release: matriz adversarial aplicável, ZAP ativo autorizado, cross-browser, migration/load/resilience e mutation conforme risco;
- nightly/schedule: RESTler profundo, mutation ampliado, DAST/dependencies periódicos ou cargas prolongadas quando houver benefício real.

## Thresholds

Não invente valores universais. Mutation score, Lighthouse budget, k6 latency/error thresholds e t-way strength precisam vir de requisito, SLO, baseline ou análise específica do produto.

## Custo

A Factory não exige SaaS pago nem segunda IA paga para esta camada. Em repositório privado, GitHub-hosted Actions pode consumir franquia; se minutos/custo forem problema, use runner próprio/local já disponível em vez de habilitar cobrança sem autorização.
