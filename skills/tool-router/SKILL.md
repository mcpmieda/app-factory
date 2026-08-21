---
name: tool-router
description: Decide qual ambiente, agente ou ferramenta deve executar cada fase de um projeto, priorizando simplicidade, custo, capacidade de verificação e mínimo trabalho manual do usuário.
---

# Tool Router

Use quando houver dúvida sobre onde executar uma tarefa ou quando uma fase do projeto estiver mudando de natureza.

## Regra

Classifique a necessidade antes de escolher a ferramenta.

### ChatGPT
Preferir para raciocínio, produto, pesquisa, arquitetura conceitual, documentação, revisão e pequenas edições GitHub que não dependam de execução local.

### Codex
Preferir quando houver necessidade de checkout/local, terminal, múltiplos arquivos, dependências, build, testes, navegador, debugging, migrations ou prova executável.

### Outro agente
Só recomendar quando trouxer vantagem concreta não coberta pelo ambiente atual. A Factory não deve empurrar o usuário para novas ferramentas por novidade.

## Economia inteligente

Não usar Codex apenas porque existe código envolvido. Não evitar Codex quando a segurança da conclusão depende de executar e testar o sistema.

## Menor trabalho humano

Se o agente atual puder fazer a tarefa com segurança, faça. Não mande o usuário abrir terminal, copiar arquivos ou executar comandos que um agente com acesso adequado pode executar.

## Handoff

Ao encaminhar para outro ambiente, forneça apenas o contexto necessário e a referência ao estado versionado do projeto.