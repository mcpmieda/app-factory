# HeroUI / HeroUI Pro — Auditoria de catálogo

Data: **2026-08-24**

## Escopo

Comparação entre páginas oficiais atuais, repositórios públicos `heroui-inc`, HeroUI Pro atual, HeroUI Pro v2 legado e os catálogos `ui/heroui/` da App Factory.

Os inventários nominais completos ficam nos arquivos especializados. Este relatório registra divergências, cobertura e decisões.

## Resultado consolidado

| Superfície | Fonte oficial observada | Estado na Factory após auditoria |
| --- | ---: | --- |
| HeroUI React v3 `All Components` | 71 top-level | **completo** |
| React v3 public component exports | 82 módulos no índice, incluindo 11 além do catálogo top-level | **completo e separado por status** |
| React Aria bridge / building blocks | exports públicos adicionais | **catalogados** |
| React hooks | 10 módulos no índice de hooks | **catalogados** |
| HeroUI Pro React | 65 componentes / 477 variantes-exemplos | **completo** |
| Pro React templates | 4 | **completo** |
| Pro themes | Brutalism, Glass, Mouve (+ light/dark) | **completo** |
| HeroUI Native OSS `All Components` | 39 top-level | **completo** |
| Native OSS public component exports | 43 módulos, 4 além do top-level | **completo e separado** |
| HeroUI Pro Native | 44 top-level atuais | **corrigido** |
| Pro Native templates | 2 | **completo** |
| HeroUI Pro v2 | 220 blocos / 34 famílias | **famílias e contagens completas; nomes individuais quase totais** |
| Tooling / GitHub / MCP / Figma / Skills | ecossistema oficial | **fontes ampliadas** |

## Divergências encontradas e corrigidas

### 1. React OSS tinha mais superfície pública que a página `All Components`

O site lista 71 componentes top-level, e esses 71 já estavam corretos na App Factory.

O repositório oficial, porém, exporta 11 módulos de componentes adicionais no índice público:

- EmptyState
- Header
- ListBoxItem
- ListBoxSection
- Menu
- MenuItem
- MenuSection
- Radio
- SwitchGroup
- Tag
- CalendarYearPicker

`CalendarYearPicker` está marcado como `in progress` no source oficial. Por isso não foi promovido a componente estável.

Também foram catalogados building blocks do bridge React Aria, providers/utilities e hooks públicos.

Arquivo canônico: `HEROUI_REACT_V3_CATALOG.md`.

### 2. Native OSS também possui exports além do índice visual

O site lista 39 top-level. O `src/index.tsx` oficial exporta quatro módulos de componente adicionais:

- GlassView
- Radio
- SubMenu
- ThemeBackground

Arquivo canônico: `HEROUI_NATIVE_CATALOG.md`.

### 3. HeroUI Pro Native estava desatualizado

A Factory registrava 51 componentes Pro Native. A página oficial atual lista **44**.

Os sete nomes que não aparecem mais no índice atual são:

- MorphButton
- Carousel
- Table
- Agenda
- Autocomplete
- ComboBox
- PhoneNumberField

Eles foram rebaixados para **histórico / não confirmado no catálogo atual**. Não devem ser escolhidos automaticamente para projeto novo.

### 4. HeroUI Pro React estava correto

O catálogo atual confirma **65 componentes / 477 variantes-exemplos**. Nenhum componente top-level ficou ausente no arquivo Pro React da Factory.

A documentação de instalação também reforça que alguns componentes possuem peers/subpaths específicos; existência no catálogo não significa que toda dependência deva ser instalada por padrão.

Arquivo canônico: `HEROUI_PRO_REACT_CATALOG.md`.

### 5. O Pro v2 precisava de mais nomes individuais

As **34 famílias e 220 blocos** já estavam corretamente contabilizados, mas o arquivo anterior nomeava apenas uma parcela dos blocos.

A auditoria recuperou nominalmente, entre outros:

- Graph 1 / Graph 2;
- 24 padrões de Authentication;
- 5 Scrolling Banners;
- Playground;
- 8 Banners;
- 8 Cookie Consents;
- 9 Product List;
- 4 Checkouts;
- 6 Reviews;
- além das famílias já nomeadas de Cards, Sidebars, Marketing, AI etc.

Restam somente duas áreas parcialmente resolvidas no nível de título interno do site legado:

- **Filters:** 9 blocos confirmados; `Pricing Filter` confirmado nominalmente e oito títulos não recuperados de forma confiável;
- **Product View:** 1 bloco confirmado pela família/contagem, mas o título interno não foi recuperado.

A Factory não inventará esses nove títulos para forçar “100% nominal”.

Arquivo canônico: `HEROUI_PRO_V2_VISUAL_ARCHIVE.md`.

## Tooling oficial que também faz parte do catálogo de capacidades

Além de componentes visuais, a Factory agora referencia explicitamente:

- `heroui-inc/heroui`;
- `heroui-inc/heroui-native`;
- `heroui-inc/heroui-cli`;
- `heroui-inc/heroui-mcp`;
- `heroui-inc/tailwind-variants`;
- templates oficiais Next.js/Vite/React Router;
- Storybook v3;
- HeroUI OSS Skills;
- HeroUI Pro MCP;
- Pro React Skill;
- Pro Native Skill;
- Design Taste;
- Design Systems;
- AI Chat/export;
- Figma OSS/Pro e Theme Sync.

Arquivo canônico: `OFFICIAL_SOURCES.md`.

## Critério de completude

Para a Factory, “catálogo completo” passa a significar:

1. todos os componentes top-level do site atual registrados;
2. exports públicos auxiliares do repo identificados separadamente;
3. experimental/in-progress não confundido com stable;
4. Pro atual separado de Pro v2 legado;
5. templates, themes e tooling registrados;
6. itens removidos do índice atual mantidos apenas como histórico;
7. dependências e versão reconfirmadas antes de implementação.

## Estado final

**CURRENT_CATALOG_RECONCILED**

Para Web/React e Native atuais, não foi encontrada lacuna nominal de componentes top-level após as correções. A única incompletude nominal conhecida está em nove títulos internos do catálogo comercial legado v2 (oito Filters e um Product View), embora suas famílias e contagens estejam registradas.