# Semantic Assurance Contract

Este contrato define como a App Factory verifica a **qualidade da própria especificação** antes de usar `core/SEMANTIC_VERIFICATION.md` para provar a implementação.

A separação de responsabilidades é deliberada:

- **Semantic Assurance** pergunta: a intenção está suficientemente clara, coerente, completa, modelada e rastreável para ser implementada com segurança?
- **Semantic Verification** pergunta: a implementação atual satisfaz a especificação atual?
- **System Engineering** define a profundidade mínima da arquitetura.
- **API Engineering** define contratos de interface quando existirem.
- **Independent Verification** executa motores externos/adversariais e transforma propriedades/modelos semânticos em gates quando aplicável.

Semantic Assurance não substitui decisão humana de produto. Ferramentas formais ou geradores de teste provam propriedades do modelo fornecido; não provam que o modelo representa perfeitamente o mundo real.

## 1. Fontes e princípios incorporados

A Factory adota, sem copiar cegamente uma ferramenta única:

- estrutura inspirada em **EARS** para tornar condição, gatilho, sujeito e resposta explícitos;
- **NASA FRET/FRETish** para requisitos temporais/reativos quando precisão adicional trouxer valor;
- análise cruzada de requisitos, gaps e artefatos inspirada em workflows modernos de spec-driven development;
- property/stateful/model-based testing para explorar valores e sequências além dos exemplos manuais;
- combinatorial/t-way testing com covering arrays, preferindo **NIST ACTS** quando o espaço finito de configurações justificar;
- métodos formais condicionais para restrições, relações, estados, concorrência, temporalidade, decisões e policies.

A Factory não transforma linguagem natural em “prova matemática” silenciosamente. Toda formalização/modelo que virar gate precisa ser recuperável, revisável e ligado à origem.

## 2. Profundidade semântica

### `none`

Documentação/chore ou mudança sem comportamento observável. Não criar artefatos semânticos por reflexo.

### `scenario`

Funcionalidade pequena ou regra isolada. `specs/semantic-contract.json` com invariantes e critérios `given/when/then` normalmente basta.

### `domain`

Use quando múltiplos conceitos/regras interagirem, houver papéis, estados, relações, decisões, domínio institucional/comercial ou risco de interpretação divergente.

Além do contrato semântico, materialize `specs/semantic-assurance.json` com vocabulário, modelo de domínio, requisitos normalizados, restrições e rastreabilidade.

### `formal`

Use somente quando custo de erro e natureza do problema justificarem análise formal: concorrência/distribuição, safety/liveness, requisitos temporais críticos, policies complexas, relações combinatórias, grande espaço de estados ou sistema crítico.

`formal` não significa instalar todas as ferramentas. Selecione a técnica adequada ao problema.

## 3. Estrutura de requisitos

Para `domain`/`formal`, cada requisito relevante deve ser normalizado em campos estruturados em vez de depender apenas de frase livre.

Campos recomendados:

- `id`: `REQ-###`;
- `priority`: `must` / `should` / `may`;
- `pattern`: `ubiquitous`, `event`, `state`, `unwanted`, `optional`, `complex`, `decision` ou `policy`;
- `component`;
- `scope`;
- `preconditions`;
- `trigger`;
- `response`;
- `timing`;
- `concept_refs`;
- `acceptance_refs`;
- `invariant_refs`;
- `formalization_refs`.

A estrutura segue o espírito EARS/FRET, sem exigir sintaxe textual universal ou runtime Cucumber.

## 4. Vocabulário e modelo de domínio

A partir de `domain`, torne explícitos apenas conceitos cuja ambiguidade mudaria comportamento.

`specs/semantic-assurance.json` pode conter:

- `glossary`;
- `entities`;
- `relations` e cardinalidades relevantes;
- `states`;
- `transitions` permitidas/negadas;
- `constraints`;
- `open_questions`.

Não transforme todo substantivo em entidade. Modele conceitos que afetam regra, persistência, autorização, integração, estados ou interpretação.

## 5. Consistência determinística mínima

O engine deve detectar sem IA, quando os dados estruturados permitirem:

- IDs duplicados;
- referências quebradas;
- relações apontando para entidades inexistentes;
- transições para estados inexistentes;
- cardinalidade impossível (`min > max`);
- range impossível (`min > max`);
- enum cujos valores permitidos foram todos proibidos;
- dependência e proibição/exclusão simultâneas;
- critérios `must` sem origem em requisito em `domain/formal`;
- requisitos `must` sem critério de aceite;
- pergunta aberta `blocking`;
- termos vagos conhecidos como finding advisory, nunca como prova automática.

Finding determinístico deve indicar IDs envolvidos e, quando possível, contraexemplo simples.

## 6. Cobertura semântica

Não mostrar porcentagem enganosa de “correção semântica”. Reportar cobertura estrutural separada:

- requisito `must` → critério;
- critério `must` → requisito;
- requisito → conceitos usados;
- invariante → requisito/critério;
- critério → evidência executável;
- formalização/modelo → origem.

Cobertura incompleta é sinal objetivo. **100% não significa** que a intenção humana esteja correta.

## 7. Semantic Diff e impacto

Compare por IDs estáveis e fingerprints.

O **Semantic Diff** deve apontar:

- requisitos adicionados/removidos/alterados;
- conceitos/entidades/relações alterados;
- restrições/estados alterados;
- critérios/invariantes impactados;
- gates/testes impactados quando rastreáveis;
- formalizações, propriedades ou modelos combinatoriais potencialmente stale.

Mudança semântica material invalida evidência dependente até nova passagem.

