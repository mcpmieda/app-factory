# AGENTS.md — App Factory

## Posicionamento

A App Factory é uma **caixa de ferramentas opcional** para engenharia de software. Ela não deve ser ativada automaticamente só porque o usuário pediu para criar, corrigir, manter ou evoluir software.

Use a App Factory somente quando:

- o usuário pedir explicitamente para usá-la; ou
- o repositório declarar de forma atual e explícita `governance: "app-factory"` e o usuário não tiver desativado essa governança.

A simples existência de arquivos `.factory`, specs antigas, documentos históricos ou código da Factory não torna um projeto governado por ela.

## Processo padrão

Quando a App Factory não estiver explicitamente ativa, siga o fluxo normal do próprio repositório:

1. entender o pedido;
2. ler somente os arquivos relevantes;
3. fazer a menor alteração segura que resolva o problema;
4. executar validação proporcional ao que mudou;
5. usar branch/PR quando o repositório exigir;
6. concluir sem criar artefatos de governança desnecessários.

Não criar por padrão:

- `.app-factory.json`;
- `.factory/state.json`;
- semantic contract/assurance;
- verification plan/review evidence;
- matrizes extensas de scanners;
- handoffs e documentos de continuidade;
- classifications de scale/risk/system level;
- merge trains especiais.

## Quando a App Factory for escolhida

Mesmo em projeto opt-in, use **proporcionalidade**. A menor profundidade suficiente é o padrão.

- mudança trivial: alteração + checks locais relevantes;
- mudança funcional comum: testes, lint/typecheck/build aplicáveis;
- mudança de domínio/segurança/persistência: especificação e verificações adicionais somente quando trouxerem valor concreto;
- release crítica: gates adicionais apenas para as superfícies realmente afetadas.

Project Adoption, Semantic Assurance/Verification, Independent Verification, formal methods, scanners, recovery drills e outros módulos são recursos opcionais. Eles não devem ser encadeados automaticamente em toda tarefa.

## Compatibilidade dos módulos opcionais

O **Project Adoption Gate** continua disponível em `skills/project-adoption/SKILL.md` e `core/PROJECT_ADOPTION_GATE.md` para projetos que o escolherem explicitamente. Seus estados `pre-implementation` e `delivery` são recursos opt-in, não fases universais. Da mesma forma, a regra histórica sobre `React + CSS próprio` permanece apenas dentro desse módulo e não governa projetos que não o adotaram.

## Segurança que permanece obrigatória

Simplificação de processo não autoriza:

- expor secrets ou credenciais;
- colocar dados pessoais reais em Git/logs públicos;
- mover autorização protegida apenas para o cliente;
- executar operação destrutiva sem autorização;
- alterar produção, permissões ou migrations de forma implícita;
- declarar validação que não foi executada.

## Manutenção

Em código existente, preserve comportamento estável e remova tentativas descartadas quando isso puder ser feito com segurança. Não é necessário transformar uma correção pequena em refactor amplo.

## Ferramentas especializadas

Os documentos e Skills em `core/`, `skills/`, `profiles/`, `engine/` e `scripts/` continuam disponíveis como biblioteca. Carregue apenas o recurso que o trabalho explicitamente exigir.

`factory-router` deixa de ser entrada universal. Consulte `core/ENTRYPOINT.md` para a regra opt-in.

## Conclusão

Código escrito não é prova suficiente, mas a verificação deve ser proporcional. Para alterações comuns, os testes e checks normais do repositório são suficientes. Evidência adicional só é obrigatória quando o risco específico da alteração justificar.
