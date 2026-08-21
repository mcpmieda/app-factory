# App Factory — Plano consolidado

## Visão

Criar um sistema operacional de desenvolvimento com IA: uma base portátil que orienta agentes a planejar, construir, testar, revisar e entregar aplicações com qualidade, usando o mínimo de intervenção manual do usuário.

## Problemas que a Factory deve resolver

- projetos começando do zero sem padrão;
- contexto perdido entre chats e agentes;
- excesso de microtarefas e cliques;
- código criado sem teste real;
- bibliotecas reinventadas;
- interfaces genéricas ou inconsistentes;
- uso desnecessário de agentes caros para tarefas simples;
- dificuldade para recuperar uma versão segura;
- regras importantes existindo apenas em documentação manual.

## Arquitetura da solução

A Factory será composta por:

1. **Core** — princípios, risco, roteamento e definição de pronto.
2. **Skills** — conhecimento especializado carregado sob demanda.
3. **Templates** — estruturas prontas por tipo de aplicação.
4. **UI system** — política de escolha e uso de shadcn, ReUI e HeroUI.
5. **Registry/MCP** — distribuição e consulta de componentes, regras, páginas, testes e automações.
6. **Scripts/CI** — guardrails executáveis.
7. **Research** — referências avaliadas como ADOTAR / INSPIRAR / DESCARTAR.

## Ferramentas e papéis

### ChatGPT

Preferir para produto, pesquisa, especificação, comparação de alternativas, arquitetura conceitual, documentação, revisão e pequenas alterações GitHub que não dependam de execução local.

### Codex

Preferir quando a tarefa exige repositório local, terminal, dependências, múltiplos arquivos coordenados, build, testes, navegador, debugging, migrations ou prova executável.

### Outros agentes

A Factory deve permanecer portátil. Claude Code, Cursor e futuros agentes podem ser usados por adaptadores sem alterar o núcleo.

## Estratégia de UI

- Sistemas administrativos e dashboards: **shadcn + ReUI** como primeira opção.
- shadcn é a base de composição e propriedade do código.
- ReUI é acelerador para componentes e padrões avançados.
- HeroUI é alternativa seletiva para aplicações em que seu sistema visual seja claramente mais adequado.
- Não misturar os três automaticamente.
- Pesquisar componente/bloco existente antes de implementar equivalente do zero.

## Estratégia de trabalho

- GitHub é a fonte de verdade.
- Trabalhar em fatias funcionais completas.
- Baseline/diff/rollback são essenciais em manutenção de sistemas existentes.
- Em projeto novo, evitar fragmentação artificial em microalterações.
- Fazer o máximo possível antes de pedir intervenção humana.
- Governança cresce proporcionalmente ao risco e à complexidade.
- Regras repetitivas devem virar mecanismos automáticos quando possível.

## Fases da Factory

### V0.1 — Bootstrap

Consolidar decisões, criar Core, primeiras Skills e templates mínimos.

### V0.2 — Pesquisa estruturada

Avaliar 30–50 repositórios e fontes fortes em agentes, starters, UI, auth, banco, testes, segurança, CI/CD e arquitetura. Classificar cada referência.

### V0.3 — Starter real

Criar starter de web app/admin com stack moderna e verificações automáticas.

### V0.4 — Registry + MCP

Distribuir componentes, layouts, regras, templates e automações pelo mecanismo apropriado.

### V0.5 — Projeto piloto

Construir uma aplicação pequena real usando somente a Factory. Registrar fricções e falhas.

### V1.0 — Estável

Factory validada por projeto real, com documentação enxuta, guardrails automáticos e fluxo portátil entre agentes.

## Critério principal de sucesso

Um usuário deve poder descrever o sistema em linguagem simples e receber orientação clara sobre o próximo passo e a ferramenta adequada, enquanto o agente assume a maior parte das decisões técnicas rotineiras e da execução verificável.