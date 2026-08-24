# Data Access Efficiency Contract

Este contrato define como a App Factory evita interfaces excessivamente "faladoras" (`chatty`) e projeta aquisição de dados eficiente entre cliente, backend e provedores externos.

Ele é **general-purpose** e orientado por comportamento. Não obriga toda tela a fazer uma única requisição, não cria um endpoint gigante `/api/tudo` e não adiciona cache, read model ou batching quando isso não traz ganho real.

Aplique este contrato quando uma tela, fluxo ou cliente depende de múltiplas leituras/escritas por rede para montar uma única experiência ou quando custo, latência, quotas, throttling ou estabilidade do provedor são materiais.

## 1. Princípio anti-chatty

Quando vários dados são necessários juntos para cumprir **um mesmo caso de uso**, prefira uma fronteira orientada ao caso de uso em vez de obrigar o cliente a orquestrar muitas chamadas independentes.

Exemplo preferido:

```text
Tela de aluno
    ↓
GET /api/alunos/{id}/resumo
    ↓
backend compõe as fontes necessárias
    ↓
resposta pronta para o caso de uso
```

Evite por padrão:

```text
Tela de aluno
    ↓
GET /api/alunos/{id}
GET /api/alunos/{id}/notas
GET /api/alunos/{id}/turma
GET /api/alunos/{id}/alertas
GET /api/alunos/{id}/situacao
...
```

quando todas essas respostas são sempre necessárias juntas para a mesma tela/ação.

A regra vale também para Server Components, Server Actions, RPC, GraphQL resolvers ou funções internas que cruzem fronteira de rede; não depende da existência de uma API pública formal.

## 2. Não transformar agregação em API monolítica

Agregação deve seguir o **caso de uso**, não produzir um endpoint universal.

Prefira superfícies como:

```text
/api/admin/resumo
/api/turmas/{id}/painel
/api/alunos/{id}/dossie
/api/conselho/{alunoId}/contexto
```

quando esses conjuntos representam necessidades reais e coesas.

Evite:

```text
/api/tudo
/api/bootstrap-completo-do-sistema
```

quando a resposta carrega dados sem relação, cresce sem limite, amplia exposição ou acopla telas independentes.

Internamente, mantenha serviços/domínio pequenos e composáveis. Um endpoint agregador pode chamar vários serviços internos sem transformar toda a lógica em uma função única.

## 3. Cliente não deve ser orquestrador de infraestrutura

O frontend pode coordenar estados de UI, carregamento progressivo e interações independentes. Ele não deve, por conveniência, conhecer detalhes desnecessários de:

- múltiplas listas/tabelas usadas para montar uma mesma visão;
- sequência de chamadas a provedores externos;
- retries/backoff do provedor;
- detalhes de paginação interna;
- credenciais ou escopos privilegiados;
- composição de dados que pertence ao backend.

Quando a composição é parte da regra do produto, do controle de acesso ou da eficiência operacional, ela pertence ao servidor/backend ou camada server-side equivalente.

## 4. Paralelismo, batching e composição no backend

Quando o backend precisa consultar várias fontes independentes:

- execute em paralelo somente operações realmente independentes;
- preserve dependências de ordem quando existirem;
- use batching nativo do provedor quando ele reduzir round trips sem enfraquecer semântica, autorização ou tratamento de erro;
- respeite o limite documentado pelo provedor em vez de hard-code universal da Factory;
- trate resposta parcial de batch explicitamente;
- não agrupe mutações apenas para esconder falta de idempotência/transação.

Para Microsoft Graph, por exemplo, use JSON batching quando adequado ao caso e respeite os limites oficiais vigentes do serviço. O princípio é provider-neutral: outros provedores podem oferecer batch, bulk, pipeline ou protocolo equivalente.

## 5. Rate limits, throttling e retry

Integrações externas seguem também `core/API_ENGINEERING.md`.

Quando um provedor responder com throttling/rate limit:

- respeite `Retry-After` quando fornecido;
- retry somente quando a operação for segura para repetição;
- aplique limite de tentativas e backoff/jitter proporcional;
- não faça loop agressivo;
- não transforme erro permanente em retry infinito;
- preserve idempotência/checkpoint para escrita remota suscetível a repetição;
- registre correlação suficiente sem vazar dados sensíveis.

Reduzir chamadas desnecessárias é parte da estratégia de resiliência; retry não compensa arquitetura excessivamente chatty.

## 6. Paginação e seleção de dados

Não resolva excesso de chamadas retornando coleções ilimitadas.

Quando conjuntos podem crescer:

- pagine no lado adequado;
- filtre cedo;
- selecione somente campos necessários quando o provedor permitir;
- evite N+1 de rede;
- prefira consulta/batch/índice coerente com o acesso real;
- não faça o cliente baixar uma base inteira para filtrar localmente sem justificativa.

## 7. Read models e resumos pré-computados

Para dashboards, matrizes, relatórios frequentes ou telas que exigem agregações caras, considere um **read model** ou resumo pré-computado.

Use somente quando houver benefício material de latência, custo ou estabilidade.

O read model:

