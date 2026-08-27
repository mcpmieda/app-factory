# Multiagent Execution

## Objetivo

A App Factory distribui fatias independentes de construção, verificação e revisão entre provedores substituíveis, sem prender a execução a um computador ou a um único fornecedor.

Princípio obrigatório:

> Nenhuma Factory Run pode depender do computador que a iniciou para preservar seu estado.

O GitHub é a fonte técnica de verdade para manifesto, issues, labels, sessões, branches, commits, PRs, CI e evidência de merge. Worktree, stdout, cache e sessão local nunca são estado durável suficiente.

## Arquitetura-alvo

```text
                 App Factory
                     ↓
              divide o trabalho
                     ↓
       ┌─────────────┼─────────────┐
       ↓             ↓             ↓
 Antigravity       Jules      OpenCode/Ollama
 headless          remoto       worker local
       ↓             ↓             ↓
   worktree       branch/PR       worktree
       └─────────────┼─────────────┘
                     ↓
               Merge Train
                     ↓
     CodeRabbit + Semgrep + Sonar
                     ↓
               CI / testes
                     ↓
            revisão excepcional
                  Codex
```

Codex é fallback premium/manual. O registry baseline mantém `automatic=false`, mesmo quando execução metered é permitida.

## Estado comprovado

A Factory Run `jules-api-pilot-002`, no `mcpmieda/ecossistema-escola`, comprovou em execução real:

- dispatch Jules pela REST API;
- dois workers paralelos;
- dependente liberado após os merges;
- PR e branch isolados por worker;
- escopo fechado por arquivos;
- CI `workflow_dispatch` identificado pelo `head_sha` exato;
- retomada de task em `factory:ci` depois de restart, sem sessão duplicada;
- squash merge somente na integration branch;
- CI completo da integration branch;
- PR final draft para `main`;
- nenhum merge final e nenhum deploy de produção automático.

A evidência detalhada está em `docs/JULES_API_FIRST_PILOT_EVIDENCE.md`.

Isso comprova o caminho Jules. Antigravity e OpenCode/Ollama estão implementados e testados, mas ainda precisam de pilotos live em executores isolados antes de serem declarados homologados.

## Registry e política de custo

Cada `ProviderSpec` declara:

- classe de custo;
- modo de execução;
- capacidades;
- limite de paralelismo;
- necessidade de máquina local;
- elegibilidade automática.

Ordem baseline:

1. `zero`;
2. `free_quota`;
3. `included`;
4. `metered`, somente por autorização explícita.

Custo nunca supera capacidade, risco, escopo, Semantic Assurance, Independent Verification, CI ou Definition of Done.

## Factory Run

O manifesto é portátil, versionado e imutável depois da materialização. Campos mínimos:

```json
{
  "schema_version": 1,
  "run_id": "project-phase-001",
  "goal": "Entregar uma fase funcional sem tocar produção.",
  "tasks": [
    {
      "id": "implementation-a",
      "title": "Implementar a fatia A",
      "role": "implementation",
      "depends_on": [],
      "paths": ["src/feature-a"],
      "required_capabilities": ["reasoning", "repo_read", "repo_write", "test"],
      "preferred_providers": ["opencode_ollama", "jules", "antigravity"],
      "human_gates": []
    }
  ]
}
```

Texto de objetivo ou tarefa nunca vira shell. Adapters constroem argumentos fixos e inputs fechados.

## Paralelismo seguro

`max_parallel` é obrigatório entre 1 e 3.

Duas tasks entram na mesma wave somente quando:

- dependências anteriores foram concluídas;
- existe provider automático, disponível e saudável;
- capacidades são suficientes;
- limites global e do provider não foram excedidos;
- escopos de arquivo não se sobrepõem.

Ausência de `paths`, wildcard ou prefixos conflitantes equivalem a escopo inseguro. Dependência explícita estabelece ordem; não autoriza sobreposição simultânea.

## Guardrails de escrita

Nenhum worker automático pode escrever em:

- `.github`;
- `infra/factory`;
- `infra/validation`.

O runtime rejeita tanto o caminho protegido quanto um escopo pai capaz de alcançá-lo, como `infra`.

Nenhum provider automático pode:

- fazer merge para `main` ou target;
- ativar produção;
- habilitar sincronização do Banco de Notas;
- ampliar permissões;
- ler credenciais não destinadas ao executor;
- modificar Git config, hooks, refs, remotes, worktrees ou metadados do repositório.

## Provider Runtime

