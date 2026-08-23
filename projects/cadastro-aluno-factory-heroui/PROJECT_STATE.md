# PROJECT_STATE

## Objetivo vigente

Manter uma **gestão local completa de alunos** para demonstração e teste da App Factory, preservando a simplicidade arquitetural de um `local-app` mesmo quando distribuído pelo Vercel.

## Estado atual

- fase: `field test v0.2 — fechamento`;
- versão do app: `0.2.0`;
- escala de processo: `S/M — evolução funcional relevante`;
- nível do sistema: `local-app`;
- perfil: `web-admin` com HeroUI v3;
- API mode: `none`;
- semantic depth: `domain`;
- Independent Verification: `baseline` proporcional ao baixo risco e à ausência de backend/API;
- fonte autoritativa dos dados: `localStorage` do navegador atual;
- contrato de persistência: `v2`, com migração automática de `v1`;
- backend/banco compartilhado: `não aplicável ao escopo atual`;
- autenticação/autorização: `não aplicável ao escopo atual`;
- stack: Next.js 16 + React 19 + TypeScript + Tailwind CSS 4 + HeroUI v3;
- validação: Zod + invariantes de coleção;
- testes: Vitest + Playwright;
- publicação: Vercel;
- URL de produção registrada no repositório: `https://cadastroaluno-ecru.vercel.app`;
- verificação ao vivo da URL: não confirmada pelo conector Vercel disponível nesta execução;
- Motion Profile: `ambient`, atenuado para `subtle` em dados densos;
- reduced motion: obrigatório.

## Capacidades

1. cadastrar e editar aluno;
2. impedir matrícula equivalente duplicada;
3. pesquisar e filtrar registros;
4. ordenar resultados;
5. visualizar detalhes;
6. arquivar, reativar ou marcar transferência;
7. excluir com confirmação;
8. mostrar indicadores resumidos;
9. migrar registros locais legados v1 → v2;
10. gerar backup JSON versionado;
11. restaurar backup somente após validação e confirmação;
12. exportar CSV.

## Contratos importantes

- hospedagem pública **não altera** a classificação para sistema multiusuário;
- a persistência local continua sendo a fonte de verdade deste produto;
- migração não pode inventar dados que não existiam no contrato antigo;
- backup inválido não pode substituir registros atuais;
- unicidade de matrícula é invariante da coleção, não apenas do schema de um registro;
- a interface deve continuar deixando explícito que os dados não são compartilhados.

## Verificação

Artefatos V1.4 usados neste field test:

- `specs/semantic-contract.json`;
- `specs/semantic-assurance.json`;
- `specs/verification-plan.json`;
- `specs/review-evidence.json` no fechamento semântico;
- `SEMANTICS.md`;
- `VERIFICATION.md`.

Gates obrigatórios:

- lint;
- typecheck;
- 17 testes unitários;
- build;
- 10 E2E desktop/mobile;
- `npm audit` completo;
- validação do contrato/assurance/rastreabilidade;
- revisão semântica válida e atual.

## Resultado do field test até o fechamento

- especificação e Semantic Assurance: verdes;
- lint/typecheck/build: verdes;
- testes unitários: 17/17 verdes;
- Playwright: 10/10 verdes em Chromium desktop/mobile;
- `npm audit`: verde após atualização compatível do ESLint;
- `package-lock.json`: gerado em runner limpo e versionado antes do CI congelado;
- instalação final: deve usar `npm ci`.

## Limitações conhecidas

- dados não são compartilhados entre dispositivos;
- não há usuário autenticado nem autorização por papel;
- restauração substitui a coleção local inteira após confirmação;
- exclusão é local e imediata após confirmação;
- o projeto não precisa de API fuzz, DAST, load testing ou migration SQL porque essas superfícies não existem.

## Próxima ação

Gerar a revisão semântica no estado final, trocar o workflow transitório por CI somente leitura com `npm ci`, repetir todos os gates e integrar o PR. Em seguida, aplicar os aprendizados generalizáveis deste field test na App Factory em PR separado.
