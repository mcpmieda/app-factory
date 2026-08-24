# HeroUI React v3 — Catálogo OSS

Snapshot: **2026-08-24**.

Fontes primárias: documentação oficial HeroUI v3 e repositório `heroui-inc/heroui`.

Versão exibida no site oficial no snapshot: **HeroUI React v3.2.4**.

## Componentes top-level atuais

A página oficial `All Components (React)` lista 71 componentes top-level.

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

## Componentes úteis para um sistema completo

### Shell e navegação

Base OSS sugerida: `Breadcrumbs`, `Tabs`, `Accordion`, `Disclosure`, `Dropdown`, `Toolbar`, `Drawer`, `Popover`, `Link`, `Pagination`.

Para shell administrativo mais sofisticado, consultar também HeroUI Pro: `AppLayout`, `Sidebar`, `Navbar`, `Command`, `Segment` e `Stepper`.

### Formulários

Combinar `Form`, `Fieldset`, `TextField`, `Input`, `InputGroup`, `Select`, `Autocomplete`, `ComboBox`, `Checkbox`, `RadioGroup`, `DatePicker`, `NumberField`, `TextArea`, `InputOTP`, `Label`, `Description`, `FieldError` e `ErrorMessage`.

### Dados e administração

Base OSS: `Table`, `Pagination`, `Badge`, `Chip`, `Skeleton`, `Spinner`, `Alert`, `Toast`, `Drawer`, `Modal`.

Para workloads complexos, consultar HeroUI Pro: `Data Grid`, `Action Bar`, `KPI`, `KPI Group`, charts, `List View`, `File Tree`, `Timeline`, `Kanban` e `Widget`.

### Autenticação

OSS suficiente para construir login/recuperação/OTP com `Card`, `Form`, `TextField`, `Input`, `InputOTP`, `Checkbox`, `Button`, `Alert` e `Link`.

O arquivo Pro v2 contém repertório visual adicional de `Authentication` com 24 blocos.

## Princípios técnicos v3

- React 19+.
- Tailwind CSS v4.
- `@heroui/react` para comportamento/componentes.
- `@heroui/styles` para CSS/design system.
- React Aria Components como base de acessibilidade.
- arquitetura compound (`Card.Header`, `Card.Content`, etc.).
- animações principalmente em CSS, sem depender de runtime JS para cada componente.
- CSS variables + BEM para customização global.
- possibilidade de imports seletivos de CSS.
- headless possível removendo a camada de estilos e mantendo comportamento/acessibilidade.

## Temas e linguagem visual

HeroUI v3 usa CSS variables e tokens semânticos. Ao construir um produto integralmente HeroUI:

- definir um tema consistente no início;
- manter a mesma escala de radius, spacing, shadows e typography;
- usar light/dark ou um tema customizado via `data-theme`;
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
- React package guide: https://github.com/heroui-inc/heroui/blob/v3/packages/react/README.md
- Styles package: https://github.com/heroui-inc/heroui/blob/v3/packages/styles/README.md
- React Agent Skill oficial: https://github.com/heroui-inc/heroui/blob/v3/skills/heroui-react/SKILL.md
- Storybook v3: https://storybook-v3.heroui.com/

## Observação de contagem

O anúncio oficial do v3 descreve **75+ web components**. A página nominal atual `All Components (React)` lista 71 entradas top-level. Subcomponentes compound não são contados separadamente neste arquivo.