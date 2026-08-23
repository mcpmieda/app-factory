# API Engineering Contract

Este contrato define como a App Factory decide, projeta, protege, evolui e verifica APIs e integrações. Ele é **condicional**: não cria uma API onde o produto não precisa dela e não transforma Server Actions, funções internas ou um app local em uma plataforma de APIs sem motivo.

`core/SYSTEM_ENGINEERING.md` continua decidindo a profundidade mínima da arquitetura do produto. Este arquivo entra quando existe uma fronteira de API, integração externa, contrato compartilhado, mensageria/eventos ou um backend consumido de forma independente.

## 1. Quando este contrato se aplica

Aplique quando houver pelo menos uma destas situações:

- frontend e backend se comunicam por uma interface HTTP/RPC tratada como contrato independente;
- dois ou mais clientes consomem o mesmo backend, como web + mobile + extensão + automação;
- uma API será exposta a parceiro, público ou outro time/sistema;
- o produto consome API externa relevante para um fluxo real;
- há webhooks, eventos, filas, mensagens ou integração assíncrona;
- serviços internos se comunicam por contrato de rede;
- a estabilidade da interface precisa sobreviver à evolução independente entre consumidor e provedor.

Não exija uma API formal apenas porque existe backend. Server Actions, chamadas internas da mesma aplicação ou funções locais podem permanecer sem contrato público separado quando não existe consumidor independente nem risco de compatibilidade que justifique a sobrecarga.

## 2. Modos de governança

Classifique a superfície de API independentemente do nível do sistema. O nível do produto vem de `core/SYSTEM_ENGINEERING.md`; o modo abaixo define quanto rigor a **interface** precisa.

### `none`

Não existe fronteira de API relevante ou ela é detalhe interno inseparável da aplicação.

- não criar OpenAPI/GraphQL schema/gRPC/AsyncAPI só para cumprir checklist;
- testes normais da aplicação continuam válidos.

### `lightweight`

Existe uma interface interna pequena, com um consumidor controlado e evolução coordenada.

Exigir proporcionalmente:

- inputs/outputs e erros explícitos no código;
- validação no lado que recebe a mutação;
- autenticação/autorização quando aplicável;
- teste de integração/smoke do fluxo material;
- timeout/retry quando houver dependência de rede externa.

Contrato machine-readable é opcional enquanto o custo de incompatibilidade continuar baixo.

### `contract`

A interface é compartilhada, possui múltiplos consumidores, evolui separadamente ou integra sistemas diferentes.

Exigir:

- fonte de verdade machine-readable adequada ao protocolo;
- contrato definido antes ou junto da implementação, não reconstruído apenas depois;
- lint/validação do contrato;
- verificação de compatibilidade em mudanças;
- testes que exercitem implementação real ou ambiente equivalente;
- estratégia explícita de autenticação/autorização, erros e evolução.

### `governed`

API pública, de parceiro, institucional, de produção crítica, de alto impacto ou com consumidores que não podem ser coordenados a cada alteração.

Além de `contract`, exigir proporcionalmente:

- política de breaking change/depreciação;
- inventário/owner e lifecycle recuperáveis no repositório;
- gates de segurança alinhados a OWASP API Security;
- testes negativos/fuzz/property-based quando suportados;
- observabilidade e correlação de falhas;
- rate limiting/abuse protection quando exposição justificar;
- resiliência de integrações externas;
- evidência de rollout/rollback ou compatibilidade segura;
- contract testing consumidor-provedor quando múltiplos componentes evoluem independentemente e isso trouxer ganho real.

Escolha o menor modo que preserve compatibilidade, segurança e operação reais. Não use `lightweight` para evitar um contrato que o produto claramente precisa.

## 3. Seleção de protocolo e estilo

Não padronize REST como resposta universal. Escolha pelo comportamento:

