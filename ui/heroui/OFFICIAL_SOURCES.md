# HeroUI — Fontes oficiais

Snapshot auditado: **2026-08-24**.

## Hierarquia de autoridade

Usar nesta ordem quando houver divergência:

1. página oficial atual `All Components` para catálogo nominal;
2. repositório/package oficial para exports auxiliares e composição;
3. release notes para status, mudanças e itens experimentais;
4. documentação Pro atual para componentes licenciados;
5. HeroUI Pro v2 apenas como repertório legado.

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

- Getting Started: https://heroui.com/en/docs/native/getting-started
- Native Components: https://heroui.com/en/docs/native/components
- Native Styling: https://heroui.com/en/docs/native/getting-started/styling
- Native Design Principles: https://heroui.com/en/docs/native/getting-started/design-principles
- Native Releases: https://heroui.com/en/docs/native/releases

## GitHub oficial

Organização: https://github.com/heroui-inc

Repositórios principais:

- React/Web monorepo: https://github.com/heroui-inc/heroui
- React Native: https://github.com/heroui-inc/heroui-native
- HeroUI MCP OSS: https://github.com/heroui-inc/heroui-mcp
- CLI: https://github.com/heroui-inc/heroui-cli
- Tailwind Variants: https://github.com/heroui-inc/tailwind-variants
- Native Example: https://github.com/heroui-inc/heroui-native-example

Templates oficiais OSS:

- Next.js App Router: https://github.com/heroui-inc/next-app-template
- Next.js Pages Router: https://github.com/heroui-inc/next-pages-template
- Vite: https://github.com/heroui-inc/vite-template
- React Router: https://github.com/heroui-inc/react-router-template

Arquivos úteis para agentes/arquitetura:

- React package guide: https://github.com/heroui-inc/heroui/blob/v3/packages/react/README.md
- React component exports: https://github.com/heroui-inc/heroui/blob/v3/packages/react/src/components/index.ts
- React Aria bridge: https://github.com/heroui-inc/heroui/blob/v3/packages/react/src/components/rac/index.ts
- React hooks: https://github.com/heroui-inc/heroui/blob/v3/packages/react/src/hooks/index.ts
- Styles package guide: https://github.com/heroui-inc/heroui/blob/v3/packages/styles/README.md
- AGENTS.md oficial: https://github.com/heroui-inc/heroui/blob/v3/AGENTS.md
- HeroUI React Skill: https://github.com/heroui-inc/heroui/blob/v3/skills/heroui-react/SKILL.md
- HeroUI Native Skill: https://github.com/heroui-inc/heroui/blob/v3/skills/heroui-native/SKILL.md
- Native public exports: https://github.com/heroui-inc/heroui-native/blob/main/src/index.tsx

## HeroUI CLI

Repository: https://github.com/heroui-inc/heroui-cli

Capacidades relevantes incluem init/templates, install, upgrade, uninstall, doctor, env e `agents-md` para baixar/indexar documentação oficial atual para agentes.

## HeroUI MCP OSS

Repository: https://github.com/heroui-inc/heroui-mcp

Usar quando o ambiente estiver trabalhando somente com HeroUI OSS. Quando houver HeroUI Pro autorizado, preferir o MCP Pro unificado, que cobre OSS + Pro.

## HeroUI Pro React

- Site: https://heroui.pro/
- Getting Started: https://heroui.pro/docs/react/getting-started
- Components: https://heroui.pro/docs/react/components
- Templates: https://heroui.pro/docs/react/templates
- Installation: https://heroui.pro/docs/react/getting-started/installation
- Theming / Design Systems: https://heroui.pro/docs/react/getting-started/theming
- Figma: https://heroui.pro/docs/react/getting-started/figma
- MCP: https://heroui.pro/docs/react/getting-started/mcp-server
- Agent Skills: https://heroui.pro/docs/react/getting-started/agent-skills
- Design Taste: https://heroui.pro/docs/react/getting-started/design-taste
- Releases: https://heroui.pro/docs/react/releases

## HeroUI Pro Native

- Components: https://heroui.pro/docs/native/components
- Templates: https://heroui.pro/docs/native/templates
- Getting Started: https://heroui.pro/docs/native/getting-started
- Agent Skills: https://heroui.pro/docs/native/getting-started/agent-skills
- Releases: https://heroui.pro/docs/native/releases

## HeroUI Pro Themes

Temas premium atuais documentados:

- Brutalism
- Glass
- Mouve

Cada um possui variantes light/dark. Fonte: https://heroui.pro/docs/react/getting-started/theming

## HeroUI Pro Design Systems / AI tooling

O ecossistema Pro oferece:

- Design Systems com export de Web CSS / Native CSS / `DESIGN.md` / `PRODUCT.md`;
- AI Chat e export de interfaces;
- MCP oficial unificado OSS + Pro;
- skill React Pro;
- skill Native Pro;
- Design Taste skill;
- Figma files Pro e Figma Theme Sync.

O MCP Pro documenta ferramentas para listar componentes, consultar docs/CSS/theme variables, acessar source OSS e importar exports de AI Chat/Design Systems.

## HeroUI Pro v2 — arquivo público legado

- Components: https://v2.heroui.pro/components
- Charts: https://v2.heroui.pro/components/charts
- Application: https://v2.heroui.pro/components/application
- AI: https://v2.heroui.pro/components/ai
- Marketing: https://v2.heroui.pro/components/marketing
- E-commerce: https://v2.heroui.pro/components/ecommerce

Usar apenas como repertório visual/funcional para projetos novos, salvo manutenção v2 explícita.

## Auditoria local

Consultar `CATALOG_AUDIT_2026-08-24.md` para a reconciliação item a item entre site, source oficial e catálogo da Factory.

## Atualização

Ao encontrar diferença material:

1. confiar na fonte oficial atual;
2. verificar release/migration;
3. atualizar os catálogos em `ui/heroui/`;
4. rebaixar itens removidos para histórico em vez de tratá-los como atuais;
5. registrar a mudança relevante no estado/histórico da Factory.