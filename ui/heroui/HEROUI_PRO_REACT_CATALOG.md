# HeroUI Pro React — Catálogo atual

Snapshot: **2026-08-24**.

Fonte primária: documentação pública oficial `heroui.pro`.

Release pública mais recente encontrada no snapshot: **1.0.0-beta.8 (julho de 2026)**.

## Inventário

A página oficial atual lista **65 componentes React** e **477 variantes/exemplos**.

### Charts — 8 componentes / 53 variantes

| Componente | Variantes |
| --- | ---: |
| Area Chart | 6 |
| Bar Chart | 8 |
| Chart Tooltip | 7 |
| Composed Chart | 5 |
| Line Chart | 10 |
| Pie Chart | 7 |
| Radar Chart | 5 |
| Radial Chart | 5 |

### Data Display — 17 componentes / 126 variantes

| Componente | Variantes |
| --- | ---: |
| Agenda | 1 |
| Action Bar | 2 |
| Carousel | 6 |
| Data Grid | 12 |
| Empty State | 8 |
| File Tree | 11 |
| Floating TOC | 10 |
| Hover Card | 6 |
| Kanban | 4 |
| Item Card | 12 |
| Item Card Group | 12 |
| KPI | 8 |
| KPI Group | 3 |
| List View | 5 |
| Map | 10 |
| Timeline | 8 |
| Widget | 8 |

### AI — 14 componentes / 45 variantes

| Componente | Variantes |
| --- | ---: |
| Chain Of Thought | 4 |
| Chat Attachment | 3 |
| Chat Conversation | 3 |
| Chat List View | 2 |
| Chat Loader | 1 |
| Chat Message | 3 |
| Chat Message Actions | 3 |
| Chat Source | 5 |
| Chat Tool | 6 |
| Code Block | 1 |
| Markdown | 3 |
| Prompt Input | 8 |
| Prompt Suggestion | 2 |
| Text Shimmer | 1 |

### Feedback — 5 componentes / 47 variantes

| Componente | Variantes |
| --- | ---: |
| Emoji Reaction Button | 4 |
| Number Value | 8 |
| Pressable Feedback | 17 |
| Rating | 12 |
| Trend Chip | 6 |

### Layout — 1 componente / 7 variantes

| Componente | Variantes |
| --- | ---: |
| Resizable | 7 |

### Forms — 11 componentes / 96 variantes

| Componente | Variantes |
| --- | ---: |
| Cell Color Picker | 6 |
| Cell Select | 7 |
| Cell Slider | 7 |
| Cell Switch | 7 |
| Checkbox Button Group | 11 |
| Drop Zone | 9 |
| Inline Select | 5 |
| Native Select | 12 |
| Number Stepper | 13 |
| Radio Button Group | 12 |
| Rich Text Editor | 7 |

### Navigation — 7 componentes / 83 variantes

| Componente | Variantes |
| --- | ---: |
| AppLayout | 14 |
| Command | 9 |
| Context Menu | 7 |
| Navbar | 7 |
| Segment | 11 |
| Sidebar | 16 |
| Stepper | 19 |

### Overlays — 2 componentes / 20 variantes

| Componente | Variantes |
| --- | ---: |
| Emoji Picker | 4 |
| Sheet | 16 |

## Templates React completos — 4

### Dashboard

Analytics dashboard com páginas de orders, tracker, settings e help.

Preview oficial: https://template-dashboard.heroui.pro

### Mail

Cliente de e-mail com folders, threads e compose.

Preview oficial: https://template-email.heroui.pro

### Chat

Interface de AI/chat com conversations, library e exploration.

Preview oficial: https://template-chat.heroui.pro

### Finances

Dashboard financeiro com portfolio, spending e transactions.

Preview oficial: https://template-4.heroui.pro

## Pro Themes — 3 atuais documentados

### Brutalism

Tema premium com linguagem brutalista. Disponível em modos light/dark.

### Glass

Tema premium com superfícies/transparência/blur. Disponível em modos light/dark e variável `--glass-blur`.

### Mouve

Tema mauve/warm-purple contemporâneo com tratamento elevado/tátil em superfícies e controles de destaque. Disponível em modos light/dark.