## 8. Property-based e stateful testing

Exemplos `given/when/then` continuam importantes, mas não devem ser a única exploração de domínio com espaço grande.

Quando houver invariantes, ranges, sequências ou máquina de estados:

- Python: preferir **Hypothesis**;
- JavaScript/TypeScript: preferir **fast-check**;
- outras linguagens: equivalente maduro/open source;
- gerar valores/sequências e validar invariantes a cada passo quando stateful;
- preservar seed/contraexemplo reproduzível;
- transformar finding importante em regressão determinística.

Property testing não substitui mutation testing: mutation pergunta se os testes detectam defeitos; property testing procura valores/estados que violem uma propriedade declarada.

Não introduzir property-based testing em lógica trivial sem ganho real.

## 9. Combinatorial testing / NIST ACTS

Quando múltiplas dimensões finitas interagirem, teste exaustivo pode crescer de forma impraticável. Nesse caso considere **NIST ACTS** ou covering-array generator equivalente.

Candidatos típicos, em qualquer domínio:

- roles × permissions × states;
- feature flags × plans × regions;
- browser × auth mode × configuration;
- product variants × rules × channel;
- qualquer combinação de parâmetros discretos com risco de interação.

Regras:

- não usar ACTS só porque há muitos campos;
- derive parâmetros/valores/restrições do domínio real;
- escolha força t-way por evidência/risco, não número arbitrário;
- quando a combinação for material, versionar `specs/combinatorial-model.json` ou artefato equivalente;
- um modelo materializado pode virar gate de Independent Verification;
- sem modelo executável, a recomendação permanece advisory.

ACTS reduz o espaço de combinações do modelo; não prova comportamentos que não foram modelados.

## 10. Métodos formais condicionais

### Restrições e combinatória lógica

Use **Z3**/SMT quando regras estruturadas puderem ser expressas como restrições e for útil perguntar satisfatibilidade/contraexemplo.

Use **Alloy** quando o problema for predominantemente relacional: entidades, cardinalidades, ownership, composições e invariantes estruturais.

### Temporal/reativo

Use **NASA FRET/FRETish** quando timing, scope, condição e resposta exigirem semântica temporal precisa.

Não gerar FRETish aproximado e tratá-lo como prova. Ferramenta real precisa validar artefato quando virar gate.

### Estados, concorrência e distribuído

Considere P, **Quint/TLA+** ou equivalente para interleavings, mensagens, falhas, safety/liveness e concorrência.

### Decisão de negócio

Considere **DMN**/decision tables quando comportamento for predominantemente tabular/combinatório e precisar ser revisável/executável.

### Authorization/policy-as-code

Considere **OPA/Rego** ou **Cedar** para policies complexas separadas da implementação.

Nenhuma técnica é dependência universal.

## 11. Formalization registry

Quando método formal for usado, registre por requisito:

- `kind`: `z3`, `alloy`, `fret`, `p`, `quint`, `tla+`, `dmn`, `opa`, `cedar` ou equivalente;
- `artifact` versionado;
- `source_refs`;
- `gate` executável quando obrigatório;
- `status`: `required`, `advisory` ou `experimental`.

Formalização sem `source_refs` não é rastreabilidade. Ferramenta não executada não conta como prova.

## 12. Ambiguidade e análise por IA

IA pode sugerir:

- termos indefinidos;
- pressupostos implícitos;
- conflitos distantes;
- edge cases ausentes;
- conflito funcional × não funcional;
- diferença entre regra escrita e domínio conhecido.

Mas finding da IA é hipótese até ser resolvido por contrato estruturado, evidência, usuário/domínio ou prova determinística/formal.

Não bloqueie automaticamente por mera suspeita probabilística. `blocking` só quando a ambiguidade impede implementação segura/correta ou exige decisão humana genuína.

## 13. Handoff para Independent Verification

Fluxo preferido:

```text
intenção
→ Semantic Assurance proporcional
→ semantic-contract + semantic-assurance quando aplicável
→ consistência/cobertura
→ propriedades/modelos combinatórios/formalizações quando justificados
→ implementação
→ verification-plan + testes/gates
→ Independent Verification
→ review desacoplado
→ delivery
```

Semantic Assurance identifica **o que vale explorar**; Independent Verification decide quando isso vira gate:

- invariantes/ranges/estados → Hypothesis/fast-check;
- múltiplas dimensões finitas → NIST ACTS;
- formalization registry → solver/model checker;
- critérios → evidência executável normal.

`semantic-contract.json` continua autoridade dos critérios/invariantes observáveis. `semantic-assurance.json` complementa com domínio/requisitos/consistência; não duplica OpenAPI, schema de banco ou arquitetura inteira.

## 14. Definition of Done semântica

Em `domain/formal`, não concluir especificação se:

- houver erro estrutural/contradição determinística não resolvida;
- `open_question` blocking existir;
- requisito `must` não tiver critério;
- critério `must` não tiver origem rastreável;
- referência obrigatória estiver quebrada;
- formalização `required` estiver ausente/stale/não executada quando gate existir.

Para `formal`, registre limites e assumptions do modelo.

Property/combinatorial testing só bloqueia quando Independent Verification o selecionar como `required`; não tornar toda modelagem semântica um gerador pesado por padrão.

## 15. Regra final

A meta não é formalizar nem gerar tudo. É aumentar precisão onde ambiguidade/combinação custa caro.

Use a forma mais leve que preserve corretamente a intenção:

`scenario → domain → formal`

Suba quando relações, estados, combinações, decisões, risco ou custo de erro justificarem. Simplifique quando complexidade adicional não produz evidência melhor.
