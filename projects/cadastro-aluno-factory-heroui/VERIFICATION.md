# VERIFICATION

## Classificação

- risco: `low`;
- nível do sistema: `local-app`;
- API mode: `none`;
- Independent Verification: `baseline`;
- executor preferido: `github_ci`;
- política de custo: `free-only`.

A classificação `baseline` é deliberada: o produto não possui backend, API independente, autenticação, banco remoto ou integração externa. Elevar para `independent/adversarial` adicionaria ferramentas sem uma superfície real adicional para provar.

## Evidência primária

| Superfície | Gate | Status esperado |
| --- | --- | --- |
| lint | `package:lint` | required |
| typecheck | `package:typecheck` | required |
| regras/migração/exportação/invariantes de coleção | `package:test` | required |
| build | `package:build` | required |
| comportamento desktop/mobile | `package:e2e` | required |
| dependências | `npm audit` no workflow | required |
| semantic spec/assurance/traceability | validadores App Factory | required |
| revisão semântica | `semantic-status` | required |

## Evidência obtida no field test

- 17/17 testes unitários aprovados;
- 10/10 E2E aprovados em Chromium desktop/mobile;
- lint, typecheck e build aprovados;
- `npm audit` completo aprovado;
- migração v1 → v2 exercitada no navegador;
- backup/restauração exercitados no navegador;
- leitura, escrita, exportação e restauração rejeitam coleções com matrículas equivalentes duplicadas;
- Semantic Assurance com 7/7 requisitos obrigatórios rastreados, 7/7 critérios `must` com gate executável e 4/4 invariantes referenciados.

## Revisão semântica

Como o risco do contrato é `low`, `deterministic-ci` é um modo válido de revisão semântica conforme a política atual. A revisão só é registrada depois que todos os gates obrigatórios executam sobre o mesmo estado do projeto. Qualquer mudança posterior dentro do projeto invalida o fingerprint e exige nova revisão.

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
- rejeição de coleção v2 adulterada com matrícula duplicada;
- confirmação antes de substituição;
- persistência após reload.

## Regra

Ferramenta não selecionada é `not-applicable`, não `pass`. O projeto só fecha quando todos os checks `required` executarem no estado final reproduzível com lockfile versionado e `npm ci`.
