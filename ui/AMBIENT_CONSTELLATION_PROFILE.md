# Ambient Constellation Profile

## Objetivo

`ambient-constellation` é a assinatura ambiental reutilizável da App Factory para interfaces vivas com linguagem de constelação: gradientes frios/brand-aware, glows difusos e camadas de partículas/estrelas que derivam lentamente em velocidades diferentes.

O efeito deve ser **claramente perceptível pelo usuário**, mas continuar atrás da tarefa. Ele cria profundidade e identidade sem competir com leitura, foco, navegação ou dados.

## Ativação

### Ativação explícita

Tratar como solicitação deste perfil quando o usuário pedir termos como:

- `ambient constellation`;
- `ambient constellarion`;
- `ambiente de constelação`;
- `ambiente constelar`;
- `constellation ambient`;
- referência inequívoca ao cabeçalho/modal HeroUI Pro com estrelas flutuantes.

Quando houver ativação explícita:

```text
Ambient Surface Profile: ambient-constellation
Constellation Intensity: strong
Motion Profile: ambient, salvo preferência explícita mais restritiva
```

Não pedir ao usuário que escolha densidade, amplitude, blur ou velocidade quando puderem ser inferidos.

### HeroUI obrigatório por padrão

Quando **HeroUI for o design system principal de um sistema novo**, `ambient-constellation` é obrigatório por padrão e deve vir nativamente, sem o usuário precisar pedir.

Exceções legítimas:

- o usuário pedir explicitamente para não usar constelação;
- requisito de marca/produto incompatível;
- restrição material de desempenho/plataforma;
- contexto de acessibilidade que exija reduzir movimento.

Mesmo em `prefers-reduced-motion: reduce`, preservar a identidade constelar com composição **estática** sempre que possível; reduzir movimento não significa apagar automaticamente gradiente, estrelas e profundidade visual.

## DNA visual

A referência pública principal é o banner/modal HeroUI Pro no repositório OSS `heroui-inc/heroui`, que combina:

- superfície clara azul/lilás;
- blob/glow ciano→violeta fortemente desfocado;
- partículas brancas com diferentes tamanhos e opacidades;
- duas camadas de estrelas em drift diagonal oposto;
- ciclos diferentes, evitando sincronização visual;
- conteúdo em camada superior, com partículas sem interação.

Parâmetros observados na implementação oficial em 2026-08-24, usados como **baseline de comportamento**, não como obrigação de copiar valores literalmente:

- base aproximada: `#E9E9FF → #CCE5F1`;
- glow aproximado: `#5DD0E7 → #7300FF`;
- drift A: ~12 s, deslocamento diagonal de ~40 px e retorno;
- drift B: ~15 s, direção oposta e retorno;
- easing: `ease-in-out`;
- partículas com opacidades variadas e baixa dominância;
- overflow recortando um campo de estrelas maior que a superfície visível.

O repositório HeroUI v3 está sob Apache-2.0. Se um projeto copiar código OSS diretamente, cumprir os requisitos de licença/NOTICE. A Factory prefere uma primitive própria baseada nos padrões gerais, para facilitar branding e portabilidade.

## Composição obrigatória

Uma superfície `ambient-constellation` forte deve possuir, quando a plataforma permitir:

1. **base tonal** — gradiente ou superfície temática coerente com a marca;
2. **glow/blob grande** — difuso, estático ou quase estático, sem borda dura;
3. **camada de partículas A** — drift lento;
4. **camada de partículas B** — velocidade diferente e direção contrária/defasada;
5. **conteúdo foreground** — legível, estável e separado do efeito;
6. **overflow/mask** — partículas entram/saem naturalmente da área visível;
7. **fallback estático** — para reduced motion/performance.

Não depender de estrelas perfeitas. Pontos, pequenos glints, microcruzes e partículas suaves podem coexistir; evitar confete, neve ou aparência de screensaver.

## Intensidade `strong`

`strong` significa presença visual inequívoca, não movimento rápido.

A percepção deve vir de:

- contraste tonal suficiente entre base e glow;
- campo de partículas visível à primeira observação;
- pelo menos duas profundidades/camadas;
- composição ocupando área visual relevante;
- períodos longos e não sincronizados;
- pequenas diferenças de tamanho/opacidade entre partículas;
- reforço em superfícies-chave do produto.

