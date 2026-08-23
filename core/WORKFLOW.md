# Universal Workflow

## Loop autônomo

Quando o runtime estiver disponível, o fluxo operacional padrão é:

`resume/context → next → agir → registrar evento → next → ... → done`

O usuário não conduz transições técnicas. O Autonomy Engine escolhe a próxima fase e o Context Engine evita releitura integral desnecessária.

Para trabalho funcional relevante, o fluxo inclui uma etapa semântica explícita:

`planning → semantic assurance proporcional → specification → implementation → verification → review → delivery`

A etapa `specification` usa `core/SEMANTIC_VERIFICATION.md`. Antes dela, `core/SEMANTIC_ASSURANCE.md` decide se uma spec simples em profundidade `scenario` é suficiente ou se o domínio exige `domain`/`formal`. Semantic Assurance não cria uma fase pesada universal: em trabalho simples, ela termina na própria classificação `scenario`.

Para `domain`/`formal`, `specs/semantic-assurance.json` complementa `semantic-contract.json` com requisitos estruturados, vocabulário/domínio, restrições, consistência, cobertura e semantic diff. Erros determinísticos e perguntas `blocking` devem ser resolvidos antes da implementação.

A arquitetura do produto também deve respeitar `core/SYSTEM_ENGINEERING.md`: a Factory pode manter processo leve, mas não pode substituir persistência compartilhada/servidor/autorização necessários por uma demo local apenas para reduzir trabalho.

Quando houver API/integração relevante, `core/API_ENGINEERING.md` entra como contrato especializado da interface. Ele não cria uma fase paralela obrigatória: suas decisões de protocolo, contrato, compatibilidade, segurança e gates são incorporadas a planejamento/especificação/verificação na profundidade necessária.

`core/INDEPENDENT_VERIFICATION.md` também não cria uma fase paralela universal. Ele aprofunda a fase de **verification** quando risco, nível do sistema, API ou release justificarem evidência externa ao raciocínio implementador. Projetos simples permanecem `baseline`.

## Projeto novo

1. Descoberta — entender problema, usuários e resultado desejado.
2. Pesquisa — verificar soluções, repositórios, bibliotecas e padrões existentes.
3. Produto — consolidar fluxos, escopo e critérios de sucesso.
4. Classificação arquitetural — aplicar `core/SYSTEM_ENGINEERING.md`, registrar nível do produto e, para `persistent-app` ou superior, fonte autoritativa dos dados; para `multi-user-system` ou superior, derivar backend/server-side, persistência compartilhada, identidade/autorização, validação, migrations e recovery proporcionais.
5. Classificação da interface — se existir API, integração, webhook, evento ou contrato compartilhado, aplicar `core/API_ENGINEERING.md`, escolher `none`/`lightweight`/`contract`/`governed`, consumidores, protocolo e fonte de verdade; não formalizar API sem necessidade real.
6. Classificação semântica — decidir se Semantic Verification é necessária e, quando for, escolher `scenario`/`domain`/`formal` conforme `core/SEMANTIC_ASSURANCE.md`. A profundidade vem do domínio/risco, não do desejo de usar ferramentas sofisticadas.
7. Semantic Assurance — em `domain`/`formal`, materializar/atualizar `specs/semantic-assurance.json`, normalizar requisitos, modelar apenas conceitos/relações/estados materiais e executar consistency/coverage. Resolver referências quebradas, contradições determinísticas e perguntas `blocking` antes de implementar. Selecionar método formal apenas quando tecnicamente justificável.
8. Classificação da prova independente — aplicar `core/INDEPENDENT_VERIFICATION.md` a risco + nível de sistema + API mode + sinais técnicos, escolher `baseline`/`independent`/`adversarial`/`release` e planejar apenas checks gratuitos/open source tecnicamente aplicáveis.
9. Especificação semântica — para trabalho funcional relevante, materializar objetivo, invariantes e critérios `given/when/then` antes do código. `semantic-contract.json` é a autoridade dos comportamentos observáveis; `semantic-assurance.json` complementa o domínio/requisitos sem duplicar OpenAPI/schema/arquitetura.
10. Arquitetura — escolher stack proporcional ao problema e suficiente ao nível de sistema, sem tratar demo/localStorage/mock como arquitetura final compartilhada quando o produto exigir persistência real; interfaces e verificadores devem seguir os modos decididos.
11. Bootstrap — criar projeto a partir do starter/template mais adequado. Copiar templates/gates de API, Semantic Assurance ou Independent Verification somente quando realmente exigidos.
12. Construção — implementar por blocos funcionais completos, mantendo contrato e implementação da API no mesmo bloco quando aplicável.
13. Verificação — derivar rastreabilidade da spec, executar testes estáticos/comportamento/browser e provar cada critério `must` aplicável. Para ranges/invariantes/state machines, acrescentar property/stateful/model-based evidence quando ela trouxer cobertura real. Para sistemas persistentes/multiusuário, exercitar persistência/autorização reais ou ambiente equivalente; para APIs `contract`/`governed`, executar gates proporcionais; para Independent Verification acima de `baseline`, executar a matriz `required/advisory` selecionada.
14. Reparação — quando houver falha, corrigir e reverificar com limite explícito de tentativas. Scanner/model checker/gate não executado não vira sucesso.
15. Revisão — preferir segundo agente/contexto independente; quando indisponível, usar clean-context review limitado a spec + conteúdo/evidências atuais. Semantic diff e mudanças de contrato entram no pacote. Scanners/solvers determinísticos são evidência complementar, não reviewer semântico.
16. Entrega — PR/merge/deploy somente com checks, arquitetura, contratos, Semantic Assurance aplicável, Independent Verification exigida e review evidence atuais.
17. Aprendizado — atualizar Factory somente quando surgir padrão realmente reutilizável.

