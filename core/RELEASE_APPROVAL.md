# Production Approval Protocol

Este contrato define como a App Factory trata validação em ambiente oficial e autorização explícita para liberar uma versão aos usuários finais.

## Regra central

A Factory deve separar **estar implantado para validação** de **estar oficialmente liberado**.

Quando a infraestrutura permitir com segurança, um módulo novo pode ser testado no endereço oficial do produto, protegido por feature flag, allowlist, papel de testador ou autorização equivalente. O fato de o código estar implantado no domínio oficial não significa que esteja liberado ao público-alvo.

Preview separado continua válido quando isolamento de dados, segurança, infraestrutura ou risco exigir. Não existe obrigação universal de criar uma URL de preview.

## Comando oficial

A frase exata:

`APROVADO PARA PRODUÇÃO`

é a autorização explícita do usuário para liberar oficialmente **a versão/candidata que acabou de ser apresentada e validada**.

Expressões genéricas como `aprovado`, `ok`, `pode seguir`, elogios ou aprovação de uma tela/ideia não devem ser interpretadas automaticamente como autorização de produção quando houver ambiguidade.

## Antes da aprovação

Enquanto a aprovação explícita não existir:

- o módulo pode estar implantado no ambiente oficial apenas para validação controlada;
- acesso deve permanecer restrito aos testadores/papéis autorizados;
- não deve aparecer para usuários definitivos apenas porque CI, testes ou revisão técnica passaram;
- escritas destrutivas, migrações irreversíveis ou operações sensíveis devem permanecer protegidas conforme risco;
- a versão candidata deve ser identificável para que a aprovação não seja aplicada silenciosamente a alterações posteriores.

## O que `APROVADO PARA PRODUÇÃO` autoriza

Ao receber a frase, a Factory deve tratar a aprovação como autorização para executar o release da candidata aprovada, sem pedir ao usuário para repetir passos técnicos rotineiros. O agente deve, na ordem adequada ao projeto:

1. confirmar que a candidata atual é a mesma que foi submetida à validação do usuário;
2. confirmar que não surgiram mudanças materiais posteriores que tornem a aprovação stale;
3. executar os gates de release, segurança, regressão, migrations, compatibilidade e rollback aplicáveis;
4. aplicar permissões e feature flags definitivas previstas pela especificação;
5. remover somente restrições, dados, flags, rotas, código ou scaffolding temporários de teste que ficaram obsoletos;
6. preservar mecanismos permanentes de segurança, rollback, feature flag ou rollout que continuem tendo função real;
7. integrar na branch/release oficial segundo a política do projeto;
8. executar CI/CD e publicação;
9. validar saúde, autorização, rotas e comportamento crítico no ambiente oficial;
10. atualizar estado, documentação, versão e evidências;
11. executar Change Hygiene para não deixar duas implementações concorrentes ou remendos temporários.

A aprovação humana **não substitui** os gates técnicos. Se um gate obrigatório falhar, a Factory deve reparar e reverificar antes de liberar.

## Limites da autorização

`APROVADO PARA PRODUÇÃO` não autoriza automaticamente:

- mudar regra de produto não apresentada;
- ampliar escopo funcional;
- adicionar custo não autorizado;
- conceder permissões mais amplas;
- executar migração destrutiva nova que não fazia parte da candidata aprovada;
- ignorar falha de segurança, integridade, compatibilidade ou recuperação;
- publicar mudanças materiais feitas depois da aprovação sem nova validação quando essas mudanças alterarem comportamento, dados, segurança ou experiência aprovada.

## Aprovação stale

A aprovação deixa de valer para a candidata atual quando, depois dela, ocorrer mudança material em comportamento, regra, dados, autorização, segurança, fluxo do usuário ou integração relevante. Correção puramente técnica que preserve integralmente o comportamento aprovado pode seguir após regressão proporcional, desde que o agente consiga provar que a candidata funcional não mudou.

## Continuidade

Projetos que adotem este protocolo devem registrar sua implementação concreta no próprio repositório: domínio oficial, branch de produção, mecanismo de restrição de teste, feature flags, papéis, gates e procedimento de release.

A frase `APROVADO PARA PRODUÇÃO` deve continuar curta para o usuário; a complexidade operacional pertence ao repositório e à automação, não ao comando humano.