- não substitui silenciosamente a fonte autoritativa;
- precisa ter regra clara de atualização/reconstrução;
- deve tolerar/reconhecer defasagem quando consistência imediata não for possível;
- deve ser derivável/reparável quando a fonte oficial continua sendo outra;
- não deve duplicar dados sensíveis em cache/provedor desnecessário.

## 8. Cache

Cache é otimização, não correção para uma interface mal desenhada.

Antes de adicionar cache, elimine chamadas redundantes e N+1 evitáveis.

Quando cache for útil:

- defina chave, escopo, TTL e invalidação;
- não compartilhe resposta entre usuários/escopos incompatíveis;
- autorize antes de servir dado protegido;
- não armazene segredo, token ou dado sensível em cache público;
- use `no-store` quando a natureza do dado exigir;
- trate cache miss como caminho normal e correto.

## 9. Request budget por fluxo crítico

Para telas/fluxos importantes, registre ou teste um **request budget** quando o número de round trips for material para custo, limite gratuito, latência ou estabilidade.

Não existe threshold universal da Factory como "máximo 3 requests por tela".

O budget deve ser derivado do caso real, por exemplo:

```text
Tela: painel da turma
- navegação inicial: até N chamadas próprias de backend justificadas
- nenhuma chamada N+1 por aluno
- nenhuma repetição idêntica sem invalidação
- chamadas externas agregadas/batched quando vantajoso
```

Um número maior pode ser correto quando dados são independentes, progressivos ou acionados pelo usuário. Um número baixo pode continuar errado se cada chamada for enorme ou insegura.

## 10. Detecção de arquitetura excessivamente fragmentada

Em revisão, trate como sinal de investigação:

- várias chamadas `/api/*` disparadas sempre juntas ao abrir uma tela;
- waterfall de rede sem dependência real;
- N+1 por item de tabela/lista;
- mesma consulta repetida em componentes irmãos;
- frontend fazendo join/composição de fontes protegidas;
- dezenas de endpoints minúsculos que refletem tabelas internas em vez de casos de uso;
- retry simultâneo em múltiplos componentes para a mesma dependência;
- polling frequente sem requisito de atualização que o justifique.

Esses sinais não são falha automática. A revisão deve decidir se agregação, batch, paralelismo, paginação, read model, cache ou mudança de contrato traz ganho real.

## 11. Observabilidade

Quando custo/latência de rede for material, registre métricas técnicas suficientes para descobrir regressões, como:

- quantidade de requests próprios por fluxo;
- quantidade de chamadas ao provedor externo;
- latência p50/p95 quando houver infraestrutura para medir;
- respostas `429`/throttling;
- retries;
- tamanho de payload quando relevante.

Não logue tokens, secrets ou payloads sensíveis apenas para medir eficiência.

## 12. Verificação

Quando este contrato for material, a prova pode incluir proporcionalmente:

- teste de integração do endpoint agregador;
- teste que impede N+1 conhecido;
- instrumentação/trace em ambiente de teste;
- Playwright interceptando/contando requests do fluxo crítico;
- teste de batching contra stub/ambiente equivalente;
- teste de `Retry-After`/backoff;
- teste de paginação;
- teste de read model/rebuild quando aplicável.

Não transforme contagem de requests em métrica de vaidade. Verifique o comportamento que protege custo, latência e estabilidade reais.

## 13. Saída mínima de arquitetura

Quando aquisição de dados for material, registre no repositório, em `ARCHITECTURE.md`, `API.md` ou equivalente:

- telas/fluxos críticos;
- quais dados precisam chegar juntos;
- fronteira cliente/backend escolhida;
- endpoints/casos de uso agregadores relevantes;
- estratégia de paginação;
- batching/paralelismo com provedores externos;
- retry/rate limit;
- cache/read models quando usados;
- request budget/evidência quando necessário.

Não crie documento separado se uma nota curta na arquitetura já for suficiente.

## 14. Definition of Done

Quando este contrato se aplicar materialmente, não considere o fluxo pronto se:

- a tela depende de N+1 evitável para funcionar;
- múltiplas chamadas sempre necessárias juntas continuam no cliente sem justificativa;
- integração ignora throttling/`Retry-After` relevante;
- coleção potencialmente grande é carregada inteira sem estratégia;
- cache/read model expõe dado fora do escopo autorizado;
- regressão de round trips ameaça quota/custo/SLO conhecido e não há evidência ou decisão registrada.

## Relação com outros módulos

- `core/SYSTEM_ENGINEERING.md` decide se o produto precisa de backend/persistência e a profundidade arquitetural.
- `core/API_ENGINEERING.md` governa contrato, segurança, compatibilidade e resiliência da interface.
- este arquivo governa **eficiência de aquisição/composição de dados e round trips**.
- `core/SEMANTIC_VERIFICATION.md` transforma comportamento material em critérios verificáveis.
- `core/INDEPENDENT_VERIFICATION.md` pode selecionar load/concurrency/browser checks quando risco/SLO justificar.
- `core/DEFINITION_OF_DONE.md` fecha os gates aplicáveis.

## Princípio final

**O cliente deve pedir o que o caso de uso precisa, não reconstruir a infraestrutura chamada por chamada.** Minimize round trips quando isso melhora custo, latência ou estabilidade, sem criar endpoints gigantes, cache artificial ou complexidade sem necessidade.