Use `TASK_ROUTER.md` para escolher a rota de execução mais leve e verificável, priorizando current-agent + GitHub/CI antes de handoff local. Gates formais/independentes determinísticos preferem GitHub CI quando ele consegue executá-los sem custo não autorizado.

## Projeto existente

1. executar/interpretar `resume` quando o runtime estiver disponível;
2. recuperar `PROJECT_STATE.md`, `SEMANTICS.md`, `VERIFICATION.md` quando existirem e estado Git;
3. atualizar o Context Engine e reconciliar delta se o fingerprint mudou;
4. identificar baseline seguro;
5. entender escopo e impacto;
6. confirmar se o nível de sistema e a fonte autoritativa dos dados continuam coerentes com `core/SYSTEM_ENGINEERING.md`, sobretudo quando a evolução transforma demo/local app em sistema persistente ou multiusuário;
7. se houver API/integração relevante, confirmar se o modo de governança, consumidores e fonte de verdade continuam coerentes com `core/API_ENGINEERING.md`, principalmente antes de alteração potencialmente incompatível;
8. decidir se a mudança altera comportamento/regra/contrato o suficiente para exigir Semantic Verification e recalcular semantic depth se a complexidade de domínio, estados, políticas, temporalidade ou concorrência mudou;
9. quando a mudança for `domain`/`formal`, validar o fingerprint de `semantic-assurance.json` contra o contrato atual, atualizar o assurance antes da implementação e calcular semantic diff para identificar requisitos/ACs/invariantes/gates afetados;
10. recalcular Independent Verification quando risco, nível do sistema, API, autenticação/dependências/UI ou condição de release mudarem; não manter `baseline` apenas porque o projeto começou simples;
11. quando Semantic Verification exigir, atualizar a spec antes da implementação e regenerar a rastreabilidade afetada;
12. para contrato machine-readable, atualizar o contrato no mesmo bloco da implementação e comparar breaking changes quando aplicável;
13. revisar diff e dependências diretas;
14. preservar comportamento fora do escopo e compatibilidade prometida a consumidores;
15. testar o que mudou e regressão diretamente relacionada;
16. executar gates formais/property/stateful selecionados e checks independentes aplicáveis, registrando findings/exceções proporcionais;
17. reparar automaticamente falhas verificadas dentro do limite configurado;
18. ampliar auditoria apenas quando risco ou extensão justificarem;
19. fazer revisão desacoplada quando exigida e registrar novo estado confiável.