- **HTTP resource-oriented / REST-like**: default forte para CRUD, integrações HTTP e APIs amplamente consumíveis; use OpenAPI como contrato quando o modo for `contract` ou `governed`;
- **GraphQL**: use quando consumidores precisam compor consultas flexíveis sobre um domínio conectado e o ganho compensa cache, autorização por campo/objeto, custo de consulta e operação mais complexos; o schema GraphQL é o contrato;
- **gRPC/Protobuf**: considere para comunicação service-to-service fortemente tipada, baixa latência e ambientes em que os clientes suportam o protocolo; `.proto` é o contrato;
- **eventos/mensageria**: use AsyncAPI quando produtores/consumidores, canais e mensagens assíncronas formarem uma interface relevante;
- **workflows multi-etapas**: use Arazzo quando uma sequência de operações precisa ser descrita de forma executável/repetível, especialmente integrações, automações e agentes; não exigir para CRUD simples.

Não introduza GraphQL, gRPC, mensageria ou Arazzo apenas por sofisticação técnica.

## 4. Contract-first e fonte de verdade

Para modos `contract` e `governed`, a interface deve possuir uma fonte de verdade versionável antes de consumidores dependerem de comportamento implícito.

Artefatos preferidos:

```text
api/openapi.yaml        # HTTP/OpenAPI
api/schema.graphql      # GraphQL SDL
api/proto/*.proto       # gRPC/Protobuf
api/asyncapi.yaml       # eventos/mensageria
api/arazzo.yaml         # workflow multi-etapas, quando útil
```

O caminho pode variar pelo stack. O requisito é ter **uma** autoridade clara e evitar duas descrições divergentes.

Regras:

- contrato e implementação devem evoluir no mesmo bloco funcional;
- gerar documentação ou SDK a partir do contrato é preferível a manter cópia manual quando o ecossistema suportar;
- código gerado não substitui a revisão do contrato que o originou;
- exemplos no contrato devem ser válidos e não conter secrets/dados reais sensíveis;
- versão da especificação deve ser estável e suportada pelo toolchain atual; não atualizar apenas para usar a versão mais nova.

## 5. Semântica HTTP quando aplicável

Para APIs HTTP:

- use métodos HTTP conforme sua semântica real; não esconda toda ação atrás de `POST` sem motivo;
- use status codes coerentes e documentados;
- recursos, IDs e relações devem refletir o domínio, não a estrutura acidental do banco;
- `GET` deve permanecer livre de efeitos de escrita relevantes;
- `PUT`, `DELETE` e operações que precisem ser repetíveis devem respeitar idempotência semântica; para `POST` suscetível a retry/duplicação, use chave de idempotência ou estratégia equivalente quando material;
- paginação deve ser projetada antes de conjuntos potencialmente grandes; não retornar coleção ilimitada por conveniência;
- filtros, ordenação, busca e campos selecionáveis devem ter contrato estável quando expostos;
- concorrência deve usar versionamento/ETag/lock otimista ou outra estratégia quando sobrescrita silenciosa for risco real;
- operações demoradas não devem depender de uma conexão HTTP aberta indefinidamente; prefira job/operação assíncrona com status quando necessário.

Use RFC 9110 e padrões HTTP atuais como referência sem reproduzir suas regras integralmente dentro da Factory.

## 6. Erros consistentes

Para APIs HTTP novas que exponham erros estruturados, prefira **RFC 9457 Problem Details** (`application/problem+json`) ou formato equivalente já consolidado no projeto.

O erro deve permitir ao consumidor distinguir de forma estável:

- tipo/categoria;
- status;
- mensagem segura para o contexto;
- identificador/correlação quando útil;
- erros de campo/validação quando aplicável.

Não vaze stack trace, SQL, secrets, tokens ou detalhes internos desnecessários. Não altere uma API legada inteira somente para trocar o envelope de erro sem plano de compatibilidade.

## 7. Identidade, autorização e segurança

`core/SYSTEM_ENGINEERING.md` decide quando identidade e autorização são requisitos arquiteturais. `skills/security-review` executa a revisão de segurança. Este contrato define o que a superfície de API deve garantir.

Quando aplicável:

