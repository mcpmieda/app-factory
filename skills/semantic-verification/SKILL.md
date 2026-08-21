---
name: semantic-verification
description: Transforma intenção funcional em contrato verificável, liga critérios de aceite a testes/gates e exige revisão desacoplada antes da entrega quando o risco justificar.
---

# Semantic Verification

Use em funcionalidade nova, bugfix relevante, regra de negócio, contrato de dados/API ou mudança estrutural de médio/alto risco.

## Sequência

1. Criar/atualizar `specs/semantic-contract.json` antes da implementação.
2. Expressar regras essenciais como invariantes e critérios `AC-###` em `given / when / then`.
3. Gerar `specs/verification-plan.json` a partir da spec.
4. Para cada critério `must`, ligar ao menos um teste/gate executável.
5. Implementar somente depois da spec válida.
6. Executar os gates reais; rastreabilidade não substitui execução.
7. Fazer revisão por `independent-agent` quando disponível ou `clean-context` quando não houver segundo agente.
8. Registrar `specs/review-evidence.json` somente após revisar o contrato atual e a evidência atual.
9. Se código/spec/plano mudar depois da revisão, revisar novamente.

## Processo proporcional

Não exigir spec formal pesada para docs/chores ou refactor pequeno sem mudança observável. Para trabalho simples, uma spec mínima com poucos critérios é suficiente.

## Regra de independência

Na revisão desacoplada, não use o raciocínio ou as justificativas produzidas durante implementação como prova. Leia somente o objetivo/spec, conteúdo atual/diff necessário e evidências executadas.

## UI

Visual regression é recomendado quando existe baseline visual estável e regressão visual é risco real. Não criar snapshots frágeis apenas para cumprir processo.

## Resultado

Uma entrega semanticamente válida responde objetivamente:

- o que deveria acontecer;
- qual teste/gate prova cada requisito obrigatório;
- se um reviewer desacoplado confirmou a correspondência;
- se a evidência ainda corresponde ao conteúdo atual.
