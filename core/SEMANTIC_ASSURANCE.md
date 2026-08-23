# Semantic Assurance Contract

Este contrato define como a App Factory verifica a **qualidade da própria especificação** antes de usar `core/SEMANTIC_VERIFICATION.md` para provar a implementação.

A separação de responsabilidades é deliberada:

- **Semantic Assurance** pergunta: *a intenção está suficientemente clara, coerente, completa, modelada e rastreável para ser implementada com segurança?*
- **Semantic Verification** pergunta: *a implementação atual satisfaz a especificação atual?*
- **System Engineering** define a profundidade mínima da arquitetura do produto.
- **API Engineering** define contratos de interface quando existirem.
- **Independent Verification** executa motores externos/adversariais contra implementação e testes.

Semantic Assurance não substitui decisão humana de produto. Ferramentas formais provam propriedades do modelo fornecido; não provam que o modelo representa perfeitamente o mundo real.

## 1. Fontes e princípios incorporados

A Factory adota, sem copiar cegamente uma ferramenta única:

- estrutura de requisitos inspirada em **EARS** para tornar condição, gatilho, sujeito e resposta explícitos;
- campos e formalização inspirados em **NASA FRET/FRETish** para requisitos temporais/reativos quando a precisão adicional trouxer valor;
- análise cruzada de requisitos, cobertura e artefatos inspirada em workflows modernos de spec-driven development;
- model-based/stateful/property-based testing para explorar sequências e valores além dos exemplos escritos manualmente;
- métodos formais condicionais para restrições, relações, estados, concorrência, temporalidade, decisões e políticas.

A Factory não transforma linguagem natural em “prova matemática” silenciosamente. Toda formalização que virar gate precisa ser recuperável, revisável e ligada ao requisito de origem.

## 2. Profundidade semântica

### `none`

Documentação/chore ou mudança sem comportamento observável. Não criar artefatos semânticos por reflexo.

### `scenario`

Funcionalidade pequena ou regra isolada. `specs/semantic-contract.json` com invariantes e critérios `given/when/then` normalmente é suficiente.

### `domain`

Use quando existirem múltiplos conceitos/regras interagindo, domínio institucional, papéis, estados, relações, decisões ou risco de interpretação divergente.

Além do contrato semântico, materialize `specs/semantic-assurance.json` com vocabulário, modelo de domínio, requisitos normalizados, restrições e rastreabilidade.

### `formal`

Use somente quando o custo de erro e a natureza do problema justificarem análise formal: concorrência/distribuição, safety/liveness, requisitos temporais críticos, políticas complexas, relações combinatórias, regras com grande espaço de estados ou sistema crítico.

`formal` não significa instalar todas as ferramentas formais. Selecione uma técnica adequada ao problema.

## 3. Estrutura de requisitos

Para profundidade `domain` ou `formal`, cada requisito relevante deve ser normalizado em campos estruturados em vez de depender apenas de uma frase livre.

Campos recomendados:

- `id`: `REQ-###`;
- `priority`: `must` / `should` / `may`;
- `pattern`: `ubiquitous`, `event`, `state`, `unwanted`, `optional`, `complex`, `decision` ou `policy`;
- `component`: quem deve responder;
- `scope`: contexto em que a regra vale;
- `preconditions`: pré-condições;
- `trigger`: evento/condição que dispara a regra;
- `response`: resultados obrigatórios observáveis;
- `timing`: limite/janela temporal quando relevante;
- `concept_refs`: termos/entidades usados;
- `acceptance_refs`: critérios `AC-###` que concretizam o requisito;
- `invariant_refs`: invariantes `INV-###` relacionados;
- `formalization`: artefato formal opcional quando houver.

A estrutura segue o espírito EARS/FRET, mas não exige que todo projeto adote sintaxe textual específica nem runtime Cucumber.

## 4. Vocabulário e modelo de domínio

A partir de `domain`, a Factory deve tornar explícitos os conceitos cuja ambiguidade mudaria o comportamento.

`specs/semantic-assurance.json` pode conter:

- `glossary`: termos, definições, aliases e conceitos proibidos/deprecados;
- `entities`: entidades de domínio e atributos relevantes;
- `relations`: relações dirigidas entre entidades, com cardinalidade quando material;
- `states`: estados de domínio importantes;
- `transitions`: transições permitidas/negadas;
- `constraints`: restrições estruturadas;
- `open_questions`: ambiguidades ou decisões ainda abertas.

Não transformar todo substantivo em entidade. Modele somente conceitos que afetam regra, persistência, autorização, integração, estados ou interpretação.

## 5. Consistência determinística mínima

O engine deve detectar sem IA, quando os dados estruturados permitirem:

- IDs duplicados;
- referências quebradas entre requisitos, conceitos, invariantes e critérios;
- relações apontando para entidades inexistentes;
- transições apontando para estados inexistentes;
- cardinalidade impossível (`min > max`);
- intervalo impossível (`min > max`);
- enumeração cuja lista permitida foi integralmente proibida;
- dependência e proibição simultâneas para o mesmo par de regras;
- critérios `must` sem requisito de origem em profundidade `domain`/`formal`;
- requisitos `must` sem critério de aceite;
- pergunta aberta `blocking`;
- uso de termos vagos conhecidos como finding advisory, nunca como “prova” automática de ambiguidade.

Um finding determinístico deve indicar os IDs envolvidos e, quando possível, um contraexemplo simples.

## 6. Cobertura semântica

A Factory não deve mostrar uma porcentagem enganosa de “correção semântica”. Em vez disso, reporte cobertura estrutural separada:

