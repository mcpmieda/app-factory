# HeroUI Native Redesign Contract

## Objetivo

Quando HeroUI for escolhido explicitamente como linguagem principal — especialmente quando o usuário pedir que a interface pareça criada do zero em HeroUI — a implementação deve ser **nativamente HeroUI**, não uma camada de compatibilidade sobre uma arquitetura visual anterior.

Este contrato complementa `README.md`, `../MOTION_POLICY.md` e `TEMPORAL_MOTION_QA.md`.

## Regra de reconstrução limpa

Em redesign explícito de um produto existente para HeroUI:

1. preservar regras de negócio, contratos, autenticação, autorização, dados, rotas e integrações;
2. reconstruir a **árvore de apresentação** a partir da anatomia HeroUI v3;
3. usar diretamente componentes e compound components oficiais (`Breadcrumbs`, `ListBox`, `SearchField`, `Kbd`, `Popover`, `Dropdown`, `Card`, `Surface`, `Alert`, `Table`, `Chip`, `Avatar`, `Drawer`, `Spinner`, `Skeleton`, `ProgressBar`, `ScrollShadow`, etc.) quando a capacidade existir;
4. remover facades/adapters cujo objetivo seja manter APIs de outro design system (`CardHeader`, `Badge`, `Button variant=default`, `asChild`, wrappers de shadcn/Radix, etc.);
5. remover arquivos, classes e dependências do design system anterior quando não tiverem consumidor real;
6. componentes locais continuam permitidos quando representam **padrões reais de produto**, mas não devem fingir a API de shadcn/ReUI para esconder HeroUI por baixo;
7. preferir a composição compound do HeroUI v3 a copiar anatomias anteriores;
8. depois de remover dependências/facades, executar também a **auditoria de substituição de componentes** descrita abaixo.

### Gate obrigatório de limpeza

Um redesign HeroUI não é considerado concluído enquanto existir uma camada de compatibilidade visual do design system anterior sem necessidade funcional comprovada.

Auditar especificamente:

- diretórios como `components/ui` herdados de shadcn;
- variantes legadas (`default`, `destructive`, `asChild`) apenas traduzidas para variantes HeroUI;
- cards reconstruídos por wrappers para manter `CardHeader/CardContent` antigos;
- tabelas HTML apenas maquiadas com classes quando o `Table` compound atual atende ao caso;
- CSS com nomes/semântica do design system anterior;
- componentes duplicados que só existem para evitar alterar imports antigos.

Se o objetivo é redesign “do zero”, **alterar os imports e a composição é parte do trabalho**, não regressão.

## Auditoria de substituição de componentes

Remover `shadcn`, `Radix`, ReUI ou facades **não basta**. Um sistema pode continuar visualmente antigo quando mantém a mesma anatomia manual usando `div`, `span`, links e CSS próprios.

Depois da limpeza de dependências, comparar cada padrão visível com o catálogo HeroUI atual e substituir implementações manuais quando existir equivalente semântico adequado.

Exemplos obrigatórios de auditoria:

| Padrão manual/legado | Preferência HeroUI v3 |
| --- | --- |
| `Centro / Página` montado com spans | `Breadcrumbs` + `Breadcrumbs.Item` |
| tecla `Ctrl K` desenhada com `<kbd>` próprio | `Kbd`, `Kbd.Abbr`, `Kbd.Content` |
| sidebar feita com links + classes de selected | coleção/navegação HeroUI apropriada + `ScrollShadow` |
| busca composta por input + popup absoluto | `SearchField` + `Popover` + coleção adequada |
| bloco avatar/nome/botão sair montado à mão | `Avatar` + `Dropdown`/Menu |
| lista de sinais ou registros com divisores manuais | `Table`, `ListBox` ou coleção HeroUI conforme semântica |
| percentual/cobertura desenhado à mão | `ProgressBar`, `Meter` ou `ProgressCircle` |
| mensagem/status institucional como card genérico | `Alert` + `Chip` conforme semântica |
| menu mobile customizado | `Drawer` compound |

### Regra de decisão

1. Se HeroUI possui componente com a semântica correta, usar o componente nativo.
2. Se o componente oficial não resolve a necessidade, compor primitives HeroUI.
3. Só então criar componente local.
4. Componente local não deve reproduzir uma API antiga por conveniência.

O gate de redesign deve procurar **resíduos visuais**, não apenas imports antigos.

