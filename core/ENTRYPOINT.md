# Universal Entrypoint

A App Factory deve ser acionada pelo objetivo do usuário, sem exigir que ele diga explicitamente "use a App Factory".

## Quando ativar

Ative o `factory-router` sempre que o pedido envolver criar, construir, projetar, melhorar, modernizar, manter, corrigir, automatizar, integrar, migrar ou continuar software, incluindo:

- aplicação web;
- sistema administrativo;
- site;
- API/backend;
- extensão de navegador;
- automação/script/integração;
- ferramenta interna;
- app mobile/desktop;
- projeto existente no GitHub.

Também ative quando o usuário expressar apenas o resultado, por exemplo:

- "Quero criar um sistema de patrimônio para a escola."
- "Quero um site para a secretaria."
- "Melhore este painel administrativo."
- "Quero automatizar este processo."
- "Continue o projeto X."

O usuário não precisa conhecer stack, arquitetura, perfis, Skills, estados internos, semantic-spec, semantic depth, scanners ou agentes.

## Primeira passagem obrigatória

1. Entenda o resultado real pretendido.
2. Determine se é projeto novo, evolução, manutenção, bug, automação ou pesquisa técnica.
3. Se existir repositório/projeto, recupere primeiro o estado versionado (`AGENTS.md`, `PROJECT_STATE.md`) e use o Context Engine para mapear/atualizar o contexto incremental quando disponível.
4. Classifique **três eixos independentes** antes de fechar arquitetura: escala (`core/PROJECT_SCALE.md`), risco (`core/RISK_MODEL.md`) e nível do produto (`core/SYSTEM_ENGINEERING.md`).
5. Se o produto for `persistent-app` ou superior, registre a fonte autoritativa dos dados e impeça que `localStorage`, mocks, arrays locais ou JSON estático sejam tratados como persistência final compartilhada.
6. Se o produto for `multi-user-system` ou superior, derive explicitamente necessidades de backend/server-side, banco compartilhado, identidade, autorização, validação server-side, migrations e recuperação proporcional antes de escolher uma arquitetura simplificada.
7. Determine se existe uma fronteira de API/integração relevante. Quando existir, aplique `core/API_ENGINEERING.md` e classifique a governança da interface como `none`, `lightweight`, `contract` ou `governed`. Não crie API formal/OpenAPI apenas porque existe backend.
8. Para API `contract`/`governed`, identifique consumidores, protocolo e fonte de verdade machine-readable antes de consumidores dependerem de comportamento implícito; carregue `api-engineering` quando houver trabalho de interface/integração a executar.
9. Classifique se o trabalho exige Semantic Verification:
   - **sim** para funcionalidade nova, bugfix relevante, regra de negócio, contrato de dados/API ou mudança estrutural de médio/alto risco;
   - **não por padrão** para documentação/chore e refactor pequeno que não muda comportamento observável.
10. Quando Semantic Verification for necessária, derive o **semantic depth** com `core/SEMANTIC_ASSURANCE.md`:
   - `scenario` quando uma spec pequena com invariantes + `given/when/then` é suficiente;
   - `domain` quando conceitos, relações, papéis, estados, decisões ou regras interagem e interpretação divergente é risco material;
   - `formal` somente quando temporalidade, concorrência/distribuição, safety/liveness, combinatória de regras ou criticidade justificarem métodos formais.
