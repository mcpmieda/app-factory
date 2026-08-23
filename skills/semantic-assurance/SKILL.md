---
name: semantic-assurance
description: Analisa a qualidade da especificação antes da implementação: normaliza requisitos, modela domínio, encontra inconsistências, mede rastreabilidade, calcula impacto semântico e deriva property/combinatorial/formal methods apenas quando justificáveis.
---

# Semantic Assurance

Use quando a mudança funcional tiver múltiplas regras/conceitos interagindo, domínio institucional ou comercial, papéis, estados, decisões, temporalidade, concorrência ou risco de interpretação divergente.

Para regra isolada e simples, `semantic-verification` em profundidade `scenario` pode ser suficiente.

## Fonte comum

Leia `core/SEMANTIC_ASSURANCE.md`. Não replique esse contrato no projeto.

## Sequência

1. Confirme que `specs/semantic-contract.json` existe e representa a intenção atual.
2. Classifique profundidade semântica: `scenario`, `domain` ou `formal`.
3. Em `domain`/`formal`, crie ou atualize `specs/semantic-assurance.json`.
4. Normalize requisitos em campos explícitos inspirados em EARS/FRET: scope, preconditions, trigger, component, response, timing e referências.
5. Modele somente termos, entidades, relações, estados e restrições cuja interpretação afeta comportamento.
6. Execute `python scripts/semantic_assurance.py analyze` ou engine equivalente.
7. Resolva erros determinísticos e perguntas `blocking` antes da implementação.
8. Use findings probabilísticos da IA como perguntas/hipóteses; não os trate como prova automática.
9. Quando houver invariantes, ranges, estados ou grande espaço de entradas, derive property/stateful tests além dos exemplos `given/when/then`:
   - Python: **Hypothesis**;
   - JavaScript/TypeScript: **fast-check**;
   - equivalente maduro em outra linguagem.
10. Quando múltiplas dimensões finitas interagirem e o teste exaustivo explodir, derive um modelo combinatorial e use **NIST ACTS** ou covering-array generator equivalente. Não escolher t-way arbitrário; documente parâmetros, restrições e objetivo de cobertura.
11. Se a natureza do problema justificar formalização, selecione uma técnica específica e registre artefato + source refs + gate.
12. Quando uma spec existente mudar, use semantic diff para localizar requisitos, critérios, invariantes, modelos de teste e gates impactados.
13. Só então siga para implementação e `semantic-verification` da implementação.

## Seleção de método

Não escolha por preferência pessoal:

- propriedade/invariantes/ranges/estado: Hypothesis / fast-check / equivalente;
- interações combinatórias discretas: NIST ACTS / covering arrays;
- restrições/satisfatibilidade: Z3/SMT;
- relações/cardinalidades: Alloy;
- temporal/reactivo: NASA FRET/FRETish;
- estados/concorrência/distribuído: P ou Quint/TLA+;
- decisão tabular: DMN;
- policy/autorização declarativa: OPA/Rego ou Cedar.

Ferramentas são condicionais. CRUD simples não deve ganhar property fuzzer, ACTS ou model checker sem ganho real.

## Handoff para Independent Verification

Semantic Assurance identifica **o que vale explorar**. `independent-verification` decide quando transformar esses candidatos em gates executáveis:

- invariantes/constraints/states → Hypothesis/fast-check;
- múltiplas dimensões finitas → NIST ACTS;
- formalization registry → solver/model checker correspondente.

Não conte quantidade de casos gerados como “qualidade semântica”. A qualidade continua ligada à rastreabilidade e à adequação do modelo.

## Limite de segurança epistemológica

A formalização ou geração de testes prova propriedades do modelo fornecido, não que o modelo corresponde perfeitamente ao desejo humano. Registre assumptions e limites em trabalho `formal`.

Não deixe uma IA converter silenciosamente texto livre em lógica formal/combinatória e marcar como `pass` sem artefato revisável e ferramenta real quando isso virar gate.

## Saída

A fase deve produzir, proporcionalmente:

- profundidade selecionada;
- requisitos normalizados;
- vocabulário/modelo de domínio;
- erros/warnings de consistência;
- cobertura estrutural de rastreabilidade;
- perguntas abertas;
- candidatos a property/stateful/combinatorial tests;
- recomendações formais condicionais;
- semantic diff/impacto quando houver baseline.

Cobertura estrutural de 100% nunca deve ser rotulada como “100% semanticamente correto”.
