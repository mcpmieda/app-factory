# Semantic Assurance — research and design basis

Data da revisão: 2026-08-22.

## Objetivo

Revisar a camada semântica da App Factory contra práticas e ferramentas externas maduras antes de implementar novas ideias próprias para consistência, cobertura, diff e modelagem de domínio.

## Achados incorporados

### NASA FRET / FRETish

Fontes:

- https://github.com/NASA-SW-VnV/fret
- https://software.nasa.gov/software/ARC-18066-1
- https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20200001989.pdf

FRET é uma referência forte porque trabalha no nível exato que faltava à Factory: elicitação, estruturação, formalização e análise de requisitos. Requisitos FRETish recebem semântica não ambígua, podem ser representados em lógica temporal/diagramas, analisados por consistência/realizability e usados para gerar testes.

Decisão: incorporar os princípios de campos estruturados + formalização rastreável e permitir FRET como método condicional para requisitos temporais/reativos. Não tornar FRET dependência universal e não gerar FRETish aproximado como se fosse prova.

### EARS / Rolls-Royce + Amazon Kiro

Fontes:

- Alistair Mavin et al., Easy Approach to Requirements Syntax (EARS), IEEE RE 2009.
- https://kiro.dev/docs/specs/feature-specs/requirements-first/
- https://kiro.dev/docs/specs/analyze-requirements/

EARS reduz ambiguidade ao separar condição/contexto, gatilho, sistema e resposta. Kiro usa EARS em specs atuais e adiciona análise cruzada para inconsistências, ambiguidades, conflitos, pressupostos e edge cases.

Decisão: adotar estrutura inspirada em EARS para requisitos `domain`/`formal`, mas manter o JSON estruturado como fonte do engine. Não exigir que o usuário escreva EARS nem instalar um runtime específico.

### GitHub Spec Kit

Fontes:

- https://github.com/github/spec-kit
- https://github.github.com/spec-kit/

Spec Kit reforça spec como artefato central e possui gates de `clarify`, `checklist` e `analyze` para consistência/cobertura entre spec, plano e tarefas.

Decisão: incorporar a ideia de análise cruzada e impacto entre artefatos, mas manter a Factory mais determinística onde possível. Spec Kit depende fortemente da interpretação do agente; a Factory continuará exigindo IDs, fingerprints, referências e gates executáveis.

### Microsoft model-based testing / P

Fontes:

- https://learn.microsoft.com/en-us/archive/msdn-magazine/2013/december/model-based-testing-an-introduction-to-model-based-testing-and-spec-explorer
- https://www.microsoft.com/en-us/research/project/model-based-testing-with-specexplorer/
- https://github.com/p-org/P

Model-based testing gera sequências e oracles a partir de modelos de estado. P leva a ideia para sistemas distribuídos, safety/liveness e exploração sistemática; o projeto registra uso em serviços AWS como S3, EBS, DynamoDB, Aurora e EC2.

Decisão: acrescentar model/stateful testing como capacidade condicional. P ou Quint/TLA+ entram apenas quando concorrência, mensagens, falhas ou grande espaço de estados forem risco real.

### TLA+ / Quint

Fontes:

- https://lamport.azurewebsites.net/tla/
- https://github.com/quint-co/quint
- https://quint.sh/docs/what-does-quint-do

TLA+ e Quint descrevem transições e propriedades temporais, permitindo model checking e contraexemplos.

Decisão: usar como opção `formal` para sistemas distribuídos/concorrentes, não como default de aplicações comuns.

### Z3

Fontes:

- https://www.microsoft.com/en-us/research/project/z3-3/
- https://github.com/Z3Prover/z3

Z3 é um solver SMT open source (MIT) útil para satisfatibilidade, contraexemplos e restrições combinatórias.

Decisão: recomendado para conjuntos estruturados de regras em que a pergunta “essas regras podem ser verdadeiras ao mesmo tempo?” seja relevante. O Core permanece stdlib; projetos instalam Z3 somente quando selecionado.

### Alloy

Fonte:

- https://alloytools.org/

Alloy é um model finder relacional. Procura instâncias/contraexemplos dentro de um escopo, sendo especialmente adequado a entidades, relações, cardinalidades e invariantes estruturais.

Decisão: opção `formal` para domínios relacionais complexos; não é necessária para um modelo de domínio comum.

### Property-based / stateful testing

Fontes:

- https://hypothesis.works/articles/what-is-hypothesis/
- https://hypothesis.works/articles/rule-based-stateful-testing/

Property-based testing define propriedades e deixa o motor explorar dados; stateful testing gera sequências de operações.

Decisão: integrar como complemento natural a invariantes, ranges e state machines. Hypothesis é default forte para Python quando aplicável; outras linguagens usam ferramenta madura equivalente.

### DMN

Fonte:

- https://www.omg.org/dmn/

Decision Model and Notation representa decisões e lógica de decisão, incluindo decision tables executáveis.

Decisão: condicional para domínios em que regras são melhor revisadas como tabela de decisão do que como código espalhado.

### OPA/Rego e Cedar

Fontes:

- https://www.openpolicyagent.org/docs/
- https://www.cedarpolicy.com/

OPA/Rego separa policy decision de enforcement. Cedar é uma linguagem open source de autorização da AWS com desenvolvimento guiado por verificação formal.

Decisão: condicional para políticas/autorização complexas; não substituir autorização simples server-side por um motor externo sem necessidade.

### SHACL

Fonte:

- https://www.w3.org/TR/shacl/

SHACL valida grafos RDF contra shapes e é forte para knowledge graphs/ontologias.

Decisão: não virar default da Factory. Só considerar quando o produto realmente usar RDF/knowledge graph; introduzir RDF apenas para obter semântica criaria complexidade artificial.

## O que não foi adotado como default

### Cucumber/Gherkin runtime

Given/When/Then continua sendo uma linguagem de aceite útil, mas Cucumber não será runtime universal. A camada de step definitions/glue pode introduzir manutenção sem melhorar a prova em projetos onde stakeholders não editam diretamente os cenários.

A Factory mantém `given/when/then` no contrato semântico e liga diretamente cada critério a testes/gates reais.

### “Uma IA lê tudo e decide se é consistente”

Análise probabilística é útil para sugerir conflitos e lacunas, mas não pode ser o único gate. A nova camada separa:

- erros determinísticos de estrutura/referência/restrição;
- findings probabilísticos/advisory;
- análise formal quando justificada;
- decisão humana quando a ambiguidade é de produto/domínio.

## Arquitetura escolhida

```text
intenção
  ↓
Semantic Assurance
  ├─ requisitos estruturados EARS/FRET-inspired
  ├─ glossário + domínio + relações + estados
  ├─ consistency/coverage
  ├─ semantic diff/impact
  ├─ property/model-based testing recomendado
  └─ formal methods condicionais
       ↓
Semantic Verification
  ├─ invariantes + given/when/then
  ├─ verification plan
  └─ review evidence
       ↓
Independent Verification
       ↓
Definition of Done
```

## Regra de adoção

A nova camada deve permanecer proporcional:

- `scenario`: contrato semântico atual é suficiente;
- `domain`: modelo e consistência estruturados;
- `formal`: ferramenta formal específica quando o risco/problema justificar.

Nenhuma ferramenta pesquisada foi considerada boa justificativa para transformar todo aplicativo em projeto de métodos formais.