# HeroUI React v3 — Catálogo OSS

Snapshot auditado: **2026-08-24**.

Fontes primárias: documentação oficial HeroUI v3 e repositório público `heroui-inc/heroui` na branch `v3`.

Versão exibida no site oficial no snapshot: **HeroUI React v3.2.4**.

## Camadas do inventário

O HeroUI possui duas superfícies que não devem ser confundidas:

1. **All Components** — catálogo nominal/documentado do site oficial: **71 componentes top-level**.
2. **Public package exports** — módulos públicos realmente exportados por `@heroui/react`; inclui auxiliares usados pela composição compound e um item ainda marcado como `in progress`.

Para descoberta visual, começar pelos 71 componentes documentados. Para implementação e auditoria, consultar também os exports públicos adicionais abaixo.

## All Components — 71 componentes documentados

### Buttons — 5

- Button
- ButtonGroup
- CloseButton
- ToggleButton
- ToggleButtonGroup

### Collections — 3

- Dropdown
- ListBox
- TagGroup

### Colors — 6

- ColorArea
- ColorField
- ColorPicker
- ColorSlider
- ColorSwatch
- ColorSwatchPicker

### Controls — 2

- Slider
- Switch

### Data Display — 3

- Badge
- Chip
- Table

### Date and Time — 6

- Calendar
- DateField
- DatePicker
- DateRangePicker
- RangeCalendar
- TimeField

### Feedback — 6

- Alert
- Meter
- ProgressBar
- ProgressCircle
- Skeleton
- Spinner

### Forms — 16

- Checkbox
- CheckboxGroup
- Description
- ErrorMessage
- FieldError
- Fieldset
- Form
- Input
- InputGroup
- InputOTP
- Label
- NumberField
- RadioGroup
- SearchField
- TextField
- TextArea

### Layout — 4

- Card
- Separator
- Surface
- Toolbar

### Media — 1

- Avatar

### Navigation — 7

- Accordion
- Breadcrumbs
- Disclosure
- DisclosureGroup
- Link
- Pagination
- Tabs

### Overlays — 6

- AlertDialog
- Drawer
- Modal
- Popover
- Toast
- Tooltip

### Pickers — 3

- Autocomplete
- ComboBox
- Select

### Typography — 2

- Kbd
- Typography

### Utilities — 1

- ScrollShadow

## Public exports adicionais do repositório oficial — 11 módulos

Estes módulos aparecem em `packages/react/src/components/index.ts`, mas não são entradas top-level da página `All Components`.

### Auxiliares/compound suportados

- EmptyState
- Header
- ListBoxItem — exposto visualmente como `ListBox.Item`
- ListBoxSection — exposto visualmente como `ListBox.Section`
- Menu
- MenuItem — usado por composições de Menu/Dropdown
- MenuSection — usado por composições de Menu/Dropdown
- Radio — item individual usado por `RadioGroup`
- SwitchGroup
- Tag — item individual usado por `TagGroup`

### Experimental / repository-only

- CalendarYearPicker — exportado no pacote, porém marcado como **`in progress`** no índice oficial do código. Não tratar como API estável sem verificar release/documentação atual.

Portanto, o repositório oficial expõe atualmente **82 módulos de componentes** no índice principal: 71 correspondentes ao catálogo top-level e 11 módulos adicionais. Isso não significa “82 componentes estáveis documentados”; é uma distinção deliberada entre catálogo de produto e superfície pública do pacote.

## Public building blocks adicionais de `@heroui/react`

O bridge de React Aria também exporta recursos úteis que podem aparecer em sistemas maiores:

- Collection
- ListBoxLoadMoreItem
- RouterProvider
- I18nProvider
- Virtualizer
- TableLayout
- ListLayout
- isRTL
- useLocale
- useFilter
- getLocalizationScript
- parseColor

Tipos públicos relevantes incluem `Key`, `Direction`, `Orientation`, `PressEvent`, `PointerType`, `Selection`, `DateValue`, `DateRange`, `ValidationResult`, `RangeValue`, `RouterConfig`, `Color`, `ColorFormat`, `ColorSpace`, `ColorChannel`, `ColorChannelRange`, `ColorAxes` e `SortDescriptor`.

O package root também reexporta `tv`, `cn` e `VariantProps` de `tailwind-variants`.

## Hooks públicos

O índice de hooks do pacote exporta módulos para:

