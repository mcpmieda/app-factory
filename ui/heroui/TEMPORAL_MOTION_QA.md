# Temporal Motion QA — Integridade da Evidência

## Objetivo

Impedir falso-positivo em validações de Living UI e qualquer motion cuja presença perceptível seja requisito de produto.

## Regra central

A existência de `animation:` no CSS, duas screenshots diferentes ou dois atributos com nomes diferentes **não prova** que o movimento executou.

Quando o requisito for movimento perceptível, o QA deve comparar o estado computado do mesmo elemento em dois instantes e provar que o relógio da animação avançou.

## Evidência mínima recomendada

Para uma animação CSS contínua relevante:

1. abrir a interface real ou fixture que importe a primitive real;
2. localizar o mesmo elemento animado nos dois instantes;
3. ler `element.getAnimations()` e `animation.currentTime` quando disponível;
4. ler a propriedade computada que deve mudar (`transform`, `opacity` ou equivalente);
5. aguardar tempo real suficiente — normalmente 2–4 s para motion lento;
6. repetir as leituras;
7. falhar se `currentTime` não avançar de forma material;
8. falhar se o valor computado esperado permanecer idêntico;
9. registrar os valores inicial/final como artifact ou log recuperável.

Para `prefers-reduced-motion`, executar uma segunda prova e confirmar que o movimento não essencial foi reduzido/parado conforme a política do projeto e que a interface continua funcional e legível.

## Anti-padrões

Não aceitar como prova:

- comparar strings completas como `data-motion-start="..."` e `data-motion-later="..."`, pois os nomes dos atributos já tornam as strings diferentes mesmo quando os valores são iguais;
- testar apenas que existe `animation-name` no stylesheet;
- testar apenas que duas capturas foram geradas;
- mover manualmente `animation.currentTime` e apresentar isso como prova de execução natural;
- considerar `setTimeout` isolado como evidência sem verificar o estado computado do elemento;
- usar fixture que reimplemente o efeito em vez de importar a primitive real.

## Forma segura de comparação

Se atributos auxiliares forem usados, extrair e comparar **somente o valor**. Para um gate forte, preferir leitura direta pelo navegador via Web Animations API / DevTools Protocol.

Exemplo conceitual:

```text
primeira leitura:
  currentTime = 150 ms
  transform = matrix(...)

aguardar 3,5 s reais

segunda leitura:
  currentTime = 3660 ms
  transform = matrix(... diferente ...)

PASS somente se:
  currentTime avançou materialmente
  E transform mudou
```

## Reduced motion

Quando `prefers-reduced-motion: reduce` estiver ativo:

- animação não essencial deve ficar ausente, pausada ou suficientemente reduzida conforme a implementação;
- o estado computado deve refletir essa redução entre as leituras;
- a composição deve permanecer legível e utilizável;
- nenhum conteúdo funcional pode depender do loop.

## Aplicação no contrato HeroUI

Esta regra complementa `HEROUI_NATIVE_REDESIGN_CONTRACT.md` e `../MOTION_POLICY.md`.

Quando o contrato exigir comparar dois frames separados por 2–4 s, a comparação deve validar valores reais, não apenas a existência de dois registros. Para motion considerado requisito visual do produto, usar prova temporal real sempre que a infraestrutura de QA permitir.
