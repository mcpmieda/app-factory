# Ambient Constellation Profile

## Objetivo

`ambient-constellation` é a assinatura ambiental reutilizável da App Factory para interfaces vivas com linguagem de constelação: gradientes frios/brand-aware, glows difusos e camadas de micro-partículas/estrelas que derivam lentamente em velocidades diferentes.

O efeito deve ser **claramente perceptível pelo usuário**, mas continuar atrás da tarefa. Ele cria profundidade e identidade sem competir com leitura, foco, navegação ou dados.

> Regra central: presença forte vem de **área, densidade, profundidade e glow**, não de partículas grandes. Em escala normal de tela, a constelação deve parecer poeira luminosa/microestrelas, nunca círculos voadores.

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
- partículas brancas muito pequenas com diferentes opacidades;
- duas camadas de estrelas em drift diagonal oposto;
- ciclos diferentes, evitando sincronização visual;
- conteúdo em camada superior, com partículas sem interação.

### Calibração proporcional da referência oficial — 2026-08-25

A inspeção da implementação oficial atual mostrou um detalhe que deve ser preservado na Factory:

- card/modal: `288px` de largura;
- faixa visual superior: `180px` de altura;
- primitive `FloatingStars`: aproximadamente `760.706 × 637.702px`;
- o campo inteiro é centralizado e renderizado dentro de `scale-50` antes do recorte;
- portanto, antes do clipping, o campo efetivo fica em aproximadamente `380 × 319px`, ou cerca de **1,32× a largura e 1,77× a altura** da área visível;
- as estrelas usam um SVG `709.134 × 573.351` com glints muito pequenos; muitas partículas recebem opacidade `0.11` ou `0.3` dentro de um grupo com opacidade `0.7`;
- drift A: `12s`, ida de aproximadamente `40px` em X/Y e retorno;
- drift B: `15s`, direção oposta e retorno;
- como o conjunto é exibido em `scale-50`, a amplitude visual observada fica aproximadamente na ordem de **20px**, não 40px;
- o efeito final é de micro-pontos/poeira luminosa, sem discos grandes perceptíveis.

Essas proporções são **baseline de comportamento**, não uma obrigação de copiar o SVG oficial.

### Regra de escala das partículas

Para superfícies web comuns:

- maioria das partículas: aproximadamente `0.6–1.2 CSS px` de diâmetro percebido;
- partículas secundárias: aproximadamente `1.2–1.5 CSS px`;
- glints raros podem chegar a aproximadamente `1.8 CSS px`, mas não devem formar discos dominantes;
- mobile: preferir `0.5–1.3 CSS px`;
- evitar qualquer partícula recorrente acima de `2 CSS px` salvo efeito específico e deliberado;
- variar principalmente **opacidade**, não tamanho.

Nunca dimensionar o raio da partícula como porcentagem direta da viewport. Em especial, evitar SVG de `viewBox="0 0 100 100"` ocupando a tela inteira com círculos de `r≈1`: em uma viewport grande isso pode virar discos de dezenas de pixels.

### Regra de overscan/crop

O campo de estrelas deve ser maior do que a superfície e depois recortado. Como baseline:

- largura do campo: aproximadamente `1.25–1.45×` a área visível;
- altura do campo: aproximadamente `1.55–1.90×` a área visível;
- centralizar/offsetar o campo para que partículas entrem e saiam naturalmente;
- nunca ampliar as próprias partículas para conseguir presença visual.

## Composição obrigatória

Uma superfície `ambient-constellation` forte deve possuir, quando a plataforma permitir:

1. **base tonal** — gradiente ou superfície temática coerente com a marca;
2. **glow/blob grande** — difuso, estático ou quase estático, sem borda dura;
3. **camada de micro-partículas A** — drift lento;
4. **camada de micro-partículas B** — velocidade diferente e direção contrária/defasada;
5. **conteúdo foreground** — legível, estável e separado do efeito;
6. **overscan + overflow/mask** — campo maior que a área e recortado;
7. **fallback estático** — para reduced motion/performance.

Não depender de estrelas perfeitas. Pontos, pequenos glints e microcruzes podem coexistir; evitar confete, neve, bolhas ou aparência de screensaver.

## Intensidade `strong`

`strong` significa presença visual inequívoca, não movimento rápido nem partículas grandes.

A percepção deve vir de:

- contraste tonal suficiente entre base e glow;
- **densidade de micro-pontos**, não diâmetro de pontos;
- campo de partículas visível à primeira observação;
- pelo menos duas profundidades/camadas;
- composição ocupando área visual relevante;
- períodos longos e não sincronizados;
- pequenas diferenças de opacidade/tamanho entre partículas;
- reforço em superfícies-chave do produto.

Evitar tornar `strong` por:

