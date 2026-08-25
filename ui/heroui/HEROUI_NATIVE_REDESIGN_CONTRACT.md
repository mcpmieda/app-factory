# HeroUI Native Redesign Contract

## Objetivo

Quando HeroUI for escolhido explicitamente como linguagem principal — especialmente quando o usuário pedir que a interface pareça criada do zero em HeroUI — a implementação deve ser **nativamente HeroUI**, não uma camada de compatibilidade sobre uma arquitetura visual anterior.

Este contrato complementa `README.md`, `../AMBIENT_CONSTELLATION_PROFILE.md` e `../MOTION_POLICY.md`.

## Regra de reconstrução limpa

Em redesign explícito de um produto existente para HeroUI:

1. preservar regras de negócio, contratos, autenticação, autorização, dados, rotas e integrações;
2. reconstruir a **árvore de apresentação** a partir da anatomia HeroUI v3;
3. usar diretamente componentes e compound components oficiais (`Card`, `Surface`, `Alert`, `Table`, `Chip`, `Avatar`, `Drawer`, `Input`, `Spinner`, `Skeleton`, `ScrollShadow`, etc.) quando a capacidade existir;
4. remover facades/adapters cujo objetivo seja manter APIs de outro design system (`CardHeader`, `Badge`, `Button variant=default`, `asChild`, wrappers de shadcn/Radix, etc.);
5. remover arquivos, classes e dependências do design system anterior quando não tiverem consumidor real;
6. componentes locais continuam permitidos quando representam **padrões de produto** (ex.: `AmbientConstellation`, `LivingSurface`, visualização acadêmica), mas não devem fingir a API de shadcn/ReUI para esconder HeroUI por baixo;
7. preferir a composição compound do HeroUI v3 a copiar anatomias anteriores.

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

## Hierarquia HeroUI recomendada

A interface deve explorar níveis semânticos do ecossistema:

- `Surface` para ilhas, painéis e regiões de layout;
- `Card` compound para unidades de informação;
- `Alert` para estados institucionais/validação;
- `Chip` para status e categorias;
- `Table` compound para dados estruturados;
- `ScrollShadow` para navegação/áreas roláveis;
- `Drawer`/overlays HeroUI para mobile;
- `Spinner`, `Skeleton`, `Progress*` para espera;
- `Button` e `Link` nativos para ações/navegação;
- tokens `surface`, `surface-secondary`, `surface-tertiary`, `overlay`, `accent`, `muted`, `success`, `warning`, `danger` como semântica principal.

Não transformar toda a aplicação em cards idênticos. Usar `Surface` e espaços negativos para criar hierarquia.

## Ambient Constellation — correção de movimento proporcional

A referência HeroUI Pro deve ser reproduzida por **proporção percebida**, não por copiar valores fixos isolados.

No modal de referência, o campo visível tem cerca de 288×180 px e o drift percebido fica em torno de 20 px. Isso representa aproximadamente:

- ~7% da largura visível;
- ~11% da altura visível;
- ~5% do campo de estrelas com overscan.

Portanto, usar `20px` como amplitude fixa em uma viewport de 1200–1600 px torna o movimento praticamente invisível e **não é fiel à referência**.

### Regra revisada

- tamanho das partículas continua fixo em screen-space (microestrelas, normalmente 0.5–1.5 CSS px);
- **o deslocamento do grupo pode ser proporcional à superfície**;
- em superfícies fortes, preferir drift relativo de aproximadamente `4–6%` do campo com overscan, ou valor equivalente perceptível;
- limitar amplitudes extremas por contexto/performance, mas não reduzir a ponto de o usuário não conseguir perceber o drift após alguns segundos;
- ciclos de ~12 s e ~15 s continuam baseline, em direções opostas/defasadas;
- o movimento deve ser verificável em vídeo, captura temporal ou comparação de frames, não apenas pela presença de `animation:` no CSS.

Em shell de página inteira, a assinatura deve ser mais fácil de perceber em **zonas delimitadas** (hero, header, waiting/empty panel) e pode usar amplitude maior no campo global. Não depender de um único campo muito transparente cobrindo 1440 px.

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
- drawers e busca seguem motion nativo HeroUI.

### Superfícies estáticas

Mesmo sem alteração de dados, páginas com espaço visual podem manter vida por:

- glows/auroras respirando lentamente;
- constelação em drift;
- gradiente luminoso quase estático com pequena deriva;
- pequenos elementos de profundidade fora da região de leitura.

Não animar texto, tabela ou conteúdo principal continuamente.

### Espera/loading

Uma página de espera não deve ser apenas skeletons imóveis. Combinar quando adequado:

- `Spinner`/Skeleton HeroUI;
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

1. nenhum import residual de facade shadcn/ReUI na camada de apresentação;
2. nenhum diretório de compatibilidade visual sem consumidor necessário;
3. componentes HeroUI compound aparecem diretamente na composição;
4. Ambient Constellation claramente perceptível em 100% zoom;
5. comparar dois frames separados por 2–4 s para provar movimento do campo;
6. desktop e mobile;
7. loading, empty/planned, erro/restrição e pelo menos duas rotas normais;
8. `prefers-reduced-motion`: loops espaciais param e composição permanece legível;
9. teclado/foco e console;
10. ausência de jank/overflow.

A validação deve falhar se o efeito existir tecnicamente mas for imperceptível visualmente.