11. Para `domain`/`formal`, carregue `semantic-assurance`, materialize `specs/semantic-assurance.json` e exija consistência/referências/cobertura estrutural válidas antes da implementação. Métodos como Z3, Alloy, NASA FRET, P, Quint/TLA+, DMN, OPA/Rego ou Cedar são selecionados pelo tipo de problema; não são dependências universais.
12. Derive o modo de `core/INDEPENDENT_VERIFICATION.md` a partir do risco, nível do sistema, API mode e sinais técnicos do projeto. Use `baseline`, `independent`, `adversarial` ou `release` sem pedir ao usuário para escolher scanners. Carregue `independent-verification` somente quando o modo ficar acima de `baseline`.
13. Se existir `.factory/state.json`, use o Autonomy Engine para retomar. Se não existir, inicialize/infera o objetivo; quando a classificação anterior exigir prova semântica, crie o novo estado com `require_spec` sem perguntar ao usuário por essa decisão técnica.
14. Verifique `profiles/` e selecione um perfil validado quando o produto corresponder claramente; não force perfil quando nenhum servir. Nenhum perfil pode reduzir requisitos mínimos de `core/SYSTEM_ENGINEERING.md`, `core/API_ENGINEERING.md`, `core/SEMANTIC_ASSURANCE.md` nem `core/INDEPENDENT_VERIFICATION.md` quando estes se aplicarem.
15. Quando Semantic Verification se aplicar, carregue `semantic-verification` e materialize o contrato estruturado antes da implementação. Em `domain`/`formal`, a qualidade da especificação é validada por Semantic Assurance antes de tratá-la como alvo pronto.
16. Escolha o executor com `core/TASK_ROUTER.md`, priorizando as capacidades do agente atual + GitHub/CI antes de handoff. Para verificadores independentes/formais determinísticos, prefira `github_ci` ou runner gratuito/equivalente capaz.
17. Carregue apenas as demais Skills necessárias.
18. Pesquise solução existente antes de construir equivalente do zero quando houver ganho real.
19. Defina o próximo bloco funcional completo e, quando aplicável, seus critérios `given/when/then` antes do código.
20. Execute imediatamente tudo que o ambiente atual permitir com segurança e continue o loop técnico sem pedir ao usuário o próximo passo rotineiro.

## Contexto incremental

`core/CONTEXT_ENGINE.md` define o mapa de repositório. O mapa é cache de navegação; arquivos reais e GitHub continuam sendo autoridade.

Ao retomar um projeto existente:

- atualize o mapa;
- leia primeiro o resumo compacto;
- abra em detalhe apenas os arquivos relevantes;
- se o fingerprint tiver mudado durante uma fase ativa, reconcilie o delta antes de continuar.

O grafo atual de imports é deliberadamente leve. Não fingir que ele é um call graph semântico universal; análises profundas devem ser promovidas somente após pilotos por stack/linguagem.

`engine/semantic_assurance.py` mantém apenas o grafo semântico explícito que o projeto declarou por IDs/referências. Ele não inventa um call graph completo do código.

## Autonomia

`core/AUTONOMY_ENGINE.md` define a máquina de estados. O agente deve avançar por contexto, planejamento, especificação quando aplicável, implementação, verificação, reparo, revisão e entrega até concluir ou encontrar bloqueio real.

Não devolva ao usuário perguntas como "quer que eu continue?", "qual o próximo passo?" ou escolhas técnicas rotineiras quando o engine/agente puder decidir com segurança.

## Engenharia de sistemas

`core/SYSTEM_ENGINEERING.md` separa página/site, app local, app persistente, sistema multiusuário, sistema de produção e sistema crítico.

A classificação é por comportamento esperado, não pela palavra usada no pedido. Exemplos de sinais que elevam a arquitetura:

- dados institucionais compartilhados entre computadores;
- usuários com papéis diferentes;
- necessidade de histórico, autoria ou permissões;
- dados que não podem depender do armazenamento de um navegador;
- operação real de uma organização.

Para `multi-user-system` ou superior, interface funcional sozinha não prova completude. A arquitetura e os testes precisam cobrir a camada real de persistência, regras server-side e autorização aplicáveis.

## Engenharia de APIs

`core/API_ENGINEERING.md` é condicional e independente do nível do produto: ele governa a **interface**, não decide sozinho a arquitetura inteira.

Aplique quando existir API compartilhada, integração externa, múltiplos consumidores, webhook, evento/mensageria ou contrato de rede que precise evoluir com segurança. Para uma função/server action interna sem consumidor independente, mantenha o modo leve ou `none`.

