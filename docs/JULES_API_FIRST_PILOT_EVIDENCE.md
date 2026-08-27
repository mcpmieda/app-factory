# Evidência do piloto Jules API-first

## Identificação

- Repositório: `mcpmieda/ecossistema-escola`
- Parent issue: `#80`
- Run ID: `jules-api-pilot-002`
- Integration branch: `factory/jules-api-pilot-002`
- Target: `main`
- Paralelismo: `2`
- PR final draft: `#93`
- Head homologado: `88be41f559e8dc2d35a17da27741080182f5f91c`

## Tasks

- `#81` — worker A
- `#82` — worker B
- `#83` — verificação, dependente de A+B

## Resultado

1. A e B foram criadas pela REST API Jules e executadas em paralelo.
2. Jules criou os PRs `#84` e `#85` com um único arquivo por task e dentro do escopo.
3. B passou pelo CI e foi squash-merged somente na integration branch.
4. A chegou a `factory:ci`; após restart do runner, foi retomada sem nova sessão Jules.
5. O CI de A foi localizado pelo `head_sha` exato e A foi integrada somente na integration branch.
6. A conclusão de A+B liberou automaticamente a task dependente `#83`.
7. Jules criou o resultado de verificação no PR `#92`; CI passou e o PR foi integrado somente na integration branch.
8. O CI final da integration branch, run `33029827105`, concluiu `success` para o SHA exato homologado.
9. O PR final `#93` foi criado como draft de integration para `main` e marcado `factory:final`.
10. O CI do PR final, run `33071522640`, concluiu `success`.
11. Format, lint, typecheck, semantic contract, tests, build, actionlint, GitHub control-plane policy e zizmor passaram.
12. Deploy production e recovery after deploy ficaram corretamente `skipped`.
13. Nenhum merge final foi feito.
14. Nenhuma produção foi ativada.

## Bug e hardening comprovados

O piloto anterior revelou que tasks em `factory:ci` não eram retomadas. O hotfix integrado pelo PR `#91` tornou esse estado reconciliável:

- `running` e `ci` são processáveis;
- `merged/failed` não são reprocessados;
- retomada não cria sessão Jules duplicada;
- sessão/PR existentes são reutilizados;
- CI exige `workflow_dispatch` e `head_sha` exato;
- CI verde existente do mesmo SHA não é duplicado;
- merge continua restrito à integration branch.

## Limitação operacional encontrada

O runner concluiu tasks e CI, mas o `GITHUB_TOKEN` não pôde criar o PR final porque a configuração do repositório **Allow GitHub Actions to create and approve pull requests** está desativada.

Para preservar o gate humano, o PR draft `#93` foi criado pelo GitHub Control Plane conectado. Isso não invalida a prova da orquestração Jules, mas futuras Factory Runs só encerrarão com criação totalmente autônoma do PR final quando essa permissão administrativa for habilitada.

## Conclusão

Com base nessa execução real, estão comprovados:

- Jules API-first;
- paralelismo controlado;
- dependency release;
- integration branch isolada;
- CI por SHA exato;
- retomada durável de `factory:ci`;
- merge automático somente para integration;
- CI final completo;
- PR final draft/humano;
- produção protegida.

A prova cobre o caminho Jules. Antigravity, OpenCode/Ollama, health/fallback e Merge Train multi-provider ainda exigem pilotos live próprios.
