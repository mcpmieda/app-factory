# Change Hygiene

## Objetivo

Toda evolução, manutenção, correção, modernização ou revisão de sistema existente deve terminar com **uma implementação vigente clara**, não com uma sequência de patches acumulados que apenas se anulam entre si.

Este contrato vale igualmente para:

- projetos criados pela App Factory;
- projetos externos trazidos posteriormente para revisão/manutenção;
- código legado sem documentação própria da Factory.

A regra central é:

> **preservar comportamento estável não significa preservar implementação obsoleta.**

Quando uma implementação ruim puder ser substituída com segurança, a Factory deve preferir uma solução única, integrada e testada a adicionar uma nova camada que neutralize a anterior.

## Code health como critério de fechamento

Uma mudança não deve piorar a saúde do código na área tocada. O objetivo não é perfeição global nem reescrita oportunista do projeto inteiro; é garantir que o bloco alterado fique pelo menos tão compreensível, testável e sustentável quanto antes — e, quando a mudança já exige tocar a estrutura, preferencialmente melhor.

Isso segue a disciplina de revisão madura: complexidade pequena também se acumula ao longo do tempo. Portanto, uma sequência de alterações funcionalmente corretas pode ainda ser rejeitada se deixar o caminho final mais difícil de entender/manter sem justificativa real.

## Regras obrigatórias

### 1. Um caminho ativo por responsabilidade

Para uma mesma responsabilidade funcional, visual ou de configuração, mantenha **uma fonte autoritativa vigente** sempre que tecnicamente possível.

Evite como estado final:

- `funcao()`, `funcaoNova()`, `funcaoCorrigida()`, `funcaoV2()` quando apenas uma deveria existir;
- componentes `Old`, `New`, `Final`, `Fixed`, `Copy` deixados lado a lado sem fronteira de compatibilidade real;
- CSS novo criado apenas para sobrescrever CSS antigo que poderia ser corrigido na origem;
- wrappers/adapters sucessivos cuja única função é evitar corrigir a implementação imediatamente abaixo;
- feature flags temporárias sem condição de remoção;
- implementação antiga comentada "por segurança"; o Git já é o histórico.

### 2. Substituir, não sombrear

Se a mudança substitui uma implementação, a versão substituída e seus resíduos devem ser removidos no mesmo bloco final quando não houver consumidor legítimo que ainda dependa deles.

Remover também, quando ficarem órfãos:

- imports;
- exports;
- listeners/handlers;
- rotas;
- estilos;
- testes da implementação removida que não representem comportamento ainda válido;
- mocks/fixtures temporários;
- dependências;
- arquivos;
- documentação/configuração correspondente.

Testes de regressão que protegem comportamento vigente **não são resíduos** e devem permanecer.

### 3. Consolidação após repair loop

Tentativas intermediárias podem existir durante diagnóstico, mas **não são o produto final**.

Após encontrar a solução que funciona, execute uma passagem explícita de consolidação:

1. comparar o estado final com o baseline;
2. identificar tentativas anteriores ainda presentes;
3. remover código morto e caminhos substituídos;
4. retirar suppressions/overrides que deixaram de ser necessários;
5. remover arquivos e dependências temporárias;
6. simplificar o caminho de execução final;
7. rodar novamente lint/typecheck/test/build e regressões aplicáveis.

Se a terceira tentativa só funciona porque as duas tentativas anteriores continuam anulando parte do sistema, a tarefa **ainda não está pronta**.

### 4. Compatibilidade é exceção explícita, não desculpa genérica

Dois caminhos podem coexistir quando existe uma fronteira de compatibilidade real: API pública, migração gradual, consumidor externo, rollout controlado, formato legado ainda aceito ou outro requisito comprovável.

Nesse caso, registre no estado/issue/VERIFICATION equivalente:

- por que o caminho antigo ainda existe;
- quem/qual consumidor depende dele;
- condição objetiva para remoção;
- como os dois caminhos são testados durante a transição.

