# App Factory — Decisões vigentes

- **D-001:** a Factory vive em repositório próprio.
- **D-002:** `AGENTS.md` é mapa curto; detalhes ficam em Core, Skills e políticas.
- **D-003:** GitHub é a fonte técnica de verdade; chat não é o mecanismo principal de continuidade.
- **D-004:** o núcleo deve ser portátil entre ChatGPT, Codex, Claude Code, Cursor e futuros agentes.
- **D-005:** a Factory deve escolher executor por capacidade, não exigir que o usuário decida ChatGPT/Codex manualmente.
- **D-006:** o agente deve minimizar trabalho manual do usuário e assumir decisões técnicas rotineiras.
- **D-007:** trabalhar em blocos funcionais completos, não microtarefas artificiais.
- **D-008:** baseline/diff/rollback são fortes em manutenção, não dogma para criação de projeto novo.
- **D-009:** admin/dashboard/CRUD avalia primeiro shadcn + ReUI; HeroUI é alternativa seletiva.
- **D-010:** pesquisar e reutilizar antes de criar equivalente do zero.
- **D-011:** pesquisar 30–50 referências fortes antes de congelar a V1.
- **D-012:** a pasta histórica `Boas práticas/` é origem de princípios, não conteúdo para copiar integralmente.
- **D-013:** usar Skills modulares e carregamento progressivo de contexto.
- **D-014:** Registry/MCP recebe somente padrões validados em starter/piloto.
- **D-015:** o repositório começa privado.
- **D-016:** a stack final não deve ser congelada antes da pesquisa e do piloto.
- **D-017:** validação executável faz parte da implementação; build isolado não prova comportamento/UX.
- **D-018:** governança cresce proporcionalmente ao risco e à complexidade.
- **D-019:** Execution Fabric filtra por capacidade/disponibilidade e usa `current_agent → github_ci → sandbox → local_full` como ordem baseline, sem tornar Codex dependência arquitetural.
- **D-020:** Learning Engine é local-only e privacy-safe por padrão; somente metadados técnicos allowlisted podem ser persistidos e nenhuma telemetria externa é enviada.
- **D-021:** aprendizado é subordinado a capacidade, disponibilidade, fallback da tarefa, segurança/risco e Definition of Done; amostra pequena não altera o baseline e `local_full` não é promovido sobre backend leve capaz apenas por score.
- **D-022:** duração usada pelo aprendizado mede execuções bem-sucedidas; falhar rápido nunca deve melhorar a preferência de executor.

Quando uma decisão for substituída, registrar a nova decisão e marcar a anterior como superada; não apagar silenciosamente o histórico.
