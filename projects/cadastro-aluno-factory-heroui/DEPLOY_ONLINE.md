# Gestão de Alunos online

Produção conhecida:

`https://cadastro-aluno-factory-heroui.vercel.app`

## Configuração Vercel

Repositório: `mcpmieda/app-factory`

Root Directory:

`projects/cadastro-aluno-factory-heroui`

Nenhuma variável de ambiente é necessária enquanto o produto permanecer um `local-app`.

## O que a publicação significa

O Vercel distribui a aplicação. Os dados continuam no `localStorage` de cada navegador.

Portanto, abrir a mesma URL em outro computador **não** apresenta os mesmos cadastros. Para mover dados manualmente, use o backup JSON e a restauração.

Se uma futura versão exigir dados compartilhados, usuários, permissões ou continuidade entre dispositivos, a arquitetura deve ser reclassificada antes da implementação; não basta alterar a hospedagem.
