# Independent Verification — tooling template

Use este diretório como referência para materializar workflows de verificação independente em projetos gerados/evoluídos pela App Factory.

## Regra central

Não copie todas as ferramentas para todo projeto. Rode primeiro o planner determinístico e materialize somente o que for aplicável:

```bash
python scripts/factory.py --root <projeto> independent-plan \
  --risk medium \
  --system-level multi-user-system \
  --api-mode contract
```

Quando a CLI central não estiver disponível no repositório do produto, use `VERIFICATION.md` + `core/INDEPENDENT_VERIFICATION.md` como contrato de seleção.

## Ferramentas default gratuitas/open source

- Trivy — dependências, secrets e misconfiguration;
- Semgrep Community Edition — SAST;
- StrykerJS — mutation testing JS/TS;
- mutmut — mutation testing Python;
- Schemathesis — property/fuzz/stateful API testing;
- OWASP ZAP — DAST baseline/active em alvo autorizado;
- axe-core + Playwright — acessibilidade automatizada;
- Lighthouse CI — regressão de performance/qualidade quando houver baseline estável.

## Workflow real

Ao gerar `.github/workflows/independent-verification.yml` para um projeto:

1. usar `permissions: contents: read` salvo necessidade explícita;
2. fixar versões/commits de actions e CLIs;
3. usar lockfile/instalação reproduzível;
4. não injetar secrets em fork PR;
5. iniciar app/banco com dados fictícios quando necessário;
6. usar `timeout-minutes`;
7. destruir serviços efêmeros com `if: always()`;
8. nunca inferir URL de produção para ZAP/Schemathesis destrutivo;
9. salvar apenas relatórios sem dados sensíveis;
10. separar `required` de `advisory`.

## Cadência recomendada

- iteração rápida: testes primários;
- PR: Trivy/Semgrep/axe + gates adversariais aplicáveis;
- release: mutation ampliado, ZAP ativo autorizado, Lighthouse com baseline e recovery quando exigido;
- schedule opcional: dependências/DAST periódico, somente se custo de CI e ambiente permitirem.

## Custo

A Factory não deve exigir SaaS pago ou segunda IA paga para esta camada. Em repositório privado, GitHub-hosted Actions pode consumir a franquia do plano; quando custo/minutos forem problema, use runner próprio/local já disponível em vez de habilitar cobrança sem autorização.
