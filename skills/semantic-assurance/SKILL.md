---
name: semantic-assurance
description: Analisa a qualidade da especificação antes da implementação: normaliza requisitos, modela domínio, encontra inconsistências, mede rastreabilidade, calcula impacto semântico e seleciona métodos formais apenas quando justificáveis.
---

# Semantic Assurance

Use quando a mudança funcional tiver múltiplas regras/conceitos interagindo, domínio institucional, papéis, estados, decisões, temporalidade, concorrência ou risco de interpretação divergente.

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
9. Quando houver grande espaço de entradas/estados, derive property/stateful tests além dos exemplos `given/when/then`.
10. Se a natureza do problema justificar formalização, selecione uma técnica específica e registre artefato + source refs + gate.
11. Quando uma spec existente mudar, use semantic diff para localizar requisitos, critérios, invariantes e gates impactados.
12. Só então siga para implementação e `semantic-verification` da implementação.

## Seleção de método formal

Não escolha por preferência pessoal:

- restrições/satisfatibilidade: Z3/SMT;
- relações/cardinalidades: Alloy;
- temporal/reactivo: NASA FRET/FRETish;
- estados/concorrência/distribuído: P ou Quint/TLA+;
- decisão tabular: DMN;
- policy/autorização declarativa: OPA/Rego ou Cedar.

Ferramenta formal é condicional. CRUD simples não deve ganhar um model checker sem necessidade.

## Limite de segurança epistemológica

A formalização prova propriedades do modelo, não que o modelo corresponde perfeitamente ao desejo humano. Registre assumptions e limites do modelo em trabalho `formal`.

Não deixe uma IA converter silenciosamente texto livre em lógica formal e marcar como `pass` sem artefato revisável e ferramenta real quando isso virar gate.

## Saída

A fase de Semantic Assurance deve produzir, proporcionalmente:

- profundidade selecionada;
- requisitos normalizados;
- vocabulário/modelo de domínio;
- erros/warnings de consistência;
- cobertura estrutural de rastreabilidade;
- perguntas abertas;
- recomendações formais condicionais;
- semantic diff/impacto quando houver baseline.

Uma cobertura estrutural de 100% nunca deve ser rotulada como “100% semanticamente correto”.