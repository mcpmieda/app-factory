# HeroUI / HeroUI Pro — Auditoria de catálogo

Data: **2026-08-24**

## Escopo

Comparação cruzada entre:

1. páginas oficiais atuais `heroui.com`;
2. páginas oficiais atuais `heroui.pro`;
3. catálogo legado público `v2.heroui.pro`;
4. exports dos repositórios públicos `heroui-inc/heroui` e `heroui-inc/heroui-native`;
5. arquivos `ui/heroui/` da App Factory.

A auditoria distingue **componente top-level documentado**, **módulo público exportado**, **template**, **tema/tooling** e **repertório legado**. Não somar essas categorias como se fossem a mesma coisa.

# 1. HeroUI React v3 OSS

## Catálogo oficial `All Components` — 71

### Buttons
Button; ButtonGroup; CloseButton; ToggleButton; ToggleButtonGroup.

### Collections
Dropdown; ListBox; TagGroup.

### Colors
ColorArea; ColorField; ColorPicker; ColorSlider; ColorSwatch; ColorSwatchPicker.

### Controls
Slider; Switch.

### Data Display
Badge; Chip; Table.

### Date and Time
Calendar; DateField; DatePicker; DateRangePicker; RangeCalendar; TimeField.

### Feedback
Alert; Meter; ProgressBar; ProgressCircle; Skeleton; Spinner.

### Forms
Checkbox; CheckboxGroup; Description; ErrorMessage; FieldError; Fieldset; Form; Input; InputGroup; InputOTP; Label; NumberField; RadioGroup; SearchField; TextField; TextArea.

### Layout
Card; Separator; Surface; Toolbar.

### Media
Avatar.

### Navigation
Accordion; Breadcrumbs; Disclosure; DisclosureGroup; Link; Pagination; Tabs.

### Overlays
AlertDialog; Drawer; Modal; Popover; Toast; Tooltip.

### Pickers
Autocomplete; ComboBox; Select.

### Typography
Kbd; Typography.

### Utilities
ScrollShadow.

## Exports de componente no repo oficial que não são cards top-level — 11

EmptyState; Header; ListBoxItem; ListBoxSection; Menu; MenuItem; MenuSection; Radio; SwitchGroup; Tag; CalendarYearPicker.

`CalendarYearPicker` está marcado como `in progress` no índice de source e não deve ser promovido a componente estável apenas por estar exportado.

### Outros building blocks públicos relevantes

Collection; ListBoxLoadMoreItem; RouterProvider; I18nProvider; Virtualizer; TableLayout; ListLayout; isRTL; useLocale; useFilter; getLocalizationScript; parseColor; `tv`; `cn`; `VariantProps`.

### Hooks do package

useCssVariable; useIsHydrated; useListData; useMeasuredHeight; useMounted; useOverlayState; useSafeLayoutEffect; useIsomorphicLayoutEffect; useMediaQuery; useTheme.

## Resultado contra App Factory

**Antes da auditoria:** os 71 top-level estavam completos, mas os 11 módulos adicionais e building blocks públicos não estavam catalogados como camada separada.

**Depois da auditoria:** corrigido em `HEROUI_REACT_V3_CATALOG.md`.

# 2. HeroUI Pro React atual

## Catálogo oficial — 65 componentes / 477 variantes-exemplos

### Charts — 8 / 53
Area Chart (6); Bar Chart (8); Chart Tooltip (7); Composed Chart (5); Line Chart (10); Pie Chart (7); Radar Chart (5); Radial Chart (5).

### Data Display — 17 / 126
Agenda (1); Action Bar (2); Carousel (6); Data Grid (12); Empty State (8); File Tree (11); Floating TOC (10); Hover Card (6); Kanban (4); Item Card (12); Item Card Group (12); KPI (8); KPI Group (3); List View (5); Map (10); Timeline (8); Widget (8).

### AI — 14 / 45
Chain Of Thought (4); Chat Attachment (3); Chat Conversation (3); Chat List View (2); Chat Loader (1); Chat Message (3); Chat Message Actions (3); Chat Source (5); Chat Tool (6); Code Block (1); Markdown (3); Prompt Input (8); Prompt Suggestion (2); Text Shimmer (1).

### Feedback — 5 / 47
Emoji Reaction Button (4); Number Value (8); Pressable Feedback (17); Rating (12); Trend Chip (6).

### Layout — 1 / 7
Resizable (7).

### Forms — 11 / 96
Cell Color Picker (6); Cell Select (7); Cell Slider (7); Cell Switch (7); Checkbox Button Group (11); Drop Zone (9); Inline Select (5); Native Select (12); Number Stepper (13); Radio Button Group (12); Rich Text Editor (7).