Quando a interface for `contract`/`governed`, preserve uma fonte de verdade machine-readable adequada ao protocolo e gates proporcionais de lint, compatibilidade, runtime e segurança. OpenAPI, GraphQL, gRPC/Protobuf, AsyncAPI e Arazzo são opções condicionais, não tecnologias obrigatórias universais.

## Semantic Assurance

`core/SEMANTIC_ASSURANCE.md` governa a qualidade da especificação **antes** de a implementação ser usada como objeto de prova.

Profundidades:

- `scenario` — invariantes + critérios observáveis normalmente bastam;
- `domain` — acrescenta requisitos estruturados, vocabulário, entidades/relações, estados/restrições, consistency/coverage e semantic diff;
- `formal` — acrescenta uma técnica formal específica quando custo de erro/natureza do problema justificarem.

Em `domain`/`formal`, `specs/semantic-assurance.json` deve apontar para o fingerprint do `semantic-contract.json`. Referência quebrada, contradição determinística ou pergunta `blocking` impede a fase de especificação de ficar ready.

Análise por IA pode sugerir ambiguidade, lacuna ou pressuposto, mas findings probabilísticos não viram automaticamente falha formal. Quando necessário, uma decisão humana/domain owner resolve a ambiguidade.

Semantic coverage mede rastreabilidade estrutural, não “percentual de verdade”. 100% de cobertura não prova que a intenção humana foi modelada corretamente.

## Verificação independente

`core/INDEPENDENT_VERIFICATION.md` governa **evidência técnica independente do raciocínio da IA implementadora**.

Ela não adiciona outra IA paga. Por padrão é `free-only` e usa ferramentas open source/determinísticas executáveis em GitHub Actions, runner próprio ou ambiente equivalente.

Modos:

- `baseline` — alteração/projeto simples, sem scanners pesados por checklist;
- `independent` — adiciona verificadores independentes de baixo/médio custo quando aplicáveis;
- `adversarial` — adiciona mutation testing, fuzz/property testing, DAST e outras tentativas de quebrar sistemas/APIs de maior risco quando houver pré-condições;
- `release` — amplia a matriz em release de produção/alto impacto.

A matriz pode escolher, conforme stack/risco, Trivy, Semgrep Community Edition, StrykerJS/mutmut, Schemathesis, OWASP ZAP, axe-core + Playwright e Lighthouse CI. Ferramenta equivalente gratuita pode substituir um default quando tecnicamente melhor.

Regras fortes:

- scanner não executado/indisponível não conta como `pass`;
- DAST ativo/fuzz destrutivo nunca aponta para produção por inferência;
- ferramentas de CI usam versões/commits reproduzíveis e permissões mínimas;
- projetos simples não recebem toda a matriz;
- esses motores não contam como `independent-agent` semântico: eles não entendem sozinhos a intenção do produto.

## Prova semântica

`core/SEMANTIC_VERIFICATION.md` define quando a intenção precisa virar alvo estruturado e verificável.

Quando aplicável:

- `specs/semantic-contract.json` define objetivo, invariantes e critérios observáveis;
- `specs/semantic-assurance.json` complementa o contrato em profundidade `domain`/`formal`;
- `specs/verification-plan.json` liga cada critério `must` a evidência executável/gate real;
- risco médio/alto exige revisão desacoplada, preferencialmente outro agente/contexto ou, na ausência, um `clean-context` baseado em spec + diff + evidências atuais;
- `specs/review-evidence.json` fica ligado por fingerprints àquilo que foi realmente revisado;
- código/spec/plano alterados depois tornam a revisão anterior stale;
- semantic diff material exige rever ACs/invariantes/gates impactados.

Deterministic CI, formal methods e Independent Verification continuam evidências importantes, mas não são sozinhos reviewers semânticos para risco médio/alto.

## Regra de perfis

