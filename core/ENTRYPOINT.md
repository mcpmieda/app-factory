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

O usuário não precisa conhecer stack, arquitetura, perfis, Skills, estados internos ou agentes.

## Primeira passagem obrigatória

1. Entenda o resultado real pretendido.
2. Determine se é projeto novo, evolução, manutenção, bug, automação ou pesquisa técnica.
3. Se existir repositório/projeto, recupere primeiro o estado versionado (`AGENTS.md`, `PROJECT_STATE.md`) e use o Context Engine para mapear/atualizar o contexto incremental quando disponível.
4. Se existir `.factory/state.json`, use o Autonomy Engine para retomar; se não existir, ele pode inicializar/inferir o objetivo a partir do estado versionado.
5. Classifique a escala em `core/PROJECT_SCALE.md`.
6. Verifique `profiles/` e selecione um perfil validado quando o produto corresponder claramente; não force perfil quando nenhum servir.
7. Aplique risco em `core/RISK_MODEL.md`.
8. Escolha o executor com `core/TASK_ROUTER.md`, priorizando as capacidades do agente atual + GitHub/CI antes de handoff.
9. Carregue apenas as Skills necessárias.
10. Pesquise solução existente antes de construir equivalente do zero quando houver ganho real.
11. Defina o próximo bloco funcional completo.
12. Execute imediatamente tudo que o ambiente atual permitir com segurança e continue o loop técnico sem pedir ao usuário o próximo passo rotineiro.

## Contexto incremental

`core/CONTEXT_ENGINE.md` define o mapa de repositório. O mapa é cache de navegação; arquivos reais e GitHub continuam sendo autoridade.

Ao retomar um projeto existente:

- atualize o mapa;
- leia primeiro o resumo compacto;
- abra em detalhe apenas os arquivos relevantes;
- se o fingerprint tiver mudado durante uma fase ativa, reconcilie o delta antes de continuar.

## Autonomia

`core/AUTONOMY_ENGINE.md` define a máquina de estados. O agente deve avançar por contexto, planejamento, implementação, verificação, reparo, revisão e entrega até concluir ou encontrar bloqueio real.

Não devolva ao usuário perguntas como "quer que eu continue?", "qual o próximo passo?" ou escolhas técnicas rotineiras quando o engine/agente puder decidir com segurança.

## Regra de perfis

Perfis transformam evidência real em defaults condicionais. Eles não substituem entendimento do produto.

Exemplo: um sistema de patrimônio com login, CRUD, filtros e dashboard provavelmente corresponde a `profiles/web-admin/PROFILE.md`. A Factory pode usar os defaults comprovados desse perfil, mas só ativa autenticação, banco, ReUI ou outros módulos quando o produto realmente precisar.

Requisitos específicos do projeto têm precedência sobre defaults do perfil, salvo conflito de segurança.

## Regra de GitHub

### Projeto novo

A Factory instalada já contém suas regras; não é necessário abrir o repositório `app-factory` a cada pedido apenas para reaprender o método.

Quando o projeto ganhar repositório próprio, grave nele pelo menos:

- `AGENTS.md` com vínculo explícito à App Factory;
- `PROJECT_STATE.md`;
- `.factory/state.json` em handoffs importantes quando o runtime estiver em uso;
- artefatos de produto/arquitetura proporcionais à escala;
- perfil selecionado e desvios relevantes quando aplicável;
- testes/CI quando aplicáveis.

O cache `.factory/context/` é regenerável e normalmente não deve ser versionado.

### Projeto existente

O repositório do projeto é a fonte de verdade. Não reconstrua contexto somente a partir de memória de chat quando o estado real puder ser lido no GitHub.

Se o `AGENTS.md` do projeto indicar App Factory, use o plugin/Skills instalados e as regras locais em conjunto. Regras locais específicas do projeto têm precedência sobre defaults genéricos, salvo conflito de segurança.

## Regra de interação

Não pergunte ao usuário qual framework, ORM, linter ou biblioteca usar quando isso for uma decisão técnica rotineira que o agente consegue avaliar.

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
- perfil selecionado, se houver;
- risco;
- fingerprint/contexto atual;
- fase e próxima ação do Autonomy Engine;
- Skill(s) necessárias;
- executor recomendado;
- evidência que definirá conclusão.

Para o usuário, explique somente o necessário e faça o máximo possível antes de devolver uma ação manual.

## Handoff

Quando uma fase realmente precisar mudar de executor, deixe estado no GitHub e forneça uma instrução curta baseada em Issue/PR/branch. O usuário não deve copiar a conversa inteira.
