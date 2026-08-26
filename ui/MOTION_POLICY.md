# Living UI / Semantic Motion Policy

## Objetivo

Fazer interfaces parecerem vivas, responsivas e naturais sem transformar movimento em decoração obrigatória ou distração.

Esta política é **independente do design system**. HeroUI, shadcn/ui, ReUI, componentes próprios ou outro kit podem ser usados; o comportamento de motion continua sendo uma regra da App Factory.

## Motion Profile

Toda interface deve registrar um Motion Profile.

Perfis disponíveis:

- `none` — remove movimento não essencial; usar somente quando o produto, ambiente ou acessibilidade exigir;
- `subtle` — microinterações e transições discretas, sem atmosfera contínua;
- `ambient` — **default contextual da Factory**: microinterações + movimento semântico + atmosfera viva quando adequada;
- `expressive` — movimento mais presente para landing pages, apresentações, experiências promocionais ou produtos em que motion faça parte da identidade.

Uma preferência explícita do usuário tem precedência. O agente não deve substituir `ambient` por outro perfil apenas por gosto próprio.

## Princípio semântico

Movimento deve comunicar pelo menos uma destas funções:

1. continuidade;
2. resposta à interação;
3. mudança de estado;
4. progressão de dados;
5. hierarquia/atenção;
6. orientação espacial/navegação;
7. atmosfera contextual sem competir com o conteúdo.

Se uma animação não melhora nenhuma dessas funções e só adiciona ruído, ela deve ser removida.

## Categorias

### 1. Ambient

Para cabeçalhos, hero, login, telas de espera, estados vazios e áreas com espaço visual suficiente.

Exemplos:

- gradiente/aurora muito lento;
- luz/halo respirando suavemente;
- partículas discretas quando justificadas pelo produto;
- formas que derivam poucos pixels;
- profundidade/parallax mínimo quando não prejudicar leitura.

Regras:

- baixa a média amplitude;
- velocidade lenta;
- contraste controlado;
- nunca passar por cima do conteúdo principal;
- não usar atmosfera contínua apenas para preencher espaço em telas densas;
- nenhum padrão ambiental específico é obrigatório globalmente.

### 2. Interaction

Elementos interativos devem responder naturalmente ao usuário.

Aplicar quando adequado a:

- botões;
- cards;
- campos;
- menus;
- dropdowns;
- tabs;
- toggles;
- linhas clicáveis;
- controles de gráfico.

Preferir mudanças sutis de escala, elevação, opacidade, brilho ou deslocamento curto. Evitar saltos, bounce excessivo e movimentos que alterem o layout de forma inesperada.

### 3. Data

Gráficos, indicadores, barras, linhas, gauges, números e progresso podem usar motion para tornar mudanças compreensíveis.

Exemplos:

- barras crescendo até o valor;
- linhas sendo reveladas progressivamente;
- valores interpolando entre estado anterior e novo;
- atualização de série sem teletransporte visual;
- destaque temporário do dado que acabou de mudar.

Não reanimar todos os dados a cada pequeno rerender. O movimento deve representar mudança real.

### 4. State

Estados do sistema devem comunicar transição:

- loading;
- saving;
- uploading;
- sincronizando;
- sucesso;
- erro;
- conclusão;
- habilitado/desabilitado.

O usuário deve perceber que o sistema recebeu a ação e em que estado ela está, sem depender apenas de texto estático.

### 5. Attention

Ações ou informações que realmente exigem atenção podem receber movimento mais perceptível.

Exemplos:

- botão de ação pendente;
- badge com item novo;
- erro bloqueante;
- confirmação necessária;
- tarefa aguardando intervenção;
- prazo ou alerta relevante.

Preferir halo, pulso suave, glow ou pequena mudança periódica. **A animação de atenção deve parar, reduzir ou entrar em cooldown quando a atenção já foi obtida**, por exemplo após abrir o aviso ou focar a ação.

