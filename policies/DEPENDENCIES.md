# Dependency Policy

Antes de adicionar biblioteca, serviço, starter ou código externo, avalie o valor líquido.

## Perguntas mínimas

- já existe solução no projeto?
- resolve problema real ou apenas reduz poucas linhas?
- licença permite o uso pretendido?
- projeto está mantido?
- dependências transitivas são razoáveis?
- existe impacto de bundle/runtime?
- há risco de supply chain ou segurança conhecido?
- funciona com a stack/versões do projeto?
- cria lock-in relevante?
- o agente consegue verificar a integração?

## Repositórios externos

Classifique como:

- **ADOTAR** — usar diretamente ou integrar oficialmente;
- **INSPIRAR** — aproveitar padrão/arquitetura sem importar o pacote inteiro;
- **DESCARTAR** — ganho não justifica custo ou risco.

## Regra de UI

Não instalar múltiplas bibliotecas para fornecer a mesma função sem justificativa. Em projetos shadcn/ReUI, HeroUI não entra automaticamente.

## Atualizações

Não atualizar dependências centrais durante tarefa não relacionada apenas porque existe versão mais nova.