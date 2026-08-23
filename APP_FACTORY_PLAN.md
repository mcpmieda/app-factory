# App Factory — Plano consolidado

## Visão

Manter um sistema operacional portátil de desenvolvimento com IA que transforma intenção em software funcional, recuperável e verificável, com pouca intervenção manual do usuário e sem depender de um agente ou fornecedor específico.

## Problemas que a Factory deve resolver

- projetos começando do zero sem padrão;
- contexto perdido entre chats, computadores e agentes;
- excesso de microtarefas e cliques;
- código criado sem teste real ou sem provar a intenção;
- especificações ambíguas, contraditórias ou incompletas tratadas como verdade apenas porque foram escritas pela IA;
- testes escritos pela mesma IA que implementou sem evidência técnica externa suficiente para risco alto;
- demos locais apresentadas como sistemas completos;
- APIs criadas sem contrato, compatibilidade ou segurança proporcional;
- bibliotecas e componentes reinventados;
- interfaces genéricas ou inconsistentes;
- uso desnecessário de executores pesados para tarefas simples;
- dificuldade para recuperar uma versão segura;
- regras importantes existindo apenas em documentação manual;
- divergência entre intenção, domínio, especificação, documentação, arquitetura, contratos, verificação e implementação.

## Arquitetura atual da Factory

A Factory é composta por camadas complementares com responsabilidades separadas:

1. **Core** — princípios, interação humana, escala, risco, workflow, Definition of Done e contratos transversais.
2. **System Engineering** — classifica a profundidade mínima da arquitetura do produto e impede falsa persistência/completude.
3. **API Engineering** — governa APIs, integrações, eventos e webhooks somente quando existe uma fronteira real, com contrato e gates proporcionais.
4. **Semantic Assurance** — verifica a qualidade da própria especificação antes da implementação, com profundidade `scenario`/`domain`/`formal`, domínio explícito, consistência, cobertura estrutural e semantic diff.
5. **Independent Verification** — seleciona, por risco/arquitetura, motores determinísticos gratuitos/open source que tentam encontrar falhas independentemente do raciocínio da IA implementadora.
6. **Context Engine** — recupera o repositório incrementalmente sem substituir arquivos reais como fonte de verdade.
7. **Autonomy Engine** — mantém estado e calcula a próxima ação técnica.
8. **Semantic Verification** — transforma intenção funcional relevante em critérios observáveis, rastreabilidade e revisão desacoplada, provando implementação contra a especificação atual.
9. **Execution Fabric** — escolhe executor por capacidade/disponibilidade e usa CI para prova determinística quando adequado; GitHub CI é o executor preferido da matriz independente/formal quando capaz.
10. **Learning Engine** — otimiza decisões localmente somente com evidência técnica allowlisted, sempre subordinado aos gates.
11. **Skills** — conhecimento especializado carregado sob demanda.
12. **Profiles/starters/templates** — defaults comprovados e estruturas reutilizáveis, sem congelar uma stack universal.
13. **UI system** — política de design system, Living UI e Semantic Motion.
14. **Scripts/CI** — guardrails executáveis e regressão.
15. **Research/audits** — evidência para promover novos padrões à Factory.

## Relação entre os contratos

```text
objetivo do produto
      │
      ├── PROJECT_SCALE ───── profundidade do processo
      ├── RISK_MODEL ─────── risco e gates adicionais
      └── SYSTEM_ENGINEERING profundidade mínima do produto
                 │
                 └── existe API/integração relevante?
                         │
                         └── API_ENGINEERING
                             contrato/protocolo/compatibilidade

intenção funcional relevante
      │
      ├── SEMANTIC_ASSURANCE
      │   qualidade da especificação
      │   scenario / domain / formal
      │   domínio → consistência → cobertura → diff
      │
      └── SEMANTIC_VERIFICATION
          critérios → evidência → revisão

risco + sistema + API + sinais técnicos
      └── INDEPENDENT_VERIFICATION
          matriz externa free-only
          required/advisory/exception

entrega
      └── DEFINITION_OF_DONE
          confirma que todos os gates aplicáveis passaram
```