A ativação dos temas usa nomes como `brutalism-light`, `brutalism-dark`, `glass-light`, `glass-dark`, `mouve-light` e `mouve-dark`.

## Design Systems Pro

O recurso oficial `Design Systems` permite:

- importar um site ou começar do zero;
- customizar cores, radius, fonts, shadows e overrides de componentes;
- visualizar mudanças ao vivo;
- manter brand guidance e assets associados;
- exportar Web CSS;
- exportar Native CSS;
- exportar `DESIGN.md`;
- exportar `PRODUCT.md`;
- reutilizar o design system no AI Chat HeroUI.

Para um sistema inteiro na linguagem HeroUI, esta é a referência preferencial quando houver licença Pro.

## Figma Pro

O Pro oferece:

- HeroUI Pro Figma Kit V3;
- HeroUI Pro Native Figma Kit;
- plugin de sincronização de variáveis de tema;
- anatomia/variants/slots alinhados aos componentes Pro.

Os arquivos `.fig` Pro são exclusivos de titulares de licença. Não armazenar cópia deles na App Factory.

## AI tooling oficial

### MCP Server Pro

O MCP oficial Pro cobre HeroUI Pro **e** HeroUI OSS e pode fornecer:

- lista de componentes;
- documentação de componentes;
- CSS/BEM;
- documentação geral;
- source code OSS;
- theme variables e temas `default`, `brutalism`, `glass`, `mouve`;
- import de AI Chat exports;
- import/export de Design Systems.

O source code Pro não é exposto pelo MCP público/licenciado como source browse; obtê-lo apenas pelos mecanismos oficiais autorizados da licença.

### Skills

Skills oficiais Pro:

- `heroui-react-pro` — convenções e padrões de `@heroui-pro/react`;
- `heroui-pro-design-taste` — princípios de design e acabamento HeroUI.

O Design Taste declara **78 princípios em 10 categorias** e se aplica ao ecossistema HeroUI OSS/Pro Web/Native.

## Composição recomendada para um sistema completo

### Shell principal

`AppLayout` + `Sidebar` + `Navbar` + `Command` + `Context Menu` + OSS Breadcrumbs/Tabs.

### Dashboard

`KPI` + `KPI Group` + charts + `Widget` + `Timeline` + `Data Grid`.

### CRUD administrativo

`Data Grid` + `Action Bar` + `Sheet` + OSS Form/TextField/Select/DatePicker + `Cell Select`/`Cell Switch`/`Cell Slider` quando adequados.

### Arquivos/documentos

`File Tree` + `List View` + `Drop Zone` + `Item Card`/`Item Card Group` + `Rich Text Editor`.

### Workflow

`Kanban` + `Agenda` + `Timeline` + `Stepper` + `Segment` + `Action Bar`.

### Assistente/IA

`Chat Conversation` + `Chat Message` + `Chat Message Actions` + `Prompt Input` + `Prompt Suggestion` + `Chat Attachment` + `Chat Source` + `Chat Tool` + `Chain Of Thought` + `Markdown` + `Code Block` + `Chat Loader`.

### Mapas/localização

`Map` + `Hover Card` + `Item Card` + `Sheet`.

## Fontes oficiais

- Components: https://heroui.pro/docs/react/components
- Templates: https://heroui.pro/docs/react/templates
- Getting Started: https://heroui.pro/docs/react/getting-started
- Installation: https://heroui.pro/docs/react/getting-started/installation
- Theming: https://heroui.pro/docs/react/getting-started/theming
- Figma: https://heroui.pro/docs/react/getting-started/figma
- MCP Server: https://heroui.pro/docs/react/getting-started/mcp-server
- Agent Skills: https://heroui.pro/docs/react/getting-started/agent-skills
- Design Taste: https://heroui.pro/docs/react/getting-started/design-taste
- Releases: https://heroui.pro/docs/react/releases

## Licença e propriedade

Este arquivo registra apenas metadados e fatos públicos do catálogo. **Não copiar código, assets, screenshots, Figma ou templates Pro para a Factory.** Em projeto com licença válida, instalar/consultar o conteúdo pelo CLI/MCP/dashboard oficial e respeitar os termos da licença.