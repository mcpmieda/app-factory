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
- **D-023:** software real novo criado pela Factory deve usar, por padrão, `projects/<slug-do-projeto>/`; `examples/`, `audits/` e `starters/` permanecem reservados a evidência, auditoria e moldes da própria Factory.
- **D-024:** o endereço canônico de inspeção/uso deve ser simples e baseado em caminho sob `escolaieda.com`, por exemplo `https://escolaieda.com/bancodenotas`; o slug público preferido é compacto, em minúsculas, sem acentos, espaços ou pontuação quando isso não gerar ambiguidade.
- **D-025:** hospedagem é detalhe interno: conteúdo estático pode ser servido diretamente pelo site escolar; aplicações com backend/runtime podem usar Vercel ou outro backend adequado, mas devem permanecer acessíveis pelo mesmo padrão `escolaieda.com/<slug>` através de rewrite/proxy quando a infraestrutura permitir.
- **D-026:** URLs temporárias de preview/deploy são técnicas e descartáveis; a Factory deve apresentar ao usuário principalmente o endereço canônico simples e manter o mesmo link após atualizações aprovadas.
- **D-027:** alterações de DNS, domínio ou roteamento global do `escolaieda.com` são infraestrutura de maior impacto e exigem implantação controlada; até essa camada estar configurada, a Factory deve registrar a URL canônica desejada sem fingir que o roteamento já existe.
- **D-028:** funcionalidade nova, bugfix relevante, regra de negócio, contrato de dados/API e mudança estrutural de médio/alto risco devem possuir contrato semântico verificável antes da implementação; documentação/chore e refactor pequeno sem mudança observável permanecem leves.
- **D-029:** critérios `must` da spec precisam ser rastreados até evidência executável/gate declarado; testes escritos somente depois da implementação, sem vínculo com a intenção, não bastam como prova semântica.
- **D-030:** risco médio/alto exige revisão semântica desacoplada antes da entrega: `independent-agent` quando disponível ou `clean-context` como fallback provider-neutral; deterministic CI sozinho continua necessário, mas não suficiente como reviewer semântico.
- **D-031:** review evidence é ligado por fingerprint à spec, ao plano de verificação e ao conteúdo revisado; qualquer mudança posterior invalida a revisão anterior até nova passagem.
- **D-032:** visual regression é gate condicional quando existe baseline visual estável e regressão visual é risco material; não criar snapshots frágeis para interfaces ainda exploratórias.
- **D-033:** não promover call graph universal superficial baseado em regex como se fosse análise semântica; dependência profunda deve ser pilotada por linguagem/stack antes de virar regra da Factory.
- **D-034:** typecheck/build/lockfile/runtime são defesa padrão contra uso incorreto de APIs; integrações não tipadas ou dependentes de runtime devem ganhar smoke/integration evidence específica em vez de consulta online obrigatória e instável no CI.

Quando uma decisão for substituída, registrar a nova decisão e marcar a anterior como superada; não apagar silenciosamente o histórico.