Nenhuma camada deve copiar integralmente a responsabilidade da outra. Security Review continua sendo o dono do threat model; Semantic Assurance não substitui decisão humana de domínio; Independent Verification apenas transforma riscos automatizáveis em prova externa.

## Estratégia de execução

Não existe divisão fixa “ChatGPT faz X / Codex faz Y”. A Execution Fabric decide por capacidade:

1. `current_agent` quando possui as capacidades necessárias;
2. `github_ci` para prova determinística/headless, gates formais e matriz independente quando adequado;
3. `sandbox` quando disponível e suficiente;
4. `local_full` quando browser/runtime/debug/migrations interativos ou outra capacidade local forem realmente necessários.

Codex pode ser um executor `local_full`, mas não é dependência arquitetural. Claude Code, Cursor e futuros agentes continuam possíveis por adaptadores finos.

Independent Verification e métodos formais não adicionam um novo backend de raciocínio: scanners, solvers e model checkers são **gates determinísticos executados por um backend**.

## Estratégia de arquitetura de produto

- escolher a arquitetura mais simples que satisfaça o produto real, não apenas a tela;
- `local-app` pode usar persistência local quando isso for requisito legítimo;
- `persistent-app` ou superior exige fonte autoritativa durável adequada;
- `multi-user-system` ou superior exige compartilhamento/server-side, autorização e validação proporcionais quando aplicáveis;
- produção/criticidade elevam recovery, observabilidade, auditoria, segurança e rollout conforme risco;
- perfis fornecem defaults, mas não podem reduzir os contratos centrais.

## Estratégia de Semantic Assurance

- não criar um segundo documento pesado para toda funcionalidade;
- usar `scenario` quando invariantes + `given/when/then` forem suficientes;
- usar `domain` quando conceitos, relações, papéis, estados, decisões ou regras interagirem;
- usar `formal` somente quando temporalidade, concorrência/distribuição, safety/liveness, policy complexa, combinatória ou criticidade justificarem;
- em `domain`/`formal`, manter `specs/semantic-assurance.json` ligado por fingerprint ao contrato semântico;
- estruturar requisitos inspirados em EARS/FRET com scope/precondition/trigger/component/response/timing + referências, sem impor runtime Cucumber ou FRET a todo projeto;
- detectar determinísticamente referências quebradas, cardinalidades/ranges impossíveis, enum inviável, dependências contraditórias e perguntas `blocking`;
- medir cobertura somente como rastreabilidade estrutural; 100% não significa correção humana total;
- usar semantic diff por IDs/fingerprints para propagar impacto a REQ/AC/INV/gates;
- property/stateful/model-based testing entra quando invariantes/ranges/state machines justificarem exploração adicional;
- Z3/SMT, Alloy, NASA FRET/FRETish, P, Quint/TLA+, DMN, OPA/Rego e Cedar são opções condicionais conforme a natureza da propriedade;
- formalização `required` só conta como prova com artefato versionado, `source_refs` e gate executado;
- findings probabilísticos da IA permanecem hipótese/advisory até resolução estruturada, formal ou humana.

## Estratégia de APIs e integrações

- não criar API formal somente porque existe backend;
- classificar governança como `none`, `lightweight`, `contract` ou `governed`;
- para `contract`/`governed`, usar uma fonte de verdade machine-readable adequada ao protocolo;
- HTTP/OpenAPI é um default forte para APIs HTTP compartilhadas, não padrão universal;
- GraphQL, gRPC/Protobuf, AsyncAPI e Arazzo entram somente quando o comportamento justificar;
- segurança usa OWASP API Security como referência de ameaça;
- integrações externas materiais recebem timeout/retry/rate-limit/idempotência/recovery proporcionais;
- compatibilidade e breaking changes viram gates quando consumidores dependem de estabilidade;
- Redocly CLI, oasdiff, Schemathesis e Pact são ferramentas condicionais/substituíveis, com versões fixadas em CI quando usadas;
- quando API Engineering selecionar fuzz/negative/DAST como evidência, Independent Verification controla a combinação e execução segura sem duplicar o contrato.