- autentique a identidade no servidor/provedor confiável;
- autorize **recurso + ação + escopo**, não apenas a presença de login;
- não confie em IDs enviados pelo cliente para inferir propriedade sem verificar autorização;
- valide input no boundary e proteja output contra exposição excessiva;
- endpoints administrativos recebem gates explícitos;
- secrets/API keys ficam fora do Git e do cliente público;
- tokens/credenciais recebem menor escopo e duração compatíveis com o caso;
- CORS, CSRF, cookies, bearer tokens e origem confiável são tratados conforme o modelo de cliente, não por checklist genérico;
- uploads, URLs remotas e callbacks recebem validação contra classes de abuso/SSRF quando relevantes;
- limites de consumo entram quando custo, disponibilidade ou exposição puderem ser abusados.

Use **OWASP API Security Top 10** como referência de ameaça para APIs expostas, com atenção especial a autorização por objeto/função, autenticação, consumo de recursos, exposição indevida, inventário e consumo inseguro de APIs externas.

## 8. Evolução, compatibilidade e versionamento

Versionar a API não significa obrigatoriamente colocar `/v1` na URL. Escolha estratégia compatível com protocolo, consumidores e operação.

Para `contract`/`governed`:

- mudanças compatíveis são preferíveis a quebras coordenadas;
- breaking changes devem ser detectadas contra uma baseline conhecida;
- remoção de campo/operação usada exige depreciação e janela/migração proporcional ao impacto;
- não reutilize o mesmo campo com significado incompatível;
- mudanças de enum, nullability, required/optional, formatos e status podem ser breaking mesmo sem alterar o endpoint;
- versionamento maior entra quando compatibilidade não puder ser preservada razoavelmente;
- registre exceções aprovadas em vez de desabilitar permanentemente o gate inteiro.

Para OpenAPI, **oasdiff** é a ferramenta preferida da Factory para detectar breaking changes quando o projeto puder executá-la de forma reproduzível. Ferramenta equivalente pode substituí-la se houver razão técnica documentada.

## 9. Integrações externas e resiliência

Consumir uma API externa cria uma dependência operacional. Quando material:

- defina timeout explícito; não dependa de timeout infinito/default desconhecido;
- retry somente em falhas/operações seguras para repetição, com limite e backoff/jitter quando adequado;
- respeite `Retry-After`/rate limits do provedor quando disponíveis;
- use idempotency key/checkpoint para impedir duplicidade quando escrita remota puder ser repetida;
- diferencie erro transitório, erro permanente, autenticação e validação;
- valide respostas externas antes de transformá-las em estado confiável;
- registre correlação suficiente para diagnóstico sem logar secrets/dados sensíveis;
- considere circuit breaker/fila/dead-letter apenas quando volume/criticidade justificar;
- documente dependência, owner/provedor, credencial necessária e estratégia de degradação/recovery;
- não assuma propriedades/IDs/capacidades da API: consulte documentação/metadata/execução real quando possível.

## 10. Webhooks

Quando receber webhooks:

- verificar assinatura/autenticidade quando o provedor oferecer mecanismo;
- proteger contra replay quando aplicável;
- responder rapidamente e mover processamento pesado para job/fila quando necessário;
- tornar o handler idempotente usando event ID/chave equivalente;
- registrar evento processado/falhado proporcionalmente ao risco;
- não confiar em payload externo sem validação.

Quando enviar webhooks, documente retry, assinatura, timeout, ordenação e possibilidade de duplicidade.

## 11. Ferramentas e gates preferidos

As ferramentas são defaults comprovados, não dependências universais.

### OpenAPI / AsyncAPI / Arazzo — lint e consistência

Preferir **Redocly CLI** quando compatível com o stack. O gate deve validar o contrato com ruleset versionado no projeto; `recommended-strict` é um ponto de partida, não substitui regras de domínio.

Exemplo de execução reproduzível:

```bash
npx @redocly/cli@<versao-fixada> lint api/openapi.yaml
```

Fixe versão em CI/lockfile; `@latest` serve para exploração, não para gate reprodutível.

### Compatibilidade OpenAPI

Preferir **oasdiff** para comparar baseline e revisão:

```bash
oasdiff breaking base-openapi.yaml api/openapi.yaml
```

