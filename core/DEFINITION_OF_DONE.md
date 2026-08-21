# Definition of Done

Uma funcionalidade não está pronta porque o código foi escrito.

A Factory deve adaptar esta lista ao tipo de projeto e risco, mas por padrão verificar:

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

## Comportamento

- fluxo principal foi exercitado;
- estados de loading, vazio, sucesso e erro foram considerados quando aplicáveis;
- regressão direta foi verificada;
- operações repetíveis não criam duplicidade quando idempotência for requisito.

## UI

Quando houver interface:

- desktop verificado;
- mobile/responsividade verificada;
- interação real verificada no navegador quando possível;
- acessibilidade básica considerada;
- componentes seguem o design system do projeto;
- não há mistura visual sem justificativa.

## Segurança e dados

Quando relevante:

- autenticação/autorização verificadas;
- inputs validados;
- segredos não foram adicionados ao repositório;
- migrations e alterações de dados têm estratégia de recuperação.

## Entrega

- diff revisado proporcionalmente ao risco;
- estado do projeto continua recuperável pelo Git;
- documentação/PROJECT_STATE é atualizada apenas quando o estado vigente realmente mudou;
- limitações ou testes impossíveis de executar são declarados explicitamente.

## Regra final

Nunca declarar "pronto" se houver erro conhecido que invalide o objetivo principal. Distinguir claramente: implementado, testado, validado e pronto para produção.