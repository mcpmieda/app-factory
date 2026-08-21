# Cadastro de Aluno — App Factory + HeroUI

Aplicativo de cadastro de aluno em **uma única etapa**, construído segundo a App Factory e usando **HeroUI v3** como design system.

## Teste mais fácil: GitHub Codespaces

Este projeto já contém `.devcontainer/devcontainer.json`.

Depois de colocar os arquivos em um repositório no GitHub:

1. abra o repositório;
2. clique em **Code**;
3. abra a aba **Codespaces**;
4. clique em **Create codespace on main**.

O Codespaces irá automaticamente:

- instalar as dependências;
- instalar o Chromium do Playwright;
- iniciar o Next.js;
- encaminhar a porta `3000`;
- abrir o app no navegador.

Você não precisa executar `npm install` manualmente.

## Abrir online com Vercel

Este projeto está pronto para ser publicado como um site Next.js sem variáveis de ambiente.

Quando ele estiver dentro do repositório `mcpmieda/app-factory`, use como **Root Directory** no Vercel:

```text
projects/cadastro-aluno-factory-heroui
```

Depois basta clicar em **Deploy**. O Vercel instala as dependências, executa `next build` e fornece um endereço `*.vercel.app`.

Os dados cadastrados continuam no `localStorage` do navegador. Portanto, esta publicação é uma demonstração funcional, não um cadastro compartilhado entre computadores.

## Testar toda a estrutura

No terminal do Codespaces:

```bash
npm run test:all
```

Esse único comando executa:

1. ESLint;
2. TypeScript typecheck;
3. testes unitários com Vitest;
4. build do Next.js;
5. testes E2E com Playwright em desktop e mobile.

Também é possível usar no VS Code/Codespaces:

**Terminal → Run Task → ✅ Verificar app completo**

## Rodar localmente

```bash
bash scripts/bootstrap.sh
npm run dev
```

Abra `http://localhost:3000`.

## Stack

- Next.js 16
- React 19
- TypeScript
- Tailwind CSS 4
- HeroUI v3
- Zod
- Vitest
- Playwright

## Motion

Motion Profile: `ambient`.

Em áreas de dados, o movimento é atenuado para `subtle`.
`prefers-reduced-motion` é respeitado para movimento não essencial.

## Persistência

Esta baseline usa `localStorage`, adequada para demonstração e teste local.
Ela não deve ser confundida com uma solução multiusuário de produção.