- acelerar partículas;
- aumentar drasticamente amplitude;
- aumentar diâmetro até os pontos parecerem círculos;
- piscar/twinkle rápido;
- colocar estrelas sobre texto e controles;
- usar saturação extrema em toda a viewport.

## Cobertura por superfície

Quando o perfil estiver ativo, aplicar **fortemente** às superfícies que existirem no produto:

| Superfície | Regra |
| --- | --- |
| App shell/background | camada persistente de baixa/média densidade, micro-partículas discretas, sem interferir no conteúdo |
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

Default recomendado, calibrado para a referência HeroUI:

- 2 camadas animadas; 3 apenas quando houver espaço/performance;
- baseline preferencial: aproximadamente `12s` e `15s`;
- faixa aceitável: `12–18s` e `15–24s`;
- amplitude visual desktop típica: `14–24px`;
- amplitude visual mobile típica: `8–16px`;
- usar amplitudes maiores somente em superfícies muito grandes e sempre preservando movimento lento;
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

1. SVG agregado ou camada única de micro-pontos posicionados; se usar DOM, animar o **grupo**, não cada partícula;
2. partículas com tamanho final em screen-space controlado, sem escalar diretamente com viewport;
3. animação CSS de grupos por `transform` e, quando necessário, `opacity`;
4. blur/glow **estático**; não animar blur continuamente;
5. `pointer-events: none` e `aria-hidden="true"` para decoração;
6. conteúdo em stacking context superior;
7. `overflow: hidden|clip` na superfície;
8. campo de estrelas maior que a área visível e recortado;
9. primitive reutilizável em vez de dezenas de partículas animadas individualmente.

Não usar `requestAnimationFrame` para um drift simples que CSS resolve. Não animar `top/left/width/height`, background-position pesado ou propriedades que provoquem layout/repaint contínuo sem necessidade.

### SVG — regra preventiva

Se SVG for usado:

- não usar `preserveAspectRatio="none"` em um campo de círculos quando isso transformar pontos em elipses ou ampliar o raio de forma inesperada;
- preferir coordenadas/geometry que mantenham o tamanho percebido em aproximadamente 0.5–1.8 CSS px;
- validar visualmente o maior ponto na viewport real;
- `vector-effect="non-scaling-stroke"` não impede que `r`/geometria preenchida escale: não tratá-lo como proteção de tamanho.

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
- partículas ficam agregadas em SVG/camadas ou em grupos estáticos, não dezenas/centenas de nós animados individualmente;
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

- partículas grandes o bastante para parecerem círculos/bolhas;
- raio em `%`, `vw`, `vh` ou unidade de viewBox pequeno que resulte em tamanho dependente da viewport;
- campo `viewBox 0 0 100 100` ocupando a viewport com `r≈1` para estrelas;
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
- **nenhuma partícula recorrente parece um círculo voador**;
- maior partícula visual típica `≤ 2 CSS px` em desktop e `≤ 1.5 CSS px` em mobile, salvo exceção deliberada documentada;
- densidade/overscan suficientes para manter a assinatura mesmo com partículas pequenas;
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

### Teste visual de escala obrigatório

Em pelo menos uma viewport desktop e uma mobile:

1. observar a tela em 100% de zoom;
2. confirmar que os pontos leem como poeira/estrelas, não bolhas;
3. comparar a relação partícula/superfície com a referência HeroUI Pro;
4. confirmar que a força visual vem do glow + quantidade + camadas;
5. se um ponto individual chama mais atenção que o conteúdo sem ser um glint deliberado, reduzir tamanho/opacidade antes de aprovar.

## Registro no projeto

Quando ativo, registrar:

```text
Motion Profile: ambient
Ambient Surface Profile: ambient-constellation
Constellation Intensity: strong
Particle scale: micro, screen-space bounded
Dense content: clean islands; constellation remains in shell/header/perimeter
Reduced motion: static constellation fallback
```

Para HeroUI novo, esses valores são inferidos automaticamente salvo exceção explícita.

## Fontes de engenharia

Referências usadas para esta política:

- HeroUI OSS `pro-banner.tsx`, `floating-stars.tsx`, `pro-title.tsx` e `global.css` — padrão visual/motion público do banner Pro;
- inspeção da implementação oficial em 2026-08-25 — card 288px, hero 180px, `FloatingStars` 760.706×637.702 em `scale-50`, drift 12s/15s e micro-opacidades;
- HeroUI v3 license — Apache-2.0;
- web.dev — high-performance CSS animations: priorizar `transform` e `opacity`;
- MDN — `prefers-reduced-motion` e otimização de animações;
- MDN — `prefers-reduced-transparency` como progressive enhancement;
- W3C/WCAG — Animation from Interactions e Three Flashes;
- Motion for React — `useReducedMotion` e `MotionConfig`.

URLs e inventário HeroUI ficam em `ui/heroui/OFFICIAL_SOURCES.md`.