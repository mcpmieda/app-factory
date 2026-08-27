# Provider Runtime

## Responsabilidade

O Provider Runtime transforma uma task já planejada em execução controlada de um provider local/headless. Ele não decide produto, não altera o manifesto e não substitui o GitHub Control Plane.

Entrada confiável:

- Factory Run e task IDs;
- repositório `owner/name`;
- worktree absoluto e dedicado;
- integration, target e worker branches distintas;
- escopos explícitos;
- instrução fechada;
- comandos determinísticos permitidos;
- timeout;
- remote Git conhecido.

Saída confiável:

- status do provider;
- session ID quando disponível;
- telemetria sanitizada;
- SHA validado;
- arquivos alterados;
- confirmação de push da worker branch.

Sem push confirmado, a execução não está concluída.

## Request imutável

`ProviderTaskRequest` é frozen e validado antes da execução. Ele rejeita:

- repositório fora do formato `owner/name`;
- worktree relativo;
- branch inválida ou compartilhada com integration/target;
- `paths` ausentes, wildcard, absolutos ou com traversal;
- escopo que sobrepõe `.github`, `infra/factory` ou `infra/validation`;
- timeout fora de 1–7200 segundos;
- remote com forma de URL/comando;
- comando composto, shell arbitrário, rede direta, Git mutável ou operação destrutiva.

## Ambiente

O subprocess runner usa `shell=False`, argumentos separados e uma allowlist de variáveis de ambiente. Tokens e credenciais comuns do processo pai não são herdados.

Cada provider recebe profile dedicado fora do worktree:

- `ANTIGRAVITY_PROFILE_HOME` para Antigravity;
- `OPENCODE_PROFILE_HOME` para OpenCode/Ollama.

`HOME`, diretórios XDG e equivalentes Windows são redirecionados para esse profile. O profile deve conter apenas estado necessário ao provider, nunca credenciais gerais do usuário.

Executores locais ainda devem usar conta, VM, container ou host dedicado proporcional ao risco. Permissões de ferramenta e validação de Git não substituem isolamento do sistema operacional para código não confiável.

## Antigravity adapter

Comando base:

```text
agy -p <task-instruction> --output-format json
```

Flags opcionais são adicionadas como argumentos fixos:

- `--model`;
- `--effort low|medium|high`;
- `--agent`.

Invariantes:

- profile dedicado obrigatório;
- profile fora do worktree;
- saída JSON;
- prompt ocultado em logs/preview;
- nenhuma flag que ignore permissões;
- health exige CLI, autenticação isolada e descoberta de modelo.

## OpenCode/Ollama adapter

Comando base:

```text
opencode run --auto --format json --dir <worktree> --model ollama/<model> <task-instruction>
```

`--auto` não abre autoridade irrestrita: a configuração inline define `deny` como padrão e libera somente operações explícitas.

Invariantes:

- apenas provider `ollama`;
- URL Ollama restrita a loopback e sem credenciais;
- modelo explícito;
- profile dedicado fora do worktree;
- config global real não é herdada;
- apenas `ollama` fica habilitado;
- plugins padrão, Claude config, model fetch, auto-share e autoupdate ficam desabilitados;
- MCP, plugins, instructions e commands inline ficam vazios;
- `external_directory`, web, subagents, skills e question ficam negados;
- `.git` e arquivos `.env` ficam ilegíveis;
- edição usa allowlist por escopo e deny explícito para paths protegidos;
- Git mutável fica negado;
- somente comandos determinísticos fornecidos pelo Control Plane são liberados.

Como configs OpenCode são mescladas, o adapter rejeita `opencode.json`, `opencode.jsonc` e `.opencode` no repositório durante a primeira homologação. Uma política futura pode substituir essa proibição por parsing/allowlist formal, mas nunca por confiança implícita.

## Proteção Git

Antes do provider:

- worktree precisa estar limpo;
- top-level precisa ser exatamente o worktree informado;
- branch atual precisa ser a worker branch;
- SHA inicial é capturado;
- `.git` control entry, config, hooks, atributos/info, refs e remote são capturados.

Depois do provider e antes de confiar em outro comando Git:

- control entry e metadados sensíveis são comparados diretamente;
- branch atual precisa permanecer a worker branch;
- SHA inicial precisa ser ancestral;
- merge commits introduzidos pelo provider são recusados;
- somente o ref da worker branch pode mudar;
- remote precisa permanecer idêntico;
- todos os arquivos alterados precisam ficar no escopo.

O runtime confiável executa `git add`, `git commit` e `git push` com hooks desabilitados. O push usa o remote capturado antes do provider e somente:

```text
HEAD:refs/heads/<working_branch>
```

Após o push, `ls-remote` confirma que o SHA remoto é exatamente o SHA validado.

## Telemetria

Eventos possuem:

- run/task/provider;
- fase;
- outcome;
- timestamp UTC;
- detalhe sanitizado;
- métricas numéricas.

Redação cobre campos como token, secret, password, API key, authorization, credenciais em URL e formatos comuns de token GitHub.

A telemetria produzida pelo runtime é estruturada, mas sua persistência durável no GitHub pertence ao Control Plane.

## Health e fallback

Probe não executa task. Ele verifica capacidade real mínima:

- Antigravity: binary, versão, profile/auth e modelos;
- OpenCode/Ollama: binaries, serviço local, modelo instalado e enumeração do provider isolado.

`healthy` e `degraded` podem ser usados pelo roteador. `unavailable` e `unknown` não recebem task automática.

## Limites atuais

Implementado e coberto por testes:

- adapters reais de CLI;
- ambiente sanitizado;
- profiles isolados;
- permission config OpenCode;
- scope guard;
- proteção de Git;
- commit/push controlado;
- confirmação remota do SHA;
- telemetria e health;
- CLI machine-readable.

Ainda pendente de evidência live:

- execução Antigravity real;
- execução OpenCode/Ollama real;
- executor local durável/efêmero operacional;
- persistência automática de health/telemetria no GitHub;
- retomada de provider local interrompido a partir do Control Plane.
