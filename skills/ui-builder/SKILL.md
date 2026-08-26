---
name: ui-builder
description: Escolhe e aplica padrões de interface modernos para páginas, dashboards e sistemas, priorizando reutilização, consistência visual, Professional UI, Living UI/Semantic Motion e uso seletivo de shadcn, ReUI ou HeroUI conforme o tipo de aplicação.
---

# UI Builder

## Decisão do design system

1. Para sistemas administrativos, CRUDs, dashboards e ferramentas internas: usar **shadcn/ui como base**, salvo preferência explícita do produto por HeroUI.
2. Usar **ReUI seletivamente** quando um componente administrativo avançado reduzir trabalho e justificar dependências/complexidade.
3. Após instalar ReUI/registry, auditar arquivos e dependências adicionados e remover módulos não usados.
4. Considerar **HeroUI** como alternativa principal em aplicações onde seu sistema visual ofereça vantagem clara.
5. Quando o usuário pedir um sistema **baseado em HeroUI/HeroUI Pro**, tratar HeroUI como linguagem transversal do produto; não misturar shadcn/ReUI apenas para variedade visual.
6. Quando o projeto seguir o perfil `web-admin`, consultar `profiles/web-admin/PROFILE.md`.

A seleção da biblioteca e o acabamento profissional são decisões diferentes: shadcn/ReUI continuam preferenciais no admin **quando não existe uma escolha explícita de HeroUI**. Uma solicitação explícita de sistema HeroUI prevalece sobre esse default.

## Catálogo HeroUI obrigatório quando HeroUI for selecionado

Antes de criar componente, tela ou padrão próprio em um projeto HeroUI, ler `ui/heroui/README.md` e consultar o catálogo adequado:

- `ui/heroui/HEROUI_REACT_V3_CATALOG.md` — HeroUI React OSS atual;
- `ui/heroui/HEROUI_PRO_REACT_CATALOG.md` — HeroUI Pro React atual, variantes, templates, themes e tooling;
- `ui/heroui/HEROUI_NATIVE_CATALOG.md` — HeroUI Native OSS + Pro Native;
- `ui/heroui/HEROUI_PRO_V2_VISUAL_ARCHIVE.md` — repertório visual legado do Pro v2;
- `ui/heroui/OFFICIAL_SOURCES.md` — documentação, GitHub, Storybook, CLI, MCP, Skills e Figma oficiais;
- `ui/heroui/CATALOG_AUDIT_2026-08-24.md` — diferenças entre catálogo documentado e exports públicos;
- `ui/heroui/OVERLAY_INTERACTION_HARDENING.md` — semântica de navegação/ação, estado único de overlays, QA com ponteiro real e runtime gates.

Regras:

1. pesquisar no catálogo e na fonte oficial antes de recriar capacidade existente;
2. para projetos novos Web, preferir HeroUI v3 atual; usar v2 somente como repertório visual/funcional;
3. confirmar versão/release atual antes de instalar ou depender de uma API;
4. quando houver licença HeroUI Pro válida no projeto, preferir CLI/MCP/Skills oficiais para obter conteúdo autorizado;
5. nunca armazenar token Pro, código Pro, assets, screenshots, Figma ou templates comerciais na Factory;
6. sem licença Pro, usar nomes/padrões públicos como referência e implementar com HeroUI OSS ou componente local compatível;
7. manter HeroUI em shell, formulários, dados, overlays, estados, motion, tokens e temas — não só em cards/botões.

HeroUI não ativa automaticamente partículas, estrelas, fundos especiais, glows ou outro efeito ambiental. Esses recursos podem existir em um projeto quando forem desejados ou fizerem sentido, mas não são uma obrigação da App Factory.

## Overlays e navegação HeroUI — regra forte

Antes de construir ou revisar Drawer, Popover, Modal, busca/command ou navegação dentro de overlay, ler `ui/heroui/OVERLAY_INTERACTION_HARDENING.md`.

Regras obrigatórias:

- link é link; ação é `Button`/command apropriado; componente de seleção não substitui automaticamente navegação apenas por aparência;
- `ListBox`, `Select`, `ComboBox` e equivalentes permanecem para seleção/collection behavior quando essa for a semântica real;
- cada overlay controlado deve ter **uma única fonte de estado**; evitar trigger interno, `onPress`, `isOpen/onOpenChange` e listener global competindo pelo mesmo estado;
- quando um clique dentro do overlay navega e deve fechá-lo, preferir fechar na **mesma interação** do usuário e deixar a navegação ocorrer normalmente;
- não usar listener global como caminho primário de fechamento se isso puder competir com a renderização da nova rota;
- QA deve usar ponteiro real/hit-testing quando possível e aguardar o alvo ficar efetivamente atingível durante animações;
- erro/exceção não tratado da página/runtime, `console.error` relevante, overlay órfão, foco preso ou root recuperado inesperadamente são falhas de QA;
- quando performance for gate, definir antes ambiente, cache/rede, viewport, início/fim da medição e threshold derivado do SLO/baseline do projeto; depois medir múltiplas amostras e usar mediana para latência sustentada;
- antes de alterar a aplicação por uma falha automatizada, confirmar se o harness modela o elemento real;
- smoke no domínio oficial não pode criar sessão/cookie falso ou reduzir segurança.