Em CI, configure saída/exit code para bloquear breaking change não aprovado.

### Testes gerados a partir do contrato

Para API HTTP/OpenAPI ou GraphQL relevante, **Schemathesis** é a opção preferida para property-based/fuzz/negative/stateful testing quando o ambiente consegue executar a API de teste.

Exemplo conceitual:

```bash
uvx schemathesis run api/openapi.yaml --url http://127.0.0.1:8000 --mode all
```

Fixe a versão no projeto/CI e adapte autenticação/seed/ambiente; não rode fuzz destrutivo contra produção.

### Contract testing consumidor-provedor

Use **Pact** ou equivalente quando consumidores e provedores evoluírem independentemente e OpenAPI/schema sozinho não provar os comportamentos realmente consumidos. Não obrigar Pact em monólito ou único cliente coordenado.

### Workflows

Use **Arazzo** quando a correção depende da ordem/encadeamento entre operações e isso trouxer verificabilidade real. Use **AsyncAPI** para contratos assíncronos relevantes.

## 12. Design references

A Factory usa estas fontes como referências complementares, não como regras copiadas integralmente:

- OpenAPI Specification — contrato de APIs HTTP;
- Google API Improvement Proposals (AIPs) — recursos, métodos, paginação, operações longas, idempotência e evolução;
- Zalando RESTful API Guidelines — API First, compatibilidade e governança prática;
- Microsoft API Guidelines — consistência e evolução de APIs em escala;
- OWASP API Security — threat model específico para APIs;
- IETF HTTP Semantics / RFC 9110;
- RFC 9457 Problem Details;
- AsyncAPI e Arazzo quando o protocolo/workflow exigir.

Quando essas referências divergirem, preserve padrões existentes do projeto, requisitos do produto, compatibilidade e segurança. Não misture convenções de várias organizações sem uma decisão local clara.

## 13. Relação com Semantic Verification

Não duplique responsabilidades:

- `API_ENGINEERING` define **como a interface deve ser desenhada e governada**;
- `SEMANTIC_VERIFICATION` transforma os comportamentos relevantes dessa interface em critérios/evidências verificáveis;
- `DEFINITION_OF_DONE` decide se os gates exigidos realmente passaram.

Mudança de contrato observável, breaking change, autorização, idempotência, paginação, retry ou fluxo multi-etapas material deve aparecer na spec semântica quando `core/SEMANTIC_VERIFICATION.md` se aplicar.

## 14. Saída mínima de arquitetura quando aplicável

Para modo `contract` ou `governed`, registre no repositório:

- modo de governança da API;
- consumidores e owner;
- protocolo/estilo escolhido e motivo curto;
- fonte de verdade do contrato e caminho;
- autenticação/autorização;
- estratégia de erros;
- paginação/filtros/concorrência/idempotência quando materiais;
- versão/compatibilidade/depreciação;
- dependências externas e política de timeout/retry;
- gates de lint, compatibilidade e testes;
- workflows/eventos relevantes.

Use `templates/project/API.md` quando a API for importante o bastante para merecer documento próprio; caso contrário mantenha a decisão concisa em `ARCHITECTURE.md`.

## 15. Definition of Done específico de API

Uma API `contract`/`governed` não está pronta apenas porque responde requests.

Conforme aplicável, prove que:

- contrato machine-readable atual valida/linta;
- implementação e contrato correspondem no fluxo crítico;
- autenticação/autorização possuem casos permitido e negado;
- inputs inválidos e erros esperados não viram 500 acidental;
- breaking changes foram comparadas contra baseline;
- retry/idempotência não duplica escrita crítica;
- API externa tem timeout e falha controlada;
- webhook duplicado/replay não corrompe estado quando esse risco existe;
- testes gerados/negativos foram executados quando o modo/risco justificar;
- documentação não promete comportamento que a implementação não fornece.

## Princípio final

**Contrato proporcional, compatibilidade verificável e segurança no boundary.** A Factory deve escolher a interface mais simples que satisfaça consumidores reais e depois automatizar o máximo possível da prova de que ela continua correta.