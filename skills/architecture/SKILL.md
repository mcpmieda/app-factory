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
5. Separe configuração variável de lógica.
6. Defina onde autenticação, autorização e validação acontecem.
7. Considere observabilidade e recuperação conforme o risco.
8. Registre apenas decisões que realmente afetam o futuro do projeto.

## Regra de novidade

Não trocar tecnologia estabelecida por tendência nova sem ganho mensurável em segurança, velocidade, manutenção ou requisito do produto.

## Portabilidade

Evite acoplamento desnecessário a um fornecedor quando uma solução padrão atende ao objetivo, mas não adicione camada abstrata apenas para um futuro hipotético.