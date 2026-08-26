# HeroUI Reference Catalog

Snapshot auditado em **2026-08-24** a partir dos sites oficiais HeroUI/HeroUI Pro e repositórios públicos `heroui-inc`.

## Objetivo

Dar à App Factory um índice amplo e recuperável do ecossistema HeroUI para projetos que escolham **HeroUI como linguagem visual principal**, sem transformar a Factory em cópia de catálogo comercial.

Este diretório deve ser consultado pelo `ui-builder` quando:

- o projeto escolher HeroUI como design system principal;
- o usuário pedir explicitamente linguagem HeroUI/HeroUI Pro;
- for necessário localizar componente, padrão, template ou referência visual antes de criar algo próprio;
- um projeto HeroUI precisar de design system, tema, motion, Figma ou tooling para agentes.

## Contrato de redesign nativo

Antes de remodelar um sistema existente para HeroUI, ler `HEROUI_NATIVE_REDESIGN_CONTRACT.md`.

Quando o usuário pedir que a interface pareça **inteiramente criada do zero em HeroUI**, a preservação deve ocorrer na camada funcional, não na anatomia visual antiga. É obrigatório reconstruir a árvore de apresentação usando diretamente componentes/compound components HeroUI e remover facades/adapters de shadcn/ReUI/Radix cuja única finalidade seja conservar APIs e imports do design system anterior.

Componentes locais continuam permitidos para padrões reais de produto, mas não para simular `CardHeader`, `Badge`, `Button asChild` ou outras APIs herdadas apenas para evitar a migração estrutural.

## Integridade da prova temporal

Quando motion perceptível for requisito, ler também `TEMPORAL_MOTION_QA.md`.

Não considerar uma animação validada apenas porque existe `animation:` no CSS, porque duas screenshots foram geradas ou porque duas strings auxiliares são diferentes. Para motion material, o QA deve comparar o estado computado do **mesmo elemento** em instantes separados e, quando possível, confirmar avanço real de `animation.currentTime` com Web Animations API / Chrome DevTools Protocol.

A regra existe para impedir falso-positivo em Living UI e qualquer motion requerido pelo produto: movimento tecnicamente declarado, mas não executado ou não perceptível, continua sendo falha de QA.

## Integridade de overlays e navegação

Para Drawer, Popover, Modal, busca/command e navegação dentro de overlays, ler também `OVERLAY_INTERACTION_HARDENING.md`.

O contrato exige:

- semântica real de link/ação/seleção antes da aparência da coleção;
- uma única fonte de estado por overlay controlado;
- fechamento na mesma interação que navega quando aplicável;
- QA com ponteiro real e hit-testing após animações de entrada;
- captura browser-neutral de erros/exceções não tratados e `console.error` relevante; CDP é apenas um adaptador possível;
- protocolo/SLO ou baseline reproduzível antes de transformar latência em gate, seguido de múltiplas amostras/mediana;
- diagnóstico do harness antes de alterar o produto por um falso positivo;
- nenhum bypass de autenticação no domínio oficial.

## HeroUI como linguagem principal

Quando HeroUI for selecionado, registrar normalmente:

```text
Design System: HeroUI
Professional UI Profile: professional-default
Motion Profile: ambient | subtle | expressive | none
```

HeroUI deve aparecer de forma transversal em shell, formulários, dados, overlays, estados, tokens, temas e motion quando aplicável. Não misturar shadcn/ReUI apenas para preencher lacunas estéticas.

**Nenhum efeito ambiental específico é obrigatório.** Fundo, partículas, glows, gradientes ou outras atmosferas entram somente por decisão explícita do produto/projeto ou por uma composição que a App Factory julgue adequada naquele sistema, sempre sujeita a desempenho, acessibilidade e coerência. O simples fato de HeroUI ter sido escolhido não ativa automaticamente um efeito visual adicional.

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

A comunicação de lançamento do HeroUI v3 usa **75+ web components**. O índice `All Components` do snapshot contém 71 entradas top-level, enquanto o source público exporta módulos auxiliares adicionais. Por isso a Factory registra separadamente **catálogo documentado** e **superfície pública exportada**.

