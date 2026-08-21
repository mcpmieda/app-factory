# PROJECT_STATE

> Estado vigente da App Factory. Não usar como diário.

## Objetivo atual

Transformar os aprendizados validados do piloto V0.3 em um perfil `web-admin` reutilizável e, depois, gerar um starter limpo para um segundo teste do zero.

## Estado

- fase: `V0.4 — promoção do perfil web-admin`;
- baseline oficial: `main` após merge do PR #6 (`2e786d39505cfdbc766f6481535cb65413d2b735`);
- V0.1 bootstrap: concluída;
- V0.2 pesquisa: concluída e integrada;
- V0.2.1 entry router: concluído e integrado;
- Issue #3 / Codex Plugin: concluída e revisada;
- V0.3 piloto web-admin: concluído, revisado, CI reproduzível e integrado;
- Issues #4 e #8: concluídas;
- CI: valida Core/Skills/plugin e o piloto web-admin em checkout limpo.

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
- Zod, Vitest, Playwright e lint oficial do Next foram promovidos para o perfil;
- Biome fica opcional/complementar;
- Spec Kit continua proporcional à escala;
- starters permanecem componíveis, sem serviços opcionais impostos;
- instalação limpa e CI reproduzível são gates, não apenas testes locais.

## Trabalho atual

- bloco: promover `profiles/web-admin/PROFILE.md` e ligar o perfil ao `factory-router`/`app-planner`;
- ambiente recomendado: ChatGPT + GitHub;
- motivo: é consolidação de arquitetura/documentação já comprovada, sem necessidade de ambiente local neste bloco;
- branch: `promote/web-admin-profile-v0.4`.

## Próxima ação

Após CI/revisão e merge da V0.4, criar uma Issue para Codex gerar um starter `web-admin` limpo a partir do perfil, sem copiar cegamente `pilots/web-admin/`, e validar um segundo app do zero.

## Handoff

Outro agente deve começar por:

1. `AGENTS.md`;
2. este `PROJECT_STATE.md`;
3. `profiles/web-admin/PROFILE.md`;
4. `research/V0.3_WEB_ADMIN_PILOT.md`;
5. `starters/web-admin/README.md`;
6. PR da branch `promote/web-admin-profile-v0.4` quando existir.