### Navigation — 7 / 83
AppLayout (14); Command (9); Context Menu (7); Navbar (7); Segment (11); Sidebar (16); Stepper (19).

### Overlays — 2 / 20
Emoji Picker (4); Sheet (16).

## Templates React — 4

- Dashboard — analytics dashboard, orders, tracker, settings, help.
- Mail — folders, message threads, compose.
- Chat — conversations, library, exploration.
- Finances — portfolio, spending, transactions.

## Temas Pro

- Brutalism — light/dark.
- Glass — light/dark, incluindo controle de blur.
- Mouve — light/dark, linguagem mauve/warm-purple e superfícies táteis.

## Recursos de plataforma Pro

- Design Systems com customização de colors, radius, fonts, shadows e overrides;
- export de Web CSS, Native CSS, `DESIGN.md` e `PRODUCT.md`;
- Figma Pro Component Kit V3;
- HeroUI Pro Native Figma Kit;
- Figma Theme Sync;
- AI Chat/export de interfaces;
- MCP unificado Pro + OSS;
- React Pro Skill;
- Design Taste Skill.

## MCP Pro — ferramentas públicas documentadas

list_components; get_component_docs; get_css; get_docs; get_component_source_code (OSS); get_theme_variables; get_chat_export_manifest; get_chat_export_files; get_design_system_manifest; get_design_system_export.

## Dependências/subpaths específicos a considerar

O catálogo visual estava completo, mas a instalação oficial deixa claro que alguns componentes podem exigir peers/subpaths próprios, incluindo Map, Rich Text Editor, Markdown, charts/KPI, Carousel, Code Block/Chat Tool e Number Stepper. A App Factory deve pesquisar a instalação atual antes de adicionar qualquer um deles.

## Resultado contra App Factory

**Catálogo nominal atual:** completo. Os 65 componentes e 477 variantes já estavam registrados corretamente.

**Melhoria de governança:** manter distinção entre componente existente e dependências opcionais necessárias para usá-lo.

# 3. HeroUI Native OSS

## Catálogo oficial `All Components` — 39

### Buttons
Button; CloseButton; LinkButton.

### Collections
Menu; TagGroup.

### Controls
Slider; Switch.

### Forms
Checkbox; ControlField; Description; FieldError; Input; InputGroup; InputOTP; Label; RadioGroup; SearchField; Select; TextArea; TextField.

### Navigation
Accordion; ListGroup; Tabs.

### Overlays
BottomSheet; Dialog; Popover; Toast.

### Feedback
Alert; Skeleton; SkeletonGroup; Spinner.

### Layout
Card; Separator; Surface.

### Media
Avatar.

### Data Display
Chip.

### Typography
Typography.

### Utilities
PressableFeedback; ScrollShadow.

## Exports do repo além do índice top-level — 4

GlassView; Radio; SubMenu; ThemeBackground.

O package também exporta Portal, contexts, hooks, utils e providers.

## Resultado contra App Factory

**Antes:** os 39 top-level estavam completos, mas os quatro exports adicionais não estavam destacados.

**Depois:** corrigido em `HEROUI_NATIVE_CATALOG.md`.

# 4. HeroUI Pro Native atual

## Catálogo oficial — 44

### Buttons — 6
FAB; ProgressButton; SlideButton; SocialAuthButton; ToggleButton; ToggleButtonGroup.

### Charts — 10
AreaChart; BarChart; ChartCrosshair; ChartIndicator; ChartTooltip; ComposedChart; LineChart; PieChart; RadarChart; RadialChart.

### Data Display — 5
Badge; EmptyState; FlipCard; Timeline; Widget.

### Date and Time — 9
Calendar; DateField; DatePicker; DateRangePicker; DateTimePicker; RangeCalendar; TimePicker; WheelDateTimePicker; WheelTimePicker.

### Feedback — 5
NumberValue; ProgressBar; ProgressCircle; Rating; TrendChip.

### Forms — 6
Number Stepper; NumberField; NumberPad; RadioButtonGroup; WheelPicker; WheelPickerGroup.

### Navigation — 3
Segment; Stepper; SplitView.

## Templates Native — 2

Crypto Wallet; Fitness App.

## Divergência encontrada

A App Factory registrava **51** itens. Sete nomes não aparecem mais no índice oficial atual:

MorphButton; Carousel; Table; Agenda; Autocomplete; ComboBox; PhoneNumberField.

Eles permanecem apenas como **histórico/não confirmado no catálogo atual**. Não devem ser escolhidos automaticamente para um projeto novo.

# 5. HeroUI Pro v2 — repertório legado

O catálogo público legado continua declarando **220 blocos em 34 famílias**.

## Charts — 21
Bars And Circles (10); Graphs (2); KPI Stats (9).

