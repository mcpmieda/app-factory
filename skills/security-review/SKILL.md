---
name: security-review
description: Revisa segurança de aplicações e mudanças com foco em autenticação, autorização, validação, segredos, dependências, dados sensíveis e privilégio mínimo sem adicionar controles desproporcionais.
---

# Security Review

## Verificar quando aplicável

- autenticação e sessões;
- autorização por recurso/ação;
- validação de inputs e outputs;
- exposição de dados;
- secrets e configuração;
- permissões/privilégio mínimo;
- dependências e supply chain;
- XSS/CSRF/injection e classes relevantes à stack;
- uploads/arquivos;
- logs sem dados sensíveis;
- endpoints administrativos;
- migrations e operações destrutivas.

## Regra

Priorize riscos concretos do sistema. Não gere checklist genérica como substituto de análise do fluxo real.

## Guardrails

Quando uma falha importante puder ser evitada automaticamente, prefira secret scanning, schema validation, teste, lint, policy ou CI em vez de depender apenas de documentação.