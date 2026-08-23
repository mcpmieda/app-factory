# System Engineering Contract

Este contrato impede que um pedido de sistema real seja reduzido silenciosamente a uma demonstração local ou a uma página com dados efêmeros.

A regra é orientada por capacidades e risco, não apenas pelas palavras usadas pelo usuário.

## Classificação de produto

Classifique o produto em um dos níveis abaixo antes de fechar a arquitetura.

### 1. `website`

Conteúdo predominantemente público/editorial, sem dados próprios mutáveis como núcleo do produto.

Pode ser estático quando isso satisfizer o objetivo.

### 2. `local-app`

Aplicação de uso local/individual em que os dados podem legitimamente existir apenas no dispositivo/navegador do usuário.

`localStorage`, IndexedDB ou arquivo local podem ser armazenamento autoritativo somente quando o requisito for explicitamente local e não compartilhado.

Hospedar/distribuir um `local-app` em Vercel, Cloudflare, GitHub Pages ou equivalente **não** o transforma automaticamente em `persistent-app` ou `multi-user-system`. A classificação depende de onde estão os dados autoritativos e de como o produto é usado, não de onde os arquivos do frontend são servidos.

### 3. `persistent-app`

Aplicação que possui dados próprios que precisam sobreviver de forma confiável e independente de um navegador/dispositivo.

Exige persistência durável adequada ao ambiente. Dados mockados, arrays hardcoded e `localStorage` podem existir em protótipo/teste, mas não como fonte autoritativa final.

### 4. `multi-user-system`

Sistema com múltiplos usuários, dados compartilhados, colaboração, gestão institucional, cadastros operacionais ou uso por perfis distintos.

Por padrão exige:

- backend ou camada server-side equivalente para operações protegidas;
- persistência durável compartilhada;
- autenticação quando a identidade do usuário altera acesso, autoria ou experiência;
- autorização server-side quando existem perfis, papéis, escopos ou dados restritos;
- validação server-side para mutações;
- modelo de domínio e relacionamentos explícitos;
- migrations/versionamento de schema quando houver banco próprio;
- estratégia de concorrência/idempotência para operações suscetíveis a repetição ou conflito;
- testes do fluxo crítico com persistência real ou ambiente equivalente.

Ter backend não obriga uma API pública/formal. Quando existir uma fronteira de API, integração externa, múltiplos consumidores independentes, webhooks, eventos ou mensageria, aplique também `core/API_ENGINEERING.md` no modo proporcional ao risco da interface.

### 5. `production-system`

Sistema destinado a operação real com dados importantes, múltiplos usuários, continuidade esperada ou impacto operacional relevante.

Além de `multi-user-system`, exige proporcionalmente:

- configuração separada por ambiente e segredos fora do Git;
- estratégia de backup/restore ou recuperação compatível com o provedor;
- logs/auditoria para operações relevantes;
- observabilidade suficiente para diagnosticar falhas de produção;
- política de erro/retry para integrações externas;
- rollout/rollback ou estratégia equivalente de recuperação;
- proteção de operações destrutivas;
- verificação de deploy/produção e não apenas build local.

Detalhes de contrato, compatibilidade, timeout/retry, webhooks e gates específicos de API pertencem a `core/API_ENGINEERING.md`; este contrato mantém apenas a exigência arquitetural de alto nível.

### 6. `critical-system`

Sistema em que falha, corrupção, indisponibilidade ou acesso indevido pode causar impacto alto em pessoas, operação, finanças, conformidade ou dados sensíveis/importantes.

Além dos níveis anteriores, exige arquitetura e gates formais proporcionais ao risco, incluindo revisão de segurança, runbook, auditoria ampliada, recuperação testada e decisões explícitas para disponibilidade, integridade e controle de acesso.

## Regra de classificação

Não classifique pelo nome do projeto sozinho. Use o comportamento esperado.

Sinais fortes de `multi-user-system` ou superior:

- vários usuários ou computadores acessam os mesmos dados;
- aluno/professor/turma/usuário/cliente/patrimônio/estoque/processo são registros institucionais;
- existem papéis como administrador, professor, secretaria, operador, gestor ou cliente;
- o produto precisa de histórico, autoria, permissões ou colaboração;
- os dados não podem desaparecer ao limpar o navegador;
- o usuário espera continuar o trabalho em outro dispositivo;
- o sistema será usado na operação real de uma organização.

Quando houver dúvida entre dois níveis, escolha o nível mais alto se a diferença afetar integridade, compartilhamento, segurança ou recuperação dos dados.

## Proibição de falsa persistência

Para `persistent-app`, `multi-user-system`, `production-system` e `critical-system`:

- `localStorage`, IndexedDB, fixtures, mocks, arrays locais e JSON estático não podem ser apresentados como persistência final compartilhada;
- uma demonstração pode usar esses recursos somente se estiver marcada claramente como demo/protótipo e houver plano explícito para a arquitetura final;
- interface bonita, CRUD visual e dados que sobrevivem a um refresh não são prova de sistema completo.

## Evolução de dados em `local-app`

Dados locais não exigem banco remoto, mas também não devem ser tratados como descartáveis quando o produto promete preservá-los.

