---
name: architecture
description: Define ou revisa arquitetura de aplicações de forma proporcional ao problema, evitando complexidade prematura e registrando contratos, limites, dependências e decisões importantes.
---

# Architecture

## Processo

1. Parta dos fluxos e requisitos de produto.
2. Verifique restrições reais de ambiente, custo e compatibilidade.
3. Prefira stack consolidada e pequena ao conjunto mais sofisticado possível.
4. Defina fronteiras, dados, integrações e contratos antes de abstrações internas complexas.
5. Aplique `core/SYSTEM_ENGINEERING.md` para a profundidade mínima do produto.
6. Quando uma fronteira de API/integração for relevante, delegue protocolo, contract-first, compatibilidade e gates específicos a `core/API_ENGINEERING.md`/`api-engineering`; não replique essas regras aqui.
7. Separe configuração variável de lógica.
8. Defina onde autenticação, autorização e validação acontecem.
9. Considere observabilidade e recuperação conforme o risco.
10. Registre apenas decisões que realmente afetam o futuro do projeto.

## Regra de novidade

Não trocar tecnologia estabelecida por tendência nova sem ganho mensurável em segurança, velocidade, manutenção ou requisito do produto.

Não criar API formal, GraphQL, gRPC, mensageria ou contrato adicional apenas para parecer mais arquitetado. Quando a interface exigir governança, use o modo proporcional definido em `core/API_ENGINEERING.md`.

## Portabilidade

Evite acoplamento desnecessário a um fornecedor quando uma solução padrão atende ao objetivo, mas não adicione camada abstrata apenas para um futuro hipotético. Para contratos de interface, prefira padrões abertos adequados ao protocolo quando isso reduzir acoplamento e melhorar interoperabilidade.
