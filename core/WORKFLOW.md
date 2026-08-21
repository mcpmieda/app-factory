# Universal Workflow

## Loop autônomo

Quando o runtime V1.1 estiver disponível, o fluxo operacional padrão é:

`resume/context → next → agir → registrar evento → next → ... → done`

O usuário não conduz transições técnicas. O Autonomy Engine escolhe a próxima fase e o Context Engine evita releitura integral desnecessária.

## Projeto novo

1. Descoberta — entender problema, usuários e resultado desejado.
2. Pesquisa — verificar soluções, repositórios, bibliotecas e padrões existentes.
3. Produto — consolidar fluxos, escopo e critérios de sucesso.
4. Arquitetura — escolher stack proporcional ao problema.
5. Bootstrap — criar projeto a partir do starter/template mais adequado.
6. Construção — implementar por blocos funcionais completos.
7. Verificação — testes estáticos, comportamento real e browser quando aplicável.
8. Reparação — quando houver falha, corrigir e reverificar com limite explícito de tentativas.
9. Revisão — revisar diff, UX, segurança e riscos relevantes.
10. Entrega — PR/merge/deploy com checks.
11. Aprendizado — atualizar Factory somente quando surgir padrão realmente reutilizável.

Use `TASK_ROUTER.md` para escolher a rota de execução mais leve e verificável, priorizando current-agent + GitHub/CI antes de handoff local.

## Projeto existente

1. executar/interpretar `resume` quando o runtime estiver disponível;
2. recuperar `PROJECT_STATE.md` e estado Git;
3. atualizar o Context Engine e reconciliar delta se o fingerprint mudou;
4. identificar baseline seguro;
5. entender escopo e impacto;
6. revisar diff e dependências diretas;
7. preservar comportamento fora do escopo;
8. testar o que mudou e regressão diretamente relacionada;
9. reparar automaticamente falhas verificadas dentro do limite configurado;
10. ampliar auditoria apenas quando risco ou extensão justificarem;
11. revisar e registrar novo estado confiável.

## Tamanho do trabalho

Evite microtarefas artificiais e missões gigantes sem critérios verificáveis. Prefira uma fatia vertical completa, como `gerenciamento de usuários = listagem + busca + criação + edição + validação + persistência + estados + testes`.

## Falha e estagnação

Não repita indefinidamente a mesma correção. O Autonomy Engine usa repair loop limitado (default 3). Ao atingir o limite:

1. registre o bloqueio técnico;
2. mude estratégia/modelo/executor quando possível;
3. só envolva o usuário se existir decisão humana real ou se nenhum executor disponível conseguir prosseguir com segurança.

## Handoff entre agentes

Aponte para repositório/branch/PR, `PROJECT_STATE.md`, `.factory/state.json` quando versionado, Issue/bloco funcional e critérios de conclusão. Não use transcrição integral de conversa como mecanismo principal de continuidade.
