# Definition of Done

Uma funcionalidade não está pronta porque o código foi escrito.

A Factory deve adaptar esta lista ao tipo de projeto e risco, mas por padrão verificar:

## Correspondência com a intenção

Quando a mudança exigir Semantic Verification (`core/SEMANTIC_VERIFICATION.md`):

- `specs/semantic-contract.json` representa o objetivo e as regras atuais antes da implementação;
- critérios obrigatórios estão expressos como comportamentos observáveis (`given / when / then`);
- todo critério `must` está ligado em `specs/verification-plan.json` a pelo menos uma evidência executável/gate declarado;
- os gates referenciados foram realmente executados e passaram; rastreabilidade textual não substitui execução;
- `specs/review-evidence.json` corresponde à spec, ao plano e ao conteúdo atual;
- risco médio/alto recebeu revisão desacoplada (`independent-agent` ou `clean-context`), não apenas autoavaliação do mesmo raciocínio;
- mudança posterior em código/spec/plano invalida a revisão anterior até nova verificação.

Documentação, chore e refactor pequeno sem mudança observável não precisam receber especificação formal pesada.

## Adequação da arquitetura

Quando `core/SYSTEM_ENGINEERING.md` se aplicar:

- o nível do produto foi classificado e registrado de forma proporcional;
- `persistent-app` ou superior possui fonte autoritativa de dados durável compatível com o requisito real;
- `multi-user-system` ou superior não depende de `localStorage`, mocks, arrays locais ou JSON estático como persistência final compartilhada;
- identidade/autenticação existe quando necessária ao produto;
- autorização é aplicada server-side quando usuários/perfis possuem escopos diferentes;
- mutações protegidas possuem validação server-side;
- mudanças de schema persistente usam migrations/versionamento equivalente;
- concorrência, repetição/idempotência e recovery foram considerados quando materiais;
- um protótipo/demo não é rotulado como produção apenas porque a interface e o CRUD visual funcionam.

## Implementação

- comportamento solicitado existe;
- requisitos relevantes foram atendidos;
- não foram removidas funcionalidades fora do escopo;
- solução reutiliza padrões existentes quando adequado;
- não há dependências ou abstrações desnecessárias conhecidas.

## Qualidade executável

Quando o projeto suportar:

- lint passa;
- typecheck passa;
- testes relacionados passam;
- build passa;
- erros novos de console não são ignorados.

Typecheck/build são também defesa contra imports/assinaturas inexistentes. Integrações pouco tipadas ou dependentes de runtime devem ter smoke/integration test quando a falha de API for risco material.

## Comportamento

- fluxo principal foi exercitado;
- estados de loading, vazio, sucesso e erro foram considerados quando aplicáveis;
- regressão direta foi verificada;
- operações repetíveis não criam duplicidade quando idempotência for requisito;
- para `persistent-app` ou superior, o fluxo crítico exercita persistência real ou ambiente equivalente, não apenas estado de navegador;
- para fluxos protegidos, testes cobrem acesso permitido e negado quando autorização for requisito material.

## UI

Quando houver interface:

- desktop verificado;
- mobile/responsividade verificada;
- interação real verificada no navegador quando possível;
- acessibilidade básica considerada;
- componentes seguem o design system do projeto;
- não há mistura visual sem justificativa;
- quando existe baseline visual estável e regressão visual é risco material, screenshot diff/visual regression entra como gate executável; não criar snapshots frágeis apenas para cumprir checklist.

## Segurança e dados

Quando relevante:

- autenticação/autorização verificadas;
- inputs validados;
- segredos não foram adicionados ao repositório;
- migrations e alterações de dados têm estratégia de recuperação;
- para `production-system` ou superior, backup/restore ou recuperação compatível com o provedor foi definido quando perda de dados for material;
- logs/auditoria/observabilidade existem no nível necessário para diagnosticar operações e falhas relevantes.

## Entrega

- diff revisado proporcionalmente ao risco;
- estado do projeto continua recuperável pelo Git;
- documentação/PROJECT_STATE é atualizada apenas quando o estado vigente realmente mudou;
- nível do sistema e decisões de persistência/identidade/recovery ficam recuperáveis no repositório quando relevantes;
- limitações ou testes impossíveis de executar são declarados explicitamente.

## Regra final

Nunca declarar "pronto" se houver erro conhecido que invalide o objetivo principal. Distinguir claramente: implementado, testado, validado e pronto para produção.

Para trabalho funcional com spec aplicável, `lint + typecheck + build + testes verdes` sem rastreabilidade e revisão semântica atual ainda não é Definition of Done completa.

Para `multi-user-system` ou superior, UI completa + CRUD visual + dados no navegador também não são Definition of Done de produção sem a arquitetura compartilhada e os gates exigidos por `core/SYSTEM_ENGINEERING.md`.
