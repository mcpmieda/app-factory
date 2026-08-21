# PROJECT_STATE

## Objetivo vigente

Aplicativo simples de cadastro de aluno em uma única etapa, com interface HeroUI e experiência de teste fácil no navegador.

## Estado atual

- fase: `baseline inicial`;
- escala: `S — projeto pequeno`;
- perfil de produto: `web-admin` simplificado;
- stack: Next.js 16 + React 19 + TypeScript + Tailwind CSS 4 + HeroUI v3;
- validação: Zod;
- persistência: `localStorage` (demonstração/local, sem backend);
- testes: Vitest + Playwright;
- ambiente de teste fácil: GitHub Codespaces;
- publicação online preparada: Vercel, sem variáveis de ambiente;
- Motion Profile: `ambient`;
- dense data views: attenuate to `subtle`;
- reduced motion: mandatory.

## Fluxo crítico

1. usuário preenche os dados do aluno;
2. validação ocorre na mesma tela;
3. matrícula duplicada é bloqueada;
4. cadastro é persistido localmente;
5. registro aparece na lista;
6. recarregar a página preserva os dados.

## Critérios de sucesso

- cadastro em uma única etapa;
- desktop e mobile;
- estados vazio, erro e sucesso;
- foco/teclado e labels acessíveis via HeroUI/React Aria;
- `prefers-reduced-motion`;
- lint, typecheck, unit test, build e E2E disponíveis por scripts;
- Codespaces abre a aplicação na porta 3000 automaticamente.

## Limitações conhecidas

- não há backend, banco compartilhado ou autenticação;
- os dados existem somente no navegador/dispositivo atual;
- o `package-lock.json` será criado na primeira instalação porque o ambiente de geração deste pacote não possui acesso ao npm para materializar o lockfile;
- a verificação executável final deve ser rodada no Codespaces com `npm run test:all`.

## Próxima ação lógica

Executar o gate do projeto no GitHub Actions. Para visualização online permanente, importar o repositório `mcpmieda/app-factory` no Vercel usando `projects/cadastro-aluno-factory-heroui` como Root Directory. O `package-lock.json` deve ser materializado em uma futura instalação com acesso ao npm para tornar a instalação totalmente reproduzível com `npm ci`.
