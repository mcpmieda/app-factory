# Professional UI Profile — Default

## Objetivo

Elevar o acabamento visual da App Factory para um nível profissional consistente sem transformar a Factory em clone de um design system, catálogo comercial ou coleção de efeitos.

Este perfil é **transversal e library-neutral**. Ele define qualidade de composição, não a biblioteca que deve ser instalada.

## Relação com os design systems

A ordem atual da Factory continua vigente:

1. **Admin, dashboard, CRUD e ferramenta interna:** `shadcn/ui` continua a base preferencial.
2. **Admin avançado:** `ReUI` continua complemento seletivo para Data Grid, filtros complexos, calendários, Kanban e padrões equivalentes quando houver ganho real.
3. **Produto altamente visual:** `HeroUI` continua alternativa principal quando sua linguagem visual oferecer vantagem clara.
4. **Projeto existente:** preservar o design system atual salvo redesign explícito ou problema real.

O Professional UI Profile não autoriza misturar shadcn, ReUI e HeroUI por estética. Ele deve ser implementado com o sistema visual já escolhido sempre que possível.

## Origem e limite de propriedade intelectual

O perfil foi inspirado por padrões públicos observáveis em produtos profissionais, incluindo a linguagem `Default` apresentada pelo HeroUI Pro, além das referências já adotadas de shadcn, ReUI e HeroUI open source.

A Factory **não armazena nem reproduz código, templates, assets, screenshots comerciais ou componentes proprietários do HeroUI Pro**. Nomes de classes de interface como `Data Grid`, `Command`, `Stats`, `Filters`, `Agenda` ou `Kanban` descrevem arquétipos genéricos de produto, não cópias de implementação proprietária.

Se um projeto possuir licença própria para conteúdo comercial, o uso desse conteúdo continua sendo uma decisão específica daquele projeto e não vira patrimônio automático da Factory.

## Seleção

### Default

Para UI funcional destinada a usuário final, o perfil padrão é:

`professional-default`

Ele pode ser reduzido somente quando:

- o artefato for protótipo descartável/exploratório;
- a interface for deliberadamente utilitária e mínima;
- existir limitação real de plataforma, desempenho ou escopo;
- o usuário pedir explicitamente outra direção visual.

Mesmo nesses casos, acessibilidade, estados de interação e coerência não são opcionais.

## Modificadores

O perfil visual é independente do Motion Profile.

Registrar quando relevante:

- **density:** `compact`, `comfortable` ou `spacious`;
- **surface:** `flat`, `layered` ou `immersive`;
- **emphasis:** `quiet`, `balanced` ou `bold`;
- **Motion Profile:** `none`, `subtle`, `ambient` ou `expressive` conforme `ui/MOTION_POLICY.md`.

Defaults contextuais:

- admin/data-heavy: `comfortable + layered + balanced`, atenuando motion para `subtle` em áreas densas;
- produto visual/marketing: `spacious + layered/immersive + balanced/bold` conforme identidade;
- mobile utilitário: `comfortable + flat/layered + balanced`.

Não perguntar esses detalhes ao usuário quando a Factory puder inferi-los pelo produto e pela preferência já registrada.

## 1. Hierarquia visual

Toda tela relevante deve possuir uma hierarquia perceptível antes de depender de cor ou animação.

Esperado:

- um foco primário claro por região;
- título, contexto e ação principal com pesos distintos;
- ações secundárias visualmente subordinadas;
- conteúdo de apoio com contraste suficiente, mas sem competir com o foco;
- seções agrupadas por proximidade, alinhamento e superfície, não apenas por bordas;
- informação densa organizada para leitura em varredura.

Evitar:

- cinco cards com o mesmo peso visual;
- todos os botões parecendo ação principal;
- títulos, labels e valores com tamanhos quase idênticos;
- excesso de texto explicativo onde a estrutura poderia comunicar sozinha.

## 2. Ritmo de espaçamento

Usar uma escala de espaçamento pequena e repetível baseada nos tokens do design system escolhido.

Regras:

- repetir intervalos em vez de escolher valores arbitrários por componente;
- usar mais espaço entre grupos do que dentro do mesmo grupo;
- formulários, tabelas, cards e cabeçalhos devem compartilhar ritmo reconhecível;
- reduzir densidade com intenção, não comprimindo apenas para caber mais conteúdo;
- mobile preserva hierarquia mesmo quando o layout empilha.

Não copiar números proprietários de referências externas; usar os tokens e escala do projeto.

