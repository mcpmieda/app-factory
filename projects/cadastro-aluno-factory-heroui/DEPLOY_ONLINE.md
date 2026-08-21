# Abrir o Cadastro de Aluno online

## Opção recomendada: Vercel

1. Entre no Vercel com sua conta GitHub.
2. Clique em **Add New → Project**.
3. Importe o repositório **mcpmieda/app-factory**.
4. Em **Root Directory**, escolha:

   `projects/cadastro-aluno-factory-heroui`

5. Não precisa criar variáveis de ambiente.
6. Clique em **Deploy**.
7. Quando terminar, clique em **Visit**.

O endereço gerado ficará parecido com `https://cadastro-aluno-factory-heroui.vercel.app`.

## Observação importante

O app usa `localStorage`. Cada navegador guarda seus próprios cadastros. Esta versão é adequada para demonstração e teste; não é ainda um sistema multiusuário com banco compartilhado.

## Opção para desenvolvimento: GitHub Codespaces

No repositório, abra **Code → Codespaces → New with options**, escolha a configuração **Cadastro de Aluno - HeroUI**, crie o Codespace e aguarde. O servidor inicia automaticamente na porta 3000.
