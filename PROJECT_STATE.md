# PROJECT_STATE

> Estado vigente da App Factory. Não usar como diário.

## Objetivo atual

Executar a **auditoria final V1.0 end-to-end em ambiente limpo**, provando bootstrap/plugin isolado, roteamento por pedido comum, criação real do zero, qualidade executável, continuidade por outro agente e recuperação após regressão controlada.

## Estado

- fase: `V1.0 release candidate — aguardando revisão final`;
- baseline oficial: `main` após merge da V0.9 (`38421c037c04df1999701e56a7c8946e80bba486`);
- V0.1 bootstrap: concluída e integrada;
- V0.2 pesquisa: concluída e integrada;
- V0.2.1 entry router: concluído e integrado;
- V0.3 piloto web-admin: concluído e integrado;
- V0.4 perfil web-admin: concluído e integrado;
- V0.5 starter + segundo app: concluída e integrada;
- V0.6 hardening PostgreSQL/Auth: concluído e integrado;
- V0.7 Living UI / Semantic Motion: concluída e integrada;
- V0.8 Living UI executável: concluída e integrada;
- V0.9 validação universal: concluída, revisada e integrada;
- Issue #22: concluída;
- Issue #25: aberta e liberada para Codex;
- perfil `web-admin`: `v1-rc`;
- perfis `website`, `web-app`, `chrome-extension` e `automation`: `validated`;
- CI: Core/Skills/plugin, web-admin starter/recipes, PostgreSQL/Auth real, asset-admin, Living UI e quatro pilotos universais.

## Decisões vigentes

- intenção de software ativa a Factory automaticamente;
- AI serve ao objetivo, não ao texto literal do prompt;
- reuse-first e maior fatia segura são regras centrais;
- perfis são defaults condicionais, não stacks universais;
- stack `web-admin` não contamina outros tipos por reflexo;
- Living UI / Semantic Motion é transversal quando existe UI;
- Motion Profile default contextual: `ambient`;
- `prefers-reduced-motion` é obrigatório para movimento não essencial;
- `web-admin` tem caminho validado Better Auth + Drizzle + PostgreSQL quando necessário;
- website, web-app, Chrome extension e automation possuem contratos validados próprios;
- instalação limpa, testes executáveis, CI reproduzível, recuperação e continuidade via GitHub são gates de release;
- refinamentos não bloqueantes e novos perfis ficam para pós-V1.

## Trabalho atual

- bloco: Issue #25 — auditoria final V1.0;
- ambiente recomendado: Codex em configuração/diretórios isolados sempre que possível;
- pedido final do teste é linguagem natural e não contém stack/framework;
- projeto de auditoria deve nascer do zero e provar uma jornada real de empréstimo/devolução de equipamentos;
- segundo agente sem contexto deve conseguir compreender, modificar e validar o projeto apenas pelo repositório;
- uma regressão controlada deve ser detectada e recuperada antes do baseline final verde;
- nenhuma tag/release V1.0 deve ser criada antes da revisão final do ChatGPT.

## Próxima ação

Revisar o draft PR da Issue #25, seus checks, o relatório `research/V1.0_FINAL_AUDIT.md`, a evidência do segundo agente e o teste de recuperação. Não fazer merge, tag ou release antes dessa revisão.

Se todos os critérios objetivos passarem e o relatório declarar `APP FACTORY V1.0 READY FOR RELEASE`, a próxima ação será revisar, integrar e publicar/taguear a V1.0. Não criar fase intermediária apenas por refinamento.

## Handoff

Outro agente deve começar por:

1. `AGENTS.md`;
2. este `PROJECT_STATE.md`;
3. Issue #25;
4. `core/ENTRYPOINT.md`;
5. `skills/factory-router/SKILL.md`;
6. `profiles/README.md`;
7. somente depois, os Skills/perfis que o roteamento indicar;
8. `research/V0.9_UNIVERSAL_VALIDATION.md` apenas como evidência anterior, não como instrução para copiar os pilotos.
