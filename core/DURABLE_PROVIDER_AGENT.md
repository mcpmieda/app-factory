# Durable Provider Agent

## Objetivo

Permitir que Antigravity e OpenCode/Ollama executem tasks locais ou headless sem transformar o computador iniciador em fonte de verdade.

Princípio obrigatório:

> Nenhuma Factory Run depende do computador que iniciou a execução para preservar estado, autoridade ou resultado aproveitável.

O agente local é um executor substituível. GitHub continua sendo a autoridade para:

- manifesto imutável;
- issue da task;
- seleção do provider;
- lease;
- branches e commits;
- heartbeat aceito;
- resultado aceito;
- CI;
- Merge Train;
- encerramento da task.

## Modelo de confiança

O protocolo separa três responsabilidades:

1. **GitHub Control Plane** — concede lease e valida resultados;
2. **executor local/headless** — executa a task na worker branch;
3. **Provider Runtime** — protege worktree, escopo, Git, commit e push.

Uma lease só é confiável quando sua origem real no GitHub foi verificada como `github-actions[bot]`. O campo `actor` dentro do JSON não substitui a verificação do autor do comentário/evento pela API do GitHub.

Por isso, a CLI local:

- valida o conteúdo da lease antes de executar;
- nunca publica uma decisão final;
- emite somente candidatos de heartbeat/resultado;
- marca esses candidatos como `pending-github-control-plane-validation`;
- depende do workflow confiável para verificar a procedência da lease e persistir a decisão.

## Lease durável

`FactoryLease` vincula exatamente:

- `lease_id`;
- `run_id`;
- `task_id`;
- número da issue;
- provider;
- executor/worker ID;
- repositório;
- worker branch;
- integration branch;
- target branch;
- SHA-256 do request portátil;
- SHA-256 do manifesto imutável;
- emissão e expiração;
- ator observado pelo Control Plane.

Providers automáticos aceitos nesta fase:

- `antigravity`;
- `opencode_ollama`.

`codex` não pertence ao conjunto automático durável.

TTL permitido:

- mínimo: 60 segundos;
- máximo: 21.600 segundos.

Uma lease expirada não é renovada implicitamente por heartbeat. Renovação ou takeover exige nova decisão do Control Plane.

## Fingerprints

### Request

O fingerprint do request inclui o contrato material da task:

- run/task;
- repositório;
- branches;
- paths;
- instrução;
- comandos permitidos;
- timeout;
- remote.

O caminho local do worktree é excluído. Assim, outro executor pode materializar a mesma task em diretório diferente e obter o mesmo fingerprint.

### Manifesto

O manifesto completo é serializado de forma canônica e recebe SHA-256. Alteração posterior invalida a lease.

Isso preserva a imutabilidade do Factory Run depois da materialização.

## Heartbeat

Fases permitidas:

- `claimed`;
- `preparing`;
- `running`;
- `publishing`;
- `completed`;
- `failed`.

Heartbeat contém apenas:

- identidade da lease/task/provider/executor;
- fase;
- timestamp;
- head SHA opcional;
- detalhe sanitizado;
- métricas numéricas.

Heartbeat não:

- renova a lease;
- altera manifesto;
- concede merge;
- concede produção;
- amplia permissões;
- transforma resultado local em conclusão durável.

## Resultado

`DurableProviderResult` registra:

- lease/run/task/issue;
- provider e executor;
- estado terminal;
- worker branch;
- commit SHA validado;
- remote SHA confirmado;
- paths alterados;
- confirmação de push;
- fingerprints do request e manifesto;
- timestamp;
- session ID e erro sanitizados.

Resultado `success` só pode ser concluído quando:

1. a lease estava ativa no timestamp do resultado;
2. lease, request, manifesto e executor coincidem exatamente;
3. branch é a worker branch concedida;
4. commit SHA é válido;
5. remote SHA é idêntico ao commit validado;
6. push foi confirmado;
7. existem alterações rastreadas;
8. todos os paths permanecem no escopo;
9. nenhum path protegido foi alterado.

Resultado de falha pode ser aceito como evento terminal vinculado à lease, mas nunca é marcado como task concluída.

## Recovery e takeover

`select_recoverable_lease()` aplica fail-closed:

- exatamente uma lease ativa, confiável e compatível: pode executar/retomar;
- nenhuma lease ativa: executor não possui autoridade; o Control Plane pode emitir nova lease;
- mais de uma lease ativa compatível: conflito; nenhuma execução deve prosseguir.

O estado aproveitável permanece na worker branch e no GitHub. Cache, stdout, memória do processo e sessão local não são necessários para outro executor continuar.

## Relação com Provider Runtime

Depois da autorização local da lease, `scripts/durable_provider_agent.py run` chama o Provider Runtime existente, que:

- exige worktree limpo e branch dedicada;
- sanitiza ambiente;
- protege `.github`, `infra/factory` e `infra/validation`;
- protege Git config, hooks, refs, remote e histórico;
- valida todos os changed paths;
- cria commit controlado;
- publica somente a worker branch;
- confirma o SHA remoto.

O Durable Provider Agent não reduz nenhum desses controles.

## CLI

### Fingerprints

```text
python scripts/durable_provider_agent.py fingerprint provider-task.json factory-run.json
```

A saída não inclui worktree nem instrução em texto aberto.

### Validar lease

```text
python scripts/durable_provider_agent.py validate \
  provider-task.json \
  factory-run.json \
  lease.json \
  --worker-id executor-01
```

### Heartbeat candidato

```text
python scripts/durable_provider_agent.py heartbeat lease.json \
  --phase running \
  --head-sha <sha> \
  --metric elapsed_seconds=120
```

A saída ainda precisa ser enviada ao workflow do Control Plane, que revalida e persiste o evento como bot.

### Executar e publicar

```text
python scripts/durable_provider_agent.py run \
  provider-task.json \
  factory-run.json \
  lease.json \
  --worker-id executor-01 \
  --publish \
  --profile-home /isolated/provider-profile
```

O provider é determinado pela lease. O executor não escolhe Codex nem troca o provider concedido.

`--publish` é obrigatório. Trabalho local sem SHA remoto confirmado não representa conclusão.

## Marcadores

O Core possui serialização segura de marcadores HTML para o gateway GitHub. Apenas marcadores cuja autoria real foi verificada como `github-actions[bot]` podem ser tratados como estado confiável.

Nunca confiar somente em:

- texto copiado pelo executor;
- campo `actor` enviado pelo cliente;
- comentário de usuário;
- cache local;
- nome de branch sem SHA;
- resultado sem lease ativa.

## Autoridade preservada

Mesmo com resultado aceito:

- a task avança no máximo para o gate de CI/reconciliação;
- worker automático não faz merge no target;
- worker automático não cria autoridade de produção;
- PR final continua draft;
- merge final continua humano;
- Banco de Notas sync não é habilitado;
- Codex continua manual e excepcional.

## Estado de implementação

Implementado e coberto por regressões:

- fingerprints portáteis;
- manifesto imutável por hash;
- leases confiáveis/expiráveis;
- binding exato de identidade;
- heartbeat sanitizado;
- resultado por SHA remoto;
- recovery/takeover fail-closed;
- CLI machine-readable;
- integração com Provider Runtime.

Ainda depende do Control Plane do repositório operacional:

- emissão da lease por GitHub Actions;
- verificação da autoria real do marcador;
- workflow_dispatch de heartbeat/resultado;
- persistência de provider health;
- transição para CI;
- reconciliation depois de restart.

Essa integração deve ser implementada no repositório consumidor sem conceder merge final, produção ou permissões adicionais ao executor.
