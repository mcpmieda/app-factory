# App Factory — Plano consolidado

## Visão

Manter um sistema operacional portátil de desenvolvimento com IA que transforma intenção em software funcional, recuperável e verificável, com pouca intervenção manual do usuário e sem depender de um agente ou fornecedor específico.

## Problemas que a Factory deve resolver

- projetos começando do zero sem padrão;
- contexto perdido entre chats, computadores e agentes;
- excesso de microtarefas e cliques;
- código criado sem teste real ou sem provar a intenção;
- demos locais apresentadas como sistemas completos;
- APIs criadas sem contrato, compatibilidade ou segurança proporcional;
- bibliotecas e componentes reinventados;
- interfaces genéricas ou inconsistentes;
- uso desnecessário de executores pesados para tarefas simples;
- dificuldade para recuperar uma versão segura;
- regras importantes existindo apenas em documentação manual;
- divergência entre documentação, arquitetura, contratos e implementação.

## Arquitetura atual da Factory

A Factory é composta por camadas complementares com responsabilidades separadas:

1. **Core** — princípios, interação humana, escala, risco, workflow, Definition of Done e contratos transversais.
2. **System Engineering** — classifica a profundidade mínima da arquitetura do produto e impede falsa persistência/completude.
3. **API Engineering** — governa APIs, integrações, eventos e webhooks somente quando existe uma fronteira real, com contrato e gates proporcionais.
4. **Context Engine** — recupera o repositório incrementalmente sem substituir arquivos reais como fonte de verdade.
5. **Autonomy Engine** — mantém estado e calcula a próxima ação técnica.
6. **Semantic Verification** — transforma intenção funcional relevante em critérios observáveis, rastreabilidade e revisão desacoplada.
7. **Execution Fabric** — escolhe executor por capacidade/disponibilidade e usa CI para prova determinística quando adequado.
8. **Learning Engine** — otimiza decisões localmente somente com evidência técnica allowlisted, sempre subordinado aos gates.
9. **Skills** — conhecimento especializado carregado sob demanda.
10. **Profiles/starters/templates** — defaults comprovados e estruturas reutilizáveis, sem congelar uma stack universal.
11. **UI system** — política de design system, Living UI e Semantic Motion.
12. **Scripts/CI** — guardrails executáveis e regressão.
13. **Research/audits** — evidência para promover novos padrões à Factory.

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
      └── SEMANTIC_VERIFICATION
          critérios → evidência → revisão

entrega
      └── DEFINITION_OF_DONE
          confirma que os gates aplicáveis passaram
```

Nenhuma camada deve copiar integralmente a responsabilidade da outra.

## Estratégia de execução

Não existe divisão fixa “ChatGPT faz X / Codex faz Y”. A Execution Fabric decide por capacidade:

1. `current_agent` quando possui as capacidades necessárias;
2. `github_ci` para prova determinística/headless quando adequado;
3. `sandbox` quando disponível e suficiente;
4. `local_full` quando browser/runtime/debug/migrations interativos ou outra capacidade local forem realmente necessários.

Codex pode ser um executor `local_full`, mas não é dependência arquitetural. Claude Code, Cursor e futuros agentes continuam possíveis por adaptadores finos.

## Estratégia de arquitetura de produto

- escolher a arquitetura mais simples que satisfaça o produto real, não apenas a tela;
- `local-app` pode usar persistência local quando isso for requisito legítimo;
- `persistent-app` ou superior exige fonte autoritativa durável adequada;
- `multi-user-system` ou superior exige compartilhamento/server-side, autorização e validação proporcionais quando aplicáveis;
- produção/criticidade elevam recovery, observabilidade, auditoria, segurança e rollout conforme risco;
- perfis fornecem defaults, mas não podem reduzir os contratos centrais.

## Estratégia de APIs e integrações

- não criar API formal somente porque existe backend;
- classificar governança como `none`, `lightweight`, `contract` ou `governed`;
- para `contract`/`governed`, usar uma fonte de verdade machine-readable adequada ao protocolo;
- HTTP/OpenAPI é um default forte para APIs HTTP compartilhadas, não padrão universal;
- GraphQL, gRPC/Protobuf, AsyncAPI e Arazzo entram somente quando o comportamento justificar;
- segurança usa OWASP API Security como referência de ameaça;
- integrações externas materiais recebem timeout/retry/rate-limit/idempotência/recovery proporcionais;
- compatibilidade e breaking changes viram gates quando consumidores dependem de estabilidade;
- Redocly CLI, oasdiff, Schemathesis e Pact são ferramentas condicionais/substituíveis, com versões fixadas em CI quando usadas.

## Estratégia de UI

- sistemas administrativos e dashboards: shadcn como base do perfil `web-admin`, com ReUI seletivo para componentes avançados;
- HeroUI permanece alternativa visual quando seu sistema for mais adequado;
- não misturar design systems apenas por estética;
- pesquisar componente/bloco existente antes de implementar equivalente;
- motion é transversal ao design system e segue `ui/MOTION_POLICY.md`;
- `ambient` é contextual, podendo ser atenuado para `subtle` em telas densas;
- `prefers-reduced-motion` é obrigatório para movimento não essencial.

## Estratégia de trabalho

- GitHub é a fonte técnica de verdade;
- recuperar contexto/estado antes de depender de memória de chat;
- trabalhar em fatias funcionais completas;
- em manutenção, preservar baseline e revisar diff/impacto;
- em projeto novo, evitar fragmentação artificial;
- fazer o máximo seguro antes de pedir intervenção humana;
- governança cresce proporcionalmente ao risco, sistema e custo de incompatibilidade;
- pesquisar/reutilizar antes de construir equivalente;
- transformar regras repetitivas importantes em teste, lint, policy ou CI quando houver retorno real;
- manter conhecimento durável em uma fonte comum e apontar para ela em vez de duplicá-la.

## Linha evolutiva consolidada

- **V1.0** — baseline estável, starter/pilotos, portabilidade e validação final.
- **V1.1** — Context Engine + Autonomy Engine.
- **V1.2** — Execution Fabric + CI Executor.
- **V1.3** — Learning Engine local e conservador.
- **V1.4** — Semantic Verification e revisão desacoplada.
- **Governance hardenings sobre V1.4** — System Engineering + API Engineering, sem alterar os engines nem inventar uma versão nova.

Novas capacidades só viram defaults/perfis estáveis após evidência/pilotos suficientes. Complexidade não comprovada permanece condicional.

## Critério principal de sucesso

Um usuário deve poder descrever um objetivo em linguagem simples e a Factory deve recuperar o estado, classificar arquitetura/risco/interface, escolher ferramentas e executor, implementar a maior fatia segura possível, provar o resultado e preservar continuidade — sem exigir que o usuário conheça frameworks, protocolos, Skills ou fases internas.
