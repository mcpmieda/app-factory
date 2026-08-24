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

### HeroUI como linguagem principal

Quando o usuário pedir um **sistema baseado em HeroUI/HeroUI Pro** ou quando HeroUI for selecionado como design system principal de um sistema novo:

- HeroUI deve ser linguagem transversal do produto, não apenas fonte de alguns cards/botões;
- consultar obrigatoriamente `ui/heroui/README.md` e seus catálogos;
- ativar nativamente `ui/AMBIENT_CONSTELLATION_PROFILE.md`;
- registrar `Ambient Surface Profile: ambient-constellation`;
- usar `Constellation Intensity: strong` por padrão;
- aplicar a constelação fortemente a shell/header/hero/login/dashboard overview/empty-waiting/AI/modal importante/painéis e cards especiais quando existirem;
- manter Data Grid, tabelas, formulários e áreas longas de leitura em superfícies limpas, preservando a constelação no shell/perímetro/cabeçalho;
- usar tokens/tema HeroUI para adaptar a paleta, sem hardcode universal do azul da referência;
- reduced motion deve parar/reduzir drift, mantendo fallback constelar estático quando legível.

Só remover esse default por preferência explícita do usuário ou restrição real de produto, acessibilidade, plataforma ou desempenho.

## Professional UI Profile

Toda UI funcional destinada a usuário final deve considerar `ui/PROFESSIONAL_UI_PROFILE.md`.

Default de acabamento da Factory: **`professional-default`**.

Este perfil é um **quality bar transversal**, não um design system. Ele define composição profissional — hierarquia, ritmo de espaçamento, tipografia, superfícies, densidade, estados completos, responsividade, acessibilidade, microcopy e visual QA — usando a biblioteca já escolhida pelo projeto.

Consequências:

- **shadcn continua preferencial** em admin/dashboard/CRUD quando não houver escolha explícita de HeroUI;
- **ReUI continua complemento seletivo** para padrões administrativos avançados;
- **HeroUI continua alternativa principal** quando o produto for altamente visual ou sua linguagem oferecer vantagem clara;
- escolha explícita de HeroUI para o sistema inteiro prevalece sobre o default administrativo shadcn/ReUI;
- não misturar bibliotecas para “alcançar o perfil”;
- HeroUI Pro pode inspirar linguagem/composição publicamente observável, mas a Factory não copia código, templates ou assets proprietários;
- protótipo descartável pode reduzir o acabamento, mas não pode ignorar coerência, estados essenciais ou acessibilidade básica.

Quando a UI for relevante, registrar no projeto:

- design system;
- Professional UI Profile: `professional-default` ou exceção justificada;
- density: `compact`, `comfortable` ou `spacious` quando material;
- surface: `flat`, `layered` ou `immersive` quando material;
- emphasis: `quiet`, `balanced` ou `bold` quando material;
- Motion Profile conforme `ui/MOTION_POLICY.md`;
- Ambient Surface Profile quando ativo;
- Constellation Intensity quando `ambient-constellation` estiver ativo.

Não obrigar o usuário a escolher detalhes técnicos quando a Factory puder inferi-los pelo tipo do produto e pela preferência já conhecida.

## Motion Profile universal

Toda interface deve seguir `ui/MOTION_POLICY.md` e registrar um Motion Profile.

Default contextual da Factory: **`ambient`**.

Isso significa interface viva por movimento semântico, microinterações e atmosfera suave quando o contexto permitir.

Perfis disponíveis:

- `none`;
- `subtle`;
- `ambient`;
- `expressive`.

O perfil ambiental `ambient-constellation` é definido separadamente em `ui/AMBIENT_CONSTELLATION_PROFILE.md`. Pedidos como `ambient constellation`, `ambient constellarion` e `ambiente de constelação` o ativam com intensidade `strong`; HeroUI novo o herda automaticamente.

Uma preferência explícita do usuário sobre design/motion tem precedência. O Motion Profile é independente do design system e do Professional UI Profile.

## Regras

1. Pesquisar antes de construir componente equivalente.
2. Consultar registry/MCP quando disponível.
3. Preferir blocks/padrões completos quando reduzirem trabalho sem importar complexidade inútil.
4. Verificar licença, manutenção, dependências e compatibilidade antes de incorporar código externo.
5. Evitar dependências duplicadas para a mesma função.
6. Preservar o design system vigente em manutenção, salvo redesign explícito.
7. Criar tokens e convenções locais para não depender visualmente dos defaults da biblioteca.
8. Após instalar código de registry, revisar arquivos/dependências adicionados e remover o que não for utilizado.
9. Não instalar outro design system apenas para obter animação ou acabamento visual.
10. Usar movimento para comunicar interação, dados, estado, atenção, navegação ou atmosfera contextual; remover animação que só gere ruído.
11. Respeitar `prefers-reduced-motion`; `prefers-reduced-transparency` pode ser progressive enhancement.
12. Para UI média/grande, fazer inventário dos arquétipos necessários antes de criar componentes próprios: shell, page header, stats, search/command, filters, data view, form, detail/inspector, feedback e somente então calendar/kanban/chart quando o produto exigir.
13. Evitar padrões de aparência genérica de app gerado por IA: excesso de cards equivalentes, múltiplos CTAs primários, gradientes/glow sem função, hierarquia fraca e mistura de design systems.
14. Quando `ambient-constellation` estiver ativo, seguir o mapa de superfícies e QA do perfil canônico; não improvisar partículas ad hoc em cada página.
15. Intensidade `strong` significa presença por composição/profundidade, não velocidade, strobe, saturação extrema ou estrelas sobre conteúdo.

## Padrões mínimos de tela

Quando aplicável, tratar loading, empty state, error state, success feedback, disabled, foco/teclado, responsividade, contraste/acessibilidade, densidade adequada e feedback de motion coerente com o contexto.

Ações importantes podem receber atenção visual temporária; gráficos podem animar mudanças reais; transições de navegação devem preservar continuidade. Nada disso deve competir com conteúdo ou permanecer chamando atenção indefinidamente.

O estado ideal não basta: quando material, verificar também hover, focus-visible, pressed, selected, loading, empty, partial data, warning, error, permission denied e recovery/retry.

## Verificação visual

UI relevante deve ser validada no browser real quando a capacidade estiver disponível.

Verificar proporcionalmente:

- desktop;
- viewport móvel;
- teclado/foco;
- loading/empty/error;
- ação principal e destrutiva;
- overflow/clipping;
- console sem erro relevante;
- `prefers-reduced-motion`;
- acessibilidade básica;
- `ambient-constellation` perceptível e não obstrutivo quando ativo;
- fallback constelar estático sob reduced motion;
- ausência de flashing/strobe;
- screenshot regression somente quando houver baseline estável e risco material.

## Perfil web-admin validado

Consultar `profiles/web-admin/PROFILE.md` para defaults e módulos opcionais comprovados. O perfil herda esta UI Policy, portanto mantém shadcn como base e ReUI seletivo **quando HeroUI não foi escolhido explicitamente**. Se o projeto administrativo for explicitamente HeroUI, a escolha HeroUI é transversal e herda `ambient-constellation` strong.

## Registry futuro

A Factory deverá distribuir somente componentes, layouts, páginas, convenções, motion primitives, testes e configurações **aprovados e licenciados** por registry. `ambient-constellation` deve virar primitive reutilizável somente depois de implementação real validada; a política já define o contrato independente da implementação.