A auditoria também corrigiu o HeroUI Pro Native: o snapshot anterior registrava 51 itens, mas o índice oficial atual lista 44. Os sete nomes que deixaram de aparecer foram preservados apenas como referência histórica/não confirmada no arquivo Native.

## Arquivos

- `HEROUI_REACT_V3_CATALOG.md` — HeroUI React OSS: componentes documentados, exports adicionais, hooks e building blocks públicos.
- `HEROUI_PRO_REACT_CATALOG.md` — HeroUI Pro React atual: componentes, variantes, templates, themes e tooling.
- `HEROUI_NATIVE_CATALOG.md` — HeroUI Native OSS + exports adicionais + HeroUI Pro Native atual.
- `HEROUI_PRO_V2_VISUAL_ARCHIVE.md` — catálogo visual legado do Pro v2, útil como repertório de composição.
- `OFFICIAL_SOURCES.md` — sites, documentação, repositórios, Storybook, Figma, CLI, MCP e Skills oficiais.
- `CATALOG_AUDIT_2026-08-24.md` — comparação formal entre sites oficiais, repositórios oficiais e o catálogo da App Factory.
- `HEROUI_NATIVE_REDESIGN_CONTRACT.md` — contrato de reconstrução limpa, Living UI e QA de redesign HeroUI.
- `TEMPORAL_MOTION_QA.md` — integridade da evidência temporal para motion e reduced-motion.
- `OVERLAY_INTERACTION_HARDENING.md` — contrato de semântica, estado, fechamento, hit-testing, runtime e performance para overlays/navegação.

## Regra de autoridade

1. **site `All Components`** define o catálogo nominal/documentado atual;
2. **source/package oficial** revela exports auxiliares e recursos que podem não ter página top-level;
3. **release notes** definem status, novidades, deprecações e itens experimentais;
4. **HeroUI Pro v2** é repertório legado, não default técnico;
5. o catálogo local é índice de descoberta e deve ser revalidado antes de implementação material.

## Regra de uso

### HeroUI OSS

Pode ser usado como implementação conforme a licença do repositório/pacote e a política de dependências da Factory. O repositório v3 auditado usa Apache-2.0. Antes de implementar, verificar versão, documentação e obrigações de licença atuais.

### HeroUI Pro

A Factory registra **nomes, categorias, contagens, URLs, finalidade e padrões públicos observáveis**. Não armazena código-fonte Pro, assets, screenshots ou templates comerciais copiados.

Quando um projeto tiver acesso autorizado ao HeroUI Pro, obter componentes/templates pelos mecanismos oficiais e tratar o material como dependência licenciada daquele projeto, não como patrimônio redistribuível da Factory.

Sem acesso Pro, usar o catálogo como referência de arquitetura e composição e implementar com HeroUI OSS ou componentes próprios compatíveis.

### HeroUI Pro v2

Tratar como **arquivo de repertório visual**, não como default técnico. Para projetos novos, preferir HeroUI v3 atual e adaptar apenas padrões de tarefa/composição que continuem úteis.

## Direção visual para sistema inteiro

Quando HeroUI for escolhido, construir o produto de forma coerente com:

- tokens e CSS variables HeroUI;
- composição compound;
- `Surface`, `Card`, `Alert`, `Table`, `Chip`, `Avatar`, `Drawer`, `ScrollShadow`, `Spinner`, `Skeleton` e outros primitives oficiais quando aplicáveis;
- superfícies, tipografia, radius, sombras e estados do mesmo design system;
- tema claro/escuro ou tema customizado coerente;
- componentes Pro atuais quando autorizados e úteis;
- `ui/PROFESSIONAL_UI_PROFILE.md`;
- `ui/MOTION_POLICY.md`;
- `HEROUI_NATIVE_REDESIGN_CONTRACT.md` em redesigns;
- `TEMPORAL_MOTION_QA.md` quando motion perceptível fizer parte dos gates;
- `OVERLAY_INTERACTION_HARDENING.md` quando navegação, busca ou ações ocorrerem em overlays;
- acessibilidade, responsividade e browser QA.

Não misturar shadcn/ReUI no mesmo produto apenas para preencher lacunas estéticas. Se uma capacidade não existir no HeroUI, primeiro compor com HeroUI; depois criar componente local compatível com seus tokens e padrões.
