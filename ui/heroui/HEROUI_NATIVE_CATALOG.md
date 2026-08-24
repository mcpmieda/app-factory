# HeroUI Native — Catálogo OSS + Pro

Snapshot auditado: **2026-08-24**.

## HeroUI Native OSS — 39 componentes top-level no site oficial

### Buttons — 3
- Button
- CloseButton
- LinkButton

### Collections — 2
- Menu
- TagGroup

### Controls — 2
- Slider
- Switch

### Forms — 13
- Checkbox
- ControlField
- Description
- FieldError
- Input
- InputGroup
- InputOTP
- Label
- RadioGroup
- SearchField
- Select
- TextArea
- TextField

### Navigation — 3
- Accordion
- ListGroup
- Tabs

### Overlays — 4
- BottomSheet
- Dialog
- Popover
- Toast

### Feedback — 4
- Alert
- Skeleton
- SkeletonGroup
- Spinner

### Layout — 3
- Card
- Separator
- Surface

### Media — 1
- Avatar

### Data Display — 1
- Chip

### Typography — 1
- Typography

### Utilities — 2
- PressableFeedback
- ScrollShadow

## Exports públicos OSS adicionais

O `src/index.tsx` oficial exporta **43 módulos de componentes**. Além das 39 entradas top-level acima, aparecem:

- GlassView
- Radio
- SubMenu
- ThemeBackground

`SubMenu` é documentado como composição de Menu. `Radio` é o item da composição de `RadioGroup`. `GlassView` e `ThemeBackground` também são exports públicos, embora não apareçam como cards próprios no índice `All Components`.

O package root ainda exporta Portal, contexts, hooks, utils e providers. Confirmar API/release antes de depender de um item que não tenha página top-level própria.

## HeroUI Pro Native — 44 componentes no índice oficial atual

### Buttons — 6
- FAB
- ProgressButton
- SlideButton
- SocialAuthButton
- ToggleButton
- ToggleButtonGroup

### Charts — 10
- AreaChart
- BarChart
- ChartCrosshair
- ChartIndicator
- ChartTooltip
- ComposedChart
- LineChart
- PieChart
- RadarChart
- RadialChart

### Data Display — 5
- Badge
- EmptyState
- FlipCard
- Timeline
- Widget

### Date and Time — 9
- Calendar
- DateField
- DatePicker
- DateRangePicker
- DateTimePicker
- RangeCalendar
- TimePicker
- WheelDateTimePicker
- WheelTimePicker

### Feedback — 5
- NumberValue
- ProgressBar
- ProgressCircle
- Rating
- TrendChip

### Forms — 6
- Number Stepper
- NumberField
- NumberPad
- RadioButtonGroup
- WheelPicker
- WheelPickerGroup

### Navigation — 3
- Segment
- Stepper
- SplitView

## Sete itens do snapshot anterior que não aparecem no índice Pro Native atual

- MorphButton
- Carousel
- Table
- Agenda
- Autocomplete
- ComboBox
- PhoneNumberField

Status: **histórico / não confirmado no catálogo atual**. Não selecionar esses sete como capacidade Pro Native vigente sem confirmação na documentação, release ou package atual.

## HeroUI Pro Native templates — 2

- Crypto Wallet — carteira mobile com portfolio, assets e transactions.
- Fitness App — atividade, workouts e daily stats.

## Direção técnica Native

- React Native;
- Tailwind CSS v4 via Uniwind;
- compound components;
- animações nativas/Reanimated quando aplicável;
- acessibilidade mobile;
- provider próprio para configuração nativa;
- não transportar automaticamente padrões Web HeroUI para Native.

## Fontes oficiais

- All Components Native OSS: https://heroui.com/en/docs/native/components
- Getting Started: https://heroui.com/en/docs/native/getting-started
- Styling: https://heroui.com/en/docs/native/getting-started/styling
- Releases: https://heroui.com/en/docs/native/releases
- GitHub: https://github.com/heroui-inc/heroui-native
- Public exports: https://github.com/heroui-inc/heroui-native/blob/main/src/index.tsx
- Native example: https://github.com/heroui-inc/heroui-native-example
- Pro Native Components: https://heroui.pro/docs/native/components
- Pro Native Templates: https://heroui.pro/docs/native/templates

## Regra de uso

Em projeto mobile, usar este catálogo para descoberta e confirmar o estado atual antes de instalar. Em projeto Web, preferir HeroUI React/Pro React.