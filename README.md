# App Factory

Sistema portátil para construir e manter software com agentes de IA de forma consistente, verificável, autônoma e com mínimo trabalho manual do usuário.

## Objetivo

Transformar uma ideia em software funcional usando um método reutilizável por ChatGPT, Codex, Claude Code, Cursor ou outro agente compatível, sem tornar nenhum executor específico obrigatório.

A App Factory combina:

- entrada universal por intenção de software;
- **System Engineering Contract** para impedir que sistemas reais sejam reduzidos a demos locais e para exigir persistência/backend/segurança proporcionais;
- **API Engineering Contract** para governar APIs e integrações apenas quando elas realmente existirem, com contrato, compatibilidade, segurança e gates proporcionais;
- **Context Engine** incremental para recuperar repositórios sem releitura integral desnecessária;
- **Autonomy Engine** para calcular e registrar o próximo passo técnico;
- **Semantic Verification** para transformar intenção funcional relevante em contrato, critérios de aceite e prova rastreável antes da entrega;
- **Execution Fabric** para escolher executor por capacidade, disponibilidade e evidência;
- GitHub Actions/CI como backend real de execução determinística;
- **Learning Engine** local e conservador para melhorar escolhas futuras sem ultrapassar segurança ou Definition of Done;
- seleção automática de perfil validado quando aplicável;
- `AGENTS.md` como mapa operacional;
- Core curto e modular;
- **17 Skills** especializadas carregadas conforme a tarefa;
- templates e starters componíveis;
- Living UI / Semantic Motion quando houver interface;
- repair loop e fallback limitados;
- GitHub como fonte de verdade para continuidade.

## Experiência desejada

O usuário pode começar apenas com o resultado desejado:

> Quero criar um sistema de patrimônio para a escola.

Ele não precisa escolher framework, Skill, executor, ChatGPT/Codex, preencher uma spec técnica nem conduzir manualmente cada fase.

```text
pedido do usuário
→ recuperar contexto/estado
→ classificar escala/risco/nível do sistema
→ decidir se existe API/integração relevante e seu modo de governança
→ planejar
→ criar spec + critérios observáveis quando aplicável
→ definir contrato machine-readable quando API contract/governed exigir
→ filtrar executores por capacidade/segurança
→ consultar aprendizado local se houver evidência suficiente
→ implementar
→ CI/verificar critérios + arquitetura + contratos
→ reparar/fallback se necessário
→ revisão independente ou clean-context quando exigida
→ entregar
→ registrar resultado técnico seguro
```

O usuário volta ao loop somente quando existir decisão genuinamente humana, dado/credencial indisponível, custo ou risco relevante.

## Camada de engenharia de sistemas

`core/SYSTEM_ENGINEERING.md` classifica o produto como `website`, `local-app`, `persistent-app`, `multi-user-system`, `production-system` ou `critical-system`.

Essa classificação impede falsa persistência: um sistema compartilhado/real não pode ser tratado como pronto se seus dados autoritativos ainda estiverem apenas em `localStorage`, mocks ou JSON estático. Backend, persistência, identidade, autorização, migrations e recovery entram somente no nível que o produto real exige.

## Camada de engenharia de APIs

`core/API_ENGINEERING.md` é independente do nível do produto e só entra quando existe uma interface relevante entre sistemas/consumidores.

Modos:

- `none` — sem fronteira de API relevante;
- `lightweight` — interface interna pequena e coordenada;
- `contract` — interface compartilhada ou com evolução independente;
- `governed` — API pública/parceira/institucional/crítica ou com alto custo de incompatibilidade.

A Factory não força REST/OpenAPI em todo backend. Conforme o caso pode usar HTTP/OpenAPI, GraphQL, gRPC/Protobuf, AsyncAPI ou Arazzo. Para OpenAPI, Redocly CLI, oasdiff e Schemathesis são ferramentas preferidas de lint/compatibilidade/teste gerado quando o projeto justificar; Pact entra condicionalmente em consumer/provider contracts.

`API_ENGINEERING` define desenho/governança da interface; `SEMANTIC_VERIFICATION` prova os comportamentos; `DEFINITION_OF_DONE` exige os gates que realmente se aplicam.

## V1.1 — Context + Autonomy

`engine/context_engine.py` mantém mapa incremental com SHA-256, fingerprint, delta `added/changed/removed`, stack, símbolos e imports, excluindo segredos, builds, dependências e binários.

`engine/autonomy_engine.py` mantém `.factory/state.json`. O fluxo leve preservado é:

`context → planning → implementation → verification → repair → review → delivery → done`

Para trabalho funcional relevante na V1.4, pode incluir `specification` entre planejamento e implementação.

O repair loop é limitado e eventos fora da fase permitida são rejeitados antes de alterar o estado.

## V1.2 — Execution Fabric