- useCssVariable
- useIsHydrated
- useListData
- useMeasuredHeight
- useMounted
- useOverlayState
- useSafeLayoutEffect
- useIsomorphicLayoutEffect
- useMediaQuery
- useTheme

Antes de depender de um nome exato de hook em código gerado, confirmar a assinatura no release/package atual.

## Componentes úteis para um sistema completo

### Shell e navegação

Base OSS sugerida: `Breadcrumbs`, `Tabs`, `Accordion`, `Disclosure`, `Dropdown`, `Menu`, `Toolbar`, `Drawer`, `Popover`, `Link`, `Pagination`.

Para shell administrativo mais sofisticado, consultar HeroUI Pro: `AppLayout`, `Sidebar`, `Navbar`, `Command`, `Context Menu`, `Segment` e `Stepper`.

### Formulários

Combinar `Form`, `Fieldset`, `TextField`, `Input`, `InputGroup`, `Select`, `Autocomplete`, `ComboBox`, `Checkbox`, `RadioGroup`, `DatePicker`, `NumberField`, `TextArea`, `InputOTP`, `Label`, `Description`, `FieldError` e `ErrorMessage`.

### Dados e administração

Base OSS: `Table`, `Pagination`, `Badge`, `Chip`, `EmptyState`, `Skeleton`, `Spinner`, `Alert`, `Toast`, `Drawer`, `Modal`.

Para workloads complexos, consultar HeroUI Pro: `Data Grid`, `Action Bar`, `KPI`, `KPI Group`, charts, `List View`, `File Tree`, `Timeline`, `Kanban`, `Map` e `Widget`.

### Autenticação

OSS suficiente para construir login/recuperação/OTP com `Card`, `Form`, `TextField`, `Input`, `InputOTP`, `Checkbox`, `Button`, `Alert` e `Link`.

O arquivo Pro v2 contém repertório visual adicional de `Authentication` com 24 blocos.

## Princípios técnicos v3

- React 19+.
- Tailwind CSS v4.
- `@heroui/react` para comportamento/componentes.
- `@heroui/styles` para CSS/design system.
- React Aria Components como base de acessibilidade.
- arquitetura compound (`Card.Header`, `Tabs.List`, `ListBox.Item`, etc.).
- animações principalmente em CSS.
- CSS variables + BEM para customização global.
- imports seletivos de CSS quando aplicável.
- possibilidade de composição/headless preservando comportamento e acessibilidade.

## Temas e linguagem visual

Ao construir um produto integralmente HeroUI:

- definir tema consistente no início;
- manter a mesma escala de radius, spacing, shadows e typography;
- usar light/dark ou tema customizado via tokens/data-theme;
- evitar sobrescritas locais divergentes por componente;
- preferir BEM/tokens para customização transversal.

## Fontes oficiais

- All Components: https://heroui.com/en/docs/react/components
- Quick Start: https://heroui.com/en/docs/react/getting-started/quick-start
- Theming: https://heroui.com/en/docs/react/getting-started/theming
- Colors: https://heroui.com/en/docs/react/getting-started/colors
- Dark Mode: https://heroui.com/en/docs/react/getting-started/dark-mode
- Releases: https://heroui.com/en/docs/react/releases
- Migration v2→v3: https://heroui.com/en/docs/react/migration
- GitHub: https://github.com/heroui-inc/heroui
- Package exports: https://github.com/heroui-inc/heroui/blob/v3/packages/react/src/components/index.ts
- React Aria bridge: https://github.com/heroui-inc/heroui/blob/v3/packages/react/src/components/rac/index.ts
- Hooks: https://github.com/heroui-inc/heroui/blob/v3/packages/react/src/hooks/index.ts
- React package guide: https://github.com/heroui-inc/heroui/blob/v3/packages/react/README.md
- Styles package: https://github.com/heroui-inc/heroui/blob/v3/packages/styles/README.md
- React Agent Skill oficial: https://github.com/heroui-inc/heroui/blob/v3/skills/heroui-react/SKILL.md
- Storybook v3: https://storybook-v3.heroui.com/

## Observação de contagem

O anúncio do v3 descreve **75+ web components**. A página nominal atual `All Components (React)` lista **71 entradas top-level**. O código público, por sua vez, exporta módulos auxiliares adicionais. Sempre registrar qual superfície está sendo contada.