# API — Project Template

> Use somente quando a API/integracao for importante o bastante para merecer documento proprio. Para interfaces pequenas, registre a decisao em `ARCHITECTURE.md` e nao crie este arquivo.

## Escopo
- modo de governanca: `lightweight` / `contract` / `governed`
- owner/provedor:
- consumidores:
- finalidade:

## Protocolo e contrato
- estilo/protocolo: HTTP/OpenAPI / GraphQL / gRPC / eventos/AsyncAPI / outro
- fonte de verdade:
- caminho do contrato:
- versao/estrategia de compatibilidade:
- documentacao/SDK gerado, se houver:

## Boundary
- autenticacao:
- autorizacao por recurso/acao/escopo:
- validacao de entrada:
- formato de erros:
- paginacao/filtros/busca:
- idempotencia/concorrencia:
- operacoes longas:

Preencha apenas o que existe no produto. Nao mantenha secoes artificiais para capacidades ausentes.

## Integracoes externas
Para cada dependencia material:
- provedor/API:
- credencial/escopo:
- timeout:
- retry/backoff/rate limit:
- idempotencia/checkpoint:
- degradacao/recovery:

## Webhooks/eventos
- autenticidade/assinatura:
- replay/idempotencia:
- ordenacao/duplicidade:
- processamento assincrono, se necessario:

## Gates
- lint/validacao do contrato:
- compatibilidade/breaking changes:
- integration/smoke:
- teste negativo/property/fuzz:
- consumer/provider contract test:
- security review:

## Workflows
- Arazzo ou descricao equivalente somente quando a ordem entre varias operacoes for parte material do contrato:

## Decisoes e excecoes
Registre apenas desvios importantes das regras da App Factory e o motivo. Nao copie `core/API_ENGINEERING.md` para este arquivo.
