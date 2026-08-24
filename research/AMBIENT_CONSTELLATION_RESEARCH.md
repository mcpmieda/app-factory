# Ambient Constellation — pesquisa e decisão

Data: **2026-08-24**

## Problema

Transformar o efeito observado no banner/modal HeroUI Pro em uma regra reutilizável da App Factory, com presença visual forte sem sacrificar navegação, acessibilidade ou desempenho.

## Fonte primária: HeroUI OSS

A implementação pública atual do site HeroUI usa, no `ProBanner`:

- superfície superior de 180 px;
- SVG de fundo com gradiente claro azul/lilás;
- blob ciano→violeta com Gaussian blur estático;
- duas camadas de estrelas/partículas brancas;
- primeira camada com `float-stars` em 12 s;
- segunda camada com `float-stars-reverse` em 15 s;
- deslocamentos diagonais opostos de aproximadamente 40 px;
- easing `ease-in-out` e loop infinito;
- campo de partículas maior que o viewport da superfície e recortado por overflow;
- entrada/saída do card com Motion spring/fade/translate;
- título HeroUI Pro com gradiente azul/ciano.

Arquivos oficiais:

- `apps/docs/src/app/[lang]/(home)/components/pro-banner.tsx`
- `apps/docs/src/app/[lang]/(home)/components/floating-stars.tsx`
- `apps/docs/src/app/[lang]/(home)/components/pro-title.tsx`
- `apps/docs/src/app/global.css`

Repositório: `https://github.com/heroui-inc/heroui`.

Licença v3 observada: **Apache License 2.0**. A Factory registra o padrão e cria primitive própria. Copiar implementação OSS diretamente para um produto exige manter as obrigações aplicáveis de licença/NOTICE.

## Padrões extraídos

### 1. Multi-layer asynchronous drift

Duas camadas lentas com períodos diferentes são mais naturais que uma camada única ou períodos idênticos. A defasagem reduz a percepção de repetição e cria pseudo-profundidade sem parallax de cursor.

**Decisão:** default de 2 camadas; 3 somente quando espaço e desempenho justificarem.

### 2. Strong by composition, not speed

A referência chama atenção porque combina superfície tonal, glow, partículas e profundidade. O movimento em si é lento.

**Decisão:** intensidade `strong` aumenta presença por área, contraste tonal, densidade moderada e número de profundidades — não por velocidade, flash ou amplitude agressiva.

### 3. Ambient islands

Efeito funciona melhor em regiões com respiro: hero, page header, login, empty state, modal header, área AI e painéis de destaque.

**Decisão:** em telas densas, manter a assinatura no shell/perímetro e colocar tabelas/formulários em ilhas limpas.

### 4. Static depth + moving particles

Blur/glow não precisa se mover para dar vida à superfície; deixar o blur estático reduz custo e mantém a composição estável.

**Decisão:** blobs/glows grandes ficam estáticos por padrão; movimento concentra-se em `transform`/`opacity` de grupos.

## Performance

### web.dev

As recomendações de animação de alta performance priorizam `transform` e `opacity`, porque alterações de layout/paint frequentes são mais caras e podem comprometer fluidez.

**Decisões:**

- animação espacial de partículas via `transform`;
- opacidade apenas quando necessário;
- não animar `top/left/width/height` para drift;
- não animar blur/filter continuamente;
- não usar JS/requestAnimationFrame para loops simples resolvíveis por CSS;
- não criar centenas de partículas DOM independentes;
- mobile recebe menor amplitude/densidade.

Fontes:

- https://web.dev/articles/animations-overview
- https://web.dev/articles/animations-guide
- https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Performance/CSS

## Reduced motion e vestibular

MDN/web.dev recomendam respeitar `prefers-reduced-motion`. W3C/WCAG 2.3.3 permite que motion não essencial acionado por interação seja desabilitado; a orientação cita explicitamente desconforto vestibular e parallax como possíveis problemas.

**Decisão:** reduced motion para `ambient-constellation` não acelera nem apenas encurta o movimento. Ele **para o drift** e mantém fallback visual estático, preservando a identidade da interface.

Fontes:

- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion
- https://web.dev/learn/accessibility/motion
- https://www.w3.org/WAI/WCAG21/Understanding/animation-from-interactions.html

## Flash / blinking

WCAG 2.3.1/2.3.2 limita flashes e reforça que conteúdo piscante pode desencadear reações físicas.

**Decisão:** constelação não usa strobe/blink. Twinkle, quando existir, é lento, de baixa amplitude e não sincronizado. Attention pulse é sistema separado e temporário.

Fontes:

- https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold
- https://www.w3.org/WAI/WCAG22/Understanding/three-flashes.html

## Reduced transparency

MDN documenta `prefers-reduced-transparency` como preferência do usuário, ainda com disponibilidade desigual.

**Decisão:** progressive enhancement. Quando suportado, aumentar opacidade das superfícies de conteúdo e reduzir dependência de glass/blur; não tornar requisito de compatibilidade universal.

Fonte:

- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-transparency

## Motion for React

Motion fornece `useReducedMotion` e configuração global `MotionConfig reducedMotion="user"`, podendo eliminar transform/layout motion mantendo mudanças como opacity/background.

**Decisão:** quando Motion já fizer parte do projeto, usá-lo para entrada/saída e motion semântico. Loops simples de partículas continuam preferindo CSS.

Fontes:

- https://motion.dev/docs/react-use-reduced-motion
- https://motion.dev/docs/react-accessibility

## Ativação de produto

### Solicitação explícita

Os aliases `ambient constellation`, `ambient constellarion`, `ambiente de constelação` e equivalentes ativam `ambient-constellation` com intensidade `strong`.

### HeroUI

Para novos sistemas cujo design system principal seja HeroUI, o perfil passa a ser **default obrigatório**, porque a intenção é tratar essa atmosfera como parte da linguagem visual transversal do produto, não como efeito opcional que o usuário precisa lembrar de pedir.

Exceção explícita ou requisito real pode desligá-lo. Reduced motion reduz movimento, não necessariamente a composição estática.

## Superfícies alvo

Prioridade de aplicação:

1. app shell/background;
2. page headers;
3. hero/welcome;
4. dashboard overview;
5. login/auth;
6. empty/waiting/onboarding;
7. painéis de destaque;
8. modal/drawer importante;
9. AI/assistant welcome/prompt shell;
10. cards/CTAs especiais.

Tabelas, grids e formulários densos ficam em superfícies limpas.

## Decisão final

**ADOTAR** como perfil oficial da App Factory: `ui/AMBIENT_CONSTELLATION_PROFILE.md`.

Integrações obrigatórias:

- `ui/MOTION_POLICY.md`;
- `ui/UI_POLICY.md`;
- `skills/ui-builder/SKILL.md`;
- `ui/heroui/README.md`;
- templates `PRODUCT.md`, `ARCHITECTURE.md`, `AGENTS.md`;
- `scripts/validate_factory.py` para impedir regressão documental;
- `PROJECT_STATE.md` e `CHANGELOG.md` para continuidade.