- requisitos `must` ligados a critérios de aceite;
- critérios `must` ligados a requisitos;
- requisitos ligados aos conceitos de domínio que usam;
- invariantes rastreados até requisitos/critério;
- critérios ligados a evidência executável via `verification-plan.json`;
- regras formais ligadas ao requisito de origem quando existirem.

Cobertura incompleta é sinal objetivo. Cobertura 100% não significa que a intenção humana esteja perfeita.

## 7. Semantic Diff e impacto

Quando a especificação mudar, compare por IDs estáveis e fingerprints.

O diff semântico deve apontar:

- requisitos adicionados/removidos/alterados;
- conceitos/entidades/relações alterados;
- restrições e estados alterados;
- critérios/invariantes impactados por referências;
- gates/testes impactados quando `verification-plan.json` permitir rastrear;
- formalizações que ficaram potencialmente stale.

Mudança textual sem mudança semântica não deve gerar impacto artificial quando os campos estruturados forem equivalentes. Mudança semântica material deve invalidar evidência/review dependente.

## 8. Model-based e property-based testing

Exemplos `given/when/then` continuam importantes, mas não devem ser a única forma de explorar um domínio com espaço grande.

Quando houver invariantes, ranges, sequências ou máquina de estados:

- prefira property-based testing compatível com a linguagem;
- para Python, Hypothesis é um default forte quando já fizer sentido na stack;
- para outras linguagens, selecione alternativa madura/open source equivalente;
- para fluxos stateful, gere sequências de operações e valide invariantes a cada estado;
- transforme contraexemplos encontrados em regressão reproduzível.

Não introduzir property-based testing em lógica trivial sem ganho real.

## 9. Métodos formais condicionais

### Restrições e regras combinatórias

Use **Z3** ou solver SMT equivalente quando regras estruturadas puderem ser expressas como restrições e for útil perguntar “existe alguma combinação que satisfaz tudo?” ou “há um contraexemplo?”.

Use **Alloy** quando o problema for predominantemente relacional: entidades, cardinalidades, ownership, composições e invariantes estruturais.

### Requisitos temporais/reativos

Use **NASA FRET/FRETish** ou técnica equivalente quando timing, scope, condição e resposta precisarem de semântica temporal precisa e realizability/consistency checking trouxer valor.

Não gerar FRETish aproximado e tratá-lo como prova. O artefato formal deve ser validado pela ferramenta real quando virar gate.

### Estados, concorrência e sistemas distribuídos

Considere **P**, **Quint/TLA+** ou equivalente quando interleavings, mensagens, falhas, safety/liveness ou concorrência forem o risco central.

### Decisões de negócio

Considere **DMN/decision tables** quando grande parte do comportamento for uma decisão tabular com combinações de entrada/saída que precisam ser revisáveis e executáveis.

### Autorização/policy-as-code

Considere **OPA/Rego** ou **Cedar** quando políticas de autorização complexas precisarem ser separadas da implementação e testadas como regras declarativas.

Nenhuma dessas ferramentas é dependência universal da Factory.

## 10. Formalization registry

Quando método formal for usado, `semantic-assurance.json` deve registrar por requisito:

- `kind`: `z3`, `alloy`, `fret`, `p`, `quint`, `tla+`, `dmn`, `opa`, `cedar` ou equivalente;
- `artifact`: caminho versionado;
- `source_refs`: requisitos/invariantes que o artefato representa;
- `gate`: gate executável quando obrigatório;
- `status`: `required`, `advisory` ou `experimental`.

Formalização sem `source_refs` não é rastreabilidade. Ferramenta não executada não conta como prova.

## 11. Ambiguidade e análise por IA

Análise por IA pode encontrar:

- termos indefinidos;
- pressupostos implícitos;
- conflitos entre requisitos distantes;
- edge cases ausentes;
- conflito funcional x não funcional;
- diferença entre regra escrita e domínio conhecido.

Mas findings da própria IA são hipóteses até serem resolvidos pelo contrato estruturado, usuário/domínio ou prova determinística/formal.

Não bloqueie automaticamente por mera suspeita probabilística. Marque como `blocking` somente quando a ambiguidade impede uma implementação segura/correta ou exige decisão humana genuína.

## 12. Relação com Semantic Verification

Fluxo preferido para trabalho relevante:

```text
intenção
→ semantic assurance proporcional
→ semantic-contract + semantic-assurance quando aplicável
→ análise de consistência/cobertura
→ specification ready
→ implementação
→ verification-plan + testes/gates
→ Independent Verification quando aplicável
→ review desacoplado
→ delivery
```

`semantic-contract.json` continua sendo a autoridade dos critérios de aceite e invariantes observáveis. `semantic-assurance.json` complementa com domínio/requisitos/consistência; não deve duplicar OpenAPI, schema de banco ou todos os detalhes de arquitetura.

## 13. Definition of Done semântica

Quando profundidade for `domain` ou `formal`, não concluir a fase de especificação se:

- existir erro estrutural/contradição determinística não resolvida;
- houver `open_question` blocking;
- requisito `must` não tiver critério de aceite;
- critério `must` não tiver origem rastreável;
- referência obrigatória estiver quebrada;
- formalização marcada `required` estiver ausente/stale/não executada quando o gate já existir.

Para `formal`, a entrega também deve registrar limites do modelo e pressupostos que ficaram fora da prova.

## 14. Regra final

A meta não é “formalizar tudo”. A meta é aumentar precisão onde a ambiguidade custa caro.

A Factory deve usar a forma mais leve que preserve corretamente a intenção real:

`scenario → domain → formal`

Subir de nível somente quando relações, estados, decisões, risco ou custo de erro justificarem. Voltar para uma forma simples quando complexidade formal não estiver produzindo evidência melhor.