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

O usuário não precisa conhecer stack, arquitetura, perfis, Skills ou agentes.

## Primeira passagem obrigatória

1. Entenda o resultado real pretendido.
2. Determine se é projeto novo, evolução, manutenção, bug, automação ou pesquisa técnica.
3. Se existir repositório/projeto, leia primeiro o estado versionado (`AGENTS.md`, `PROJECT_STATE.md`, produto/arquitetura e diff relevante).
4. Classifique a escala em `core/PROJECT_SCALE.md`.
5. Verifique `profiles/` e selecione um perfil validado quando o produto corresponder claramente; não force perfil quando nenhum servir.
6. Aplique risco em `core/RISK_MODEL.md`.
7. Escolha o ambiente com `core/TASK_ROUTER.md`.
8. Carregue apenas as Skills necessárias.
9. Pesquise solução existente antes de construir equivalente do zero quando houver ganho real.
10. Defina o próximo bloco funcional completo.
11. Execute imediatamente tudo que o ambiente atual permitir com segurança.

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
- artefatos de produto/arquitetura proporcionais à escala;
- perfil selecionado e desvios relevantes quando aplicável;
- testes/CI quando aplicáveis.

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
- dado externo indisponível.

## Saída da primeira passagem

O agente deve saber, mesmo que não exponha todos os detalhes:

- modo do trabalho;
- escala;
- perfil selecionado, se houver;
- risco;
- Skill(s) necessárias;
- ChatGPT, Codex ou outro ambiente recomendado;
- próximo bloco funcional;
- evidência que definirá conclusão.

Para o usuário, explique somente o necessário e faça o máximo possível antes de devolver uma ação manual.

## Handoff

Quando uma fase precisar mudar de ChatGPT para Codex ou vice-versa, deixe o estado no GitHub e forneça uma instrução curta baseada em Issue/PR/branch. O usuário não deve copiar a conversa inteira.