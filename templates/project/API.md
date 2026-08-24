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

## Aquisicao de dados e eficiencia

Preencha quando custo, latencia, quota, throttling ou quantidade de round trips forem materiais para o fluxo.

- telas/fluxos criticos:
- dados que precisam chegar juntos:
- composicao orientada ao caso de uso / endpoint agregador, se houver:
- justificativa para chamadas independentes quando existirem:
- risco de N+1 / como foi eliminado:
- paginacao/selecao de campos:
- batching/paralelismo com provedores externos:
- retry/backoff/`Retry-After`:
- cache/read model e regra de invalidacao/rebuild, se houver:
- request budget ou evidencia observavel do fluxo, quando necessario:

Nao force "uma requisicao por tela" e nao crie `/api/tudo`. Siga `core/DATA_ACCESS_EFFICIENCY.md`: agregue por caso de uso quando isso reduzir round trips sem ampliar acoplamento/exposicao desnecessarios.

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
- data-access evidence: request count/N+1/batching/paginacao/retry quando material:
- security review:

## Workflows
- Arazzo ou descricao equivalente somente quando a ordem entre varias operacoes for parte material do contrato:

## Decisoes e excecoes
Registre apenas desvios importantes das regras da App Factory e o motivo. Nao copie `core/API_ENGINEERING.md` nem `core/DATA_ACCESS_EFFICIENCY.md` para este arquivo.
