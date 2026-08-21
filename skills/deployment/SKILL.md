---
name: deployment
description: Prepara e executa deploys de forma proporcional ao risco, com checks, configuração por ambiente, observabilidade, rollout e recuperação quando necessários.
---

# Deployment

## Antes do deploy

- confirme branch/commit correto;
- execute checks definidos pela aplicação;
- valide configuração e variáveis necessárias sem expor secrets;
- confirme migrations e dependências;
- classifique risco da mudança.

## Estratégia

Projeto simples e baixo risco pode usar deploy direto após checks.

Mudança relevante pode exigir `preview/staging → validação → produção → smoke test`.

Mudanças de alto risco devem considerar rollout gradual, feature flag ou kill switch quando a arquitetura já suportar isso ou o benefício justificar a complexidade.

## Depois

- confirme deploy real, não apenas comando enviado;
- execute smoke test;
- observe erros relevantes;
- registre versão/commit implantado;
- acione rollback quando critérios definidos falharem.

## Regra

Não introduza infraestrutura extra apenas para tornar o processo mais sofisticado.