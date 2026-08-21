# Universal Workflow

## Loop autônomo

Quando o runtime estiver disponível, o fluxo operacional padrão é:

`resume/context → next → agir → registrar evento → next → ... → done`

O usuário não conduz transições técnicas. O Autonomy Engine escolhe a próxima fase e o Context Engine evita releitura integral desnecessária.

Para trabalho funcional relevante, o fluxo inclui uma etapa semântica explícita:

`planning → specification → implementation → verification → review → delivery`

A etapa `specification` usa `core/SEMANTIC_VERIFICATION.md`. Ela é proporcional: não aplicar contrato formal pesado a documentação/chore ou refactor pequeno sem mudança observável.

## Projeto novo

1. Descoberta — entender problema, usuários e resultado desejado.
2. Pesquisa — verificar soluções, repositórios, bibliotecas e padrões existentes.
3. Produto — consolidar fluxos, escopo e critérios de sucesso.
4. Especificação semântica — para trabalho funcional relevante, materializar objetivo, invariantes e critérios `given/when/then` antes do código.
5. Arquitetura — escolher stack proporcional ao problema.
6. Bootstrap — criar projeto a partir do starter/template mais adequado.
7. Construção — implementar por blocos funcionais completos.
8. Verificação — derivar rastreabilidade da spec, executar testes estáticos/comportamento/browser e provar cada critério `must` aplicável.
9. Reparação — quando houver falha, corrigir e reverificar com limite explícito de tentativas.
10. Revisão — preferir segundo agente/contexto independente; quando indisponível, usar clean-context review limitado a spec + conteúdo/evidências atuais.
11. Entrega — PR/merge/deploy somente com checks e review evidence atuais.
12. Aprendizado — atualizar Factory somente quando surgir padrão realmente reutilizável.

Use `TASK_ROUTER.md` para escolher a rota de execução mais leve e verificável, priorizando current-agent + GitHub/CI antes de handoff local.

## Projeto existente

1. executar/interpretar `resume` quando o runtime estiver disponível;
2. recuperar `PROJECT_STATE.md` e estado Git;
3. atualizar o Context Engine e reconciliar delta se o fingerprint mudou;
4. identificar baseline seguro;
5. entender escopo e impacto;
6. decidir se a mudança altera comportamento/regra/contrato o suficiente para exigir Semantic Verification;
7. quando exigir, atualizar a spec antes da implementação e regenerar a rastreabilidade afetada;
8. revisar diff e dependências diretas;
9. preservar comportamento fora do escopo;
10. testar o que mudou e regressão diretamente relacionada;
11. reparar automaticamente falhas verificadas dentro do limite configurado;
12. ampliar auditoria apenas quando risco ou extensão justificarem;
13. fazer revisão desacoplada quando exigida e registrar novo estado confiável.

## Tamanho do trabalho

Evite microtarefas artificiais e missões gigantes sem critérios verificáveis. Prefira uma fatia vertical completa, como `gerenciamento de usuários = listagem + busca + criação + edição + validação + persistência + estados + testes`.

Critérios verificáveis devem nascer da intenção/spec, não somente depois de o agente ver o que implementou.

## Falha e estagnação

Não repita indefinidamente a mesma correção. O Autonomy Engine usa repair loop limitado (default 3). Ao atingir o limite:

1. registre o bloqueio técnico;
2. mude estratégia/modelo/executor quando possível;
3. só envolva o usuário se existir decisão humana real ou se nenhum executor disponível conseguir prosseguir com segurança.

Falha semântica (critério `must` não provado ou review stale) é falha real de verificação, mesmo que build e testes genéricos estejam verdes.

## Handoff entre agentes

Aponte para repositório/branch/PR, `PROJECT_STATE.md`, `.factory/state.json` quando versionado, Issue/bloco funcional e critérios de conclusão. Quando Semantic Verification se aplicar, inclua também `specs/semantic-contract.json`, `specs/verification-plan.json` e o review evidence atual. Não use transcrição integral de conversa como mecanismo principal de continuidade.
