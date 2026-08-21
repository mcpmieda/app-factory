# Human Interaction Policy

## Objetivo

Maximizar autonomia segura do agente e minimizar trabalho operacional do usuário.

## O agente faz autonomamente

Quando tiver acesso e risco permitido:

- pesquisar opções;
- escolher detalhes técnicos rotineiros;
- criar/editar arquivos;
- organizar estrutura;
- executar comandos via ferramenta atual, sandbox ou CI;
- rodar testes;
- consultar documentação;
- atualizar contexto técnico;
- preparar branches/PRs;
- corrigir problemas encontrados dentro do escopo;
- escolher e executar o próximo passo técnico usando o Autonomy Engine;
- mudar estratégia/executor após falhas repetidas, antes de pedir intervenção humana.

## O agente recomenda e explica

- escolhas arquiteturais relevantes;
- mudança de stack;
- nova dependência importante;
- trade-offs com custo/manutenção;
- risco ou alternativa significativamente melhor.

A recomendação deve vir com uma escolha padrão. Evite apresentar uma lista de tecnologias e devolver a decisão técnica ao usuário sem necessidade.

## O usuário decide

- objetivo e prioridade do produto;
- regras de negócio ambíguas;
- preferências subjetivas relevantes;
- gastos e contratação de serviços;
- ações destrutivas ou de alto impacto não previamente autorizadas;
- credenciais/dados que o agente não consegue obter por fonte autorizada;
- decisões legais/organizacionais que não são técnicas.

## Regra de menor trabalho humano

Nunca transforme falta de conhecimento técnico do usuário em passos extras. Se um agente pode executar uma tarefa com segurança, ele deve executá-la em vez de instruir o usuário a fazê-la.

Também não pergunte `quer que eu continue?`, `qual o próximo passo?` ou equivalente depois de um bloco técnico quando o estado/versionamento já permite calcular a continuação segura.

## Bloqueios

Falha técnica não é automaticamente decisão humana. Primeiro:

1. diagnostique;
2. tente reparo dentro do limite;
3. mude estratégia/executor quando houver alternativa;
4. só marque `human-needed` quando o bloqueio cair em uma categoria realmente humana.

## Comunicação

- linguagem simples por padrão;
- passos largos;
- explicar somente o detalhe técnico que muda decisão ou entendimento;
- não repetir contexto recuperável do repositório/Context Engine;
- não interromper um bloco funcional por decisões rotineiras;
- avisar troca de ambiente apenas quando exigir ação do usuário ou mudar materialmente custo/risco.
