# PROJECT_STATE

> Estado vigente da App Factory. Não usar como diário.

## Objetivo atual

Gerar um starter `web-admin` limpo a partir do perfil V0.4 e validar um segundo aplicativo criado do zero, provando que o conhecimento é reutilizável e não dependente do primeiro piloto.

## Estado

- fase: `V0.5 — starter web-admin + segundo app do zero`;
- baseline oficial: `main` após merge do PR #9 (`2e2ca4e8fef963a1fe126b84e7ff55470742b66a`);
- V0.1 bootstrap: concluída;
- V0.2 pesquisa: concluída e integrada;
- V0.2.1 entry router: concluído e integrado;
- Issue #3 / Codex Plugin: concluída e revisada;
- V0.3 piloto web-admin: concluído, revisado, CI reproduzível e integrado;
- V0.4 perfil web-admin: concluído, CI aprovado e integrado;
- Issues #4 e #8: concluídas;
- Issue #10: aberta e liberada para Codex;
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
- Zod, Vitest, Playwright e lint oficial do Next fazem parte da base validada do perfil;
- Biome fica opcional/complementar;
- Spec Kit continua proporcional à escala;
- starters permanecem componíveis, sem serviços opcionais impostos;
- instalação limpa e CI reproduzível são gates, não apenas testes locais.

## Trabalho atual

- bloco: Issue #10 — gerar starter limpo e validar segundo app do zero;
- ambiente recomendado: Codex;
- motivo: exige scaffold real, gerador, dependências, recipes condicionais, testes, build e navegador;
- regra: não copiar cegamente `pilots/web-admin/`; usar `profiles/web-admin/PROFILE.md` como fonte de decisão;
- não fazer merge automático ao concluir.

## Próxima ação

Executar integralmente a Issue #10 no Codex, abrir draft PR com evidências e devolver para revisão do ChatGPT.

## Handoff

Outro agente deve começar por:

1. `AGENTS.md`;
2. este `PROJECT_STATE.md`;
3. Issue #10;
4. `profiles/web-admin/PROFILE.md`;
5. `starters/web-admin/README.md`;
6. `research/V0.3_WEB_ADMIN_PILOT.md`.