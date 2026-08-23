# PROJECT_STATE — Template

> Resumo curto do estado vigente. Não usar como diário.

## Objetivo atual
[Uma frase]

## Estado
- fase:
- branch/commit de referência:
- baseline seguro:
- nível do sistema: `website` / `local-app` / `persistent-app` / `multi-user-system` / `production-system` / `critical-system`
- fonte autoritativa dos dados: [não aplicável / navegador local / banco/serviço compartilhado / outro]
- autenticação/autorização: [não aplicável / estratégia vigente]
- persistência/migrations: [não aplicável / estratégia vigente]
- recovery/backup: [não aplicável / estratégia vigente]
- API/integracao: [não aplicável / `none` / `lightweight` / `contract` / `governed`]
- contrato autoritativo da API: [não aplicável / caminho + protocolo]
- baseline/compatibilidade da API: [não aplicável / estratégia vigente]
- profundidade semântica: [não aplicável / `scenario` / `domain` / `formal`]
- semantic assurance: [não aplicável / `specs/semantic-assurance.json` + status/baseline]
- formalizações semânticas: [não aplicável / kind + artifact + gate + status]
- Independent Verification: `baseline` / `independent` / `adversarial` / `release`
- checks independentes obrigatórios: [não aplicável / IDs ou resumo]
- checks independentes advisory/exceções: [não aplicável / resumo + referência em VERIFICATION.md]
- funcionalidades validadas:
- limitações conhecidas:

## Trabalho atual
- bloco funcional em andamento:
- critério de conclusão:
- impacto semântico conhecido: [não aplicável / REQ, AC, INV, gates]
- o que não deve ser alterado:

## Últimas decisões que afetam execução
- ...

## Bloqueios
- nenhum / ...

## Próxima ação
[Uma ação concreta]

## Ambiente recomendado
- ChatGPT / Codex / GitHub CI / outro
- motivo:

## Links internos
- produto: `PRODUCT.md`
- arquitetura: `ARCHITECTURE.md`
- API: `API.md` quando existir contrato relevante
- semântica de domínio: `SEMANTICS.md` quando profundidade for `domain`/`formal`
- contrato semântico: `specs/semantic-contract.json` quando aplicável
- semantic assurance: `specs/semantic-assurance.json` quando profundidade for `domain`/`formal`
- verificação independente: `VERIFICATION.md` quando o modo for acima de `baseline`
- decisões: `docs/decisions/` quando existir
- contrato de engenharia: App Factory `core/SYSTEM_ENGINEERING.md`
- contrato de APIs: App Factory `core/API_ENGINEERING.md` quando aplicável
- contrato de Semantic Assurance: App Factory `core/SEMANTIC_ASSURANCE.md` quando aplicável
- contrato de Independent Verification: App Factory `core/INDEPENDENT_VERIFICATION.md` quando aplicável

## Regra
Atualize apenas quando o estado vigente mudar de forma útil para a próxima sessão. Histórico detalhado pertence ao Git, PRs, Issues e changelog quando necessário.

Para `persistent-app` ou superior, mantenha nível do sistema e fonte autoritativa dos dados preenchidos. Para `multi-user-system` ou superior, mantenha também as decisões vigentes de identidade/autorização, persistência e recovery quando relevantes.

Para API `contract`/`governed`, mantenha modo, fonte de verdade e estratégia/baseline de compatibilidade recuperáveis. Para `none`/`lightweight`, não crie documentação adicional sem necessidade.

Para profundidade semântica `domain`/`formal`, mantenha `semantic-assurance.json` recuperável e coerente com o fingerprint do contrato semântico. Registre somente formalizações realmente usadas; `scenario` não exige `SEMANTICS.md` nem assurance só para preencher template.

Para Independent Verification acima de `baseline`, mantenha modo, checks `required/advisory`, ambiente de teste e exceções recuperáveis em `VERIFICATION.md`/workflow. Não trate check indisponível como `pass`.
