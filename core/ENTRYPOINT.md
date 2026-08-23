# Universal Entrypoint

A App Factory deve ser acionada pelo objetivo do usuário, sem exigir que ele diga explicitamente "use a App Factory".

## Quando ativar

Ative o `factory-router` sempre que o pedido envolver criar, construir, projetar, melhorar, modernizar, manter, corrigir, automatizar, integrar, migrar ou continuar software, incluindo:

- aplicação web;
- sistema administrativo;
- site;
- API/backend;
- extensão de navegador;
- automação/script/integração;
- ferramenta interna;
- app mobile/desktop;
- projeto existente no GitHub.

Também ative quando o usuário expressar apenas o resultado, por exemplo:

- "Quero criar um sistema de patrimônio para a escola."
- "Quero um site para a secretaria."
- "Melhore este painel administrativo."
- "Quero automatizar este processo."
- "Continue o projeto X."

O usuário não precisa conhecer stack, arquitetura, perfis, Skills, estados internos, semantic-spec ou agentes.

## Primeira passagem obrigatória

1. Entenda o resultado real pretendido.
2. Determine se é projeto novo, evolução, manutenção, bug, automação ou pesquisa técnica.
3. Se existir repositório/projeto, recupere primeiro o estado versionado (`AGENTS.md`, `PROJECT_STATE.md`) e use o Context Engine para mapear/atualizar o contexto incremental quando disponível.
4. Classifique **três eixos independentes** antes de fechar arquitetura: escala (`core/PROJECT_SCALE.md`), risco (`core/RISK_MODEL.md`) e nível do produto (`core/SYSTEM_ENGINEERING.md`).
5. Se o produto for `persistent-app` ou superior, registre a fonte autoritativa dos dados e impeça que `localStorage`, mocks, arrays locais ou JSON estático sejam tratados como persistência final compartilhada.
6. Se o produto for `multi-user-system` ou superior, derive explicitamente necessidades de backend/server-side, banco compartilhado, identidade, autorização, validação server-side, migrations e recuperação proporcional antes de escolher uma arquitetura simplificada.
7. Determine se existe uma fronteira de API/integração relevante. Quando existir, aplique `core/API_ENGINEERING.md` e classifique a governança da interface como `none`, `lightweight`, `contract` ou `governed`. Não crie API formal/OpenAPI apenas porque existe backend.
8. Para API `contract`/`governed`, identifique consumidores, protocolo e fonte de verdade machine-readable antes de consumidores dependerem de comportamento implícito; carregue `api-engineering` quando houver trabalho de interface/integração a executar.
9. Classifique se o trabalho exige Semantic Verification:
   - **sim** para funcionalidade nova, bugfix relevante, regra de negócio, contrato de dados/API ou mudança estrutural de médio/alto risco;
   - **não por padrão** para documentação/chore e refactor pequeno que não muda comportamento observável.
10. Se existir `.factory/state.json`, use o Autonomy Engine para retomar. Se não existir, inicialize/infera o objetivo; quando a classificação anterior exigir prova semântica, crie o novo estado com `require_spec` sem perguntar ao usuário por essa decisão técnica.
11. Verifique `profiles/` e selecione um perfil validado quando o produto corresponder claramente; não force perfil quando nenhum servir. Nenhum perfil pode reduzir requisitos mínimos de `core/SYSTEM_ENGINEERING.md` nem de `core/API_ENGINEERING.md` quando este se aplicar.
12. Quando Semantic Verification se aplicar, carregue `semantic-verification` e materialize o contrato estruturado antes da implementação. O agente preenche a spec; o usuário só entra se faltar uma regra genuinamente humana.
13. Escolha o executor com `core/TASK_ROUTER.md`, priorizando as capacidades do agente atual + GitHub/CI antes de handoff.
14. Carregue apenas as demais Skills necessárias.
15. Pesquise solução existente antes de construir equivalente do zero quando houver ganho real.
16. Defina o próximo bloco funcional completo e, quando aplicável, seus critérios `given/when/then` antes do código.
17. Execute imediatamente tudo que o ambiente atual permitir com segurança e continue o loop técnico sem pedir ao usuário o próximo passo rotineiro.

## Contexto incremental

`core/CONTEXT_ENGINE.md` define o mapa de repositório. O mapa é cache de navegação; arquivos reais e GitHub continuam sendo autoridade.

Ao retomar um projeto existente:

- atualize o mapa;
- leia primeiro o resumo compacto;
- abra em detalhe apenas os arquivos relevantes;
- se o fingerprint tiver mudado durante uma fase ativa, reconcilie o delta antes de continuar.

O grafo atual de imports é deliberadamente leve. Não fingir que ele é um call graph semântico universal; análises profundas devem ser promovidas somente após pilotos por stack/linguagem.

## Autonomia

`core/AUTONOMY_ENGINE.md` define a máquina de estados. O agente deve avançar por contexto, planejamento, especificação quando aplicável, implementação, verificação, reparo, revisão e entrega até concluir ou encontrar bloqueio real.

Não devolva ao usuário perguntas como "quer que eu continue?", "qual o próximo passo?" ou escolhas técnicas rotineiras quando o engine/agente puder decidir com segurança.

## Engenharia de sistemas

`core/SYSTEM_ENGINEERING.md` separa página/site, app local, app persistente, sistema multiusuário, sistema de produção e sistema crítico.

