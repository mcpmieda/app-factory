# HeroUI Reference Catalog

Snapshot pesquisado em **2026-08-24** a partir de fontes oficiais HeroUI/HeroUI Pro e repositórios `heroui-inc`.

## Objetivo

Dar à App Factory um índice amplo e recuperável do ecossistema HeroUI para projetos que escolham **HeroUI como linguagem visual principal**, sem transformar a Factory em cópia de catálogo comercial.

Este diretório deve ser consultado pelo `ui-builder` quando:

- o projeto escolher HeroUI como design system principal;
- o usuário pedir explicitamente linguagem HeroUI/HeroUI Pro;
- for necessário localizar um componente, padrão, template ou referência visual antes de criar algo próprio;
- um projeto HeroUI precisar de design system, tema, motion, Figma ou tooling para agentes.

## Inventário do snapshot

| Camada | Inventário registrado |
| --- | ---: |
| HeroUI React v3 OSS | 71 componentes top-level listados na página oficial atual |
| HeroUI Pro React atual | 65 componentes / 477 variantes-exemplos |
| HeroUI Pro React templates | 4 templates completos |
| HeroUI Native OSS | 39 componentes top-level listados na página oficial atual |
| HeroUI Pro Native | 51 componentes |
| HeroUI Pro Native templates | 2 templates completos |
| HeroUI Pro v2 visual archive | 220 blocos agrupados em 34 famílias |
| Pro themes atuais documentados | 3: Brutalism, Glass, Mouve |

A comunicação de lançamento do HeroUI v3 usa a expressão **75+ web components**. A página oficial `All Components (React)` do snapshot lista 71 entradas top-level; manter ambos os fatos e preferir a lista oficial atual como inventário nominal.

## Arquivos

- `HEROUI_REACT_V3_CATALOG.md` — catálogo HeroUI React open source atual.
- `HEROUI_PRO_REACT_CATALOG.md` — catálogo Pro React atual, variantes, templates e temas.
- `HEROUI_NATIVE_CATALOG.md` — HeroUI Native OSS + HeroUI Pro Native.
- `HEROUI_PRO_V2_VISUAL_ARCHIVE.md` — catálogo visual legado do Pro v2, útil como repertório de composição.
- `OFFICIAL_SOURCES.md` — sites, documentação, repositórios, Storybook, Figma, CLI, MCP e Skills oficiais.

## Regra de uso

### HeroUI OSS

Pode ser usado como implementação conforme a licença do repositório/pacote e a política de dependências da Factory. Antes de implementar, verificar versão e documentação atuais.

### HeroUI Pro

O catálogo da Factory registra **nomes, categorias, quantidades, URLs, finalidade e padrões públicos observáveis**. Ele não contém código-fonte Pro, assets, screenshots ou templates comerciais copiados.

Se o projeto possuir licença HeroUI Pro válida:

1. usar instalação/CLI/MCP/Skills oficiais;
2. obter componentes e templates diretamente da conta/licença do projeto;
3. nunca armazenar `HEROUI_PERSONAL_TOKEN` no Git;
4. tratar o material obtido como dependência licenciada do projeto, não como patrimônio redistribuível da Factory.

Sem licença Pro, usar o catálogo como referência de arquitetura e composição e implementar com HeroUI OSS ou componentes próprios compatíveis.

### HeroUI Pro v2

Tratar como **arquivo de repertório visual**, não como default técnico. Para projetos novos, preferir HeroUI v3 atual e adaptar apenas o padrão de tarefa/composição que continuar útil.

## Regra de atualização

Este catálogo é um índice, não uma cópia congelada da documentação. Antes de uma implementação material:

1. consultar `OFFICIAL_SOURCES.md`;
2. verificar `All Components` e releases atuais;
3. confirmar se componente/template ainda existe e se mudou de API;
4. preferir MCP/Skills oficiais quando disponíveis no ambiente/licença;
5. atualizar este catálogo quando a diferença for material.

## Direção visual

Quando HeroUI for escolhido, não usar apenas componentes isolados. Construir o sistema inteiro de forma coerente com:

- tokens e CSS variables HeroUI;
- composição compound;
- superfícies, tipografia, radius, sombras e estados do mesmo design system;
- tema claro/escuro ou tema customizado coerente;
- `ui/PROFESSIONAL_UI_PROFILE.md`;
- `ui/MOTION_POLICY.md`;
- acessibilidade, responsive e browser QA.

Não misturar shadcn/ReUI no mesmo produto apenas para preencher lacunas estéticas. Se uma capacidade não existir no HeroUI, primeiro compor com HeroUI; depois criar um componente local compatível com seus tokens e padrões.