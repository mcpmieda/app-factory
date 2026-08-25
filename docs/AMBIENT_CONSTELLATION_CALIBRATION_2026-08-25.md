# Calibração visual — Ambient Constellation — 2026-08-25

## Motivo

A implementação inicial do Centro de Administração mostrou partículas excessivamente grandes em relação à página. O problema não era falta de densidade, mas escala: um SVG `0 0 100 100` preenchia superfícies grandes usando círculos com raio próximo de `1`, fazendo os pontos crescerem junto com a viewport.

## Referência oficial inspecionada

Foi usada a implementação pública atual do banner/modal HeroUI Pro em `heroui-inc/heroui`:

- card: 288px de largura;
- área visual superior: 180px de altura;
- `FloatingStars`: aproximadamente 760.706 × 637.702px;
- wrapper visual: `scale-50`;
- campo efetivo antes do recorte: aproximadamente 380 × 319px;
- overscan aproximado: 1.32× em largura e 1.77× em altura;
- duas camadas de estrelas;
- drift de 12s e 15s em direções opostas;
- deslocamento-fonte de 40px, percebido próximo de 20px após a escala;
- partículas majoritariamente muito pequenas, com opacidades baixas (`0.11`, `0.3` e variações) dentro de grupo parcialmente transparente.

## Regra consolidada

A App Factory passa a tratar `strong` como intensidade por composição, densidade, profundidade e glow. A escala das partículas fica limitada em screen-space e não deve crescer proporcionalmente à viewport.

Baseline recomendado:

- partículas comuns: 0.6–1.2 CSS px;
- secundárias: 1.2–1.5 CSS px;
- glints raros: até ~1.8 CSS px;
- desktop: maior partícula típica ≤ 2 CSS px;
- mobile: maior partícula típica ≤ 1.5 CSS px;
- overscan do campo: ~1.25–1.45× largura e ~1.55–1.90× altura;
- drift visual: ~14–24px desktop e ~8–16px mobile;
- dois ciclos assíncronos, com 12s/15s como baseline HeroUI.

## Anti-padrão proibido

Não usar `viewBox="0 0 100 100"` em uma superfície grande com `r≈1` para representar estrelas. Isso converte microestrelas em círculos grandes conforme a superfície cresce.

## Resultado esperado

A constelação deve ser percebida como poeira luminosa e profundidade ambiental. Nenhum ponto individual deve competir visualmente com texto, botões, cards ou navegação.