A classificação é por comportamento esperado, não pela palavra usada no pedido. Exemplos de sinais que elevam a arquitetura:

- dados institucionais compartilhados entre computadores;
- usuários com papéis diferentes;
- necessidade de histórico, autoria ou permissões;
- dados que não podem depender do armazenamento de um navegador;
- operação real de uma organização.

Para `multi-user-system` ou superior, interface funcional sozinha não prova completude. A arquitetura e os testes precisam cobrir a camada real de persistência, regras server-side e autorização aplicáveis.

## Engenharia de APIs

`core/API_ENGINEERING.md` é condicional e independente do nível do produto: ele governa a **interface**, não decide sozinho a arquitetura inteira.

Aplique quando existir API compartilhada, integração externa, múltiplos consumidores, webhook, evento/mensageria ou contrato de rede que precise evoluir com segurança. Para uma função/server action interna sem consumidor independente, mantenha o modo leve ou `none`.

Quando a interface for `contract`/`governed`, preserve uma fonte de verdade machine-readable adequada ao protocolo e gates proporcionais de lint, compatibilidade, runtime e segurança. OpenAPI, GraphQL, gRPC/Protobuf, AsyncAPI e Arazzo são opções condicionais, não tecnologias obrigatórias universais.

## Prova semântica

`core/SEMANTIC_VERIFICATION.md` define quando a intenção precisa virar alvo estruturado e verificável.

Quando aplicável:

- `specs/semantic-contract.json` define objetivo, invariantes e critérios observáveis;
- `specs/verification-plan.json` liga cada critério `must` a evidência executável/gate real;
- risco médio/alto exige revisão desacoplada, preferencialmente outro agente/contexto ou, na ausência, um `clean-context` baseado em spec + diff + evidências atuais;
- `specs/review-evidence.json` fica ligado por fingerprints àquilo que foi realmente revisado;
- código/spec/plano alterados depois tornam a revisão anterior stale.

Deterministic CI continua obrigatório quando aplicável, mas não é sozinho um reviewer semântico para risco médio/alto.

## Regra de perfis

Perfis transformam evidência real em defaults condicionais. Eles não substituem entendimento do produto, `core/SYSTEM_ENGINEERING.md` nem `core/API_ENGINEERING.md` quando houver interface relevante.

Exemplo: um sistema de patrimônio com login, CRUD, filtros e dashboard provavelmente corresponde a `profiles/web-admin/PROFILE.md`. A Factory pode usar os defaults comprovados desse perfil e deve ativar persistência, autenticação/autorização, API/integração ou outros módulos quando o nível do sistema e o produto exigirem.

Requisitos específicos do projeto têm precedência sobre defaults do perfil, salvo conflito de segurança ou redução indevida dos requisitos mínimos do nível de sistema/interface.

## Regra de GitHub

### Projeto novo

A Factory instalada já contém suas regras; não é necessário abrir o repositório `app-factory` a cada pedido apenas para reaprender o método.

Quando o projeto ganhar repositório próprio, grave nele pelo menos:

- `AGENTS.md` com vínculo explícito à App Factory;
- `PROJECT_STATE.md`;
- `.factory/state.json` em handoffs importantes quando o runtime estiver em uso;
- artefatos de produto/arquitetura proporcionais à escala;
- nível de sistema e fonte autoritativa dos dados quando `persistent-app` ou superior;
- modo/fonte de verdade da API quando `contract`/`governed` se aplicar;
- `specs/` semânticos quando a mudança exigir esse nível de prova;
- perfil selecionado e desvios relevantes quando aplicável;
- testes/CI quando aplicáveis.

O cache `.factory/context/` é regenerável e normalmente não deve ser versionado.

### Projeto existente

O repositório do projeto é a fonte de verdade. Não reconstrua contexto somente a partir de memória de chat quando o estado real puder ser lido no GitHub.

Se o `AGENTS.md` do projeto indicar App Factory, use o plugin/Skills instalados e as regras locais em conjunto. Regras locais específicas do projeto têm precedência sobre defaults genéricos, salvo conflito de segurança.

## Regra de interação

Não pergunte ao usuário qual framework, ORM, linter, biblioteca, protocolo ou modo interno de verificação usar quando isso for uma decisão técnica rotineira que o agente consegue avaliar.

Pergunte quando faltar:

- regra de negócio;
- prioridade de produto;
- preferência subjetiva relevante;
- orçamento/custo;
- autorização de risco;
- credencial ou dado externo indisponível;
- decisão legal/organizacional.

## Saída da primeira passagem

O agente deve saber, mesmo que não exponha todos os detalhes:

- modo do trabalho;
- escala;
- **nível do sistema**;
- fonte autoritativa dos dados quando aplicável;
- modo de governança da API e contrato autoritativo quando aplicável;
- perfil selecionado, se houver;
- risco;
- se Semantic Verification é exigida;
- fingerprint/contexto atual;
- fase e próxima ação do Autonomy Engine;
- Skill(s) necessárias;
- executor recomendado;
- evidência que definirá conclusão.

Para o usuário, explique somente o necessário e faça o máximo possível antes de devolver uma ação manual.

## Handoff

Quando uma fase realmente precisar mudar de executor, deixe estado no GitHub e forneça uma instrução curta baseada em Issue/PR/branch. O usuário não deve copiar a conversa inteira.