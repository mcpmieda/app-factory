# HeroUI Reference Catalog

Snapshot auditado em **2026-08-24** a partir dos sites oficiais HeroUI/HeroUI Pro e repositórios públicos `heroui-inc`.

## Objetivo

Dar à App Factory um índice amplo e recuperável do ecossistema HeroUI para projetos que escolham **HeroUI como linguagem visual principal**, sem transformar a Factory em cópia de catálogo comercial.

Este diretório deve ser consultado pelo `ui-builder` quando:

- o projeto escolher HeroUI como design system principal;
- o usuário pedir explicitamente linguagem HeroUI/HeroUI Pro;
- for necessário localizar componente, padrão, template ou referência visual antes de criar algo próprio;
- um projeto HeroUI precisar de design system, tema, motion, Figma ou tooling para agentes.

## Inventário auditado

| Camada | Inventário atual |
| --- | ---: |
| HeroUI React v3 — site `All Components` | 71 componentes top-level |
| HeroUI React v3 — exports adicionais no repo | 11 módulos de componente adicionais |
| HeroUI React v3 — total de módulos no índice público de componentes | 82, sendo 1 marcado `in progress` |
| HeroUI Pro React atual | 65 componentes / 477 variantes-exemplos |
| HeroUI Pro React templates | 4 templates completos |
| HeroUI Native OSS — site `All Components` | 39 componentes top-level |
| HeroUI Native OSS — exports adicionais no repo | 4 módulos de componente adicionais |
| HeroUI Pro Native atual | 44 componentes top-level |
| HeroUI Pro Native templates | 2 templates completos |
| HeroUI Pro v2 visual archive | 220 blocos / 34 famílias |
| Pro themes atuais documentados | Brutalism, Glass, Mouve |

### Importante sobre contagens

A comunicação de lançamento do HeroUI v3 usa **75+ web components**. O índice `All Components` do snapshot contém 71 entradas top-level, enquanto o source público exporta módulos auxiliares adicionais. Por isso a Factory agora registra separadamente **catálogo documentado** e **superfície pública exportada**.

A auditoria também corrigiu o HeroUI Pro Native: o snapshot anterior registrava 51 itens, mas o índice oficial atual lista 44. Os sete nomes que deixaram de aparecer foram preservados apenas como referência histórica/não confirmada no arquivo Native.

## Arquivos

- `HEROUI_REACT_V3_CATALOG.md` — HeroUI React OSS: 71 componentes documentados, exports adicionais, hooks e building blocks públicos.
- `HEROUI_PRO_REACT_CATALOG.md` — HeroUI Pro React atual: componentes, variantes, templates, themes e tooling.
- `HEROUI_NATIVE_CATALOG.md` — HeroUI Native OSS + exports adicionais + HeroUI Pro Native atual.
- `HEROUI_PRO_V2_VISUAL_ARCHIVE.md` — catálogo visual legado do Pro v2, útil como repertório de composição.
- `OFFICIAL_SOURCES.md` — sites, documentação, repositórios, Storybook, Figma, CLI, MCP e Skills oficiais.
- `CATALOG_AUDIT_2026-08-24.md` — comparação formal entre sites oficiais, repositórios oficiais e o catálogo da App Factory.

## Regra de autoridade

Para evitar falsos positivos:

1. **site `All Components`** define o catálogo nominal/documentado atual;
2. **source/package oficial** revela exports auxiliares e recursos que podem não ter página top-level;
3. **release notes** definem status, novidades, deprecações e itens experimentais;
4. **HeroUI Pro v2** é repertório legado, não default técnico;
5. o catálogo local é índice de descoberta e deve ser revalidado antes de implementação material.

## Regra de uso

### HeroUI OSS

Pode ser usado como implementação conforme a licença do repositório/pacote e a política de dependências da Factory. Antes de implementar, verificar versão e documentação atuais.

### HeroUI Pro

A Factory registra **nomes, categorias, contagens, URLs, finalidade e padrões públicos observáveis**. Não armazena código-fonte Pro, assets, screenshots ou templates comerciais copiados.

Quando um projeto tiver acesso autorizado ao HeroUI Pro, obter componentes/templates pelos mecanismos oficiais e tratar o material como dependência licenciada daquele projeto, não como patrimônio redistribuível da Factory.

Sem acesso Pro, usar o catálogo como referência de arquitetura e composição e implementar com HeroUI OSS ou componentes próprios compatíveis.

### HeroUI Pro v2

Tratar como **arquivo de repertório visual**, não como default técnico. Para projetos novos, preferir HeroUI v3 atual e adaptar apenas padrões de tarefa/composição que continuem úteis.

## Direção visual para sistema inteiro

Quando HeroUI for escolhido, não usar apenas componentes isolados. Construir o produto de forma coerente com:

- tokens e CSS variables HeroUI;
- composição compound;
- superfícies, tipografia, radius, sombras e estados do mesmo design system;
- tema claro/escuro ou tema customizado coerente;
- componentes Pro atuais quando autorizados e úteis;
- `ui/PROFESSIONAL_UI_PROFILE.md`;
- `ui/MOTION_POLICY.md`;
- acessibilidade, responsividade e browser QA.

Não misturar shadcn/ReUI no mesmo produto apenas para preencher lacunas estéticas. Se uma capacidade não existir no HeroUI, primeiro compor com HeroUI; depois criar componente local compatível com seus tokens e padrões.