Quando uma mudança funcional relevante altera o contrato local (`localStorage`, IndexedDB ou arquivo persistente):

1. versione o contrato, chave ou formato quando houver incompatibilidade material;
2. valide o formato antigo antes de migrar;
3. migre deterministicamente e preserve todos os valores conhecidos;
4. quando um campo novo não possuir origem histórica, represente o desconhecido explicitamente em vez de inventar dado de negócio;
5. grave/valide o formato novo **antes** de remover o antigo;
6. mantenha caminho proporcional de recuperação/backup quando os dados forem importantes para o usuário;
7. teste leitura antiga → migração → reload e rejeição segura de dados incompatíveis.

Se a necessidade passar a incluir continuidade entre dispositivos, colaboração ou fonte compartilhada, reclassifique o produto; não tente resolver esse novo requisito ampliando indefinidamente armazenamento local.

## Identidade e autorização

Autenticação não é obrigatória em todo software, mas deve ser ativada quando identidade real for requisito.

Autorização é obrigatória no servidor quando usuários autenticados possuem poderes ou escopos diferentes. Esconder botão no frontend não é controle de acesso.

Regras de autorização devem ser verificadas por comportamento, incluindo pelo menos um teste de acesso permitido e um de acesso negado em fluxos críticos.

## Dados e domínio

Para sistemas com dados próprios:

1. identifique entidades principais;
2. modele relacionamentos e invariantes;
3. defina quem cria/lê/altera/arquiva/exclui;
4. diferencie exclusão permanente de arquivamento/soft delete quando o domínio exigir histórico;
5. defina constraints importantes também no banco quando possível;
6. trate migrations como histórico versionado, sem reescrever migrations já aplicadas em produção.

Validação de schema por registro não prova invariantes que atravessam a coleção. Unicidade, cardinalidade, ausência de conflito entre registros e regras agregadas precisam ser aplicadas/testadas na camada que possui visão do conjunto — coleção local, serviço/domínio e/ou banco, conforme a arquitetura.

## Capacidades condicionais

A Factory deve avaliar, sem instalar tudo por padrão:

- papéis/permissões;
- auditoria/histórico;
- soft delete/arquivamento;
- busca global;
- paginação/filtros server-side;
- arquivos/uploads;
- importação/exportação;
- APIs/contratos/integrações conforme `core/API_ENGINEERING.md`;
- notificações;
- jobs/filas/agendamentos;
- rate limiting/abuse protection;
- observabilidade;
- backup/recovery;
- integração com serviços externos;
- cache e concorrência.

Ative somente quando o produto exigir, mas não omita uma capacidade necessária apenas para manter a arquitetura simples.

## Saída mínima da arquitetura

Para `persistent-app` ou superior, a arquitetura deve registrar pelo menos:

- nível de sistema;
- fonte autoritativa dos dados;
- fronteira cliente/servidor;
- estratégia de identidade e autorização, quando aplicável;
- modelo de persistência/migrations;
- principais entidades e relações;
- estratégia de validação;
- riscos de perda/duplicidade/conflito;
- ambiente de deploy e recuperação proporcional.

Para `local-app` com dados persistentes relevantes, registre de forma leve a fonte local autoritativa e, quando houver evolução incompatível, o contrato/migração/recuperação. Não force a saída completa de `persistent-app` se o produto continua legitimamente local.

Quando houver API relevante, registre também o modo de governança e a fonte de verdade do contrato conforme `core/API_ENGINEERING.md`, sem duplicar detalhes que pertencem ao documento/API contract específico.

## Definition of Done adicional

Um projeto classificado como `multi-user-system` ou superior não pode ser declarado pronto para produção se:

- os dados autoritativos ainda estiverem apenas no navegador/dispositivo;
- regras de acesso dependerem somente do frontend;
- mutações não tiverem validação server-side;
- banco/schema tiver sido alterado sem migration/estratégia equivalente;
- não houver teste do fluxo crítico com a camada real de persistência/autorização aplicável;
- recuperação/backup for requisito material e não houver estratégia definida.

Um `local-app` com migração de dados relevante não deve ser declarado concluído se a evolução pode apagar/sobrescrever dados anteriores sem validação e recovery proporcional.

Se uma API `contract`/`governed` fizer parte do sistema, os gates específicos de `core/API_ENGINEERING.md` também integram a conclusão proporcional.

## Relação com os demais módulos

- `core/PROJECT_SCALE.md` decide profundidade de processo; este arquivo decide profundidade mínima da arquitetura do produto.
- `core/API_ENGINEERING.md` decide governança da interface quando existe API/integração relevante; não cria API por obrigação.
- `core/RISK_MODEL.md` pode elevar exigências de segurança, revisão e recovery.
- `core/SEMANTIC_VERIFICATION.md` transforma regras funcionais/arquiteturais relevantes em critérios observáveis.
- `profiles/*` fornecem stacks/defaults comprovados, mas não podem reduzir os requisitos deste contrato.
- `core/DEFINITION_OF_DONE.md` continua sendo o gate geral de conclusão.

## Princípio final

Escolha a arquitetura mais simples que satisfaça o produto real — não a arquitetura mais simples que apenas faça a tela funcionar.