`engine/provider_runtime.py` e `scripts/provider_worker.py` implementam o contrato local/headless:

1. validar request, branches, escopos, timeout e comandos;
2. exigir worktree raiz, limpa e na worker branch;
3. capturar SHA inicial e metadados Git protegidos;
4. executar o provider com `shell=false`, ambiente sanitizado e profile isolado;
5. revalidar branch, histórico, refs, remote e arquivos alterados;
6. fazer commit controlado com hooks e assinatura desabilitados;
7. publicar somente `HEAD:refs/heads/<worker>`;
8. confirmar no remote que o SHA publicado é o SHA validado;
9. considerar a task concluída somente com evidência durável.

Execução local sem push nunca equivale a conclusão.

Detalhes: `core/PROVIDER_RUNTIME.md`.

## Adapters

### Jules

O caminho remoto API-first já foi comprovado. Estado durável fica em issues, labels, sessão, branches, PRs e CI.

### Antigravity

O adapter:

- usa CLI headless com saída JSON;
- aceita model, effort e agent opcionais;
- exige `ANTIGRAVITY_PROFILE_HOME` dedicado, autenticado e fora do worktree;
- não usa bypass de permissões;
- valida binary, autenticação e descoberta de modelo antes do dispatch.

### OpenCode/Ollama

O adapter:

- usa somente provider `ollama` em URL loopback sem credenciais;
- exige modelo explícito e `OPENCODE_PROFILE_HOME` dedicado;
- aplica default-deny para edição, comandos, web, diretórios externos, subagentes e skills;
- permite escrita somente nos escopos declarados;
- nega Git mutável e libera apenas comandos determinísticos fornecidos pelo Control Plane;
- desabilita plugins, autoshare, autoupdate e model fetch;
- rejeita configuração OpenCode fornecida pelo repositório durante a primeira homologação.

## Health e fallback

Health usa `healthy`, `degraded`, `unavailable` e `unknown`.

O roteador considera apenas providers já elegíveis pelo planner. Prefere `healthy`, depois `degraded`, preservando a ordem de custo. `unavailable` e `unknown` não recebem task automática. Codex não entra no fallback automático.

Health é observação temporal; a decisão e sua evidência devem ser persistidas pelo Control Plane no GitHub.

## Merge Train

Worker PR só pode ser integrado quando:

- base é a integration branch isolada;
- head é branch dedicada;
- arquivos permanecem no escopo;
- CI veio de `workflow_dispatch`;
- CI usa exatamente o head SHA atual e está verde;
- CodeRabbit, Semgrep e Sonar estão verdes para o mesmo SHA;
- não existe revisão bloqueadora válida.

O destino permitido é somente a integration branch. O target nunca recebe auto-merge.

Depois da última task, a integration branch passa por CI completo. O PR final deve ser draft, integration → target, com merge humano. Detalhes: `core/MERGE_TRAIN.md`.

## Human gates

Nunca são autoexecutados:

- `product_decision`;
- `destructive_operation`;
- `production_activation`;
- `privilege_change`;
- `legal_or_organizational_decision`.

Dependentes permanecem bloqueados até resolução explícita.

## CLI

Planner:

```text
python scripts/factory_run.py template
python scripts/factory_run.py validate factory-run.json
python scripts/factory_run.py providers
python scripts/factory_run.py plan factory-run.json --providers jules,antigravity --max-parallel 3
```

Runtime:

```text
python scripts/provider_worker.py validate provider-task.json
python scripts/provider_worker.py probe --provider antigravity --profile-home /isolated/antigravity
python scripts/provider_worker.py probe --provider opencode_ollama --model qwen3-coder --profile-home /isolated/opencode
python scripts/provider_worker.py command --provider opencode_ollama --model qwen3-coder --profile-home /isolated/opencode provider-task.json
python scripts/provider_worker.py run --provider opencode_ollama --model qwen3-coder --profile-home /isolated/opencode --publish provider-task.json
```

`run` exige `--publish`; o modo local-only é recusado.

## Próximas homologações

1. piloto live Antigravity em host/profile isolado;
2. piloto live OpenCode/Ollama em executor durável ou efêmero controlado;
3. persistência de provider health e telemetria no Control Plane;
4. wiring real de CodeRabbit, Semgrep e Sonar;
5. piloto completo do Merge Train multi-provider;
6. escalonamento Codex excepcional, manual e auditado.

A Factory inteira só deve ser declarada pronta depois dessas evidências.
