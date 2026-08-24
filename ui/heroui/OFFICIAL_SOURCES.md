# HeroUI — Fontes oficiais

Snapshot: **2026-08-24**.

Regra: usar fontes oficiais abaixo como primeira escolha. O catálogo local ajuda descoberta; a documentação oficial confirma o estado atual antes da implementação.

## HeroUI Web OSS

- Site: https://heroui.com/
- React Components: https://heroui.com/en/docs/react/components
- Quick Start: https://heroui.com/en/docs/react/getting-started/quick-start
- Theming: https://heroui.com/en/docs/react/getting-started/theming
- Colors: https://heroui.com/en/docs/react/getting-started/colors
- Dark Mode: https://heroui.com/en/docs/react/getting-started/dark-mode
- Releases: https://heroui.com/en/docs/react/releases
- Migration v2→v3: https://heroui.com/en/docs/react/migration
- Storybook v3: https://storybook-v3.heroui.com/

## HeroUI Native OSS

- Native Getting Started: https://heroui.com/en/docs/native/getting-started
- Native Components: https://heroui.com/en/docs/native/components
- Native Quick Start: https://heroui.com/en/docs/native/getting-started/quick-start
- Native Styling: https://heroui.com/en/docs/native/getting-started/styling
- Native Design Principles: https://heroui.com/en/docs/native/getting-started/design-principles
- Native Releases: https://heroui.com/en/docs/native/releases

## GitHub oficial

Organização:

- https://github.com/heroui-inc

Repositórios principais:

- React/Web monorepo: https://github.com/heroui-inc/heroui
- React Native: https://github.com/heroui-inc/heroui-native
- CLI: https://github.com/heroui-inc/heroui-cli
- Tailwind Variants: https://github.com/heroui-inc/tailwind-variants
- Native Example: https://github.com/heroui-inc/heroui-native-example

Templates oficiais:

- Next.js App Router: https://github.com/heroui-inc/next-app-template
- Next.js Pages Router: https://github.com/heroui-inc/next-pages-template
- Vite: https://github.com/heroui-inc/vite-template
- React Router: https://github.com/heroui-inc/react-router-template

Arquivos úteis para agentes/arquitetura:

- React package guide: https://github.com/heroui-inc/heroui/blob/v3/packages/react/README.md
- Styles package guide: https://github.com/heroui-inc/heroui/blob/v3/packages/styles/README.md
- AGENTS.md oficial: https://github.com/heroui-inc/heroui/blob/v3/AGENTS.md
- HeroUI React Skill: https://github.com/heroui-inc/heroui/blob/v3/skills/heroui-react/SKILL.md
- HeroUI Native Skill: https://github.com/heroui-inc/heroui/blob/v3/skills/heroui-native/SKILL.md

## HeroUI CLI

- Repository: https://github.com/heroui-inc/heroui-cli

Capacidades relevantes:

- `init` com templates oficiais;
- `install`;
- `upgrade`;
- `uninstall`;
- `doctor`;
- `env`;
- `agents-md` para baixar/indexar docs oficiais atuais para agentes.

O comando `agents-md` pode indexar React, Native ou Migration e é preferível a manter uma cópia manual permanente de toda a documentação dentro da Factory.

## HeroUI Pro React

- Site: https://heroui.pro/
- Getting Started: https://heroui.pro/docs/react/getting-started
- Components: https://heroui.pro/docs/react/components
- Templates: https://heroui.pro/docs/react/templates
- Installation: https://heroui.pro/docs/react/getting-started/installation
- Theming: https://heroui.pro/docs/react/getting-started/theming
- Figma: https://heroui.pro/docs/react/getting-started/figma
- MCP: https://heroui.pro/docs/react/getting-started/mcp-server
- Agent Skills: https://heroui.pro/docs/react/getting-started/agent-skills
- Design Taste: https://heroui.pro/docs/react/getting-started/design-taste
- Releases: https://heroui.pro/docs/react/releases

## HeroUI Pro Native

- Components: https://heroui.pro/docs/native/components
- Templates: https://heroui.pro/docs/native/templates

## HeroUI Pro Themes

Documentados no snapshot:

- Brutalism
- Glass
- Mouve

Fonte: https://heroui.pro/docs/react/getting-started/theming

## HeroUI Pro Design Systems / AI tooling

O ecossistema Pro oferece:

- Design Systems com export de Web CSS / Native CSS / `DESIGN.md` / `PRODUCT.md`;
- AI Chat;
- MCP oficial unificado OSS + Pro;
- `heroui-react-pro` skill;
- `heroui-pro-design-taste` skill;
- Figma files Pro e Figma Theme Sync.

### Segurança

`HEROUI_PERSONAL_TOKEN` é segredo de projeto/licença:

- nunca commitar;
- nunca registrar em docs da Factory;
- usar secret/env local ou mecanismo seguro do ambiente;
- não compartilhar entre projetos sem necessidade/autorização.

## HeroUI Pro v2 — arquivo público legado

- Components: https://v2.heroui.pro/components

Categorias:

- Charts: https://v2.heroui.pro/components/charts
- Application: https://v2.heroui.pro/components/application
- AI: https://v2.heroui.pro/components/ai
- Marketing: https://v2.heroui.pro/components/marketing
- E-commerce: https://v2.heroui.pro/components/ecommerce

Usar apenas como repertório visual/funcional para projetos novos, salvo necessidade explícita de manutenção v2.

## Atualização

Ao encontrar diferença material entre este índice e a fonte oficial:

1. confiar na fonte oficial atual;
2. verificar release/migration;
3. atualizar os catálogos em `ui/heroui/`;
4. registrar mudança relevante no histórico/estado da Factory.