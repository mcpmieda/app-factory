# Portability

A App Factory pertence ao repositório, não a um modelo específico.

## Núcleo neutro

Estes elementos devem continuar independentes do agente:

- princípios;
- workflow;
- risco;
- Definition of Done;
- Skills no padrão aberto quando possível;
- Context/Autonomy/Execution/Learning contracts;
- System Engineering, API Engineering, Semantic Assurance e Independent Verification contracts;
- Semantic Verification e seus artefatos;
- templates;
- scripts;
- testes;
- Issues/PRs/Git;
- documentação de produto e arquitetura.

## APIs e contratos

Quando uma interface precisar de contrato formal, prefira padrões abertos e versionáveis adequados ao protocolo, como OpenAPI, GraphQL SDL, Protobuf, AsyncAPI ou Arazzo, sem obrigar um provedor comercial específico.

Ferramentas como Redocly CLI, oasdiff, Schemathesis e Pact são defaults condicionais da Factory porque produzem gates executáveis, mas podem ser substituídas por equivalentes quando o projeto tiver razão técnica registrada. O comportamento exigido pelo contrato importa mais que o fornecedor da ferramenta.

Não amarre a correção de uma API a consulta online em tempo de CI quando o contrato, ruleset e ferramentas puderem ser versionados/reproduzidos localmente.

## Semantic Assurance portátil

`core/SEMANTIC_ASSURANCE.md` pertence ao núcleo e não depende de uma IA, solver ou model checker específico.

A parte determinística do engine usa artefatos JSON versionáveis, IDs estáveis, fingerprints e regras de consistência reproduzíveis. Quando a profundidade for `scenario`, nenhum runtime adicional é obrigatório. Para `domain`, o próprio engine stdlib cobre estrutura, referências, cobertura e semantic diff.

Métodos formais são adapters condicionais, não lock-in:

- Z3/SMT para restrições/satisfatibilidade;
- Alloy para relações/cardinalidades;
- NASA FRET/FRETish para temporal/reactivo;
- P ou Quint/TLA+ para estado/concorrência/distribuído;
- DMN para decisões;
- OPA/Rego ou Cedar para policy/autorização.

Ferramenta equivalente gratuita/open source pode substituir um default quando preservar a propriedade/prova esperada. Formalização obrigatória precisa registrar `source_refs`, artefato e gate; uma IA não pode substituir execução real da ferramenta por uma afirmação textual.

`specs/semantic-assurance.json` é o artefato portátil principal para `domain`/`formal`; `SEMANTICS.md` contém apenas decisões/limites específicos do projeto. Coverage continua sendo estrutural, não “percentual de verdade”.

## Independent Verification portátil

`core/INDEPENDENT_VERIFICATION.md` também pertence ao núcleo, não ao GitHub, Codex ou a um fornecedor de scanner.

A matriz é `free-only` por padrão e prefere ferramentas open source executáveis localmente/CI:

- Trivy;
- Semgrep Community Edition;
- StrykerJS/mutmut;
- Schemathesis;
- OWASP ZAP;
- axe-core + Playwright;
- Lighthouse CI.

Esses nomes são defaults, não lock-in. Ferramenta gratuita equivalente pode substituir um default se preservar a classe de evidência e a decisão ficar registrada.

GitHub Actions é o executor preferido quando disponível porque oferece ambiente limpo e reproduzível, mas um runner próprio, outro CI ou execução local equivalente podem produzir a mesma evidência. A correção do projeto não pode depender de comprar minutos, SaaS comercial ou segunda IA paga.

Workflows/configs devem:

- fixar versões/commits quando usados como gate;
- manter permissões mínimas;
- evitar secrets em forks;
- usar alvo efêmero/autorizado para fuzz/DAST;
- produzir relatórios portáveis quando possível;
- distinguir `required`, `advisory`, `not-applicable` e `exception`.

## Adaptadores

### Codex

`AGENTS.md` deve funcionar como mapa do projeto e apontar para as Skills e documentos relevantes.

### Claude Code

Quando necessário, criar `CLAUDE.md` curto que aponte para o mesmo núcleo e Skills, evitando duplicar as regras.

### Cursor/outros

Criar regras/adaptadores mínimos apenas quando o cliente exigir formato próprio.

## Regra contra divergência

Nunca manter cópias completas e independentes das mesmas regras em `AGENTS.md`, `CLAUDE.md`, `.cursor/rules` etc. Os adaptadores devem apontar para uma fonte comum.

A mesma regra vale para API governance, Semantic Assurance e Independent Verification: não duplicar toda `core/API_ENGINEERING.md`, `core/SEMANTIC_ASSURANCE.md` ou `core/INDEPENDENT_VERIFICATION.md` em perfis, templates ou projetos. Esses arquivos registram somente decisões locais e apontam para o contrato comum.

## Estado do trabalho

O handoff durável entre agentes usa GitHub:

`repo + branch/PR + PROJECT_STATE + Issue + testes`.

Memória ou histórico de chat pode complementar, mas não é a fonte de verdade.

Quando houver API `contract`/`governed`, inclua também a fonte de verdade do contrato e a baseline/decisão de compatibilidade necessária para retomar com segurança.

Quando semantic depth for `domain`/`formal`, inclua `semantic-contract.json`, `semantic-assurance.json`, semantic diff/baseline relevante e formalizações `required` quando existirem. Outro agente deve conseguir reproduzir a análise sem a conversa anterior.

Quando Independent Verification estiver acima de `baseline`, inclua `VERIFICATION.md`/workflow, modo, checks `required/advisory`, alvo seguro e exceções. Outro agente deve conseguir reproduzir a matriz sem conhecer a conversa anterior.

## Dados operacionais locais

A V1.3 diferencia continuidade durável de otimização local:

- `.factory/context/` — cache regenerável;
- `.factory/execution.json` — histórico bounded da execução local;
- `.factory/learning.json` — aprendizado técnico local allowlisted;
- `.factory/state.json` — pode ser versionado em handoffs importantes quando útil.

Context/execution/learning ficam fora do Git por padrão. Portanto, ao trocar de computador, um agente pode não receber o histórico aprendido. Isso não bloqueia o projeto: a Factory volta para o roteamento baseline seguro da Execution Fabric e aprende novamente a partir de novas execuções.

O Learning Engine é otimização e nunca requisito para correção, segurança ou continuidade. Da mesma forma, a ausência de um fornecedor específico de scanner/solver não reduz automaticamente os gates: use ferramenta/runner equivalente ou registre indisponibilidade/exceção conforme o contrato; nunca marque como `pass` por conveniência.
