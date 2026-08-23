---
name: semantic-verification
description: Transforma intenção funcional em contrato verificável, liga critérios de aceite a testes/gates e exige revisão desacoplada antes da entrega quando o risco justificar. Usa semantic-assurance antes da implementação quando a qualidade da especificação exige modelagem de domínio ou análise formal.
---

# Semantic Verification

Use em funcionalidade nova, bugfix relevante, regra de negócio, contrato de dados/API ou mudança estrutural de médio/alto risco.

## Antes desta Skill

`core/SEMANTIC_ASSURANCE.md` é dono da **qualidade da especificação**. Quando a profundidade for `domain` ou `formal`, carregue `semantic-assurance`, valide `specs/semantic-assurance.json` e resolva erros/perguntas blocking antes de implementar.

Esta Skill é dona da **correspondência implementação ↔ especificação**. Não duplique glossário/modelo de domínio aqui.

## Sequência

1. Criar/atualizar `specs/semantic-contract.json` antes da implementação.
2. Se Semantic Assurance for `domain`/`formal`, validar que o assurance atual aponta para o fingerprint desse contrato e está ready.
3. Expressar regras essenciais como invariantes e critérios `AC-###` em `given / when / then`.
4. Gerar `specs/verification-plan.json` a partir da spec.
5. Para cada critério `must`, ligar ao menos um teste/gate executável; property/stateful/formal gates podem complementar exemplos quando apropriado.
6. Implementar somente depois da especificação pronta.
7. Executar os gates reais; rastreabilidade não substitui execução.
8. Fazer revisão por `independent-agent` quando disponível ou `clean-context` quando não houver segundo agente.
9. Registrar `specs/review-evidence.json` somente após revisar o contrato atual e a evidência atual.
10. Se código/spec/plano mudar depois da revisão, revisar novamente. Se Semantic Assurance indicar semantic diff material, rever também ACs/invariantes/gates impactados.

## Processo proporcional

Não exigir spec formal pesada para docs/chores ou refactor pequeno sem mudança observável. Para trabalho simples, profundidade `scenario` com poucos critérios é suficiente.

Não subir para `domain`/`formal` apenas porque a ferramenta existe. Relações, estados, decisões, temporalidade, concorrência, políticas ou risco precisam justificar o custo.

## Regra de independência

Na revisão desacoplada, não use o raciocínio ou as justificativas produzidas durante implementação como prova. Leia somente o objetivo/spec, conteúdo atual/diff necessário e evidências executadas.

## UI

Visual regression é recomendado quando existe baseline visual estável e regressão visual é risco real. Não criar snapshots frágeis apenas para cumprir processo.

## Resultado

Uma entrega semanticamente válida responde objetivamente:

- a qualidade da especificação foi adequada à profundidade selecionada;
- o que deveria acontecer;
- qual teste/gate prova cada requisito obrigatório;
- se um reviewer desacoplado confirmou a correspondência;
- se a evidência ainda corresponde ao conteúdo atual.
