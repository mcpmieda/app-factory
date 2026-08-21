# UI Policy

## Objetivo

Produzir interfaces atuais, consistentes, vivas e fáceis de manter sem transformar a aplicação em colagem de bibliotecas ou animações decorativas.

## Seleção padrão

### Admin, dashboard, CRUD, ferramentas internas

Base preferencial: **shadcn/ui**.

Usar **ReUI seletivamente** para componentes administrativos avançados quando o ganho justificar a complexidade, por exemplo Data Grid, filtros complexos, calendários, Kanban ou padrões equivalentes.

O piloto V0.3 mostrou que ReUI agrega muito valor em componentes avançados, mas pode trazer arquivos/dependências opcionais que precisam de auditoria pós-instalação. Portanto, não tratar `shadcn + ReUI` como duas bases obrigatórias instaladas integralmente em todo admin.

### Aplicações altamente visuais

Avaliar **HeroUI** como design system principal quando oferecer vantagem clara. Não adicioná-lo apenas para usar componentes decorativos se o projeto já estiver coeso em shadcn/ReUI.

## Motion Profile universal

Toda interface deve seguir `ui/MOTION_POLICY.md` e registrar um Motion Profile.

Default contextual da Factory: **`ambient`**.

Isso significa interface viva por movimento semântico, microinterações e atmosfera suave quando o contexto permitir — não partículas ou auroras obrigatórias em toda tela.

Perfis disponíveis:

- `none`;
- `subtle`;
- `ambient`;
- `expressive`.

Uma preferência explícita do usuário sobre design/motion tem precedência. O perfil de motion é independente do design system: HeroUI, shadcn, ReUI ou outro kit continuam responsáveis pela linguagem visual; a Motion Policy define como a interface se move.

## Regras

1. Pesquisar antes de construir componente equivalente.
2. Consultar registry/MCP quando disponível.
3. Preferir blocks/padrões completos quando reduzirem trabalho sem importar complexidade inútil.
4. Verificar licença, manutenção, dependências e compatibilidade antes de incorporar código externo.
5. Evitar dependências duplicadas para a mesma função.
6. Preservar o design system vigente em manutenção, salvo redesign explícito.
7. Criar tokens e convenções locais para não depender visualmente dos defaults da biblioteca.
8. Após instalar código de registry, revisar arquivos/dependências adicionados e remover o que não for utilizado.
9. Não instalar outro design system apenas para obter animação.
10. Usar movimento para comunicar interação, dados, estado, atenção, navegação ou atmosfera contextual; remover animação que só gere ruído.
11. Respeitar `prefers-reduced-motion` e reduzir movimento em leitura longa, telas densas ou contextos em que ele atrapalhe a tarefa.

## Padrões mínimos de tela

Quando aplicável, tratar loading, empty state, error state, success feedback, disabled, foco/teclado, responsividade, contraste/acessibilidade, densidade adequada e feedback de motion coerente com o contexto.

Ações importantes podem receber atenção visual temporária; gráficos podem animar mudanças reais; transições de navegação devem preservar continuidade. Nada disso deve competir com conteúdo ou permanecer chamando atenção indefinidamente.

## Perfil web-admin validado

Consultar `profiles/web-admin/PROFILE.md` para defaults e módulos opcionais comprovados. O perfil herda a Motion Policy universal e atenua `ambient` para `subtle` em telas administrativas densas quando necessário.

## Registry futuro

A Factory deverá distribuir componentes, layouts, páginas, convenções, motion primitives, testes e configurações aprovadas por registry.