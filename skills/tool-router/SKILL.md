---
name: tool-router
description: Decide qual capacidade, agente ou ferramenta deve executar cada fase de um projeto, usando a Execution Fabric e priorizando current-agent + GitHub/CI antes de um executor local completo.
---

# Tool Router

Use quando houver dúvida sobre onde executar uma tarefa ou quando uma fase do projeto mudar de natureza.

## Regra

Não escolha uma marca primeiro. Traduza a tarefa em capacidades e use `execution-router` / Execution Fabric para selecionar o backend mais leve capaz.

Ordem padrão:

1. `current_agent` — ferramentas já disponíveis para raciocínio, arquivos, GitHub e conectores;
2. `github_ci` — Actions para comandos determinísticos, testes, build e prova reproduzível;
3. `sandbox` — shell leve quando declarado disponível e suficiente;
4. `local_full` — Codex ou outro executor completo somente quando houver capacidade local/interativa necessária.

## Current-agent + GitHub/CI

Não limite o agente atual a documentação ou pequenas edições. Se ele consegue coordenar arquivos, enviar branch, observar CI, ler logs, corrigir e repetir com segurança, permaneça nele.

Múltiplos arquivos e existência de testes não são motivo para handoff.

## CI como executor

Use CI para lint/format/typecheck, unit/integration/E2E headless, build, migrations em banco efêmero, validadores e smoke tests.

Após falha, registre o resultado na Execution Fabric e repare dentro do limite do Autonomy Engine. Falhas repetidas podem fazer o roteador escolher outro backend capaz.

Nunca transforme texto livre do usuário em comando shell. O CI adapter usa gates declarados/allowlisted do repositório.

## Local/full executor

É correto quando existir necessidade real de browser/runtime interativo, debugging de processo local, serviço local não reproduzível, migration em ambiente real ou outra capacidade ausente.

Codex é uma implementação possível desse backend, não uma dependência arquitetural.

## Menor trabalho humano

Se algum backend autorizado pode executar com segurança, faça. Não mande o usuário abrir terminal, copiar arquivos, escolher executor ou conduzir fases rotineiras.

## Handoff

Quando houver handoff real, forneça apenas Issue/PR/branch, autonomy phase, context fingerprint, capacidades faltantes e critérios de conclusão. O novo agente deve conseguir rodar `resume` sem histórico de conversa.
