# Professional UI Profile — revisão e decisão

## Pergunta

A App Factory já armazenava os componentes/templates profissionais do HeroUI Pro, especialmente a linguagem visual `Default`?

## Conclusão

Não.

A Factory já possuía:

- HeroUI como design system alternativo aprovado;
- HeroUI v3 usado em piloto real;
- shadcn/ui como base preferencial do perfil administrativo;
- ReUI como complemento administrativo seletivo;
- Living UI / Semantic Motion;
- regras de hierarquia, acessibilidade, responsividade e browser QA.

Mas não havia um contrato visual transversal que transformasse essas ideias em um **quality bar profissional recuperável** para qualquer design system.

## Decisão

Criar `ui/PROFESSIONAL_UI_PROFILE.md` com perfil `professional-default`.

O perfil:

- é library-neutral;
- não altera a preferência `shadcn → ReUI seletivo` em admin/dashboard/CRUD;
- não rebaixa HeroUI, que continua alternativa principal em produtos altamente visuais;
- não força mistura de bibliotecas;
- define hierarquia, spacing, typography, surfaces, density, states, responsive, accessibility, microcopy, motion e visual QA;
- cataloga arquétipos profissionais de produto como shell, page header, stats, search/command, filters, data grid/table, form, detail/inspector, agenda/calendar, kanban e AI interface;
- funciona como camada de qualidade, não catálogo de código.

## Referências

### HeroUI open source

Uso já aprovado: design system alternativo quando sua linguagem visual for claramente mais adequada.

### HeroUI Pro

Referência pública observada: `https://heroui.pro/`, principalmente a direção visual `Default` e a organização em componentes/templates profissionais.

Decisão: **INSPIRAR**, não copiar.

O código, templates, assets e conteúdo comercial do HeroUI Pro não entram na Factory sem licença própria aplicável. A Factory absorve apenas padrões gerais de engenharia de interface que são independentes de implementação proprietária.

### shadcn/ui

Continua a base preferencial para admin/dashboard/CRUD por composição, copy-and-own, registry e integração forte com agentes.

### ReUI

Continua complemento seletivo para componentes administrativos avançados quando reduz trabalho de forma clara.

## Por que não tornar HeroUI Pro o default da Factory

1. A Factory é general-purpose e não deve depender de um catálogo comercial específico.
2. O perfil `web-admin` já foi validado com shadcn + ReUI.
3. Acabamento profissional é separável da biblioteca escolhida.
4. Misturar design systems aumenta inconsistência, bundle, dependências e custo de manutenção.
5. Um quality bar transversal beneficia também projetos React, extensões, sites e futuras stacks que não usem HeroUI.

## Mapeamento de responsabilidade

```text
UI_POLICY
  ↓ escolhe design system e regras globais
PROFESSIONAL_UI_PROFILE
  ↓ define qualidade/composição visual
MOTION_POLICY
  ↓ define comportamento de movimento
ui-builder
  ↓ aplica os três no projeto real
browser/Playwright/axe/visual regression
  ↓ verifica comportamento e acabamento quando aplicável
```

## Defaults preservados

```text
admin/dashboard/CRUD
  → shadcn/ui
  → ReUI apenas quando componente avançado justificar

produto altamente visual
  → HeroUI pode ser design system principal

qualquer UI material
  → professional-default como quality bar
  → Motion Profile contextual
```

## Critério de sucesso

A mudança está correta quando uma futura IA consegue responder sem ambiguidade:

- qual design system usar;
- que shadcn/ReUI continuam preferidos em admin;
- quando HeroUI é alternativa;
- o que significa acabamento `professional-default`;
- quais arquétipos procurar antes de criar componentes próprios;
- como tratar densidade, estados, responsividade e acessibilidade;
- que HeroUI Pro é referência de inspiração, não fonte de código proprietário.