Evitar tornar `strong` por:

- acelerar partículas;
- aumentar drasticamente amplitude;
- piscar/twinkle rápido;
- colocar estrelas sobre texto e controles;
- usar saturação extrema em toda a viewport.

## Cobertura por superfície

Quando o perfil estiver ativo, aplicar **fortemente** às superfícies que existirem no produto:

| Superfície | Regra |
| --- | --- |
| App shell/background | camada persistente de baixa/média densidade, sem interferir no conteúdo |
| Cabeçalho/page header | constelação média/forte, preferencialmente uma das assinaturas principais |
| Boas-vindas/hero | forte |
| Dashboard overview/summary | forte na área de síntese; não atrás de tabelas densas |
| Login/auth | forte, especialmente painel visual/background |
| Empty/waiting/onboarding | média/forte |
| Painel de destaque/announcement | média/forte |
| Modal/drawer importante | cabeçalho/faixa visual média/forte |
| Área de IA/assistant | forte em welcome/empty/prompt shell; atenuar em conversa longa |
| Cards especiais/CTA de destaque | seletiva, média; evitar repetir em todos os cards |
| Data Grid/tabela/formulário denso | superfície interna limpa; constelação pode permanecer no shell/perímetro |
| Sidebar/nav densa | no máximo eco tonal/glow discreto; não cobrir labels com partículas |

### Regra de continuidade HeroUI

Em um sistema HeroUI, não desligar a constelação de uma tela inteira apenas porque há dados densos. **Isole os dados em superfícies limpas e mantenha a assinatura no shell, cabeçalho, bordas ou zonas de respiro.**

## Motion pattern

### Multi-layer asynchronous drift

Default recomendado:

- 2 camadas animadas; 3 apenas quando houver espaço/performance;
- ciclos diferentes, por exemplo `12–18s` e `15–24s`;
- amplitude desktop típica `24–48px`;
- amplitude mobile típica `12–28px`;
- trajetórias diagonais ou curvas simples;
- direções opostas ou fases diferentes;
- `ease-in-out` ou easing suave equivalente;
- retorno contínuo sem salto visível.

A diferença entre períodos cria pseudo-parallax e reduz a sensação de loop mecânico.

### Twinkle

Não é obrigatório. Quando usado:

- muito lento;
- baixa variação de opacidade;
- sem sincronizar grandes grupos;
- nunca parecer flash/blink;
- não usar como mecanismo principal de atenção.

### Pointer/scroll parallax

Não usar por padrão. Só adicionar em perfil `expressive` ou experiência específica, porque movimento relativo ao cursor/scroll pode aumentar distração e desconforto vestibular. Deve desaparecer com reduced motion.

## Implementação preferida

### Web

Preferir:

1. SVG ou pseudo-elementos para campo visual;
2. animação CSS de grupos por `transform` e, quando necessário, `opacity`;
3. blur/glow **estático**; não animar blur continuamente;
4. `pointer-events: none` e `aria-hidden="true"` para decoração;
5. conteúdo em stacking context superior;
6. `overflow: hidden|clip` na superfície;
7. primitive reutilizável em vez de dezenas de partículas DOM independentes.

Não usar `requestAnimationFrame` para um drift simples que CSS resolve. Não animar `top/left/width/height`, background-position pesado ou propriedades que provoquem layout/repaint contínuo sem necessidade.

### React/Motion

Motion pode controlar entrada/saída do container, modais e transições semânticas. Para o loop de partículas, CSS continua preferível quando suficiente.

Se Motion for usado, configurar reduced motion no nível da aplicação (`MotionConfig reducedMotion="user"` ou estratégia equivalente) e/ou `useReducedMotion` para trocar deslocamento por composição estática/fade.

## Acessibilidade

### Reduced motion — obrigatório

Com `prefers-reduced-motion: reduce`:

- parar drift/parallax/loops espaciais;
- manter constelação estática ou reduzir para glow + partículas imóveis;
- entrada de modal pode virar fade curto/instantâneo;
- não remover informação funcional;
- manter foco, contraste e estados independentes do movimento.

### Reduced transparency — progressive enhancement

Quando `prefers-reduced-transparency: reduce` estiver disponível:

