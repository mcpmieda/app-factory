# UI Policy

## Objetivo

Produzir interfaces atuais, consistentes e fáceis de manter sem transformar a aplicação em colagem de bibliotecas.

## Seleção padrão

### Admin, dashboard, CRUD, ferramentas internas

Base preferencial: **shadcn/ui**.

Usar **ReUI seletivamente** para componentes administrativos avançados quando o ganho justificar a complexidade, por exemplo Data Grid, filtros complexos, calendários, Kanban ou padrões equivalentes.

O piloto V0.3 mostrou que ReUI agrega muito valor em componentes avançados, mas pode trazer arquivos/dependências opcionais que precisam de auditoria pós-instalação. Portanto, não tratar `shadcn + ReUI` como duas bases obrigatórias instaladas integralmente em todo admin.

### Aplicações altamente visuais

Avaliar **HeroUI** como design system principal quando oferecer vantagem clara. Não adicioná-lo apenas para usar componentes decorativos se o projeto já estiver coeso em shadcn/ReUI.

## Regras

1. Pesquisar antes de construir componente equivalente.
2. Consultar registry/MCP quando disponível.
3. Preferir blocks/padrões completos quando reduzirem trabalho sem importar complexidade inútil.
4. Verificar licença, manutenção, dependências e compatibilidade antes de incorporar código externo.
5. Evitar dependências duplicadas para a mesma função.
6. Preservar o design system vigente em manutenção, salvo redesign explícito.
7. Criar tokens e convenções locais para não depender visualmente dos defaults da biblioteca.
8. Após instalar código de registry, revisar arquivos/dependências adicionados e remover o que não for utilizado.

## Padrões mínimos de tela

Quando aplicável, tratar loading, empty state, error state, success feedback, disabled, foco/teclado, responsividade, contraste/acessibilidade e densidade adequada ao contexto.

## Perfil web-admin validado

Consultar `profiles/web-admin/PROFILE.md` para defaults e módulos opcionais comprovados pelo piloto V0.3.

## Registry futuro

A Factory deverá distribuir componentes, layouts, páginas, convenções, testes e configurações aprovadas por registry.