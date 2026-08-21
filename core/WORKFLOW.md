# Universal Workflow

## Projeto novo

1. Descoberta — entender problema, usuários e resultado desejado.
2. Pesquisa — verificar soluções, repositórios, bibliotecas e padrões existentes.
3. Produto — consolidar fluxos, escopo e critérios de sucesso.
4. Arquitetura — escolher stack proporcional ao problema.
5. Bootstrap — criar projeto a partir do starter/template mais adequado.
6. Construção — implementar por blocos funcionais completos.
7. Verificação — testes estáticos, comportamento real e browser quando aplicável.
8. Revisão — revisar diff, UX, segurança e riscos relevantes.
9. Entrega — PR/merge/deploy com checks.
10. Aprendizado — atualizar Factory somente quando surgir padrão realmente reutilizável.

Use `TASK_ROUTER.md` para indicar o ambiente recomendado em cada fase.

## Projeto existente

1. recuperar `PROJECT_STATE.md`/documentação e estado Git;
2. identificar baseline seguro;
3. entender escopo e impacto;
4. revisar diff e dependências diretas;
5. preservar comportamento fora do escopo;
6. testar o que mudou e regressão diretamente relacionada;
7. ampliar auditoria apenas quando risco ou extensão justificarem;
8. registrar novo estado confiável.

## Tamanho do trabalho

Evite microtarefas artificiais e missões gigantes sem critérios verificáveis. Prefira uma fatia vertical completa, como `gerenciamento de usuários = listagem + busca + criação + edição + validação + persistência + estados + testes`.

## Handoff entre agentes

Aponte para repositório/branch/PR, `PROJECT_STATE.md`, Issue/bloco funcional e critérios de conclusão. Não use transcrição integral de conversa como mecanismo principal de continuidade.