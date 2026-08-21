# PROJECT_STATE

> Estado vigente da App Factory. Não usar como diário.

## Objetivo atual

Revisar o hardening V0.6 que promove o perfil `web-admin` a candidato `v1-rc`, com recipes diretamente verificáveis, PostgreSQL de produção e manutenção segura de Better Auth/schema.

## Estado

- fase: `V0.6 — hardening implementado; aguardando revisão do draft PR`;
- baseline oficial: `main` após merge do PR #11 (`7339a25f401813f6c05778e3f30228f518914a95`);
- V0.1 bootstrap: concluída;
- V0.2 pesquisa: concluída e integrada;
- V0.2.1 entry router: concluído e integrado;
- Issue #3 / Codex Plugin: concluída e revisada;
- V0.3 piloto web-admin: concluído, revisado, CI reproduzível e integrado;
- V0.4 perfil web-admin: concluído e integrado;
- V0.5 starter + segundo app: concluída, revisada e integrada;
- Issues #4, #8 e #10: concluídas;
- Issue #12: implementação concluída na branch `pilot/web-admin-hardening-v0.6`;
- CI: valida Core/Skills/plugin, starter base, recipes SQLite diretos, PostgreSQL/Auth em banco real efêmero e exemplo `asset-admin` V0.5.

## Decisões vigentes

- Core permanece neutro e portátil;
- Codex usa adaptador/plugin fino sem duplicar Skills;
- intenção de software ativa a Factory automaticamente;
- processo varia por escala XS/S/M/L;
- Factory pode selecionar perfil validado em `profiles/` após entender o produto;
- perfil não é dogma e módulos opcionais só entram quando necessários;
- no perfil `web-admin`, shadcn é a base visual;
- ReUI é opcional/seletivo por componente avançado;
- Better Auth é primeira opção condicional quando o projeto exige autenticação própria;
- Drizzle é primeira opção condicional quando o projeto exige persistência própria;
- SQLite/better-sqlite3 permanece provider local/teste, não default universal de produção;
- V0.6 deve validar PostgreSQL como caminho de produção sem contaminar o starter base;
- Zod, Vitest, Playwright e lint oficial do Next fazem parte da base validada do perfil;
- Biome permanece opcional/complementar;
- starters permanecem componíveis, sem serviços opcionais impostos;
- instalação limpa, recipes gerados e CI reproduzível são gates de qualidade;
- migrations destrutivas não devem ser aplicadas automaticamente sem análise;
- recipes podem declarar capabilities, conflitos e variantes pequenas, sem virar framework complexo;
- Better Auth e sua CLI de schema são fixados juntos em 1.7.1 no baseline V0.6;
- o perfil `web-admin` é candidato `v1-rc`, não declaração de V1 estável ou produção pública já implantada.

## Trabalho atual

- bloco: Issue #12 — hardening pré-V1 do perfil `web-admin`;
- resultado: gerador resolve providers/conflitos; recipes são testados em árvores limpas; PostgreSQL/Auth tem migration, seed, query, sessão, schema check, build e smoke de produção;
- regressão: starter mínimo e `examples/asset-admin` SQLite permanecem inalterados funcionalmente e cobertos pelo workflow;
- gate humano remanescente: somente autorização/conta/recurso/segredos para um deploy público real;
- regra: abrir draft PR e não fazer merge automático.

## Próxima ação

Revisar o draft PR da Issue #12 e seus checks finais. Não fazer merge automático; um deploy público real deve ser autorizado como fase separada.

## Handoff

Outro agente deve começar por:

1. `AGENTS.md`;
2. este `PROJECT_STATE.md`;
3. draft PR e Issue #12;
4. `profiles/web-admin/PROFILE.md`;
5. `starters/web-admin/README.md`;
6. `research/V0.6_WEB_ADMIN_HARDENING.md`;
7. `.github/workflows/validate-web-admin-starter.yml`.