## Tamanho do trabalho

Evite microtarefas artificiais e missões gigantes sem critérios verificáveis. Prefira uma fatia vertical completa, como `gerenciamento de usuários = listagem + busca + criação + edição + validação + persistência + estados + testes`.

Para sistema multiusuário, uma fatia só é vertical de verdade quando atravessa UI + regras server-side + persistência + autorização aplicável, e não apenas quando a tela simula o fluxo.

Se a fatia atravessar uma API formal, ela também inclui contrato + implementação + compatibilidade/gates aplicáveis; entregar apenas endpoint ou apenas spec não completa o comportamento.

Se a fatia estiver em semantic depth `domain`/`formal`, requisitos/refs/contradições/pontos blocking dessa fatia precisam estar resolvidos antes do código. Formalização só entra quando a propriedade da fatia realmente justificar.

Se a fatia tiver checks independentes `required`, ela só fecha quando esses checks também executarem ou houver exceção explícita aceitável. Mutation/SAST/DAST/fuzz não são acrescentados quando não houver pré-condição real.

Critérios verificáveis devem nascer da intenção/spec, não somente depois de o agente ver o que implementou.

## Falha e estagnação

Não repita indefinidamente a mesma correção. O Autonomy Engine usa repair loop limitado (default 3). Ao atingir o limite:

1. registre o bloqueio técnico;
2. mude estratégia/modelo/executor quando possível;
3. só envolva o usuário se existir decisão humana real ou se nenhum executor disponível conseguir prosseguir com segurança.

Falha de Semantic Assurance também é falha real da fase de especificação: contradição determinística, referência obrigatória quebrada, `open_question` blocking ou formalização `required` stale/sem gate impede avançar. Finding probabilístico/advisory não deve ser promovido automaticamente a bloqueio.

Falha semântica de verificação (critério `must` não provado ou review stale) é falha real mesmo que build e testes genéricos estejam verdes.

Falha arquitetural também é falha real: um sistema classificado acima de `local-app` não pode ser entregue como produção se a fonte autoritativa ainda estiver apenas no navegador ou se regras obrigatórias de acesso existirem apenas na interface.

Falha de contrato também é falha real quando `core/API_ENGINEERING.md` exigir governança: contrato inválido, implementação divergente, breaking change não tratada ou endpoint protegido sem prova de autorização impedem conclusão proporcional.

Falha de Independent Verification também é real quando o check estiver `required`: scanner/teste falhou, não executou ou encontrou finding bloqueante. `advisory` permanece informação até existir política estável; `exception` precisa ser explícita e versionada.

## Handoff entre agentes

Aponte para repositório/branch/PR, `PROJECT_STATE.md`, `.factory/state.json` quando versionado, Issue/bloco funcional e critérios de conclusão. Inclua nível do sistema e decisões de persistência/identidade/recovery quando relevantes. Quando houver API `contract`/`governed`, inclua modo, contrato autoritativo e baseline de compatibilidade. Quando semantic depth for `domain`/`formal`, inclua `specs/semantic-assurance.json`, `SEMANTICS.md` quando existir, erros/perguntas abertas e baseline/diff relevante. Quando Independent Verification estiver acima de `baseline`, inclua `VERIFICATION.md`, checks `required/advisory`, ambiente seguro de teste e exceções relevantes. Quando Semantic Verification se aplicar, inclua `specs/semantic-contract.json`, `specs/verification-plan.json` e o review evidence atual. Não use transcrição integral de conversa como mecanismo principal de continuidade.
