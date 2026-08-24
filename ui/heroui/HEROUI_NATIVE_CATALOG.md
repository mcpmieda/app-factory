# HeroUI Native — Catálogo OSS + Pro

Snapshot: **2026-08-24**.

## HeroUI Native OSS

A página oficial atual lista **39 componentes top-level**.

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

## HeroUI Pro Native

A página oficial Pro Native atual lista **51 componentes**.

### Buttons — 7

- FAB
- MorphButton
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

### Data Display — 7

- Badge
- Carousel
- EmptyState
- FlipCard
- Table
- Timeline
- Widget

### Date and Time — 10

- Agenda
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

### Forms — 9

- Autocomplete
- ComboBox
- NumberField
- NumberPad
- Number Stepper
- PhoneNumberField
- RadioButtonGroup
- WheelPicker
- WheelPickerGroup

### Navigation — 3

- Segment
- Stepper
- SplitView

## HeroUI Pro Native templates — 2

- **Crypto Wallet** — carteira mobile com portfolio, assets e transactions.
- **Fitness App** — atividade, workouts e daily stats.

## Direção técnica Native

HeroUI Native OSS:

- React Native;
- Tailwind CSS v4 via Uniwind;
- compound components;
- animações nativas/Reanimated quando aplicável;
- acessibilidade mobile;
- import granular para reduzir bundle;
- provider próprio para configuração nativa;
- não usar padrões Web HeroUI automaticamente no Native.

A documentação oficial informa que HeroUI Native não é atualmente recomendado como solução para React Native Web; para Web usar HeroUI React.

## Fontes oficiais

- All Components Native: https://heroui.com/en/docs/native/components
- Getting Started: https://heroui.com/en/docs/native/getting-started
- Quick Start: https://heroui.com/en/docs/native/getting-started/quick-start
- Styling: https://heroui.com/en/docs/native/getting-started/styling
- Design Principles: https://heroui.com/en/docs/native/getting-started/design-principles
- Releases: https://heroui.com/en/docs/native/releases
- GitHub: https://github.com/heroui-inc/heroui-native
- Native example: https://github.com/heroui-inc/heroui-native-example
- Native Agent Skill: https://github.com/heroui-inc/heroui/blob/v3/skills/heroui-native/SKILL.md
- Pro Native Components: https://heroui.pro/docs/native/components
- Pro Native Templates: https://heroui.pro/docs/native/templates

## Regra de uso

Em projeto mobile, usar este catálogo como fonte de descoberta. Em projeto Web, não introduzir HeroUI Native apenas para reproduzir aparência; usar HeroUI React/Pro React e compartilhar apenas tokens/linguagem quando fizer sentido.