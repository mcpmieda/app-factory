---
name: ui-builder
description: Escolhe e aplica padrões de interface modernos para páginas, dashboards e sistemas, priorizando reutilização, consistência visual, Professional UI, Living UI/Semantic Motion, Ambient Constellation e uso seletivo de shadcn, ReUI ou HeroUI conforme o tipo de aplicação.
---

# UI Builder

## Decisão do design system

1. Para sistemas administrativos, CRUDs, dashboards e ferramentas internas: usar **shadcn/ui como base**, salvo preferência explícita do produto por HeroUI.
2. Usar **ReUI seletivamente** quando um componente administrativo avançado reduzir trabalho e justificar dependências/complexidade.
3. Após instalar ReUI/registry, auditar arquivos e dependências adicionados e remover módulos não usados.
4. Considerar **HeroUI** como alternativa principal em aplicações onde seu sistema visual ofereça vantagem clara.
5. Quando o usuário pedir um sistema **baseado em HeroUI/HeroUI Pro**, tratar HeroUI como linguagem transversal do produto; não misturar shadcn/ReUI apenas para variedade visual.
6. Quando o projeto seguir o perfil `web-admin`, consultar `profiles/web-admin/PROFILE.md`.

A seleção da biblioteca e o acabamento profissional são decisões diferentes: shadcn/ReUI continuam preferenciais no admin **quando não existe uma escolha explícita de HeroUI**. Uma solicitação explícita de sistema HeroUI prevalece sobre esse default.

## Catálogo HeroUI obrigatório quando HeroUI for selecionado

Antes de criar componente, tela ou padrão próprio em um projeto HeroUI, ler `ui/heroui/README.md` e consultar o catálogo adequado:

- `ui/heroui/HEROUI_REACT_V3_CATALOG.md` — HeroUI React OSS atual;
- `ui/heroui/HEROUI_PRO_REACT_CATALOG.md` — HeroUI Pro React atual, variantes, templates, themes e tooling;
- `ui/heroui/HEROUI_NATIVE_CATALOG.md` — HeroUI Native OSS + Pro Native;
- `ui/heroui/HEROUI_PRO_V2_VISUAL_ARCHIVE.md` — repertório visual legado do Pro v2;
- `ui/heroui/OFFICIAL_SOURCES.md` — documentação, GitHub, Storybook, CLI, MCP, Skills e Figma oficiais;
- `ui/heroui/CATALOG_AUDIT_2026-08-24.md` — diferenças entre catálogo documentado e exports públicos.

Regras:

1. pesquisar no catálogo e na fonte oficial antes de recriar capacidade existente;
2. para projetos novos Web, preferir HeroUI v3 atual; usar v2 somente como repertório visual/funcional;
3. confirmar versão/release atual antes de instalar ou depender de uma API;
4. quando houver licença HeroUI Pro válida no projeto, preferir CLI/MCP/Skills oficiais para obter conteúdo autorizado;
5. nunca armazenar token Pro, código Pro, assets, screenshots, Figma ou templates comerciais na Factory;
6. sem licença Pro, usar nomes/padrões públicos como referência e implementar com HeroUI OSS ou componente local compatível;
7. manter HeroUI em shell, formulários, dados, overlays, estados, motion, tokens e temas — não só em cards/botões.

## Ambient Constellation — regra forte

Antes de implementar atmosfera visual, ler `ui/AMBIENT_CONSTELLATION_PROFILE.md`.

### Ativação por prompt

Se o usuário disser `ambient constellation`, `ambient constellarion`, `ambiente de constelação`, `ambiente constelar` ou equivalente inequívoco:

```text
Motion Profile: ambient
Ambient Surface Profile: ambient-constellation
Constellation Intensity: strong
Particle scale: micro, screen-space bounded
```

Aplicar fortemente às superfícies existentes listadas no perfil: shell/background, page header, hero/welcome, dashboard overview, login/auth, empty/waiting/onboarding, painéis de destaque, modal/drawer importante, AI/assistant e cards/CTA especiais.

### HeroUI nativo

Se **HeroUI for o design system principal de um sistema novo**, ativar `ambient-constellation strong` automaticamente. Não perguntar se o usuário quer o efeito e não exigir que ele o mencione em prompts futuros.

Exceções somente por:

- opt-out explícito;
- identidade de marca incompatível;
- restrição material de plataforma/desempenho;
- acessibilidade.

Mesmo em tela densa, não apagar toda a assinatura. Colocar tabelas/forms/grids em ilhas limpas e manter constelação no shell/header/perímetro. Com reduced motion, congelar o campo em composição estática em vez de simplesmente remover a identidade visual.

### Como tornar perceptível sem atrapalhar

- pelo menos duas profundidades/camadas em superfícies fortes;
- períodos lentos diferentes e não sincronizados;
- glow grande e preferencialmente estático;
- **micro-partículas**, normalmente em torno de `0.6–1.5 CSS px`, com raros glints maiores;
- presença por composição, densidade e área, não por diâmetro ou velocidade;
- campo maior que a área visível e recortado, aproximadamente `1.25–1.45×` em largura e `1.55–1.90×` em altura como referência;
- baseline HeroUI Pro: drift visual aproximadamente `20px`, ciclos de `12s` e `15s` em direções opostas;
- nenhuma partícula sobre conteúdo interativo ou texto denso;
- `pointer-events: none`, decoração fora da árvore acessível;
- CSS `transform`/`opacity` para loops simples;
- evitar cursor/scroll parallax por padrão;
- zero strobe/blinking.

