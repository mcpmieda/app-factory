# Autonomy Engine

O Autonomy Engine mantém uma máquina de estados curta para que a App Factory consiga continuar trabalho sem depender da memória da conversa nem pedir ao usuário o próximo comando técnico.

## Princípio

O usuário fornece objetivo e decisões genuinamente humanas. O agente executa o ciclo técnico e registra eventos no runtime.

Estados principais:

`context → planning → implementation → verification → repair → review → delivery → done`

`blocked` existe para impedimentos reais. Mudança externa de contexto pode interromper temporariamente qualquer fase ativa e exigir `reconcile_context` antes da retomada.

## Interface interna

```bash
python scripts/factory.py init --goal "Criar um sistema de patrimônio"
python scripts/factory.py status
python scripts/factory.py next
python scripts/factory.py resume
python scripts/factory.py record plan-ready --summary "..."
```

O usuário não deve precisar memorizar ou executar esses comandos. Eles são uma interface comum para ChatGPT, Codex, Claude Code, Cursor, CI ou outro executor.

## Estado

O runtime grava `.factory/state.json`, que é compacto e pode ser versionado em handoffs importantes.

Ele contém:

- objetivo atual;
- fase/status;
- fingerprint do contexto reconhecido;
- resumo de planejamento/implementação;
- última verificação e revisão;
- tentativas de reparo;
- bloqueios e motivo de intervenção humana;
- histórico limitado de eventos.

O histórico é bounded; não é um log infinito.

## Next / Resume

`next` atualiza o contexto e retorna a ação tecnicamente correta para o estado atual.

`resume` funciona mesmo em sessão nova:

1. atualiza o Context Engine;
2. lê `.factory/state.json` quando existir;
3. se não existir, infere um objetivo inicial de `PROJECT_STATE.md`/`README.md`;
4. compara fingerprints;
5. se o repositório mudou fora do fluxo, retorna `reconcile_context`;
6. caso contrário retorna a próxima fase.

## Repair loop

Falhas verificadas entram em `repair`. O limite padrão é 3 tentativas.

Após o limite, o engine não insiste silenciosamente nem simula sucesso. Ele marca bloqueio técnico e recomenda trocar estratégia/executor ou fazer análise mais forte.

Bloqueio técnico não significa automaticamente perguntar ao usuário. Intervenção humana só é marcada explicitamente para categorias como:

- produto/regra de negócio;
- custo;
- risco alto;
- credencial;
- dado externo indisponível;
- decisão legal/organizacional.

## Responsabilidade do modelo/agente

O engine não tenta escrever software arbitrário por heurística. Ele decide estado, contexto e próximo passo; o agente atual executa a ação usando as ferramentas disponíveis.

A autonomia vem da combinação:

`máquina de estados + contexto incremental + agente + ferramentas + CI`.

Isso preserva portabilidade e evita criar um runtime monolítico que fique obsoleto quando modelos mudarem.