## Application — 95
Calendar (3); Authentication (24); Cards (20); Command Menus (1); Layouts (2); Navigation Headers (5); Scrolling Banners (5); Sidebars (19); Tables (1); Feedbacks (4); Forms (1); Navbars (3); Steppers (7).

## AI — 30
Prompt Containers (10); Playgrounds (1); Features (2); Prompt Inputs (11); Messages (6).

## Marketing — 45
Faqs (4); Pricing (8); Footers (4); Hero Sections (4); Pricing Comparison (8); Teams (1); Banners (8); Cookie Consents (8).

## E-commerce — 29
Filters (9); Product List (9); Checkouts (4); Product View (1); Reviews (6).

## Blocos individuais identificáveis nas páginas públicas auditadas

### Authentication — 24
Simple Sign Up; Simple Login Without Social Buttons; Simple Login; Simple Login Without Background; Simple Sign Up Without Background; Centered Sign Up; Centered Login With Animated Form; Centered Sign Up With Animated Form; Centered Login With Only Email; Centered Sign Up With Only Email; Centered Login With Two Steps; Centered Sign Up With Two Steps; Centered Login With Top Logo; Centered Sign Up With Top Logo; Left Login With Image Background; Right Sign Up With Image Background; Left Login With Right Testimonial; Left Sign Up With Right Testimonial; Right Login With Image Background; Left Sign Up With Image Background; Centered Login With Gradient Background; Centered Sign Up With Gradient Background; Centered Login With Blurred Container; Centered Sign Up With Blurred Container.

### Calendar — 3
Calendar Booking; Calendar Booking Confirmation; Calendar Booking Form.

### Bars And Circles — 10
Bars 1; Bars 2; Bars 3; Bars 4; Circles 1; Circles 2; Circles 3; Circles 4; Circles 5; Circles 6.

### KPI Stats — 9
Kpi Stat 1; Kpi Stat 2; Kpi Stat 3; Kpi Stat 4; Kpi Stat 5; Kpi Stat 6; Kpi Stat 7; Kpi Stat 8; Kpi Stat 9.

### Cards — 20
Event Announcement; Actions Cards; Card Fieldset; Dismissable Card; Discount Card; Card With Thumbnail; Spotlight Card; Invite Member; Notifications Card; Onboarding Checklist Card; Marketplace Card; Select Payment Method; Select Plan; User Profile; User Profile Extended; Notifications Settings; Personal Details; Security Settings; Account Details; Settings Tabs.

### Command Menus — 1
Command Menu With Categories.

### Layouts — 2
Messaging Application; Settings Layout.

### Navigation Headers — 5
Basic Navigation Header; Navigation Header With Search Input; Navigation Header With Tabs; Navigation Header With Heading Cta; Navigation Header With Brand Colors.

### Sidebars — 19
Basic Sidebar; Sidebar With Pro Card; Sidebar With Search Input; Sidebar With Sections; Sidebar With User Avatar; Sidebar With Teams; Sidebar With Toggle Button; Sidebar With Footer Actions; Sidebar Compact; Sidebar Off Canvas; Sidebar With Compacted Items; Sidebar Responsive; Sidebar Off Canvas Responsive; Sidebar With Long List; Sidebar With Chat History; Sidebar With Gradient Background; Sidebar With Brand Colors; Sidebar With Nested Items; Sidebar With Account And Workspace Switcher.

### Tables / Feedback / Forms
Table With Filters; Feedback Rating; Feedback Textarea; Popover Feedback; Modal Feedback; Multi Step Wizard.

### Navbars — 3
Basic Navbar; Centered Navbar Menu; Centered Items Navbar.

### Steppers — 7
Simple Stepper; Basic Stepper; Minimal Stepper; Vertical Stepper; Vertical Splitted Stepper; Vertical Splitted Stepper With Helpers; Vertical Collapsible Stepper With Helpers.

### Prompt Containers — 10
Prompt Container Empty; Prompt Container Empty Feature Cards Individual; Prompt Container Full Line Bottom Actions; Prompt Container Full Line Bottom Actions Large; Prompt Layout With Recent Messages And Conversations; Prompt Container With Conversation; Prompt Container With Failed Messages; Prompt Container With Regenerate Button; Prompt Container With Sidebar; Prompt Layout With Recent Messages.

### Features — 2
Features Cards Individual; Features Cards.

### Prompt Inputs — 11
Prompt Input Full Line; Prompt Input Full Line With Bottom Actions; Prompt Input Full Line With Bottom Actions Large; Basic Prompt Input; Prompt Input With Enclosed Actions; Prompt Input With Vertical Actions; Prompt Input With Character Count; Prompt Input With Regenerate Button; Prompt Input With Suggestions Above; Prompt Input With Uploaded Images; Prompt Input With Bottom Actions.

