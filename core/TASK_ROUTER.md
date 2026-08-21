# Task Router — escolha de ambiente e agente

A Factory deve orientar explicitamente o usuário sobre onde executar cada fase.

## Regra principal

Escolha pelo tipo de trabalho, não pela palavra "código".

### Preferir ChatGPT

Quando a tarefa for principalmente produto, pesquisa, comparação de alternativas, arquitetura conceitual, documentação, revisão ou pequena alteração GitHub que não dependa de execução local.

### Preferir Codex

Quando exigir checkout/local, vários arquivos coordenados, dependências, terminal, servidor local, lint/typecheck/testes/build, browser/E2E, debugging real, migrations, refatoração ampla ou prova executável.

### Tanto faz

README, texto, pequenas configurações e revisão simples podem ficar no ambiente já aberto. Se equivalentes, prefira ChatGPT para preservar recursos do Codex.

## Heurística

1. Precisa executar projeto/comandos? → Codex.
2. Precisa observar comportamento no navegador? → Codex.
3. Precisa modificar muitos arquivos interdependentes? → Codex.
4. É raciocínio/pesquisa/especificação/revisão? → ChatGPT.
5. É edição pequena via GitHub verificável sem ambiente local? → ChatGPT.
6. Há risco que exige prova antes de merge? → Codex implementa/verifica; ChatGPT pode revisar.

## Comunicação

Ao mudar de ambiente, informe fase, ambiente recomendado, motivo em uma frase e o que fica registrado no GitHub para continuidade.

Não encaminhe ao Codex sem necessidade. Não tente concluir apenas no ChatGPT uma tarefa que precisa de execução real para ser segura.

## Futuro

O núcleo classifica a necessidade; adaptadores mapeiam para ChatGPT, Codex, Claude Code, Cursor ou outra ferramenta disponível.