`engine/execution_engine.py` transforma cada ação em capacidades necessárias. Ordem baseline:

1. `current_agent`;
2. `github_ci`;
3. `sandbox` quando disponível;
4. `local_full` quando capacidade local/interativa realmente for necessária.

Backend incapaz nunca é escolhido. Falhas da tarefa atual podem causar fallback, mas falhas antigas não contaminam tarefas novas.

`engine/ci_executor.py` usa apenas gates declarados/allowlisted, argumentos estruturados, `shell=False`, sem comandos livres de prompt e sem secrets por padrão. Instalação reproduzível exige lockfile compatível.

## V1.3 — Learning Engine

`engine/learning_engine.py` aprende somente com metadados técnicos locais e allowlisted:

- classe de ação;
- assinatura de capacidades;
- backend;
- resultado;
- duração, quando disponível;
- timestamp.

Não armazena prompt, objetivo do usuário, nomes pessoais, código, conteúdo de arquivos, summaries/logs, task keys, secrets ou URLs privadas. `.factory/learning.json` fica fora do Git por padrão e **não existe telemetria externa**.

A ordem de autoridade é:

1. capacidade;
2. disponibilidade/permissão;
3. fallback da tarefa atual;
4. segurança, risco, contratos arquiteturais/semânticos e Definition of Done;
5. aprendizado local;
6. ordem baseline.

Com pouca amostra, a Factory mantém o baseline. Com evidência suficiente, pode reordenar somente backends leves já elegíveis. `local_full` nunca é promovido sobre um backend leve capaz apenas por score histórico. A métrica de velocidade usa duração de **execuções bem-sucedidas**, portanto falhar rápido não melhora a preferência.

Se o arquivo local de aprendizado não existir em outra máquina, nada quebra: a Factory volta ao baseline seguro e aprende novamente.

## V1.4 — Semantic Verification

A V1.4 fecha a distância entre **"o código passou nos testes"** e **"o software realmente corresponde ao que foi pedido"**.

Para funcionalidade nova, bugfix relevante, regra de negócio, contrato de dados/API ou mudança estrutural de médio/alto risco, a Factory cria antes do código:

```text
specs/semantic-contract.json
```

O contrato registra objetivo, escopo, invariantes e critérios `given / when / then`. Depois:

```text
semantic-contract
→ verification-plan
→ implementação
→ gates/testes executáveis
→ review-packet (spec + diff atual)
→ independent-agent ou clean-context review
→ review-evidence
→ delivery
```

`specs/verification-plan.json` liga cada critério `must` a uma evidência executável/gate declarado. A rastreabilidade não substitui a execução real dos testes.

Para risco médio/alto, o mesmo raciocínio de implementação não pode ser a única revisão semântica: prefira outro agente/contexto; se isso não estiver disponível, use um pacote `clean-context` contendo apenas spec, diff atual e evidências verificáveis. A revisão fica amarrada por fingerprints; mudança posterior no conteúdo/spec/plano torna a aprovação anterior stale.

O processo continua proporcional: documentação, chores e refactors pequenos sem mudança observável não recebem uma spec pesada.

Visual regression entra como gate quando existe baseline visual estável e regressão visual é risco material. O Context Engine não finge possuir call graph universal; análise profunda de dependências precisa de piloto por linguagem/stack antes de virar regra estável. Typecheck/build/runtime continuam defesa principal contra APIs inexistentes, com smoke/integration test específico quando a integração for pouco tipada ou dependente de runtime.

## Comandos internos

O usuário normalmente não precisa executá-los; são a interface portátil entre agentes:

```text
python scripts/factory.py --root <projeto> context
python scripts/factory.py --root <projeto> init --goal "..." --require-spec
python scripts/factory.py --root <projeto> status
python scripts/factory.py --root <projeto> next
python scripts/factory.py --root <projeto> resume
python scripts/factory.py --root <projeto> record <evento>
python scripts/factory.py --root <projeto> spec-validate
python scripts/factory.py --root <projeto> verification-plan-init
python scripts/factory.py --root <projeto> review-packet --base main
python scripts/factory.py --root <projeto> semantic-status
python scripts/factory.py --root <projeto> route verify
python scripts/factory.py --root <projeto> route verify --no-learning
python scripts/factory.py --root <projeto> execution-status
python scripts/factory.py --root <projeto> learning-status
python scripts/factory.py --root <projeto> learning-recommend verify
python scripts/factory.py --root <projeto> gates
```

## Comece por aqui

