# HeroUI Native Redesign Contract

## Objetivo

Quando HeroUI for escolhido explicitamente como linguagem principal — especialmente quando o usuário pedir que a interface pareça criada do zero em HeroUI — a implementação deve ser **nativamente HeroUI**, não uma camada de compatibilidade sobre uma arquitetura visual anterior.

Este contrato complementa `README.md`, `../AMBIENT_CONSTELLATION_PROFILE.md`, `../MOTION_POLICY.md` e `TEMPORAL_MOTION_QA.md`.

## Regra de reconstrução limpa

Em redesign explícito de um produto existente para HeroUI:

1. preservar regras de negócio, contratos, autenticação, autorização, dados, rotas e integrações;
2. reconstruir a **árvore de apresentação** a partir da anatomia HeroUI v3;
3. usar diretamente componentes e compound components oficiais (`Breadcrumbs`, `ListBox`, `SearchField`, `Kbd`, `Popover`, `Dropdown`, `Card`, `Surface`, `Alert`, `Table`, `Chip`, `Avatar`, `Drawer`, `Spinner`, `Skeleton`, `ProgressBar`, `ScrollShadow`, etc.) quando a capacidade existir;
4. remover facades/adapters cujo objetivo seja manter APIs de outro design system (`CardHeader`, `Badge`, `Button variant=default`, `asChild`, wrappers de shadcn/Radix, etc.);
5. remover arquivos, classes e dependências do design system anterior quando não tiverem consumidor real;
6. componentes locais continuam permitidos quando representam **padrões de produto** (ex.: `AmbientConstellation`, `LivingSurface`, visualização acadêmica), mas não devem fingir a API de shadcn/ReUI para esconder HeroUI por baixo;
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
| sidebar feita com links + classes de selected | `ListBox`/coleção HeroUI + `ScrollShadow` |
| busca composta por input + popup absoluto | `SearchField` + `Popover` + `ListBox` |
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
- `ListBox` para coleções navegáveis/selecionáveis;
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

## Ambient Constellation — referência canônica atual

A referência observável deve ser reproduzida por **proporção percebida**, sem copiar SVG/assets do HeroUI.

Snapshot público auditado em 2026-08-25:

- repositório: `heroui-inc/heroui`;
- commit auditado: `1d2164e7b9a60221e39501081f0fe4f6c564bccf`;
- modal/banner: `apps/docs/src/app/[lang]/(home)/components/pro-banner.tsx`;
- estrelas: `apps/docs/src/app/[lang]/(home)/components/floating-stars.tsx`;
- keyframes: `apps/docs/src/app/global.css`.

Características públicas observadas no modal Pro atual:

- card: `288px` de largura;
- área superior do efeito: `180px` de altura;
- gradiente base: `#E9E9FF` → `#CCE5F1`;
- glow: `#5DD0E7` → `#7300FF`;
- campo natural de estrelas: aproximadamente `760.706 × 637.702px`;
- o campo é centralizado e renderizado com `scale-50` dentro do recorte do banner;
- camada forward: `12s ease-in-out infinite`;
- camada reverse: `15s ease-in-out infinite`;
- excursão no keyframe oficial: aproximadamente `40px` por eixo, em sentidos opostos;
- estrelas brancas, muito pequenas, com opacidades variadas.

### Regra de reprodução

- **não copiar o SVG oficial**; gerar partículas próprias;
- usar a paleta acima como referência quando o produto pedir fidelidade ao modal HeroUI Pro;
- manter partículas em screen-space, normalmente `0.45–1.5 CSS px`;
- aumentar presença por **densidade, contraste, distribuição, glow e excursão**, não criando círculos grandes;
- em superfícies maiores que o modal, adaptar a excursão proporcionalmente para que o deslocamento continue perceptível após 2–4 segundos;
- manter pelo menos duas camadas assíncronas/opostas como baseline;
- glints/cross-sparkles podem existir em pequena proporção, nunca como objetos dominantes;
- campos fortes devem permanecer atrás do conteúdo, com `pointer-events: none` e `aria-hidden`;
- dados densos ficam em ilhas limpas.

### Anti-padrões

- usar `20px` ou `40px` fixos em uma viewport de 1200–1600px e declarar o movimento “equivalente”;
- aumentar o raio/tamanho das partículas para tornar a constelação visível;
- transformar o campo em bolhas/círculos flutuantes;
- manter múltiplas fontes CSS concorrentes para a mesma primitive;
- animar texto/tabelas continuamente para compensar uma atmosfera fraca.

## Living UI obrigatório para perfil expressive

Quando o usuário pedir páginas “vivas”, muitas transições ou motion forte, registrar:

```text
Motion Profile: expressive
Ambient Surface Profile: ambient-constellation
Constellation Intensity: strong
Living states: required
```

Aplicar de forma coerente:

### Navegação

- entrada de página/rota com fade + deslocamento curto;
- saída não deve bloquear navegação;
- itens da sidebar têm estado ativo com indicador/realce animado;
- drawers, dropdowns, popovers e busca seguem motion nativo HeroUI;
- breadcrumb deve refletir a rota real.

### Superfícies estáticas

Mesmo sem alteração de dados, páginas com espaço visual podem manter vida por:

- glows/auroras respirando lentamente;
- constelação em drift;
- gradiente luminoso quase estático com pequena deriva;
- pequenos elementos de profundidade fora da região de leitura.

Não animar texto, tabela ou conteúdo principal continuamente.

### Espera/loading

Uma página de espera não deve ser apenas skeletons imóveis. Combinar quando adequado:

- `Spinner`/`Skeleton`/`ProgressBar` HeroUI;
- constelação visível;
- halo respirando;
- mensagens de progresso estáveis;
- stagger curto na entrada dos skeletons/superfícies.

### Empty/planned/onboarding

Estados vazios e áreas planejadas são superfícies ideais para Living UI:

- visual central com halo/órbita lenta;
- constelação perceptível;
- entrada em camadas;
- microinteração em CTA quando houver;
- sem loops agressivos.

### Erro/restrição

- manter atmosfera viva porém mais contida;
- usar `Alert`/status semântico;
- ação de recuperação deve responder claramente;
- não transformar erro em espetáculo visual.

## QA obrigatório

Para redesign HeroUI nativo + Living UI, validar:

1. nenhum import residual de facade shadcn/ReUI/Radix na camada de apresentação;
2. nenhum diretório de compatibilidade visual sem consumidor necessário;
3. auditoria de padrões manuais concluída (`Breadcrumbs`, `Kbd`, busca, navegação, perfil, coleções, progresso etc.);
4. componentes HeroUI compound aparecem diretamente na composição;
5. Ambient Constellation claramente perceptível em 100% zoom sem partículas grandes;
6. comparar dois instantes separados por 2–4 s usando **valores computados reais**, conforme `TEMPORAL_MOTION_QA.md`;
7. desktop e mobile;
8. loading, empty/planned, erro/restrição e pelo menos duas rotas normais;
9. `prefers-reduced-motion`: loops espaciais param e composição permanece legível;
10. teclado/foco, popover/dropdown/drawer e console;
11. ausência de jank/overflow;
12. confirmar que CSS antigo ou duplicado da primitive foi removido, não apenas sobrescrito.

A validação deve falhar se o efeito existir tecnicamente mas for imperceptível visualmente, ou se a dependência antiga tiver sido removida mas a anatomia visual manual continuar reproduzindo o design anterior.
