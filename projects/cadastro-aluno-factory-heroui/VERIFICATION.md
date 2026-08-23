# VERIFICATION

## Classificação

- risco: `low`;
- nível do sistema: `local-app`;
- API mode: `none`;
- Independent Verification: `independent`;
- executor preferido: `github_ci`;
- política de custo: `free-only`.

## Evidência primária

| Superfície | Gate | Status esperado |
| --- | --- | --- |
| lint | `package:lint` | required |
| typecheck | `package:typecheck` | required |
| regras/migração/exportação | `package:test` | required |
| build | `package:build` | required |
| comportamento desktop/mobile | `package:e2e` | required |
| dependências | `npm audit --audit-level=high` no workflow | required |
| semantic spec/assurance/traceability | validadores App Factory | required |

## Verificadores deliberadamente não selecionados

- API fuzz/RESTler/Schemathesis: sem API independente;
- ZAP/DAST ativo: não há superfície de backend autenticada ou API a ser atacada neste field test;
- Squawk: sem PostgreSQL/migrations SQL;
- k6: nenhum workload/SLO de servidor faz parte do requisito;
- Toxiproxy: sem integração externa material;
- mutation testing: custo adicional não justificado pelo baixo risco desta fatia;
- cross-browser completo: Chromium desktop/mobile é suficiente para esta demonstração; expandir somente se suporte multi-engine virar requisito.

## Recovery testado

- migração automática v1 → v2;
- backup JSON válido;
- rejeição de backup inválido;
- confirmação antes de substituição;
- persistência após reload.

## Regra

Ferramenta não selecionada é `not-applicable`, não `pass`. O projeto só fecha quando todos os checks `required` executarem no estado final reproduzível.