### Messages — 6
User Message; Assistant Message; Assistant Message Failed; Assistant Message With Feedback; Conversation; Conversation With Failed Message.

### Marketing
Faqs: Basic Faqs; Centered Faqs; Faqs With Divider; Two Columns Faqs.

Pricing: Simple Pricing Selector; Basic Pricing; Pricing With Blurred Background; Pricing With Featured Tier; Pricing With Featured Tier Filled; Pricing With Most Popular Tier; Pricing With Most Popular Tier Filled; Pricing With Most Popular Tier Highlighted.

Footers: Basic Footer With Theme Switch; Centered Footer With Social Links; Footer With Columns; Footer With Columns And Newsletter.

Hero Sections: Hero Section Basic; Hero Section With Bottom App Screenshot; Hero Section With Bottom App Skewed Screenshot; Hero Section With Centered Navbar And Bottom App Screenshot.

Pricing Comparison: Basic Pricing Comparison; Pricing Comparison With Blurred Background; Pricing Comparison With Featured Tier; Pricing Comparison With Featured Tier Filled; Pricing Comparison With Highlighted Tier; Pricing Comparison With Most Popular Tier; Pricing Comparison With Most Popular Tier Soft; Pricing Comparison With Sticky Header.

Teams: Basic Team Page.

### E-commerce — Product List 9
Basic Product List; Product List With Available Colors; Product List With Popular Items; Product List With Popular Items And Cta; Product List With Ratings; Product List Without Wrapper; Place List Grid; Product List Grid; Place List Grid Loading State.

### E-commerce — Checkouts 4
Payment Checkout; Single Column Checkout; Two Columns Checkout; Multi Step Checkout.

### E-commerce — Reviews 6
Review Comment Card; Two Columns Reviews; Summary Rating Card; Reviews With Summary Rating Card; Reviews With Modal Review; Reviews With Search And Sort.

## Limite do arquivo legado

Algumas páginas do site legado não expuseram os títulos de todos os blocos de forma recuperável no snapshot, embora o índice oficial confirme suas contagens. As famílias afetadas são principalmente Graphs, Scrolling Banners, Playgrounds, Banners, Cookie Consents, Filters e Product View.

Essas famílias **não estão ausentes da Factory**: estão registradas com URL e contagem, mas nem todos os nomes internos puderam ser confirmados de forma confiável. Não inventar nomes para completar a lista.

# 6. Fontes/repositórios oficiais

## Web/React
- https://heroui.com/en/docs/react/components
- https://github.com/heroui-inc/heroui
- https://storybook-v3.heroui.com/

## Native
- https://heroui.com/en/docs/native/components
- https://github.com/heroui-inc/heroui-native

## Tooling OSS
- https://github.com/heroui-inc/heroui-cli
- https://github.com/heroui-inc/heroui-mcp
- https://github.com/heroui-inc/tailwind-variants

## Pro
- https://heroui.pro/docs/react/components
- https://heroui.pro/docs/react/templates
- https://heroui.pro/docs/react/getting-started/theming
- https://heroui.pro/docs/react/getting-started/figma
- https://heroui.pro/docs/react/getting-started/mcp-server
- https://heroui.pro/docs/native/components
- https://heroui.pro/docs/native/templates

## Legado
- https://v2.heroui.pro/components

# 7. Conclusão da auditoria

| Área | Antes | Resultado |
| --- | --- | --- |
| React OSS top-level | 71 | correto |
| React OSS exports auxiliares | não separados | **11 adicionados** |
| React Aria/building blocks/hooks | incompleto | **catalogados como camada auxiliar** |
| Pro React 65/477 | registrado | correto |
| Pro React templates/themes/tooling | registrado | correto, fontes reconfirmadas |
| Native OSS top-level | 39 | correto |
| Native OSS exports auxiliares | não separados | **4 adicionados** |
| Pro Native | 51 | **corrigido para 44 atuais** |
| Pro Native itens antigos | tratados como atuais | **7 rebaixados para histórico/não confirmado** |
| Pro v2 famílias/contagens | 220 / 34 | correto |
| Pro v2 nomes individuais | parcial | ampliado; não inventar nomes que o site legado não expõe |
| Repositórios/tooling | amplo | adicionar `heroui-inc/heroui-mcp` ao índice oficial |

## Regra operacional resultante

Quando a App Factory for construir um sistema integralmente HeroUI:

1. consultar primeiro `All Components` atual;
2. consultar source/package para auxiliares e composição compound;
3. consultar HeroUI Pro quando houver acesso autorizado;
4. consultar v2 apenas como repertório de padrões visuais;
5. verificar release e dependências antes de importar;
6. não inventar capacidade baseada em item histórico;
7. preservar HeroUI como linguagem visual transversal do produto inteiro.