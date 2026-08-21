---
name: ui-builder
description: Escolhe e aplica padrões de interface modernos para páginas, dashboards e sistemas, priorizando reutilização de componentes e consistência visual com shadcn, ReUI ou HeroUI conforme o tipo de aplicação.
---

# UI Builder

## Decisão do design system

1. Para sistemas administrativos, CRUDs, dashboards e ferramentas internas: avaliar primeiro **shadcn + ReUI**.
2. Usar **shadcn** como base quando controle, composição e propriedade do código forem prioridades.
3. Usar **ReUI** para acelerar padrões avançados e telas de sistema quando houver componente adequado.
4. Considerar **HeroUI** como alternativa principal em aplicações onde seu sistema visual ofereça vantagem clara.
5. Não misturar HeroUI com shadcn/ReUI apenas para obter variedade visual.

## Antes de construir

- pesquisar componentes, blocks e registries adequados;
- consultar documentação/MCP disponível quando o agente puder;
- preferir composição de componentes consolidados a recriação manual;
- verificar licença e dependências antes de importar código externo.

## Qualidade visual

Evitar aparência genérica de app gerado por IA. Usar hierarquia clara, espaçamento consistente, tipografia coerente, densidade adequada e estados completos de interação.

Toda tela funcional deve considerar, quando aplicável: loading, vazio, erro, sucesso, disabled, responsividade, teclado/foco e acessibilidade básica.

## Regra de sistema

Não redesenhar por impulso componentes estáveis já existentes. Em manutenção, preserve o design system vigente salvo quando a tarefa for explicitamente de redesign.

## Verificação

UI não é validada apenas por leitura de código. Quando possível, abrir a aplicação e testar visualmente/interativamente em desktop e viewport móvel.