## Estratégia de Independent Verification

- política `free-only` por padrão: nenhuma segunda IA paga ou SaaS comercial é requisito;
- classificar como `baseline`, `independent`, `adversarial` ou `release`;
- projetos simples permanecem leves e não recebem scanners empresariais por cerimônia;
- Trivy verifica supply chain/secrets/misconfiguration;
- Semgrep Community Edition fornece SAST;
- StrykerJS/mutmut fazem mutation testing seletivo e verificam força dos próprios testes;
- Schemathesis gera property/fuzz/stateful cases quando API Engineering indicar;
- OWASP ZAP faz DAST em alvo efêmero/explicitamente autorizado, nunca produção por inferência;
- axe-core + Playwright fornece evidência automatizada de acessibilidade em estados relevantes;
- Lighthouse CI detecta regressões de performance/qualidade somente quando houver baseline confiável;
- check `required` que não executou não vira `pass`;
- suppressions/exceções são pequenas, justificadas e versionadas;
- versões/commits de ferramentas/actions são fixados em CI real;
- scanner verde não significa regra de negócio correta nem segurança total; Semantic Assurance, revisão semântica e threat model permanecem separados.

## Estratégia de UI

- sistemas administrativos e dashboards: shadcn como base do perfil `web-admin`, com ReUI seletivo para componentes avançados;
- HeroUI permanece alternativa visual quando seu sistema for mais adequado;
- não misturar design systems apenas por estética;
- pesquisar componente/bloco existente antes de implementar equivalente;
- motion é transversal ao design system e segue `ui/MOTION_POLICY.md`;
- `ambient` é contextual, podendo ser atenuado para `subtle` em telas densas;
- `prefers-reduced-motion` é obrigatório para movimento não essencial;
- axe/Lighthouse/visual regression entram conforme Independent Verification/risco, não como estética obrigatória em todo projeto.

## Estratégia de trabalho

- GitHub é a fonte técnica de verdade;
- recuperar contexto/estado antes de depender de memória de chat;
- trabalhar em fatias funcionais completas;
- em manutenção, preservar baseline e revisar diff/impacto, incluindo semantic diff quando o domínio/spec mudar;
- em projeto novo, evitar fragmentação artificial;
- fazer o máximo seguro antes de pedir intervenção humana;
- governança cresce proporcionalmente ao risco, sistema e custo de incompatibilidade/ambiguidade;
- pesquisar/reutilizar antes de construir equivalente;
- transformar regras repetitivas importantes em teste, lint, policy, solver ou CI quando houver retorno real;
- manter conhecimento durável em uma fonte comum e apontar para ela em vez de duplicá-la;
- manter `SEMANTICS.md`/`semantic-assurance.json` somente para `domain`/`formal`;
- manter `VERIFICATION.md`/workflow recuperável quando a verificação independente estiver acima de `baseline`.

## Linha evolutiva consolidada

- **V1.0** — baseline estável, starter/pilotos, portabilidade e validação final.
- **V1.1** — Context Engine + Autonomy Engine.
- **V1.2** — Execution Fabric + CI Executor.
- **V1.3** — Learning Engine local e conservador.
- **V1.4** — Semantic Verification e revisão desacoplada.
- **Governance hardenings sobre V1.4** — System Engineering + API Engineering + Semantic Assurance + Independent Verification, sem alterar os engines V1.1–V1.4 nem inventar uma versão nova.

Novas capacidades só viram defaults/perfis estáveis após evidência/pilotos suficientes. Complexidade não comprovada permanece condicional.

## Critério principal de sucesso

Um usuário deve poder descrever um objetivo em linguagem simples e a Factory deve recuperar o estado, classificar arquitetura/risco/interface/semântica/verificação, escolher ferramentas e executor, melhorar a qualidade da própria especificação quando necessário, implementar a maior fatia segura possível, provar o resultado com testes primários e evidência externa proporcional, preservar continuidade e impedir que a própria IA seja a única fonte de confiança — sem exigir que o usuário conheça frameworks, protocolos, solvers, scanners, Skills ou fases internas.