- reduzir transparência extrema;
- tornar painéis de conteúdo mais opacos;
- diminuir dependência de glass/blur para contraste.

### Flash e atenção

- nenhum efeito pode piscar mais de 3 vezes por segundo;
- a primitive de constelação **não usa strobe/blinking**;
- attention motion de CTA é separado do ambiente e deve parar/reduzir após cumprir sua função.

## Performance

Regras:

- animar principalmente `transform`/`opacity`;
- limitar a 2 grupos animados por superfície como default;
- partículas ficam agregadas em SVG/camadas, não dezenas/centenas de nós animados individualmente;
- blur grande é estático e limitado à superfície;
- reduzir densidade/amplitude em mobile;
- evitar vários ambientes fortes simultâneos na mesma viewport;
- pausar/remover loops fora da viewport quando o custo for material;
- não usar `will-change` indiscriminadamente; reservar para elementos realmente animados;
- verificar jank e uso de CPU em hardware/viewport representativos quando o efeito cobrir grande área.

## Cores e temas

A constelação é um **padrão**, não uma paleta fixa.

Presets conceituais:

- `cool-light`: azul gelo + ciano + violeta, próximo à referência HeroUI;
- `deep-space`: fundo escuro/azul-noite + glows azul/violeta;
- `brand-tinted`: usa tokens da marca preservando diferenças de luminância;
- `glass-constellation`: para tema Glass, com estrelas fora/atrás da superfície translúcida;
- `mouve-constellation`: adapta glows a mauve/violeta quente;
- `brutal-constellation`: mantém estrelas, mas reduz blur e usa formas mais duras/geométricas.

Em HeroUI, preferir tokens/variables do tema e não hardcode de azul em todas as páginas.

## Anti-padrões

Rejeitar:

- partículas sobre campos/tabela/texto;
- estrelas cobrindo toda a aplicação com a mesma intensidade;
- todos os cards com constelação;
- partículas rápidas;
- loops sincronizados;
- glow saturado atrás de texto sem contraste;
- blur animado continuamente;
- canvas/WebGL para um efeito simples que SVG/CSS resolve;
- cursor-follow/parallax como default;
- efeito que some completamente em telas densas de um sistema HeroUI;
- reduced motion implementado apenas reduzindo duração (isso pode tornar movimento mais brusco).

## QA / Definition of Done

Quando `ambient-constellation` estiver ativo, verificar:

- efeito perceptível em 1–2 segundos sem precisar procurar por ele;
- conteúdo continua sendo o foco principal;
- no mínimo duas profundidades visuais nas superfícies fortes;
- períodos não sincronizados;
- nenhuma partícula intercepta clique/hover/foco;
- nenhuma mudança de layout causada pelo loop;
- tabelas/formulários densos continuam limpos;
- desktop e mobile;
- light/dark quando suportados;
- `prefers-reduced-motion` produz fallback estático adequado;
- `prefers-reduced-transparency` melhora legibilidade quando suportado;
- teclado/foco continuam normais;
- nenhuma animação de flash/strobe;
- console sem erro;
- sem jank perceptível; medir quando houver dúvida;
- screenshots antes/depois quando houver baseline visual estável.

## Registro no projeto

Quando ativo, registrar:

```text
Motion Profile: ambient
Ambient Surface Profile: ambient-constellation
Constellation Intensity: strong
Dense content: clean islands; constellation remains in shell/header/perimeter
Reduced motion: static constellation fallback
```

Para HeroUI novo, esses valores são inferidos automaticamente salvo exceção explícita.

## Fontes de engenharia

Referências usadas para esta política:

- HeroUI OSS `pro-banner.tsx`, `floating-stars.tsx`, `pro-title.tsx` e `global.css` — padrão visual/motion público do banner Pro;
- HeroUI v3 license — Apache-2.0;
- web.dev — high-performance CSS animations: priorizar `transform` e `opacity`;
- MDN — `prefers-reduced-motion` e otimização de animações;
- MDN — `prefers-reduced-transparency` como progressive enhancement;
- W3C/WCAG — Animation from Interactions e Three Flashes;
- Motion for React — `useReducedMotion` e `MotionConfig`.

URLs e inventário HeroUI ficam em `ui/heroui/OFFICIAL_SOURCES.md`.