# Learning Engine

O Learning Engine usa resultados estruturados da Execution Fabric para melhorar escolhas futuras **sem transformar histórico em autoridade**.

## Regra principal

A ordem de decisão é sempre:

1. capacidades obrigatórias;
2. disponibilidade/permissões do executor;
3. bloqueios e failure threshold da tarefa atual;
4. regras de segurança/risco e Definition of Done;
5. somente então, evidência aprendida entre candidatos que já passaram pelos filtros anteriores.

Aprendizado nunca torna um backend incapaz em candidato.

## Dados locais

O arquivo local `.factory/learning.json` guarda somente:

- timestamp;
- classe técnica de ação (`implement`, `verify`, etc.);
- assinatura de capacidades conhecida;
- backend conhecido;
- resultado (`success`, `failure`, `blocked`, `cancelled`);
- duração em milissegundos quando disponível.

Não guardar:

- prompt;
- objetivo/descrição do usuário;
- nomes pessoais;
- código;
- conteúdo de arquivos;
- logs ou summaries;
- task key;
- secrets/tokens;
- URLs privadas;
- telemetria externa.

Ações desconhecidas são reduzidas para `other`; backends/capacidades desconhecidos são rejeitados. O dataset é limitado e fica fora do Git por padrão.

## Contexto comparável

Aprendizado só compara eventos com a mesma:

`action + capability signature`

Isso evita concluir que um backend bom para documentação também é melhor para E2E, migration ou browser.

## Evidência mínima

A Factory mantém o roteamento V1.2 quando a amostra é pequena.

Default:

- pelo menos 5 resultados resolvidos para o backend baseline;
- pelo menos 5 para a alternativa;
- prior Beta conservador para evitar confiança extrema cedo demais;
- preferência por alternativa somente quando a margem de sucesso for material ou, com sucesso alto/equivalente, quando a duração mediana for materialmente menor.

`blocked` e `cancelled` são preservados para auditoria agregada, mas não contam como sucesso/falha resolvida.

## Backends pesados

`local_full` é protegido: aprendizado não o promove sobre um backend mais leve que já seja capaz e elegível.

Ele continua disponível quando:

- a capacidade local/interativa é obrigatória;
- backends leves foram eliminados por incapacidade/disponibilidade;
- o fallback da tarefa atual os rejeitou após falhas suficientes.

## Relação com Execution Fabric

- Execution Fabric decide **quem pode executar**.
- Learning Engine recomenda **qual candidato elegível tem melhor evidência**.
- Autonomy Engine decide **qual é a próxima fase**.

O aprendizado não altera Definition of Done, não reduz testes e não concede permissions/secrets.

## Interface portátil

```text
python scripts/factory.py --root <projeto> learning-status
python scripts/factory.py --root <projeto> learning-recommend verify
python scripts/factory.py --root <projeto> route verify
python scripts/factory.py --root <projeto> route verify --no-learning
```

`record-execution` atualiza o dataset local automaticamente usando somente os campos allowlisted.

## Explicabilidade

A decisão informa:

- `selection_mode: baseline` ou `learned`;
- baseline original;
- candidatos elegíveis;
- quantidade de amostras;
- sucesso posterior estimado;
- mediana de duração quando disponível;
- razão da decisão.

Quando faltam dados, o Learning Engine deve dizer `insufficient-data` e preservar a ordem baseline.

## Portabilidade

O formato é local e baseado em JSON/stdlib. Outro agente pode recuperar a evidência no mesmo projeto sem depender da conversa anterior. Não existe envio automático para servidor da App Factory ou aprendizado entre usuários/tenants na V1.3.
