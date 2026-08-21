# UI Policy

## Objetivo

Produzir interfaces atuais, consistentes e fáceis de manter sem transformar a aplicação em colagem de bibliotecas.

## Seleção padrão

### Admin, dashboard, CRUD, ferramentas internas

Preferência inicial: **shadcn + ReUI**.

### Aplicações altamente visuais

Avaliar **HeroUI** como design system principal quando oferecer vantagem clara. Não adicioná-lo apenas para usar alguns componentes decorativos se o projeto já estiver coeso em shadcn/ReUI.

## Regras

1. Pesquisar antes de construir componente equivalente.
2. Consultar registry/MCP quando disponível.
3. Preferir blocks/padrões completos quando reduzirem trabalho sem importar complexidade inútil.
4. Verificar licença, manutenção, dependências e compatibilidade antes de incorporar código externo.
5. Evitar dependências duplicadas para a mesma função.
6. Preservar o design system vigente em manutenção, salvo redesign explícito.
7. Criar tokens e convenções locais para não depender visualmente dos defaults da biblioteca.

## Padrões mínimos de tela

Quando aplicável, tratar loading, empty state, error state, success feedback, disabled, foco/teclado, responsividade, contraste/acessibilidade e densidade adequada ao contexto.

## Registry futuro

A Factory deverá distribuir componentes, layouts, páginas, convenções, testes e configurações aprovadas por registry.