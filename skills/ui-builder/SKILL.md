---
name: ui-builder
description: Escolhe e aplica padrões de interface modernos para páginas, dashboards e sistemas, priorizando reutilização, consistência visual, Living UI/Semantic Motion e uso seletivo de shadcn, ReUI ou HeroUI conforme o tipo de aplicação.
---

# UI Builder

## Decisão do design system

1. Para sistemas administrativos, CRUDs, dashboards e ferramentas internas: usar **shadcn/ui como base**.
2. Usar **ReUI seletivamente** quando um componente administrativo avançado reduzir trabalho e justificar dependências/complexidade.
3. Após instalar ReUI/registry, auditar arquivos e dependências adicionados e remover módulos não usados.
4. Considerar **HeroUI** como alternativa principal em aplicações onde seu sistema visual ofereça vantagem clara.
5. Não misturar HeroUI com shadcn/ReUI apenas para obter variedade visual ou animações.
6. Quando o projeto seguir o perfil `web-admin`, consultar `profiles/web-admin/PROFILE.md`.

## Motion Profile

Antes de implementar UI relevante, ler `ui/MOTION_POLICY.md`.

Default contextual da Factory: `ambient`.

Perfis disponíveis: `none`, `subtle`, `ambient`, `expressive`.

O motion profile é independente do design system. Preservar a biblioteca visual escolhida e aplicar movimento por seus recursos nativos, CSS/transições ou uma camada de motion especializada somente quando necessário.

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
- verificar primeiro se o design system atual já oferece a animação necessária.

## Qualidade visual

Evitar aparência genérica de app gerado por IA. Usar hierarquia clara, espaçamento consistente, tipografia coerente, densidade adequada, estados completos de interação e motion proporcional.

Toda tela funcional deve considerar, quando aplicável: loading, vazio, erro, sucesso, disabled, responsividade, teclado/foco, acessibilidade básica e feedback de movimento.

Uma interface viva não significa movimento em tudo. Conteúdo principal deve permanecer legível e estável; motion deve orientar, responder ou comunicar.

## Regra de sistema

Não redesenhar por impulso componentes estáveis já existentes. Em manutenção, preservar design system e Motion Profile vigentes salvo quando a tarefa for explicitamente de redesign ou houver problema real de acessibilidade/desempenho.

## Verificação

UI não é validada apenas por leitura de código. Quando possível, abrir a aplicação e testar visualmente/interativamente em desktop e viewport móvel.

Também verificar quando aplicável:

- coerência com Motion Profile;
- `prefers-reduced-motion`;
- animações de atenção que encerram/reduzem após cumprir a função;
- gráficos sem reanimação artificial;
- ausência de jank, overflow ou conteúdo obstruído.