## Hierarquia HeroUI recomendada

A interface deve explorar níveis semânticos do ecossistema:

- `Surface` para ilhas, painéis e regiões de layout;
- `Card` compound para unidades de informação;
- `Alert` para estados institucionais/validação;
- `Chip` para status e categorias;
- `Breadcrumbs` para localização hierárquica;
- componentes de coleção conforme a semântica real;
- `SearchField` + `Popover` para busca;
- `Dropdown` para ações de conta e menus contextuais;
- `Kbd` para atalhos;
- `Table` compound para dados estruturados;
- `ProgressBar`/`Meter`/`ProgressCircle` para cobertura, estado quantitativo e progresso;
- `ScrollShadow` para navegação/áreas roláveis;
- `Drawer`/overlays HeroUI para mobile;
- `Spinner`, `Skeleton`, `Progress*` para espera;
- `Button` e `Link` nativos para ações/navegação;
- tokens `surface`, `surface-secondary`, `surface-tertiary`, `overlay`, `accent`, `muted`, `success`, `warning`, `danger` como semântica principal.

Não transformar toda a aplicação em cards idênticos. Usar `Surface`, coleções e espaços negativos para criar hierarquia.

## Living UI quando o perfil for expressive

Quando o usuário pedir páginas “vivas”, muitas transições ou motion forte, registrar:

```text
Motion Profile: expressive
Living states: required
```

Nenhum padrão visual ambiental específico é inferido desse perfil. Escolher efeitos, fundos e atmosferas conforme a identidade e necessidade do projeto.

### Navegação

- entrada de página/rota com fade + deslocamento curto quando adequado;
- saída não deve bloquear navegação;
- itens da navegação têm estado ativo claro e podem usar transição semântica;
- drawers, dropdowns, popovers e busca seguem motion nativo HeroUI;
- breadcrumb deve refletir a rota real.

### Superfícies estáticas

Mesmo sem alteração de dados, páginas com espaço visual podem ganhar vida por recursos coerentes com a marca, por exemplo:

- gradiente lento ou halo discreto;
- mudança tonal sutil;
- profundidade de superfícies;
- pequenos elementos decorativos não interativos.

Esses recursos são opcionais. Não animar texto, tabela ou conteúdo principal continuamente apenas para tornar a página “viva”.

### Espera/loading

Uma página de espera não deve depender apenas de conteúdo imóvel quando o produto pede Living UI. Combinar quando adequado:

- `Spinner`/`Skeleton`/`ProgressBar` HeroUI;
- feedback de progresso;
- mensagens de estado estáveis;
- stagger curto na entrada dos skeletons/superfícies;
- motion de fundo opcional se realmente agregar valor.

### Empty/planned/onboarding

Estados vazios e áreas planejadas podem usar:

- composição central clara;
- entrada em camadas;
- microinteração em CTA quando houver;
- ilustração/efeito compatível com o produto quando necessário;
- sem loops agressivos.

### Erro/restrição

- usar `Alert`/status semântico;
- ação de recuperação deve responder claramente;
- motion, quando houver, deve ser contido;
- não transformar erro em espetáculo visual.

## QA obrigatório

Para redesign HeroUI nativo + Living UI, validar:

1. nenhum import residual de facade shadcn/ReUI/Radix na camada de apresentação quando a migração for integral;
2. nenhum diretório de compatibilidade visual sem consumidor necessário;
3. auditoria de padrões manuais concluída (`Breadcrumbs`, `Kbd`, busca, navegação, perfil, coleções, progresso etc.);
4. componentes HeroUI compound aparecem diretamente na composição;
5. quando motion perceptível for requisito, comparar dois instantes separados por 2–4 s usando **valores computados reais**, conforme `TEMPORAL_MOTION_QA.md`;
6. desktop e mobile;
7. loading, empty/planned, erro/restrição e pelo menos duas rotas normais quando existirem;
8. `prefers-reduced-motion`: movimento não essencial é reduzido/parado e a composição permanece legível;
9. teclado/foco, popover/dropdown/drawer e console;
10. ausência de jank/overflow;
11. confirmar que CSS antigo ou duplicado foi removido, não apenas sobrescrito.

A validação deve falhar se um requisito de motion existir tecnicamente mas não executar de forma observável, ou se a dependência antiga tiver sido removida mas a anatomia visual manual continuar reproduzindo o design anterior.
