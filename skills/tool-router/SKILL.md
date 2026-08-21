---
name: tool-router
description: Decide qual capacidade, agente ou ferramenta deve executar cada fase de um projeto, priorizando current-agent + GitHub/CI, simplicidade, custo, verificabilidade e mínimo trabalho manual do usuário.
---

# Tool Router

Use quando houver dúvida sobre onde executar uma tarefa ou quando uma fase do projeto mudar de natureza.

## Ordem padrão

Classifique a capacidade necessária antes de escolher uma marca/ferramenta:

1. **Agente atual** — use as ferramentas já disponíveis para raciocínio, arquivos, GitHub e conectores.
2. **GitHub + CI** — prefira Actions para comandos determinísticos, testes, build e prova reproduzível.
3. **Executor leve** — shell/sandbox/ACP ou equivalente quando disponível e suficiente.
4. **Codex/executor local completo** — apenas quando checkout/runtime/browser/debug/migrations interativos ou outra capacidade local forem realmente necessários.

## Current-agent + GitHub/CI

Não limite o agente atual a documentação ou pequenas edições. Se ele consegue coordenar os arquivos, enviar uma branch, observar CI, ler logs, corrigir e repetir com segurança, permaneça nele.

Múltiplos arquivos e existência de testes não são, sozinhos, motivo para handoff.

## CI como executor

Use CI para:

- lint/format/typecheck;
- unit/integration/E2E headless;
- build;
- migrations contra banco efêmero;
- validadores e smoke tests;
- qualquer prova determinística reproduzível.

Após falha, diagnostique e repare dentro do limite do Autonomy Engine em vez de devolver trabalho ao usuário.

## Codex/local

Use quando trouxer capacidade concreta não coberta pela rota anterior, como:

- browser/runtime interativo;
- debugging de processo local;
- serviço local difícil de simular em CI;
- migration delicada em ambiente real;
- refatoração que exige feedback iterativo de terminal não disponível;
- arquivos/binários/operações não suportadas pelas ferramentas atuais;
- estagnação após repair loop em que um executor local realmente melhora a chance de resolução.

## Economia inteligente

Não use Codex apenas porque existe código envolvido. Não evite Codex quando a segurança da conclusão realmente depende dele. O critério é **capacidade + evidência**, não preferência.

## Menor trabalho humano

Se o agente atual ou outro executor autorizado pode fazer a tarefa com segurança, faça. Não mande o usuário abrir terminal, copiar arquivos, escolher executor ou conduzir fases rotineiras.

## Handoff

Quando houver handoff real, forneça apenas Issue/PR/branch, estado/autonomy phase, context fingerprint e critérios de conclusão. O novo agente deve conseguir rodar `resume` sem histórico de conversa.
