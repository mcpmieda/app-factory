# PROJECT_STATE

> Estado vigente da App Factory. Não usar como diário.

## Objetivo atual

Validar a App Factory em uma aplicação web administrativa real antes de promover tecnologias e padrões a defaults da V1.

## Estado

- fase: `V0.3 — piloto web-admin em revisão`;
- baseline oficial: `main` após merge do PR #2 (`d917a891b364502d01b3644431f4b5df1d4d588c`);
- V0.1 bootstrap: concluída;
- V0.2 pesquisa: concluída e integrada;
- Issue #3 / Codex Plugin: concluída e revisada;
- adaptador Codex: validado em piloto real;
- 10 Skills: validadas e descobertas pelo Codex;
- CI: valida estrutura, Agent Skills e Codex Plugin.

## Decisões vigentes

- Core permanece neutro e portátil;
- Codex usa adaptador/plugin fino sem duplicar Skills;
- processo varia por escala XS/S/M/L;
- `shadcn + ReUI` é candidato preferencial do perfil admin;
- HeroUI é perfil alternativo;
- Better Auth + Drizzle + Zod foram aprovados para promoção ao perfil web-admin, ainda não são defaults universais;
- Playwright foi aprovado como default E2E do perfil;
- Spec Kit deve ser usado proporcionalmente à escala;
- starters devem ser componíveis, sem serviços opcionais impostos.

## Trabalho atual

- bloco: Issue #4 — piloto `web-admin` implementado na branch `pilot/web-admin-v0.3`;
- ambiente recomendado: Codex;
- motivo: exige scaffold real, dependências, banco, autenticação, build, testes e navegador;
- regra: construir o piloto de forma isolada e não alterar o Core para acomodar resultados locais sem evidência.

## Próxima ação

Revisar o draft PR da Issue #4, especialmente o advisory transitivo do `drizzle-kit`, a classificação opcional do ReUI e a futura escolha de provider de produção. Não promover o piloto ao Core antes da revisão.

## Handoff

Outro agente deve começar por:

1. `AGENTS.md`;
2. este `PROJECT_STATE.md`;
3. `research/V0.3_WEB_ADMIN_PILOT.md`;
4. `pilots/web-admin/README.md`;
5. Issue #4 e seu draft PR.
