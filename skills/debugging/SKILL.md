---
name: debugging
description: Investiga bugs e falhas por evidência, reproduzindo o problema, isolando causa raiz e validando a correção sem empilhar patches sobre estado incerto.
---

# Debugging

## Processo

1. reproduza ou obtenha evidência concreta;
2. diferencie sintoma de causa;
3. leia logs, console, testes e estado real;
4. reduza hipóteses por experimentos controlados;
5. corrija a causa mais provável sustentada por evidência;
6. execute o fluxo que falhava;
7. rode regressão direta;
8. crie teste/guardrail quando o bug for importante e repetível.

## Regras

- não alterar marcadores/estado apenas para esconder erro;
- não assumir que a última mudança é necessariamente a causa;
- não fazer várias alterações independentes de uma vez se isso impedir identificar o efeito;
- se o estado ficou incerto, compare com baseline antes de continuar.