## 3. Tipografia

A tipografia deve comunicar função.

Esperado:

- família principal limitada e estável;
- escala curta de títulos, corpo, label, metadata e números de destaque;
- pesos usados com parcimônia;
- line-height confortável em leitura;
- números/KPIs com alinhamento e contraste adequados;
- labels não dependem somente de placeholder.

Evitar misturar várias famílias/pesos apenas para parecer sofisticado.

## 4. Superfícies, bordas, raio e elevação

A interface profissional mantém um sistema de superfícies previsível.

Esperado:

- poucos níveis de elevação;
- bordas e sombras discretas quando suficientes;
- raio consistente por família de componente;
- card só quando houver agrupamento real;
- fundo, painel, popover/modal e elemento interativo visualmente distinguíveis;
- contraste funcional em light e dark quando dark mode existir.

Evitar:

- cada seção dentro de um card dentro de outro card;
- sombras grandes em toda superfície;
- gradientes, glow e glass usados sem função;
- raios aleatórios em componentes semelhantes.

## 5. Cor e ênfase

Cor serve a estado, identidade e prioridade.

Esperado:

- cor primária usada de forma controlada;
- tokens semânticos para sucesso, aviso, erro, informação e estados neutros;
- contraste acessível;
- seleção/foco/hover perceptíveis sem ruído;
- gráficos mantêm consistência de significado entre telas.

Evitar arco-íris de cores apenas para diferenciar cards ou KPIs.

## 6. Arquétipos profissionais de composição

A Factory deve pensar em **padrões completos de tarefa**, não apenas em componentes isolados.

Arquétipos comuns:

### App shell

- sidebar/top navigation;
- identidade/escopo atual;
- troca de contexto quando necessário;
- ações globais;
- perfil/conta;
- navegação responsiva.

### Page header

- título;
- contexto/subtítulo curto;
- breadcrumbs apenas quando ajudam;
- ação principal;
- ações secundárias/overflow;
- filtros ou tabs somente se pertencem ao contexto da página.

### Dashboard / Stats

- KPIs com significado e unidade;
- comparação/tendência somente quando existir dado real;
- hierarquia entre indicador primário e secundário;
- drill-down quando útil;
- estados loading/empty/error.

### Search / Command

- entrada clara;
- atalhos apenas quando descobríveis;
- agrupamento de resultados;
- estado vazio;
- navegação por teclado quando aplicável;
- ação resultante previsível.

### Filters

- filtros mais importantes visíveis;
- filtros avançados progressivos;
- chips/resumo do estado aplicado;
- limpar/redefinir sem ambiguidade;
- resultado/contagem atualizados de forma compreensível.

### Data Grid / Table

- densidade adequada ao trabalho;
- cabeçalho estável e alinhamento correto por tipo de dado;
- ações de linha subordinadas;
- seleção, ordenação e paginação consistentes;
- responsividade com estratégia real, não tabela simplesmente espremida;
- empty/loading/error;
- detalhes por drawer/painel/página quando a linha não comportar tudo.

### Form

- grupos semânticos;
- labels persistentes;
- ajuda próxima ao campo;
- erro específico;
- validação no momento adequado;
- ação primária clara;
- prevenção de perda de dados quando material;
- formulários longos divididos por etapas/seções somente quando melhora a tarefa.

### Detail / Inspector

- identidade do objeto;
- status;
- atributos organizados;
- ações contextuais;
- histórico/atividade quando relevante;
- relação com objetos associados;
- fechamento/navegação previsível.

### Agenda / Calendar

- escala temporal clara;
- estado atual destacado sem dominar;
- eventos distinguíveis por significado;
- criação/edição contextual;
- alternativa de lista quando calendário não for suficiente.

### Kanban

- colunas representam estados reais do domínio;
- drag-and-drop só quando alteração direta for permitida;
- movimento com confirmação/rollback quando necessário;
- cartões mostram informação mínima para decisão;
- alternativa acessível para teclado quando drag for essencial.

### AI / Assistant interface

- separar mensagem, ação, evidência e estado de execução;
- tool calls/progresso não competem com resposta final;
- erros e cancelamento visíveis;
- não usar brilho/gradiente como substituto de arquitetura de informação.

## 7. Estados completos

Componente profissional não é somente seu estado ideal.

Quando aplicável, implementar e testar:

- initial;
- hover;
- focus-visible;
- pressed/active;
- selected;
- disabled;
- loading/skeleton;
- empty;
- partial data;
- success;
- warning;
- error;
- permission denied;
- offline/retry quando o produto possuir rede relevante.

## 8. Densidade e progressive disclosure

Não mostrar tudo só porque existe.

- informação primária permanece visível;
- secundária entra em detalhes, popover, drawer, accordion ou página dedicada quando necessário;
- filtros avançados não ocupam o topo inteiro por padrão;
- ações raras podem usar overflow;
- ação destrutiva nunca fica visualmente equivalente à ação principal;
- telas densas reduzem motion antes de reduzir legibilidade.

## 9. Motion profissional

Aplicar `ui/MOTION_POLICY.md`.

Neste perfil:

- motion responde à interação, mudança de estado ou continuidade espacial;
- hover/click não deve deslocar layout de forma imprevisível;
- transições são curtas e consistentes;
- attention motion é temporário;
- números/gráficos só animam mudança real;
- `prefers-reduced-motion` é obrigatório para movimento não essencial;
- efeitos ambiente são opcionais e geralmente ficam fora de superfícies densas.

## 10. Responsividade

A versão móvel não pode ser apenas desktop comprimido.

Verificar:

- prioridade de conteúdo;
- reordenação ou colapso de ações;
- largura de toque;
- tabelas/listas com estratégia própria;
- modais/drawers adequados ao viewport;
- navegação e filtros utilizáveis com uma mão quando o contexto for mobile-first;
- sem overflow horizontal acidental.

## 11. Acessibilidade

Qualidade profissional inclui:

- semântica HTML adequada;
- foco visível;
- ordem de teclado coerente;
- labels/names acessíveis;
- contraste;
- estados não comunicados somente por cor;
- reduced motion;
- mensagens de erro associadas;
- tamanho/alvo de interação apropriado;
- axe/Playwright quando selecionado pela verificação independente.

## 12. Conteúdo e microcopy

- títulos descrevem a tarefa, não a implementação;
- botões usam verbo de ação específico;
- confirmação destrutiva informa consequência;
- empty state explica próximo passo quando existe;
- erros indicam o que aconteceu e, quando possível, como recuperar;
- não preencher interfaces com texto promocional interno ou jargão técnico sem necessidade.

## 13. Component inventory

Antes de construir uma UI média/grande, identificar quais arquétipos realmente existem no produto.

Exemplo de inventário:

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

Pesquisar primeiro no design system/registry atual. Criar componente próprio somente quando a composição existente não atender.

## 14. Visual QA

UI relevante deve ser verificada no browser real quando a capacidade estiver disponível.

Checklist mínimo proporcional:

- desktop;
- viewport móvel;
- teclado/foco;
- loading/empty/error quando aplicável;
- ação principal e destrutiva;
- overflow/clipping;
- console sem erro relevante;
- `prefers-reduced-motion`;
- contraste/acessibilidade básica;
- screenshot regression somente quando houver baseline estável e risco material.

## 15. Anti-padrões de “UI gerada por IA”

A Factory deve rejeitar por padrão:

- excesso de cards sem hierarquia;
- gradiente/aurora/glow em toda tela;
- ícone em todo título sem função;
- texto cinza demais e contraste fraco;
- valores/labels sem alinhamento consistente;
- múltiplos CTAs primários;
- layout simétrico artificial quando a tarefa exige prioridade;
- componentes visualmente diferentes para a mesma função;
- botão destrutivo promovido por conveniência;
- animação contínua em área de leitura/dados;
- dashboard com gráficos decorativos sem decisão associada;
- mistura de design systems para obter “mais beleza”.

## 16. Gate de conclusão visual

Quando UI material for criada ou redesenhada, considerar concluída somente quando:

1. design system e `professional-default`/exceção estiverem registrados;
2. hierarquia, spacing, typography, surfaces e density forem coerentes;
3. estados relevantes existirem;
4. desktop/mobile estiverem utilizáveis;
5. foco/teclado/reduced-motion forem tratados;
6. browser QA real tiver sido executado quando disponível;
7. a implementação usar componentes existentes antes de recriar equivalentes;
8. não houver dependência ou cópia de conteúdo comercial sem licença explícita do projeto.

## Regra final

**Professional UI é um quality bar, não um fornecedor.**

A Factory deve conseguir alcançar este padrão com shadcn/ReUI, HeroUI, componentes nativos ou outro design system adequado sem perder coerência, acessibilidade, portabilidade ou liberdade arquitetural.
