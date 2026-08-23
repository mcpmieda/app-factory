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

### HeroUI
- https://www.heroui.com/

Uso: alternativa de design system quando mais adequada que shadcn/ReUI.

### HeroUI Pro
- https://heroui.pro/

Uso: **INSPIRAR** o quality bar `professional-default`, especialmente composição visual profissional e organização por arquétipos de produto. Não é fonte de código redistribuível da Factory: não copiar templates, assets, screenshots ou componentes proprietários sem licença específica aplicável ao projeto. Ver `research/PROFESSIONAL_UI_PROFILE_REVIEW.md` e `ui/PROFESSIONAL_UI_PROFILE.md`.

## Origem interna

A pasta histórica `Boas práticas/` do repositório `mcpmieda/escolaieda` é a fonte da V0 da filosofia da Factory. Seus princípios foram filtrados; não devem ser copiados integralmente nem carregados em todo contexto.

## Regra de pesquisa

Para novas fontes registrar: problema que resolve, licença, manutenção, qualidade arquitetural, testes, dependências, segurança, compatibilidade, decisão **ADOTAR / INSPIRAR / DESCARTAR** e justificativa curta.
