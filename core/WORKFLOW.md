# Universal Workflow

## Loop autônomo

Quando o runtime estiver disponível, o fluxo operacional padrão é:

`resume/context → next → agir → registrar evento → next → ... → done`

O usuário não conduz transições técnicas. O Autonomy Engine escolhe a próxima fase e o Context Engine evita releitura integral desnecessária.

Para trabalho funcional relevante, o fluxo inclui uma etapa semântica explícita:

`planning → specification → implementation → verification → review → delivery`

A etapa `specification` usa `core/SEMANTIC_VERIFICATION.md`. Ela é proporcional: não aplicar contrato formal pesado a documentação/chore ou refactor pequeno sem mudança observável.

A arquitetura do produto também deve respeitar `core/SYSTEM_ENGINEERING.md`: a Factory pode manter processo leve, mas não pode substituir persistência compartilhada/servidor/autorização necessários por uma demo local apenas para reduzir trabalho.

## Projeto novo

1. Descoberta — entender problema, usuários e resultado desejado.
2. Pesquisa — verificar soluções, repositórios, bibliotecas e padrões existentes.
3. Produto — consolidar fluxos, escopo e critérios de sucesso.
4. Classificação arquitetural — aplicar `core/SYSTEM_ENGINEERING.md`, registrar nível do produto e, para `persistent-app` ou superior, fonte autoritativa dos dados; para `multi-user-system` ou superior, derivar backend/server-side, persistência compartilhada, identidade/autorização, validação, migrations e recovery proporcionais.
5. Especificação semântica — para trabalho funcional relevante, materializar objetivo, invariantes e critérios `given/when/then` antes do código.
6. Arquitetura — escolher stack proporcional ao problema e suficiente ao nível de sistema, sem tratar demo/localStorage/mock como arquitetura final compartilhada quando o produto exigir persistência real.
7. Bootstrap — criar projeto a partir do starter/template mais adequado.
8. Construção — implementar por blocos funcionais completos.
9. Verificação — derivar rastreabilidade da spec, executar testes estáticos/comportamento/browser e provar cada critério `must` aplicável; para sistemas persistentes/multiusuário, exercitar também persistência e autorização reais ou ambiente equivalente.
10. Reparação — quando houver falha, corrigir e reverificar com limite explícito de tentativas.
11. Revisão — preferir segundo agente/contexto independente; quando indisponível, usar clean-context review limitado a spec + conteúdo/evidências atuais.
12. Entrega — PR/merge/deploy somente com checks, arquitetura e review evidence atuais.
13. Aprendizado — atualizar Factory somente quando surgir padrão realmente reutilizável.

Use `TASK_ROUTER.md` para escolher a rota de execução mais leve e verificável, priorizando current-agent + GitHub/CI antes de handoff local.

## Projeto existente

1. executar/interpretar `resume` quando o runtime estiver disponível;
2. recuperar `PROJECT_STATE.md` e estado Git;
3. atualizar o Context Engine e reconciliar delta se o fingerprint mudou;
4. identificar baseline seguro;
5. entender escopo e impacto;
6. confirmar se o nível de sistema e a fonte autoritativa dos dados continuam coerentes com `core/SYSTEM_ENGINEERING.md`, sobretudo quando a evolução transforma demo/local app em sistema persistente ou multiusuário;
7. decidir se a mudança altera comportamento/regra/contrato o suficiente para exigir Semantic Verification;
8. quando exigir, atualizar a spec antes da implementação e regenerar a rastreabilidade afetada;
9. revisar diff e dependências diretas;
10. preservar comportamento fora do escopo;
11. testar o que mudou e regressão diretamente relacionada;
12. reparar automaticamente falhas verificadas dentro do limite configurado;
13. ampliar auditoria apenas quando risco ou extensão justificarem;
14. fazer revisão desacoplada quando exigida e registrar novo estado confiável.

## Tamanho do trabalho

Evite microtarefas artificiais e missões gigantes sem critérios verificáveis. Prefira uma fatia vertical completa, como `gerenciamento de usuários = listagem + busca + criação + edição + validação + persistência + estados + testes`.

Para sistema multiusuário, uma fatia só é vertical de verdade quando atravessa UI + regras server-side + persistência + autorização aplicável, e não apenas quando a tela simula o fluxo.

Critérios verificáveis devem nascer da intenção/spec, não somente depois de o agente ver o que implementou.

## Falha e estagnação

Não repita indefinidamente a mesma correção. O Autonomy Engine usa repair loop limitado (default 3). Ao atingir o limite:

1. registre o bloqueio técnico;
2. mude estratégia/modelo/executor quando possível;
3. só envolva o usuário se existir decisão humana real ou se nenhum executor disponível conseguir prosseguir com segurança.

Falha semântica (critério `must` não provado ou review stale) é falha real de verificação, mesmo que build e testes genéricos estejam verdes.

Falha arquitetural também é falha real: um sistema classificado acima de `local-app` não pode ser entregue como produção se a fonte autoritativa ainda estiver apenas no navegador ou se regras obrigatórias de acesso existirem apenas na interface.

## Handoff entre agentes

Aponte para repositório/branch/PR, `PROJECT_STATE.md`, `.factory/state.json` quando versionado, Issue/bloco funcional e critérios de conclusão. Inclua também nível do sistema e decisões de persistência/identidade/recovery quando relevantes. Quando Semantic Verification se aplicar, inclua `specs/semantic-contract.json`, `specs/verification-plan.json` e o review evidence atual. Não use transcrição integral de conversa como mecanismo principal de continuidade.
