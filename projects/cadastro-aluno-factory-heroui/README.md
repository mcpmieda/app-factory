# Gestão de Alunos — App Factory + HeroUI

Aplicativo local de gestão de alunos construído com **Next.js 16 + HeroUI v3** e usado como teste de campo da App Factory.

URL de produção registrada no repositório: `https://cadastroaluno-ecru.vercel.app`

> A URL está registrada como homepage do repositório. O conector Vercel disponível durante este field test não conseguiu confirmar o deploy ao vivo, portanto este documento não transforma esse registro em prova de disponibilidade.

## O que esta versão faz

- cadastro e edição de alunos;
- status `Ativo`, `Arquivado` e `Transferido`;
- pesquisa por nome, matrícula, e-mail, telefone, curso, turma ou responsável;
- filtros por status e turma;
- ordenação por atualização, nome ou turma;
- visão detalhada de cada aluno;
- painel com total, ativos, turmas e arquivados;
- backup completo em JSON versionado;
- restauração de backup com validação e confirmação;
- exportação em CSV;
- migração automática dos cadastros da versão antiga `v1` para `v2`;
- interface responsiva e `prefers-reduced-motion`.

## Arquitetura — importante

Este produto continua classificado como **`local-app`**.

O Vercel hospeda e distribui a aplicação, mas os registros são guardados no `localStorage` do navegador atual. Portanto:

- cada navegador/dispositivo possui seus próprios dados;
- não há banco compartilhado;
- não há login nem perfis de acesso;
- não existe sincronização entre computadores;
- esta versão não deve ser usada como cadastro institucional multiusuário.

Essa escolha é intencional para este teste: a evolução aumenta bastante o produto sem introduzir backend apenas por sofisticação.

## Compatibilidade com a versão anterior

A versão anterior utilizava:

`app-factory.student-registration.v1`

A versão atual utiliza:

`app-factory.student-registration.v2`

Quando o `v2` ainda não existe e o navegador contém registros válidos no `v1`, a aplicação migra automaticamente os registros. Campos que não existiam antes não recebem dados inventados; por exemplo, o turno passa a `Não informado`.

## Verificação

```bash
npm ci
npm run test:all
npm audit
```

O conjunto cobre:

1. ESLint;
2. TypeScript;
3. 15 testes unitários;
4. build Next.js;
5. 10 testes Playwright em desktop/mobile Chromium;
6. auditoria completa das dependências;
7. contrato semântico, Semantic Assurance e revisão por fingerprint no CI.

Scripts individuais:

```bash
npm run test
npm run e2e
npm run verify
```

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

Em superfícies densas de dados, o movimento é reduzido para `subtle`. `prefers-reduced-motion` desativa movimento não essencial.

## Desenvolvimento local

```bash
bash scripts/bootstrap.sh
npm run dev
```

Abra `http://localhost:3000`.

## Vercel

Root Directory:

```text
projects/cadastro-aluno-factory-heroui
```

A integração Git/Vercel pode continuar publicando alterações de `main`; nenhuma variável de ambiente é necessária nesta arquitetura local.
