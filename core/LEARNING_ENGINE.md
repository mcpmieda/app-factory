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

O arquivo local também é tratado como entrada não confiável quando lido: campos extras são descartados, contexto é recalculado e eventos com backend/capacidade/outcome inválidos são ignorados.

## Contexto comparável

Aprendizado só compara eventos com a mesma:

`action + capability signature`

Isso evita concluir que um backend bom para documentação também é melhor para E2E, migration ou browser.

## Evidência mínima

A Factory mantém o roteamento V1.2 quando a amostra é pequena.

Default:

- pelo menos 5 resultados resolvidos para o backend baseline;
- pelo menos 5 para a alternativa;
- prior Beta(2,2) conservador para evitar confiança extrema cedo demais;
- preferência por alternativa somente quando a margem de sucesso for material ou, com sucesso alto/equivalente, quando a **duração mediana das execuções bem-sucedidas** for materialmente menor.

A duração de falhas não participa da métrica de velocidade: falhar rápido nunca melhora a preferência de executor.

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
- mediana de duração das execuções bem-sucedidas quando disponível;
- razão da decisão.

Quando faltam dados, o Learning Engine informa `insufficient-data` e preserva a ordem baseline.

## Portabilidade

O formato é local e baseado em JSON/stdlib. Outro agente no mesmo ambiente pode recuperar a evidência sem depender da conversa anterior. Não existe envio automático para servidor da App Factory ou aprendizado entre usuários/tenants na V1.3.

Como `.factory/learning.json` fica fora do Git, uma nova máquina pode não receber esse histórico. Nesse caso a Factory continua corretamente pelo baseline V1.2 e reaprende; Learning Engine é otimização, não requisito de continuidade.
