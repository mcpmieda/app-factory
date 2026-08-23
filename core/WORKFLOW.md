# Universal Workflow

## Loop autônomo

Quando o runtime estiver disponível, o fluxo operacional padrão é:

`resume/context → next → agir → registrar evento → next → ... → done`

O usuário não conduz transições técnicas. O Autonomy Engine escolhe a próxima fase e o Context Engine evita releitura integral desnecessária.

Para trabalho funcional relevante, o fluxo inclui uma etapa semântica explícita:

`planning → specification → implementation → verification → review → delivery`

A etapa `specification` usa `core/SEMANTIC_VERIFICATION.md`. Ela é proporcional: não aplicar contrato formal pesado a documentação/chore ou refactor pequeno sem mudança observável.

A arquitetura do produto também deve respeitar `core/SYSTEM_ENGINEERING.md`: a Factory pode manter processo leve, mas não pode substituir persistência compartilhada/servidor/autorização necessários por uma demo local apenas para reduzir trabalho.

Quando houver API/integração relevante, `core/API_ENGINEERING.md` entra como contrato especializado da interface. Ele não cria uma fase paralela obrigatória: suas decisões de protocolo, contrato, compatibilidade, segurança e gates são incorporadas a planejamento/especificação/verificação na profundidade necessária.

`core/INDEPENDENT_VERIFICATION.md` também não cria uma fase paralela universal. Ele aprofunda a fase de **verification** quando risco, nível do sistema, API ou release justificarem evidência externa ao raciocínio implementador. Projetos simples permanecem `baseline`.

## Projeto novo

1. Descoberta — entender problema, usuários e resultado desejado.
2. Pesquisa — verificar soluções, repositórios, bibliotecas e padrões existentes.
3. Produto — consolidar fluxos, escopo e critérios de sucesso.
4. Classificação arquitetural — aplicar `core/SYSTEM_ENGINEERING.md`, registrar nível do produto e, para `persistent-app` ou superior, fonte autoritativa dos dados; para `multi-user-system` ou superior, derivar backend/server-side, persistência compartilhada, identidade/autorização, validação, migrations e recovery proporcionais.
5. Classificação da interface — se existir API, integração, webhook, evento ou contrato compartilhado, aplicar `core/API_ENGINEERING.md`, escolher `none`/`lightweight`/`contract`/`governed`, consumidores, protocolo e fonte de verdade; não formalizar API sem necessidade real.
6. Classificação da prova independente — aplicar `core/INDEPENDENT_VERIFICATION.md` a risco + nível de sistema + API mode + sinais técnicos, escolher `baseline`/`independent`/`adversarial`/`release` e planejar apenas checks gratuitos/open source tecnicamente aplicáveis.
7. Especificação semântica — para trabalho funcional relevante, materializar objetivo, invariantes e critérios `given/when/then` antes do código. Quando houver API formal, o contrato machine-readable da interface e a spec semântica se complementam sem se duplicar.
8. Arquitetura — escolher stack proporcional ao problema e suficiente ao nível de sistema, sem tratar demo/localStorage/mock como arquitetura final compartilhada quando o produto exigir persistência real; interfaces e verificadores devem seguir os modos decididos.
9. Bootstrap — criar projeto a partir do starter/template mais adequado. Copiar templates/gates de API ou Independent Verification somente quando realmente exigidos.
10. Construção — implementar por blocos funcionais completos, mantendo contrato e implementação da API no mesmo bloco quando aplicável.
11. Verificação — derivar rastreabilidade da spec, executar testes estáticos/comportamento/browser e provar cada critério `must` aplicável; para sistemas persistentes/multiusuário, exercitar também persistência e autorização reais ou ambiente equivalente; para APIs `contract`/`governed`, executar gates proporcionais; para Independent Verification acima de `baseline`, executar a matriz `required/advisory` selecionada em GitHub CI/runner equivalente.
12. Reparação — quando houver falha, corrigir e reverificar com limite explícito de tentativas. Scanner não executado não vira sucesso.
13. Revisão — preferir segundo agente/contexto independente; quando indisponível, usar clean-context review limitado a spec + conteúdo/evidências atuais. Mudanças de contrato devem incluir o contrato/diff relevante no pacote de revisão. Scanners determinísticos são evidência complementar, não reviewer semântico.
14. Entrega — PR/merge/deploy somente com checks, arquitetura, contratos, Independent Verification exigida e review evidence atuais.
15. Aprendizado — atualizar Factory somente quando surgir padrão realmente reutilizável.

Use `TASK_ROUTER.md` para escolher a rota de execução mais leve e verificável, priorizando current-agent + GitHub/CI antes de handoff local. Independent Verification prefere GitHub CI quando ele consegue executar os gates sem custo não autorizado.

