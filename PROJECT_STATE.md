# PROJECT_STATE

> Estado vigente da App Factory. Não usar como diário.

## Objetivo atual

Validar a App Factory em uma aplicação web administrativa real antes de promover tecnologias e padrões a defaults da V1.

## Estado

- fase: `V0.3 — piloto web-admin com bloqueadores de revisão corrigidos`;
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

- bloco: Issue #8 — corrigir reprodutibilidade e prova do ciclo destrutivo no draft PR #6;
- ambiente recomendado: Codex;
- motivo: exige scaffold real, dependências, banco, autenticação, build, testes e navegador;
- regra: construir o piloto de forma isolada e não alterar o Core para acomodar resultados locais sem evidência.

## Próxima ação

Revisar os checks finais do draft PR #6 após a correção da Issue #8. Confirmar `npm ci` reproduzível e o Playwright ampliado antes de qualquer promoção ao Core; não fazer merge automático.

## Handoff

Outro agente deve começar por:

1. `AGENTS.md`;
2. este `PROJECT_STATE.md`;
3. `research/V0.3_WEB_ADMIN_PILOT.md`;
4. `pilots/web-admin/README.md`;
5. Issues #4/#8 e o draft PR #6.
