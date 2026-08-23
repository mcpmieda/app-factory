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

Quando houver API/integração relevante, use `core/API_ENGINEERING.md` como fonte das exigências específicas da interface e **OWASP API Security Top 10** como threat reference. Inclua proporcionalmente autorização por objeto/função, autenticação, consumo de recursos, exposição indevida, inventário, SSRF/callbacks e consumo inseguro de APIs externas. Não copie todo o catálogo OWASP para cada projeto; transforme riscos reais em gates/testes.

## Regra

Priorize riscos concretos do sistema. Não gere checklist genérica como substituto de análise do fluxo real.

Em APIs protegidas, esconder ação no frontend nunca substitui autorização no servidor. Prove pelo menos um caso permitido e um negado quando o risco for material.

## Guardrails

Quando uma falha importante puder ser evitada automaticamente, prefira secret scanning, schema validation, teste, lint, policy ou CI em vez de depender apenas de documentação.

Para API `contract`/`governed`, combine a revisão com os gates de contrato/runtime/compatibilidade definidos em `core/API_ENGINEERING.md` sem duplicar responsabilidade entre os módulos.
