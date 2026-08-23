# PROJECT_STATE

## Objetivo vigente

Manter uma **gestão local completa de alunos** para demonstração e teste da App Factory, preservando a simplicidade arquitetural de um `local-app` mesmo quando distribuído pelo Vercel.

## Estado atual

- fase: `field test v0.2`;
- versão do app: `0.2.0`;
- escala de processo: `S/M — evolução funcional relevante`;
- nível do sistema: `local-app`;
- perfil: `web-admin` com HeroUI v3;
- API mode: `none`;
- semantic depth: `domain`;
- Independent Verification: `independent` proporcional;
- fonte autoritativa dos dados: `localStorage` do navegador atual;
- contrato de persistência: `v2`, com migração automática de `v1`;
- backend/banco compartilhado: `não aplicável ao escopo atual`;
- autenticação/autorização: `não aplicável ao escopo atual`;
- stack: Next.js 16 + React 19 + TypeScript + Tailwind CSS 4 + HeroUI v3;
- validação: Zod;
- testes: Vitest + Playwright;
- publicação: Vercel;
- URL de produção conhecida: `https://cadastro-aluno-factory-heroui.vercel.app`;
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
- a interface deve continuar deixando explícito que os dados não são compartilhados.

## Verificação

Artefatos V1.4 usados neste field test:

- `specs/semantic-contract.json`;
- `specs/semantic-assurance.json`;
- `specs/verification-plan.json`;
- `specs/review-evidence.json` após a execução dos gates;
- `SEMANTICS.md`;
- `VERIFICATION.md`.

Gates principais:

- lint;
- typecheck;
- unit tests;
- build;
- E2E desktop/mobile;
- dependency audit;
- validação do contrato/assurance/rastreabilidade.

## Limitações conhecidas

- dados não são compartilhados entre dispositivos;
- não há usuário autenticado nem autorização por papel;
- restauração substitui a coleção local inteira após confirmação;
- exclusão é local e imediata após confirmação;
- o projeto não precisa de API fuzz, DAST, load testing ou migration SQL porque essas superfícies não existem.

## Próxima ação

Executar o field test completo em CI, materializar instalação reproduzível com lockfile, validar os critérios semânticos e integrar somente com todos os gates verdes. Depois, transformar os aprendizados generalizáveis em melhorias da App Factory sem aumentar a quantidade de Skills por reflexo.
