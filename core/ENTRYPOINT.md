# App Factory — Entrypoint opcional

A App Factory não é ativada automaticamente por intenção de desenvolvimento de software.

## Quando ativar

Ative `factory-router` somente quando uma destas condições for verdadeira:

1. o usuário pedir explicitamente para usar a App Factory; ou
2. o projeto declarar atualmente `governance: "app-factory"` em `.app-factory.json` ou regra local equivalente, sem opt-out posterior do usuário.

Arquivos históricos, specs antigas, branches Factory ou diretórios `.factory` não bastam por si só para reativar governança.

## Quando não ativar

Para criação, manutenção, bugfix, refactor, UI, API, automação ou integração comum em projeto não governado, use o processo normal do repositório. Não introduza App Factory como camada adicional sem pedido explícito.

## Fluxo mínimo quando ativa

Mesmo em projeto governado, comece pelo menor processo suficiente:

1. entender o resultado;
2. recuperar apenas o contexto relevante;
3. classificar a alteração pelo risco **da mudança**, não apenas pelo risco global do sistema;
4. fazer a menor alteração segura;
5. executar os checks proporcionais;
6. ampliar a verificação somente quando a superfície afetada justificar.

### Profundidade sugerida

- **trivial** — copy, ícone, espaçamento, navegação simples: testes/checks locais relevantes;
- **local** — componente, tela ou comportamento isolado: lint/typecheck/testes relevantes/build;
- **domínio** — regra de negócio, autorização, persistência, API/contrato: especificação e testes adicionais aplicáveis;
- **crítica** — migrations, identidade, permissões, recovery, produção ou integração externa sensível: gates completos da superfície afetada.

## Módulos opcionais

Project Adoption Gate, Semantic Assurance, Semantic Verification, Independent Verification, formal methods, merge train, scanners adicionais, recovery drills, perfis e motores de autonomia são módulos sob demanda.

Não crie automaticamente todos esses artefatos para cada mudança. Um projeto pode usar somente uma parte da App Factory.

## Segurança mínima

A redução de processo não reduz requisitos concretos de segurança: secrets, PII, autorização server-side, migrations, produção e operações destrutivas continuam exigindo tratamento seguro e autorização adequada.

## Projeto novo

Não grave governança da App Factory em um novo repositório sem escolha explícita do usuário. Se ele escolher a Factory, registre somente o estado necessário aos módulos realmente adotados.

## Projeto existente

O repositório é a fonte de verdade. Se a governança tiver sido desativada posteriormente, respeite a decisão mais recente e trate artefatos antigos como históricos até que sejam removidos.

## Regra de interação

Não peça ao usuário para escolher detalhes técnicos rotineiros. Também não imponha classificações, specs ou scanners que não tragam benefício proporcional ao pedido.

## Conclusão

A App Factory deve reduzir trabalho e risco, não aumentar cerimônia. Se um recurso da Factory custar mais do que o risco que ele reduz, ele não deve ser obrigatório para aquela alteração.
