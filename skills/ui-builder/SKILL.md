---
name: ui-builder
description: Escolhe e aplica padrões de interface modernos para páginas, dashboards e sistemas, priorizando reutilização, consistência visual, Professional UI, Living UI/Semantic Motion e uso seletivo de shadcn, ReUI ou HeroUI conforme o tipo de aplicação.
---

# UI Builder

## Decisão do design system

1. Para sistemas administrativos, CRUDs, dashboards e ferramentas internas: usar **shadcn/ui como base**.
2. Usar **ReUI seletivamente** quando um componente administrativo avançado reduzir trabalho e justificar dependências/complexidade.
3. Após instalar ReUI/registry, auditar arquivos e dependências adicionados e remover módulos não usados.
4. Considerar **HeroUI** como alternativa principal em aplicações onde seu sistema visual ofereça vantagem clara.
5. Não misturar HeroUI com shadcn/ReUI apenas para obter variedade visual, animações ou aparência premium.
6. Quando o projeto seguir o perfil `web-admin`, consultar `profiles/web-admin/PROFILE.md`.

A seleção da biblioteca e o acabamento profissional são decisões diferentes: **shadcn/ReUI continuam preferenciais no admin mesmo quando `professional-default` estiver ativo**.

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

Não perguntar ao usuário detalhes de radius, spacing, shadow, density ou animação quando eles puderem ser derivados do produto. Perguntar somente quando houver preferência visual/subjetiva que realmente altere o produto.

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

Pesquisar primeiro no design system/registry atual. Não criar um “componente profissional próprio” quando a biblioteca já oferecer composição equivalente.

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
- evitar excesso de cards, glow/gradiente decorativo, múltiplos CTAs e mistura de design systems.

### Origem/licença

Referências comerciais como HeroUI Pro podem inspirar padrões públicos de composição e linguagem visual. **Não copiar código, templates, assets ou screenshots proprietários para a Factory** sem licença específica que autorize esse uso no projeto.

## Motion Profile

Antes de implementar UI relevante, ler `ui/MOTION_POLICY.md`.

Default contextual da Factory: `ambient`.

Perfis disponíveis: `none`, `subtle`, `ambient`, `expressive`.

O Motion Profile é independente do design system e do Professional UI Profile. Preservar a biblioteca visual escolhida e aplicar movimento por seus recursos nativos, CSS/transições ou uma camada de motion especializada somente quando necessário.

Aplicar movimento semanticamente quando adequado:

- **ambient**: aurora/gradiente/luz/partículas lentas em áreas com espaço visual;
- **interaction**: hover, foco, clique, cards, campos, menus;
- **data**: gráficos, indicadores, progresso e mudanças reais de valor;
- **state**: loading, saving, upload, sync, sucesso e erro;
- **attention**: ações pendentes/importantes com halo/pulso discreto e temporário;
- **navigation**: páginas, modais, drawers, tabs e expansão/recolhimento.

Não manter animação de atenção depois que o usuário já percebeu/interagiu. Não reanimar dados sem mudança real.

Em leitura longa, dashboards densos, desempenho limitado ou tarefas de alta concentração, atenuar `ambient` para comportamento `subtle` sem perder microinterações/feedback.

`prefers-reduced-motion` é obrigatório para movimento não essencial.

## Antes de construir

- pesquisar componentes, blocks e registries adequados;
- consultar documentação/MCP disponível quando o agente puder;
- preferir composição de componentes consolidados a recriação manual;
- verificar licença e dependências antes de importar código externo;
- verificar primeiro se o design system atual já oferece a animação e o padrão de composição necessários;
- registrar `professional-default`/exceção no estado de produto/arquitetura quando UI material fizer parte do projeto.

## Qualidade visual

Evitar aparência genérica de app gerado por IA. Usar hierarquia clara, espaçamento consistente, tipografia coerente, densidade adequada, estados completos de interação e motion proporcional.

Toda tela funcional deve considerar, quando aplicável: loading, vazio, erro, sucesso, disabled, responsividade, teclado/foco, acessibilidade básica e feedback de movimento.

Uma interface viva não significa movimento em tudo. Conteúdo principal deve permanecer legível e estável; motion deve orientar, responder ou comunicar.

## Regra de sistema

Não redesenhar por impulso componentes estáveis já existentes. Em manutenção, preservar design system, Professional UI Profile e Motion Profile vigentes salvo quando a tarefa for explicitamente de redesign ou houver problema real de acessibilidade/desempenho/coerência.

## Verificação

UI não é validada apenas por leitura de código. Quando possível, abrir a aplicação e testar visualmente/interativamente em desktop e viewport móvel.

Também verificar quando aplicável:

- hierarquia e densidade do `professional-default`;
- loading/empty/error e ação destrutiva;
- coerência com Motion Profile;
- `prefers-reduced-motion`;
- teclado/foco;
- animações de atenção que encerram/reduzem após cumprir a função;
- gráficos sem reanimação artificial;
- ausência de jank, overflow ou conteúdo obstruído;
- screenshot regression somente com baseline estável e risco material.