Perfis transformam evidência real em defaults condicionais. Eles não substituem entendimento do produto, `core/SYSTEM_ENGINEERING.md`, `core/API_ENGINEERING.md`, `core/SEMANTIC_ASSURANCE.md` nem `core/INDEPENDENT_VERIFICATION.md` quando aplicáveis.

Exemplo: um sistema de patrimônio com login, CRUD, filtros e dashboard provavelmente corresponde a `profiles/web-admin/PROFILE.md`. A Factory pode usar os defaults comprovados desse perfil e deve ativar persistência, autenticação/autorização, API/integração, Semantic Assurance ou verificadores independentes quando o nível do sistema, risco e produto exigirem.

Requisitos específicos do projeto têm precedência sobre defaults do perfil, salvo conflito de segurança ou redução indevida dos requisitos mínimos do nível de sistema/interface/verificação.

## Regra de GitHub

### Projeto novo

A Factory instalada já contém suas regras; não é necessário abrir o repositório `app-factory` a cada pedido apenas para reaprender o método.

Quando o projeto ganhar repositório próprio, grave nele pelo menos:

- `AGENTS.md` com vínculo explícito à App Factory;
- `PROJECT_STATE.md`;
- `.factory/state.json` em handoffs importantes quando o runtime estiver em uso;
- artefatos de produto/arquitetura proporcionais à escala;
- nível de sistema e fonte autoritativa dos dados quando `persistent-app` ou superior;
- modo/fonte de verdade da API quando `contract`/`governed` se aplicar;
- `specs/semantic-contract.json` quando Semantic Verification se aplicar;
- `specs/semantic-assurance.json` e `SEMANTICS.md` quando semantic depth for `domain`/`formal`;
- `VERIFICATION.md` e workflows/configs de verificação quando Independent Verification ficar acima de `baseline`;
- perfil selecionado e desvios relevantes quando aplicável;
- testes/CI quando aplicáveis.

O cache `.factory/context/` é regenerável e normalmente não deve ser versionado.

### Projeto existente

O repositório do projeto é a fonte de verdade. Não reconstrua contexto somente a partir de memória de chat quando o estado real puder ser lido no GitHub.

Se o `AGENTS.md` do projeto indicar App Factory, use o plugin/Skills instalados e as regras locais em conjunto. Regras locais específicas do projeto têm precedência sobre defaults genéricos, salvo conflito de segurança.

## Regra de interação

Não pergunte ao usuário qual framework, ORM, linter, biblioteca, protocolo, solver, model checker, scanner ou modo interno de verificação usar quando isso for uma decisão técnica rotineira que o agente consegue avaliar.

Pergunte quando faltar:

- regra de negócio;
- prioridade de produto;
- preferência subjetiva relevante;
- orçamento/custo;
- autorização de risco;
- credencial ou dado externo indisponível;
- decisão legal/organizacional.

Ferramenta paga é uma decisão de custo e nunca entra por inferência. Independent Verification permanece gratuita por padrão; métodos semânticos/formais preferem ferramentas gratuitas/open source quando equivalentes adequados existirem.

## Saída da primeira passagem

O agente deve saber, mesmo que não exponha todos os detalhes:

- modo do trabalho;
- escala;
- **nível do sistema**;
- fonte autoritativa dos dados quando aplicável;
- modo de governança da API e contrato autoritativo quando aplicável;
- se Semantic Verification é exigida;
- **semantic depth** (`scenario`/`domain`/`formal`) quando aplicável;
- modo de Independent Verification e checks `required/advisory` quando acima de `baseline`;
- perfil selecionado, se houver;
- risco;
- fingerprint/contexto atual;
- fase e próxima ação do Autonomy Engine;
- Skill(s) necessárias;
- executor recomendado;
- evidência que definirá conclusão.

Para o usuário, explique somente o necessário e faça o máximo possível antes de devolver uma ação manual.

## Handoff

Quando uma fase realmente precisar mudar de executor, deixe estado no GitHub e forneça uma instrução curta baseada em Issue/PR/branch. O usuário não deve copiar a conversa inteira.
