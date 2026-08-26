# Multiagent Execution

## Objetivo

Acelerar construção e evolução de software distribuindo trabalho independente entre múltiplos workers sem transformar a App Factory em dependência de um único fornecedor, sem usar Codex como motor rotineiro e sem permitir que paralelismo produza alterações concorrentes inseguras.

A App Factory continua definindo intenção, contrato, risco, dependências e Definition of Done. Workers executam fatias fechadas. GitHub permanece a fonte técnica de verdade para estado durável, branches, PRs, CI e evidência.

## Princípio

```text
objetivo
  -> decomposição em tarefas
  -> grafo de dependências
  -> escopos de arquivos/recursos
  -> seleção de providers elegíveis
  -> waves paralelas seguras
  -> branches/PRs independentes
  -> gates/revisão
  -> integração controlada
```

O núcleo nunca depende de Jules, Antigravity, OpenCode, Ollama, Codex ou outro nome específico para representar a tarefa. Providers são adaptadores substituíveis.

## Política de custo

Baseline:

1. `zero` — capacidade local sem custo de API quando explicitamente disponível;
2. `free_quota` — workers remotos com plano/cota gratuita ou alta;
3. `included` — capacidade já incluída em ambiente existente;
4. `metered` — somente escalonamento explícito.

`codex` é registrado como `metered`, `automatic=false` e não pode ser selecionado automaticamente nem quando `allow_metered` estiver habilitado. O objetivo é reservá-lo para bloqueios difíceis/revisão premium deliberada.

A política de custo nunca vence capacidade, risco, segurança, Semantic Assurance, Independent Verification ou Definition of Done.

## Providers baseline

O registry inicial em `engine/work_orchestrator.py` descreve capacidades, não credenciais:

- `opencode_ollama`: local/headless, custo de API zero, depende da máquina estar disponível;
- `jules`: worker remoto orientado a GitHub/PR, cota gratuita/limitada;
- `antigravity`: worker headless, cota gratuita/limitada e ambiente previamente autenticado/configurado;
- `codex`: escalonamento premium/manual.

Disponibilidade é sempre explícita por execução. Uma máquina sem Ollama/OpenCode simplesmente não anuncia `opencode_ollama`. Um repositório ainda não autorizado no Jules simplesmente não anuncia `jules`.

Nenhum secret, token, cookie ou API key entra no Factory Run JSON.

## Factory Run

Um Factory Run é um documento JSON portátil e versionável durante a execução. Campos mínimos:

```json
{
  "schema_version": 1,
  "run_id": "banco-notas-fase-08",
  "goal": "Entregar uma fase funcional sem tocar produção.",
  "tasks": [
    {
      "id": "ano-letivo",
      "title": "Implementar configuração do ano letivo",
      "role": "implementation",
      "depends_on": [],
      "paths": ["src/banco-de-notas/ano-letivo"],
      "required_capabilities": ["reasoning", "repo_read", "repo_write", "test"],
      "preferred_providers": ["jules", "antigravity", "opencode_ollama"],
      "human_gates": []
    }
  ]
}
```

O texto de objetivo/tarefa nunca vira shell. Adaptadores usam contratos próprios e inputs fechados.

## Paralelismo seguro

Duas tarefas podem entrar na mesma wave somente quando:

- todas as dependências necessárias já foram concluídas;
- existe provider automático disponível com todas as capacidades exigidas;
- o limite global de paralelismo não foi excedido;
- o limite do provider não foi excedido;
- os escopos de arquivo não se sobrepõem.

Escopos são conservadores. Ausência de `paths` equivale a escopo desconhecido e conflita com qualquer outra tarefa. Prefixos também conflitam: `src/banco` e `src/banco/conselho` não podem executar na mesma wave.

Isso evita múltiplos agentes escrevendo simultaneamente na mesma região lógica do código.

## Human gates

Os seguintes gates nunca são autoexecutados:

- `product_decision`;
- `destructive_operation`;
- `production_activation`;
- `privilege_change`;
- `legal_or_organizational_decision`.

Uma tarefa bloqueada por decisão humana não é marcada como concluída. Dependentes permanecem bloqueados até resolução explícita.

## Continuidade entre computadores

O Factory Run e seus resultados duráveis devem convergir no GitHub. Workers remotos continuam sem depender do computador que iniciou a execução. Workers locais são capacidade oportunística.

Nunca use um worktree local como única fonte de estado. Antes de trocar de computador, trabalho aproveitável precisa estar em branch/commit/PR ou em outro artefato versionado apropriado.

## Integração com Execution Fabric

`core/EXECUTION_FABRIC.md` continua responsável por escolher o backend para uma ação individual. Multiagent Execution fica acima dessa camada quando existe trabalho paralelizável:

```text
Autonomy Engine
  -> ação ampla
  -> Multiagent Execution decompõe/agenda
  -> worker provider executa uma tarefa
  -> Execution Fabric/CI verifica capacidades e gates
```

O novo núcleo não duplica Semantic Assurance, Independent Verification, Learning Engine, Change Hygiene ou CI Executor.

## CLI

```text
python scripts/factory_run.py template
python scripts/factory_run.py validate factory-run.json
python scripts/factory_run.py providers
python scripts/factory_run.py plan factory-run.json --providers jules,antigravity --max-parallel 4
python scripts/factory_run.py plan factory-run.json --providers opencode_ollama,jules,antigravity --max-parallel 4
```

Providers são anunciados explicitamente por máquina/control plane. Isso permite trocar PC do trabalho por PC de casa sem fingir que capacidade local continua disponível.

## GitHub Control Plane

A integração operacional recomendada é:

```text
ChatGPT/PowerShell
  -> GitHub
  -> Factory Run
  -> issues/tasks tipadas
  -> providers
  -> branches/PRs
  -> CI/review
```

GitHub Actions pode coordenar estado, validações e dispatch seguro. Não deve receber prompt livre como comando shell nem credencial de provider em logs.

## Implementação incremental

Fases recomendadas:

1. planner provider-neutral + testes;
2. Control Plane GitHub que materializa Factory Run e child tasks;
3. adaptador Jules remoto;
4. adaptador Antigravity headless;
5. adaptador local OpenCode/Ollama;
6. merge train/reconciliation e telemetria de sucesso/falha;
7. roteamento por evidência sem permitir que Learning Engine reduza gates.

Cada provider pode ser habilitado ou removido sem reescrever o Core.
