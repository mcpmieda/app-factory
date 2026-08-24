# Sources — referências iniciais

Referências influenciam a Factory, mas não viram regra automaticamente. Primeiro devem ser avaliadas criticamente.

## Agentes

### OpenAI Codex
- https://openai.com/codex/
- https://openai.com/index/introducing-codex/

Uso: `AGENTS.md`, desenvolvimento agentic, worktrees, Skills e execução verificável.

### Anthropic Agent Skills / Claude Code
- https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- https://www.anthropic.com/webinars/claude-code-foundations

Uso: Skills portáveis, `SKILL.md`, progressive disclosure, contexto do repositório, subagentes e MCP como referência arquitetural.

## UI e Registry

### shadcn/ui
- https://ui.shadcn.com/docs/registry
- https://ui.shadcn.com/docs/registry/github
- https://ui.shadcn.com/docs/mcp

Uso: registry distribuindo componentes, páginas, regras, workflows, testes e automações; MCP para agentes pesquisarem e instalarem itens. Continua base preferencial da Factory para admin/dashboard/CRUD.

### ReUI
- https://reui.io/

Uso: componentes e padrões avançados para sistemas sobre ecossistema shadcn. Continua complemento seletivo, não segunda base obrigatória.

### HeroUI OSS
- https://heroui.com/
- https://heroui.com/en/docs/react/components
- https://heroui.com/en/docs/native/components
- https://github.com/heroui-inc/heroui
- https://github.com/heroui-inc/heroui-native
- https://github.com/heroui-inc/heroui-cli
- https://storybook-v3.heroui.com/

Uso: alternativa de design system quando mais adequada que shadcn/ReUI. O inventário pesquisável da Factory está em `ui/heroui/` e deve ser consultado quando HeroUI for escolhido.

### HeroUI Pro
- https://heroui.pro/
- https://heroui.pro/docs/react/components
- https://heroui.pro/docs/react/templates
- https://heroui.pro/docs/native/components
- https://heroui.pro/docs/native/templates
- https://heroui.pro/docs/react/getting-started/theming
- https://heroui.pro/docs/react/getting-started/mcp-server
- https://heroui.pro/docs/react/getting-started/agent-skills
- https://heroui.pro/docs/react/getting-started/design-taste
- https://heroui.pro/docs/react/getting-started/figma
- https://v2.heroui.pro/components

Uso: **INSPIRAR** o quality bar governado por `ui/PROFESSIONAL_UI_PROFILE.md` e servir como catálogo autorizado de descoberta. A Factory registra nomes, categorias, variantes, templates, temas, URLs e padrões públicos em `ui/heroui/`, mas não copia código, templates, assets, screenshots ou Figma proprietários. Em projetos com licença válida, obter conteúdo Pro pelos mecanismos oficiais do projeto (CLI/MCP/dashboard) e nunca versionar `HEROUI_PERSONAL_TOKEN`.

## Origem interna

A pasta histórica `Boas práticas/` do repositório `mcpmieda/escolaieda` é a fonte da V0 da filosofia da Factory. Seus princípios foram filtrados; não devem ser copiados integralmente nem carregados em todo contexto.

## Regra de pesquisa

Para novas fontes registrar: problema que resolve, licença, manutenção, qualidade arquitetural, testes, dependências, segurança, compatibilidade, decisão **ADOTAR / INSPIRAR / DESCARTAR** e justificativa curta.
