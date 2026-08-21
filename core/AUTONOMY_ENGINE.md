# Autonomy Engine

O Autonomy Engine mantém uma máquina de estados curta para que a App Factory consiga continuar trabalho sem depender da memória da conversa nem pedir ao usuário o próximo comando técnico.

## Princípio

O usuário fornece objetivo e decisões genuinamente humanas. O agente executa o ciclo técnico e registra eventos no runtime.

Fluxo leve, quando não há mudança funcional relevante:

`context → planning → implementation → verification → repair → review → delivery → done`

Fluxo para funcionalidade/regra/contrato ou risco que exija Semantic Verification:

`context → planning → specification → implementation → verification → repair → review → delivery → done`

`blocked` existe para impedimentos reais. Mudança externa de contexto pode interromper temporariamente qualquer fase ativa e exigir `reconcile_context` antes da retomada.

## Specification

A fase `specification` é ativada com `require_spec` quando a classificação do trabalho indicar que a prova semântica é necessária. O agente, não o usuário, deve decidir isso pela política em `core/SEMANTIC_VERIFICATION.md`.

`plan-ready` envia o estado para `specification` quando `spec_required=true`. O evento `spec-ready` só é aceito se `specs/semantic-contract.json` estiver válido; o fingerprint da spec é registrado antes da implementação.

Depois:

- `verification-pass` é recusado se o plano de rastreabilidade semântica estiver inválido ou se algum `must` obrigatório não tiver evidência executável declarada;
- `review-pass` é recusado se a revisão semântica estiver ausente, inválida ou stale;
- risco médio/alto exige review desacoplado pela política semântica.

Assim, a máquina de estados não depende apenas de o mesmo agente afirmar que verificou.

## Interface interna

```bash
python scripts/factory.py init --goal "Criar um sistema de patrimônio" --require-spec
python scripts/factory.py status
python scripts/factory.py next
python scripts/factory.py resume
python scripts/factory.py record plan-ready --summary "..."
python scripts/factory.py spec-validate
python scripts/factory.py verification-plan-init
python scripts/factory.py review-packet --base main
```

O usuário não deve precisar memorizar ou executar esses comandos. Eles são uma interface comum para ChatGPT, Codex, Claude Code, Cursor, CI ou outro executor.

## Estado

O runtime grava `.factory/state.json`, que é compacto e pode ser versionado em handoffs importantes.

Ele contém:

- objetivo atual;
- fase/status;
- fingerprint do contexto reconhecido;
- resumo de planejamento/implementação;
- se Semantic Verification é exigida e o fingerprint da spec reconhecida;
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

Quando um estado novo precisar de Semantic Verification, o agente inicializa/resume com `require_spec`; isso não deve virar uma escolha técnica delegada ao usuário.

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

`máquina de estados + contexto incremental + contrato semântico quando aplicável + agente + ferramentas + CI + revisão desacoplada`.

Isso preserva portabilidade e evita criar um runtime monolítico que fique obsoleto quando modelos mudarem.