## Projeto existente

1. executar/interpretar `resume` quando o runtime estiver disponível;
2. recuperar `PROJECT_STATE.md`, `VERIFICATION.md` quando existir e estado Git;
3. atualizar o Context Engine e reconciliar delta se o fingerprint mudou;
4. identificar baseline seguro;
5. entender escopo e impacto;
6. confirmar se o nível de sistema e a fonte autoritativa dos dados continuam coerentes com `core/SYSTEM_ENGINEERING.md`, sobretudo quando a evolução transforma demo/local app em sistema persistente ou multiusuário;
7. se houver API/integração relevante, confirmar se o modo de governança, consumidores e fonte de verdade continuam coerentes com `core/API_ENGINEERING.md`, principalmente antes de alteração potencialmente incompatível;
8. recalcular Independent Verification quando risco, nível do sistema, API, autenticação/dependências/UI ou condição de release mudarem; não manter `baseline` apenas porque o projeto começou simples;
9. decidir se a mudança altera comportamento/regra/contrato o suficiente para exigir Semantic Verification;
10. quando exigir, atualizar a spec antes da implementação e regenerar a rastreabilidade afetada;
11. para contrato machine-readable, atualizar o contrato no mesmo bloco da implementação e comparar breaking changes quando aplicável;
12. revisar diff e dependências diretas;
13. preservar comportamento fora do escopo e compatibilidade prometida a consumidores;
14. testar o que mudou e regressão diretamente relacionada;
15. executar os checks independentes selecionados e registrar findings/exceções proporcionais;
16. reparar automaticamente falhas verificadas dentro do limite configurado;
17. ampliar auditoria apenas quando risco ou extensão justificarem;
18. fazer revisão desacoplada quando exigida e registrar novo estado confiável.

## Tamanho do trabalho

Evite microtarefas artificiais e missões gigantes sem critérios verificáveis. Prefira uma fatia vertical completa, como `gerenciamento de usuários = listagem + busca + criação + edição + validação + persistência + estados + testes`.

Para sistema multiusuário, uma fatia só é vertical de verdade quando atravessa UI + regras server-side + persistência + autorização aplicável, e não apenas quando a tela simula o fluxo.

Se a fatia atravessar uma API formal, ela também inclui contrato + implementação + compatibilidade/gates aplicáveis; entregar apenas endpoint ou apenas spec não completa o comportamento.

Se a fatia tiver checks independentes `required`, ela só fecha quando esses checks também executarem ou houver exceção explícita aceitável. Mutation/SAST/DAST/fuzz não são acrescentados quando não houver pré-condição real.

Critérios verificáveis devem nascer da intenção/spec, não somente depois de o agente ver o que implementou.

## Falha e estagnação

Não repita indefinidamente a mesma correção. O Autonomy Engine usa repair loop limitado (default 3). Ao atingir o limite:

1. registre o bloqueio técnico;
2. mude estratégia/modelo/executor quando possível;
3. só envolva o usuário se existir decisão humana real ou se nenhum executor disponível conseguir prosseguir com segurança.

Falha semântica (critério `must` não provado ou review stale) é falha real de verificação, mesmo que build e testes genéricos estejam verdes.

Falha arquitetural também é falha real: um sistema classificado acima de `local-app` não pode ser entregue como produção se a fonte autoritativa ainda estiver apenas no navegador ou se regras obrigatórias de acesso existirem apenas na interface.

Falha de contrato também é falha real quando `core/API_ENGINEERING.md` exigir governança: contrato inválido, implementação divergente, breaking change não tratada ou endpoint protegido sem prova de autorização impedem conclusão proporcional.

Falha de Independent Verification também é real quando o check estiver `required`: scanner/teste falhou, não executou ou encontrou finding bloqueante. `advisory` permanece informação até existir política estável; `exception` precisa ser explícita e versionada.

## Handoff entre agentes

Aponte para repositório/branch/PR, `PROJECT_STATE.md`, `.factory/state.json` quando versionado, Issue/bloco funcional e critérios de conclusão. Inclua também nível do sistema e decisões de persistência/identidade/recovery quando relevantes. Quando houver API `contract`/`governed`, inclua modo, contrato autoritativo e baseline de compatibilidade relevante. Quando Independent Verification estiver acima de `baseline`, inclua `VERIFICATION.md`, checks `required/advisory`, ambiente seguro de teste e exceções relevantes. Quando Semantic Verification se aplicar, inclua `specs/semantic-contract.json`, `specs/verification-plan.json` e o review evidence atual. Não use transcrição integral de conversa como mecanismo principal de continuidade.
