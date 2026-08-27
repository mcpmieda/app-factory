# Merge Train

## Objetivo

Consolidar resultados de múltiplos workers em uma integration branch isolada sem permitir que provider automático faça merge no target, amplie escopo ou reutilize evidência obsoleta.

## Fluxo

```text
worker branch/PR
  -> validação de base/head/escopo
  -> CI workflow_dispatch do head_sha exato
  -> CodeRabbit + Semgrep + Sonar do mesmo SHA
  -> squash merge somente na integration branch
  -> liberação de dependentes
  -> CI completo da integration branch
  -> PR final DRAFT integration -> target
  -> merge humano
```

## Worker gate

`evaluate_worker_merge()` autoriza integração somente quando todos os requisitos passam:

1. integration e target são branches distintas;
2. base do worker PR é exatamente a integration branch;
3. base nunca é o target;
4. head é branch dedicada, diferente de integration e target;
5. head SHA é válido;
6. CI veio de `workflow_dispatch`;
7. CI usa exatamente o head SHA atual;
8. CI concluiu `success`;
9. changed paths permanecem nos escopos declarados;
10. paths protegidos não foram alterados;
11. não existe revisão bloqueadora válida;
12. CodeRabbit, Semgrep e Sonar concluíram `success`;
13. cada revisão automatizada apresenta evidência do head SHA atual.

Resultado permitido:

- destination: integration branch;
- modo esperado: squash merge;
- target auto-merge: sempre `false`.

## Evidência stale

Novo commit no worker invalida:

- CI anterior;
- revisão anterior;
- aprovação automática anterior;
- decisão de merge anterior.

A autoridade é o `head_sha` atual. Nome de branch sozinho não é evidência suficiente.

## Dependências

Task dependente só pode sair de waiting depois que todas as dependências estiverem materialmente integradas na integration branch e marcadas pelo ator confiável do Control Plane.

Falha/restart não permite pular estado. Reconciliation deve retomar a task a partir da evidência durável existente.

## Integration gate

Depois da última task:

- integration branch deve estar limpa e conter todos os merges esperados;
- CI completo deve ser disparado por `workflow_dispatch`;
- o `head_sha` do CI precisa ser exatamente o head atual;
- deploy/produção deve ser pulado para integration branch;
- falha de CI impede PR final pronto.

## Final gate

`evaluate_final_gate()` exige:

- head = integration branch;
- base = target;
- PR draft;
- integration head SHA válido;
- CI `workflow_dispatch`;
- CI SHA exatamente igual ao integration head;
- conclusão `success`.

Mesmo com tudo verde:

- `draft_required=true`;
- `auto_merge_allowed=false`;
- merge final continua humano.

## Reviews automatizadas

Baseline consolidado:

- CodeRabbit: revisão de mudança e sinais semânticos;
- Semgrep: SAST/padrões de segurança;
- Sonar: qualidade, bugs e maintainability.

Esses checks complementam testes, Semantic Assurance e Independent Verification. Não substituem CI nem revisão humana quando o risco exigir.

Na integração real, nomes/contextos podem ser mapeados para checks específicos do repositório, mas o contrato lógico deve continuar exigindo:

- conclusão verde;
- SHA exato;
- ausência de finding bloqueador válido.

## Falha fechada

Qualquer campo ausente, SHA divergente, evento errado, review stale, escopo inválido ou bloqueio ativo resulta em `allowed=false`.

Não existe fallback que faça merge no target para “destravar” a Factory Run.
