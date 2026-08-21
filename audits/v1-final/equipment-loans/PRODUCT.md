# Product

## Outcome

Permitir que a equipe escolar registre empréstimos e devoluções e encontre rapidamente quem está com cada equipamento e o que está atrasado.

## Usuários e jornada

- equipe administrativa consulta disponibilidade;
- registra item, responsável e data prevista;
- o estado persiste após reload;
- identifica atrasos por badge, resumo e filtro dedicado;
- registra a devolução e o item volta a ficar disponível.

## Experience

- visual system: shadcn/ui baseline unless product requirements override it;
- Motion Profile: `ambient` contextual by default;
- dense data/reading views: attenuate to `subtle`;
- reduced motion: mandatory for non-essential movement.

Use motion to communicate interaction, data changes, state, attention and navigation. Ambient effects are appropriate for login, waiting, empty states, headers and spacious surfaces when they do not compete with the task.

## First slice

- quatro itens fictícios de categorias diferentes;
- empréstimo e devolução auditáveis;
- busca por item, patrimônio ou responsável;
- filtros disponível, emprestado e atrasado;
- estados loading, vazio, erro e sucesso;
- dois empréstimos ativos do mesmo item são impossíveis por regra e índice único parcial.

## Non-goals

- optional infrastructure without a product requirement;
- real user data or production credentials in examples;
- multiple design systems;
- continuous decorative animation in dense administrative screens.
- autenticação fictícia ou deploy de produção;
- exclusão de item ou histórico;
- dados reais de alunos, professores ou patrimônio.