`legacy`, `compat`, `temporary` ou `v2` no nome não justificam coexistência por si só.

### 5. CSS: corrigir a causa antes da cascata

Não use nova camada CSS, seletor mais específico ou `!important` apenas para vencer uma regra anterior quando a regra anterior puder ser corrigida com segurança.

Preferência:

`regra original corrigida → composição/tokens existentes → escopo explícito → override excepcional documentado`.

Stylelint pode automatizar parte objetiva quando a stack suportar: seletores/propriedades duplicados, descending specificity e, quando a política do projeto permitir, `!important`.

### 6. Código morto e duplicação

Quando aplicável e suportado pela stack:

- JS/TS: ESLint/TypeScript continuam primeira linha; **Knip** é o default recomendado para encontrar arquivos, exports e dependências sem uso quando o grafo do projeto puder ser modelado;
- Python: Ruff/Pyflakes cobrem unused imports/variables; **Vulture** pode complementar dead code, preferindo alta confiança/configuração explícita para evitar falso positivo;
- múltiplas linguagens/CSS: **jscpd** pode indicar clones/hotspots, mas não recebe percentual universal de bloqueio. Use baseline/delta/configuração do projeto antes de torná-lo gate.

Ferramenta indisponível ou não configurada não vira `pass`. Também não instale todos esses verificadores em projeto simples por checklist.

### 7. Suppression nova precisa de motivo

Novos `eslint-disable`, `stylelint-disable`, `@ts-ignore`, `# noqa`, suppressions de scanner ou equivalentes devem ser revisados. Preferir corrigir a causa. Quando a suppression for necessária, mantenha-a pequena e ligada a uma limitação real conhecida.

### 8. Código externo: adote sem reproduzir dívida

Ao revisar um sistema construído fora da App Factory:

1. descubra o caminho de execução real e fontes de verdade existentes;
2. identifique dívida pré-existente na área tocada;
3. não reescreva dívida não relacionada só para "limpar o projeto";
4. não acrescente nova camada para imitar a dívida existente;
5. consolide a área modificada e prove regressão.

A meta é **não aumentar dívida no diff** e reduzir dívida diretamente ligada à alteração quando isso puder ser feito com segurança.

## Separar refactor grande de mudança funcional

Refactor local necessário para uma correção pode entrar no mesmo bloco. Refactor estrutural grande deve, quando possível, ser separado da feature/bugfix para tornar revisão, regressão e rollback mais claros.

Uma sequência aceitável pode ser:

`testes de caracterização → refactor sem mudança observável → mudança funcional → consolidação final`.

Cada etapa deve deixar o sistema funcionando.

## Hygiene Scan

A Factory fornece `scripts/change_hygiene.py` como scanner stdlib-first. Ele não tenta provar semanticamente que todo código está limpo; ele encontra sinais objetivos de acúmulo:

- marcadores de conflito;
- arquivos temporários/backup rastreados;
- possíveis cópias `old/new/fixed/final/copy/v2` coexistindo com o arquivo-base;
- novas suppressions;
- `!important` adicionado em CSS;
- pistas de tooling de dead-code/duplication já configurado.

Bloqueadores objetivos falham. Heurísticas permanecem advisory e exigem revisão contextual.

## Definition of Done de manutenção

Antes de entregar mudança em sistema existente, confirme:

- comportamento fora do escopo foi preservado;
- implementação substituída foi removida ou sua coexistência tem justificativa/remoção explícitas;
- não restaram arquivos temporários, conflitos ou tentativas descartadas;
- não foi introduzida camada CSS/JS/config apenas para neutralizar outra sem justificativa;
- dead code/imports/dependências óbvios da área tocada foram removidos;
- regressões foram executadas novamente **depois** da consolidação;
- o diff final é o que você escolheria implementar se soubesse desde o início qual solução funcionaria.

Essa última pergunta é o teste mental principal: o histórico de tentativas pertence ao Git/review, não à arquitetura final do produto.