**Nunca** usar um campo SVG `0 0 100 100` em tela cheia com círculos de raio próximo a `1`, nem qualquer modelagem que faça os pontos crescerem proporcionalmente à viewport. Se os pontos parecem bolhas/círculos voadores em zoom 100%, a implementação falhou mesmo que a intensidade esteja configurada como `strong`.

## Professional UI Profile

Antes de implementar UI funcional destinada a usuário final, ler `ui/PROFESSIONAL_UI_PROFILE.md`.

Default da Factory: `professional-default`.

O perfil define o quality bar, não o pacote que deve ser instalado.

Derivar automaticamente quando possível:

- density: `compact`, `comfortable` ou `spacious`;
- surface: `flat`, `layered` ou `immersive`;
- emphasis: `quiet`, `balanced` ou `bold`.

Defaults comuns:

- admin/data-heavy: `comfortable + layered + balanced`;
- produto visual: `spacious + layered/immersive + balanced/bold`;
- mobile utilitário: `comfortable + flat/layered + balanced`.

Não perguntar ao usuário detalhes de radius, spacing, shadow, density ou animação quando puderem ser derivados do produto.

### Inventário antes da implementação

Para UI média/grande, identificar os arquétipos que realmente existem antes de construir componentes:

```text
shell
page-header
stats
search/command
filters
data-view (table/grid/list)
form
detail/inspector
modal/drawer
navigation/tabs
feedback
empty/error/loading
calendar/kanban/chart — somente se necessário
```

Pesquisar primeiro no design system/registry atual. Não criar componente próprio quando a biblioteca já oferecer composição equivalente.

### Regras de acabamento

- hierarquia perceptível antes de cor/motion;
- escala curta e coerente de tipografia;
- spacing por tokens, não valores aleatórios;
- poucos níveis de superfície/elevação;
- um CTA primário claro por contexto;
- cor semântica e contraste funcional;
- densidade compatível com a tarefa;
- progressive disclosure para informação/ações secundárias;
- estados completos, não apenas happy path;
- versão móvel reorganizada, não desktop simplesmente comprimido;
- microcopy orientada à tarefa e recovery;
- evitar excesso de cards, glow/gradiente sem função, múltiplos CTAs e mistura de design systems.

### Origem/licença

Referências comerciais como HeroUI Pro podem inspirar padrões públicos de composição e linguagem visual. Não copiar código, templates, assets ou screenshots proprietários para a Factory sem licença específica.

A referência de `ambient-constellation` vem do site/repositório OSS HeroUI v3. A Factory prefere primitive própria; se código OSS for copiado diretamente para um projeto, cumprir a licença aplicável e NOTICE quando exigido.

## Motion Profile

Antes de implementar UI relevante, ler `ui/MOTION_POLICY.md`.

Default contextual da Factory: `ambient`.

Perfis disponíveis: `none`, `subtle`, `ambient`, `expressive`.

Aplicar movimento semanticamente quando adequado:

- **ambient**: atmosfera contextual, incluindo `ambient-constellation` quando ativo;
- **interaction**: hover, foco, clique, cards, campos, menus;
- **data**: gráficos, indicadores, progresso e mudanças reais de valor;
- **state**: loading, saving, upload, sync, sucesso e erro;
- **attention**: ações pendentes/importantes com halo/pulso discreto e temporário;
- **navigation**: páginas, modais, drawers, tabs e expansão/recolhimento.

Não manter animação de atenção depois que o usuário já percebeu/interagiu. Não reanimar dados sem mudança real.

`prefers-reduced-motion` é obrigatório. Para constelação, usar fallback estático. `prefers-reduced-transparency` pode ser progressive enhancement.

## Antes de construir

- pesquisar componentes, blocks e registries adequados;
- consultar documentação/MCP disponível quando o agente puder;
- preferir composição de componentes consolidados a recriação manual;
- verificar licença e dependências antes de importar código externo;
- verificar primeiro se o design system atual já oferece o padrão necessário;
- registrar `professional-default`/exceção, Motion Profile e Ambient Surface Profile quando ativos.

## Qualidade visual

Evitar aparência genérica de app gerado por IA. Usar hierarquia clara, espaçamento consistente, tipografia coerente, densidade adequada, estados completos e motion proporcional.

Uma interface viva não significa movimento em tudo. Conteúdo principal deve permanecer legível e estável.

Em HeroUI, a constelação deve ser uma assinatura visual recorrente e reconhecível; áreas densas ficam limpas por composição, não por abandono completo da assinatura. A referência de escala é de **poeira luminosa**, não de círculos decorativos.

## Regra de sistema

Não redesenhar por impulso componentes estáveis já existentes. Em manutenção, preservar design system, Professional UI Profile, Motion Profile e Ambient Surface Profile vigentes salvo redesign explícito ou problema real.

## Verificação

UI não é validada apenas por leitura de código. Quando possível, abrir a aplicação e testar visualmente/interativamente em desktop e mobile.

Também verificar quando aplicável:

- hierarquia e densidade do `professional-default`;
- loading/empty/error e ação destrutiva;
- coerência com Motion Profile;
- `ambient-constellation` perceptível onde exigido;
- **maior partícula típica ≤ 2 CSS px em desktop e ≤ 1.5 CSS px em mobile**, salvo exceção explícita;
- nenhum ponto recorrente parece bolha/círculo voador;
- partículas não bloqueiam interação;
- dense content continua limpo;
- `prefers-reduced-motion` gera fallback estático;
- teclado/foco;
- animações de atenção encerram/reduzem;
- ausência de strobe/flashing;
- gráficos sem reanimação artificial;
- ausência de jank, overflow ou conteúdo obstruído;
- screenshot regression somente com baseline estável e risco material.