Nunca usar blinking agressivo como padrão. Efeitos ambientais não devem ser reutilizados como mecanismo de urgência.

### 6. Navigation

Mudanças de contexto devem preservar continuidade espacial:

- páginas;
- modais;
- drawers/painéis;
- tabs;
- accordions;
- expansão/recolhimento;
- navegação interna.

Entrada e saída devem ser curtas, previsíveis e coerentes com a direção da interface.

## Adaptação automática ao contexto

`ambient` é o default, não uma obrigação cega de manter partículas ou auroras em toda tela.

O agente pode reduzir automaticamente a intensidade para `subtle` ou equivalente local quando houver:

- leitura longa;
- tabela/dashboard muito denso;
- alta frequência de atualização de dados;
- hardware ou contexto com desempenho limitado;
- múltiplas animações competindo ao mesmo tempo;
- tarefa em que movimento atrapalhe precisão/concentração;
- preferência do sistema/usuário por movimento reduzido.

A identidade Living UI continua presente por microinterações, estados e transições mesmo quando o ambiente contínuo for reduzido.

## Acessibilidade

`prefers-reduced-motion` é obrigatório em interfaces com animação não essencial.

Quando movimento reduzido estiver ativo:

- remover/parar loops ambientes e parallax;
- eliminar grandes deslocamentos/zoom;
- reduzir transições a fades ou mudanças instantâneas quando necessário;
- manter feedback funcional de estado sem depender somente da animação;
- não esconder informação por causa da redução de motion.

Quando `prefers-reduced-transparency` estiver disponível, usar como progressive enhancement para tornar superfícies de conteúdo mais opacas e reduzir dependência de glass/blur.

Animação nunca substitui contraste, texto, ícone, foco ou outro sinal acessível necessário.

Nenhuma primitive ambiental pode usar strobe/blinking. Evitar qualquer flash; em todos os casos respeitar WCAG Three Flashes.

## Performance

- preferir `transform` e `opacity` quando possível;
- evitar animar propriedades que causem layout/reflow/repaint contínuo sem necessidade;
- limitar partículas/camadas e loops concorrentes;
- manter blur/glow grande estático sempre que possível;
- agregar partículas em SVG/camadas em vez de animar muitos nós individualmente;
- não manter animações fora da viewport quando isso gerar custo relevante;
- testar em viewport móvel;
- reduzir densidade/amplitude em mobile;
- usar `will-change` somente em elementos realmente animados;
- medir quando houver suspeita de impacto em fluidez, bateria ou tempo de interação.

Uma interface viva que engasga viola esta política.

## Design systems e bibliotecas

O Motion Profile não autoriza misturar bibliotecas visuais.

Ordem de preferência:

1. usar motion já suportado pelo design system vigente;
2. usar CSS/transições nativas quando suficientes;
3. adicionar biblioteca de motion especializada somente quando a complexidade justificar;
4. não instalar outro design system apenas para obter um efeito.

HeroUI, shadcn, ReUI ou qualquer outro sistema devem conservar sua coerência visual enquanto esta política define **como a interface se move**.

## Registro no projeto

Projetos com UI devem registrar pelo menos:

```text
Motion Profile: ambient | subtle | expressive | none
```

Efeitos ambientais específicos, quando existirem por decisão do produto, devem ser documentados no próprio projeto; a Factory não impõe um efeito visual global.

## Verificação

Para concluir trabalho relevante de UI, verificar quando aplicável:

- motion coerente com o perfil escolhido;
- ação principal responde ao usuário;
- estados assíncronos têm feedback;
- sinais de atenção não ficam pulsando indefinidamente;
- gráficos/dados não reanimam sem mudança real;
- desktop e mobile;
- `prefers-reduced-motion`;
- ausência de flashing/strobe;
- ausência de jank, overflow ou conteúdo obstruído;
- motion não impede leitura, foco ou interação.
