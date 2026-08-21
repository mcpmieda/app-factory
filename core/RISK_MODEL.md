# Risk Model

A governança deve ser proporcional ao impacto possível.

## Baixo risco

Documentação, pesquisa, protótipo descartável, texto e arquivos de exemplo sem efeito real. Executar diretamente quando autorizado, com validação simples.

## Médio risco

Funcionalidade localizada, regra de negócio não destrutiva, dependência, configuração de aplicação ou refatoração limitada.

Padrão: escopo fechado, revisão de dependências diretas, verificações relevantes, registro no Git e explicação de consequência não óbvia.

## Alto risco

Produção, exclusão, operação em massa, banco/schema, migration, permissões, autenticação, infraestrutura, dados sensíveis ou mudança estrutural ampla.

Padrão:
1. confirmar estado/baseline;
2. entender impacto;
3. ter backup/recuperação quando aplicável;
4. obter autorização quando a ação destrutiva não estiver já coberta;
5. testar em escopo controlado quando possível;
6. aplicar;
7. reler estado real;
8. testar comportamento;
9. registrar resultado e rollback.

## Regra de simplicidade

Não adicionar processo, ferramenta ou gate cujo custo de manutenção seja maior que o risco que reduz.