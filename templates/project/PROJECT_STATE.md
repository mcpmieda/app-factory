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
- funcionalidades validadas:
- limitações conhecidas:

## Trabalho atual
- bloco funcional em andamento:
- critério de conclusão:
- o que não deve ser alterado:

## Últimas decisões que afetam execução
- ...

## Bloqueios
- nenhum / ...

## Próxima ação
[Uma ação concreta]

## Ambiente recomendado
- ChatGPT / Codex / outro
- motivo:

## Links internos
- produto: `PRODUCT.md`
- arquitetura: `ARCHITECTURE.md`
- API: `API.md` quando existir contrato relevante
- decisões: `docs/decisions/` quando existir
- contrato de engenharia: App Factory `core/SYSTEM_ENGINEERING.md`
- contrato de APIs: App Factory `core/API_ENGINEERING.md` quando aplicável

## Regra
Atualize apenas quando o estado vigente mudar de forma útil para a próxima sessão. Histórico detalhado pertence ao Git, PRs, Issues e changelog quando necessário.

Para `persistent-app` ou superior, mantenha nível do sistema e fonte autoritativa dos dados preenchidos. Para `multi-user-system` ou superior, mantenha também as decisões vigentes de identidade/autorização, persistência e recovery quando relevantes.

Para API `contract`/`governed`, mantenha modo, fonte de verdade e estratégia/baseline de compatibilidade recuperáveis. Para `none`/`lightweight`, não crie documentação adicional sem necessidade.