## Professional UI Profile

Antes de implementar UI funcional destinada a usuário final, ler `ui/PROFESSIONAL_UI_PROFILE.md`.

Default da Factory: `professional-default`.

O perfil define o quality bar, não o pacote que deve ser instalado.

Derivar automaticamente quando possível:

- density: `compact`, `comfortable` ou `spacious`;
- surface: `flat`, `layered` ou `immersive`;
- emphasis: `quiet`, `balanced` ou `bold`.

Defaults comuns:

- admin/data-heavy: `comfortable + layered + balanced`;
- produto visual: `spacious + layered/immersive + balanced/bold`;
- mobile utilitário: `comfortable + flat/layered + balanced`.

Não perguntar ao usuário detalhes de radius, spacing, shadow, density ou animação quando puderem ser derivados do produto.

### Inventário antes da implementação

Para UI média/grande, identificar os arquétipos que realmente existem antes de construir componentes:

```text
shell
page-header
stats
search/command
filters
data-view (table/grid/list)
form
detail/inspector
modal/drawer
navigation/tabs
feedback
empty/error/loading
calendar/kanban/chart — somente se necessário
```

Pesquisar primeiro no design system/registry atual. Não criar componente próprio quando a biblioteca já oferecer composição equivalente.

### Regras de acabamento

- hierarquia perceptível antes de cor/motion;
- escala curta e coerente de tipografia;
- spacing por tokens, não valores aleatórios;
- poucos níveis de superfície/elevação;
- um CTA primário claro por contexto;
- cor semântica e contraste funcional;
- densidade compatível com a tarefa;
- progressive disclosure para informação/ações secundárias;
- estados completos, não apenas happy path;
- versão móvel reorganizada, não desktop simplesmente comprimido;
- microcopy orientada à tarefa e recovery;
- evitar excesso de cards, glow/gradiente sem função, múltiplos CTAs e mistura de design systems.

### Origem/licença

Referências comerciais como HeroUI Pro podem inspirar padrões públicos de composição e linguagem visual. Não copiar código, templates, assets ou screenshots proprietários para a Factory sem licença específica aplicável.

## Motion Profile

Antes de implementar UI relevante, ler `ui/MOTION_POLICY.md`.

Default contextual da Factory: `ambient`.

Perfis disponíveis: `none`, `subtle`, `ambient`, `expressive`.

Aplicar movimento semanticamente quando adequado:

- **ambient**: atmosfera contextual opcional e discreta;
- **interaction**: hover, foco, clique, cards, campos, menus;
- **data**: gráficos, indicadores, progresso e mudanças reais de valor;
- **state**: loading, saving, upload, sync, sucesso e erro;
- **attention**: ações pendentes/importantes com halo/pulso discreto e temporário;
- **navigation**: páginas, modais, drawers, tabs e expansão/recolhimento.

Não manter animação de atenção depois que o usuário já percebeu/interagiu. Não reanimar dados sem mudança real.

`prefers-reduced-motion` é obrigatório. `prefers-reduced-transparency` pode ser progressive enhancement.

## Antes de construir

- pesquisar componentes, blocks e registries adequados;
- consultar documentação/MCP disponível quando o agente puder;
- preferir composição de componentes consolidados a recriação manual;
- verificar licença e dependências antes de importar código externo;
- verificar primeiro se o design system atual já oferece o padrão necessário;
- registrar `professional-default`/exceção e Motion Profile.

## Qualidade visual

Evitar aparência genérica de app gerado por IA. Usar hierarquia clara, espaçamento consistente, tipografia coerente, densidade adequada, estados completos e motion proporcional.

Uma interface viva não significa movimento em tudo. Conteúdo principal deve permanecer legível e estável.

## Regra de sistema

Não redesenhar por impulso componentes estáveis já existentes. Em manutenção, preservar design system, Professional UI Profile e Motion Profile vigentes salvo redesign explícito ou problema real.

## Verificação

UI não é validada apenas por leitura de código. Quando possível, abrir a aplicação e testar visualmente/interativamente em desktop e mobile.

Também verificar quando aplicável:

- hierarquia e densidade do `professional-default`;
- loading/empty/error e ação destrutiva;
- coerência com Motion Profile;
- teclado/foco;
- animações de atenção encerram/reduzem;
- ausência de strobe/flashing;
- gráficos sem reanimação artificial;
- ausência de jank, overflow ou conteúdo obstruído;
- em overlays/navegação, ponteiro real consegue atingir o alvo após a animação;
- overlay fecha sem dupla fonte de estado ou listener global concorrente;
- zero erro/exceção não tratado e zero `console.error` relevante no fluxo aprovado;
- se latência for gate, protocolo de medição e threshold do projeto são definidos antes da coleta e avaliados por múltiplas amostras/mediana;
- falha de harness descartada antes de alterar a aplicação;
- screenshot regression somente com baseline estável e risco material.
