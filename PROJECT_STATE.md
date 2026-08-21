# PROJECT_STATE

> Estado vigente da App Factory. Não usar como diário.

## Objetivo atual

Validar em revisão o starter `web-admin` limpo e o segundo aplicativo gerado do zero, provando que o conhecimento promovido na V0.4 é reutilizável.

## Estado

- fase: `V0.5 — starter e segundo app implementados; aguardando revisão do draft PR`;
- baseline oficial: `main` após merge do PR #9 (`2e2ca4e8fef963a1fe126b84e7ff55470742b66a`);
- V0.1 bootstrap: concluída;
- V0.2 pesquisa: concluída e integrada;
- V0.2.1 entry router: concluído e integrado;
- Issue #3 / Codex Plugin: concluída e revisada;
- V0.3 piloto web-admin: concluído, revisado, CI reproduzível e integrado;
- V0.4 perfil web-admin: concluído, CI aprovado e integrado;
- Issues #4 e #8: concluídas;
- Issue #10: implementação concluída localmente na branch `pilot/web-admin-starter-v0.5`;
- CI: valida Core/Skills/plugin, piloto V0.3 e o novo starter/exemplo V0.5 em checkout limpo.

## Decisões vigentes

- Core permanece neutro e portátil;
- Codex usa adaptador/plugin fino sem duplicar Skills;
- intenção de software ativa a Factory automaticamente;
- processo varia por escala XS/S/M/L;
- Factory pode selecionar perfil validado em `profiles/` após entender o produto;
- perfil não é dogma e módulos opcionais só entram quando necessários;
- no perfil `web-admin`, shadcn é a base visual;
- ReUI é opcional/seletivo por componente avançado;
- HeroUI é perfil visual alternativo;
- Better Auth é primeira opção condicional quando o projeto exige autenticação própria;
- Drizzle é primeira opção condicional quando o projeto exige persistência própria;
- provider de banco é escolhido pelo ambiente; SQLite/better-sqlite3 fica local/teste salvo requisito real;
- Zod, Vitest, Playwright e lint oficial do Next fazem parte da base validada do perfil;
- Biome fica opcional/complementar;
- Spec Kit continua proporcional à escala;
- starters permanecem componíveis, sem serviços opcionais impostos;
- instalação limpa e CI reproduzível são gates, não apenas testes locais.

## Trabalho atual

- bloco: Issue #10 — gerar starter limpo e validar segundo app do zero;
- ambiente: Codex;
- resultado: starter limpo, gerador, três recipes e `examples/asset-admin/` criados a partir do perfil V0.4;
- decisão: Better Auth/Drizzle foram ativados no exemplo; ReUI foi dispensado por falta de complexidade que justificasse o grid;
- evidência: `research/V0.5_WEB_ADMIN_STARTER_VALIDATION.md`, testes, workflow e screenshots V0.5;
- regra: não fazer merge automático.

## Próxima ação

Revisar o draft PR da Issue #10 e os checks finais do gerador temporário e do exemplo antes de qualquer promoção para V1. Não fazer merge automático.

## Handoff

Outro agente deve começar por:

1. `AGENTS.md`;
2. este `PROJECT_STATE.md`;
3. Issue #10;
4. `profiles/web-admin/PROFILE.md`;
5. `starters/web-admin/README.md`;
6. `research/V0.5_WEB_ADMIN_STARTER_VALIDATION.md`;
7. `examples/asset-admin/PROJECT_STATE.md` e `.app-factory.json`.
