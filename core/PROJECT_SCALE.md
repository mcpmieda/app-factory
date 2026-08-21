# Project Scale — profundidade proporcional

A Factory não usa o mesmo processo para todo trabalho.

## XS — ajuste

Exemplos: texto, configuração simples, bug localizado, pequena UI.

- sem documentação nova por padrão;
- escopo + diff + verificação relacionada;
- ChatGPT pode executar quando não exigir ambiente local.

## S — projeto pequeno

Exemplos: utilitário, página simples, extensão pequena, automação curta.

- objetivo e critérios de sucesso;
- arquitetura mínima;
- poucos blocos funcionais;
- `PROJECT_STATE.md` somente se houver continuidade real;
- Spec Kit não obrigatório.

## M — aplicação relevante

Exemplos: sistema administrativo, app com auth/banco, múltiplos módulos.

- produto e arquitetura versionados;
- decisões importantes registradas;
- Issues/blocos funcionais;
- CI e Definition of Done;
- avaliar Spec Kit ou fluxo spec-driven equivalente;
- browser/E2E para fluxos críticos.

## L — sistema crítico ou de longa vida

Exemplos: produção com dados importantes, múltiplos serviços, muitos usuários/equipe.

- spec-driven formal;
- arquitetura e contratos claros;
- segurança/observabilidade proporcionais;
- rollout/rollback;
- runbook quando necessário;
- gates de PR/CI;
- auditoria e E2E mais amplos.

## Regra

A classificação de escala não depende apenas do tamanho do código. Considere:

- impacto de falha;
- dados;
- número de usuários;
- duração esperada;
- integrações;
- complexidade de domínio;
- custo de recuperação.

O agente deve escolher a menor profundidade de processo que preserve segurança e continuidade.