1. `AGENTS.md` — mapa para agentes.
2. `core/ENTRYPOINT.md` — ativação por intenção.
3. `core/SYSTEM_ENGINEERING.md` — profundidade arquitetural mínima do produto.
4. `core/API_ENGINEERING.md` — governança condicional de APIs/integrações.
5. `core/CONTEXT_ENGINE.md` — recuperação incremental.
6. `core/AUTONOMY_ENGINE.md` — estado e próxima ação.
7. `core/SEMANTIC_VERIFICATION.md` — contrato, rastreabilidade e revisão semântica proporcional.
8. `core/EXECUTION_FABRIC.md` — seleção e fallback de backends.
9. `core/LEARNING_ENGINE.md` — aprendizado local, confiança e privacidade.
10. `core/TASK_ROUTER.md` — ordem de decisão do executor.
11. `skills/factory-router/SKILL.md`, `skills/api-engineering/SKILL.md`, `skills/semantic-verification/SKILL.md`, `skills/execution-router/SKILL.md` e `skills/learning-engine/SKILL.md`.
12. `profiles/README.md` e `profiles/*/PROFILE.md` — defaults condicionais comprovados.
13. `ui/UI_POLICY.md` e `ui/MOTION_POLICY.md` — interface e Living UI.
14. `core/HUMAN_INTERACTION.md` — limites da intervenção humana.
15. `core/DEFINITION_OF_DONE.md` — prova de conclusão.
16. `PORTABILITY.md` — continuidade entre agentes.
17. `docs/CODEX_PLUGIN.md` — adaptador Codex.

## Perfis

`web-admin` permanece estável (`v1`). `website`, `web-app`, `chrome-extension` e `automation` permanecem `validated`. Seus stacks de piloto são evidência, não tecnologias universais congeladas.

HeroUI continua uma alternativa visual explícita válida. Living UI / Semantic Motion é independente do design system, com `ambient` contextual e `prefers-reduced-motion` obrigatório para movimento não essencial.

## Estrutura central

```text
app-factory/
├── AGENTS.md
├── PROJECT_STATE.md
├── core/
│   ├── SYSTEM_ENGINEERING.md
│   ├── API_ENGINEERING.md
│   ├── CONTEXT_ENGINE.md
│   ├── AUTONOMY_ENGINE.md
│   ├── SEMANTIC_VERIFICATION.md
│   ├── EXECUTION_FABRIC.md
│   └── LEARNING_ENGINE.md
├── engine/
│   ├── context_engine.py
│   ├── autonomy_engine.py
│   ├── semantic_verification.py
│   ├── review_packet.py
│   ├── execution_engine.py
│   ├── ci_executor.py
│   └── learning_engine.py
├── skills/
│   └── api-engineering/
├── profiles/
├── templates/
│   ├── api/
│   └── project/API.md
├── starters/
├── ui/
├── audits/
├── research/
└── scripts/
    ├── factory.py
    ├── validate_system_engineering.py
    ├── validate_api_engineering.py
    ├── validate_v1_1.py
    ├── validate_v1_2.py
    ├── validate_v1_3.py
    └── validate_v1_4.py
```

## Decisões consolidadas

- intenção de software aciona a Factory sem palavra-chave manual;
- GitHub é a fonte técnica de verdade;
- o agente faz sozinho decisões técnicas rotineiras e grandes blocos seguros;
- System Engineering impede que demo local seja rotulada como sistema real;
- API Engineering só entra quando existe interface real e usa governança proporcional;
- contrato machine-readable é fonte de verdade para API `contract`/`governed`, sem duplicar a spec semântica;
- OpenAPI não é obrigatório para todo backend; protocolo é escolhido pelo problema;
- Context Engine reduz releitura sem substituir arquivos reais;
- Autonomy Engine decide continuidade técnica;
- trabalho funcional relevante ganha contrato semântico antes do código;
- critérios `must` precisam de rastreabilidade para gates/testes executáveis;
- risco médio/alto exige revisão semântica desacoplada, sem tornar fornecedor específico obrigatório;
- Execution Fabric escolhe por capacidade e disponibilidade;
- Learning Engine é otimização subordinada, não autoridade;
- current-agent + GitHub/CI vem antes de handoff quando fornece prova suficiente;
- Codex/local é fallback de capacidade, não centro obrigatório;
- prompt não vira shell;
- aprendizado não recebe prompt/código/log/segredo e não envia telemetria;
- falhas entram em repair/fallback limitados;
- pesquisar/reutilizar precede construir do zero;
- baseline/diff/rollback permanecem centrais em manutenção;
- teste local não substitui instalação limpa e CI reproduzível.

## Estado

Versão estável dos engines: **`1.4.0` — App Factory V1.4**.

Os hardenings de **System Engineering** e **API Engineering** evoluem a governança arquitetural sobre essa baseline sem alterar os engines V1.1–V1.4. A V1.4 continua preservando os gates V1.0–V1.3 e a prova semântica proporcional, enquanto os novos contratos impedem simplificação arquitetural indevida e APIs sem governança quando o produto realmente exigir essas capacidades.
