# Student Management Field Test — App Factory

Data: 2026-08-23

## Objetivo

Testar a App Factory em evolução real de um produto já existente e publicado: transformar o cadastro simples em uma gestão local de alunos mais completa, preservar o que funcionava, validar regressões e usar falhas observadas para melhorar a própria Factory.

O teste não tinha como objetivo transformar a demonstração em sistema escolar institucional. A pergunta arquitetural principal era se a Factory conseguiria aumentar bastante a capacidade do produto **sem aumentar a arquitetura além do requisito real**.

## Baseline

Projeto: `projects/cadastro-aluno-factory-heroui`

Estado inicial:

- Next.js + HeroUI;
- cadastro simples de aluno;
- persistência em `localStorage`;
- sem backend/autenticação/banco remoto;
- publicado/distribuído pelo Vercel;
- testes unitários/E2E básicos;
- sem lockfile versionado.

Classificação confirmada: `local-app`.

A publicação no Vercel não mudou essa classificação: o frontend estava online, mas os dados autoritativos continuavam exclusivos de cada navegador.

## Evolução implementada

A fatia funcional passou a incluir:

- criação e edição;
- busca, filtros e ordenação;
- detalhes do aluno;
- status ativo/arquivado/transferido;
- indicadores resumidos;
- exclusão confirmada;
- exportação CSV;
- backup/restauração JSON versionado;
- migração automática `localStorage` v1 → v2;
- invariantes de coleção para matrícula única;
- layout responsivo mantendo HeroUI/Semantic Motion/reduced motion.

Nenhum backend, API formal, autenticação ou banco remoto foi criado porque nenhum requisito do field test exigia essas capacidades.

## Evidência final do produto

PR do produto: #48.

Estado integrado:

- `npm ci` com lockfile versionado;
- lint: pass;
- typecheck: pass;
- 17/17 unit tests: pass;
- build Next.js: pass;
- `npm audit`: pass;
- 10/10 Playwright E2E em Chromium desktop/mobile: pass;
- Semantic Assurance `domain`: 7/7 requisitos obrigatórios ligados a ACs, 7/7 ACs `must` com gate executável e 4/4 invariantes referenciados;
- Semantic Verification: 7/7 ACs `must` em `pass` com review fingerprint atual;
- workflow final somente leitura.

## Falhas encontradas e o que significam

### 1. Hospedagem não define nível do sistema

Risco observado: interpretar “já está no Vercel” como motivo para introduzir backend/banco/autenticação.

Conclusão: classificação depende de fonte autoritativa, compartilhamento, identidade e continuidade esperada. Um `local-app` pode ser distribuído por host web e continuar local.

Ação na Factory: registrar explicitamente essa regra em System Engineering.

### 2. Dados locais também precisam de lifecycle

A versão antiga possuía registros reais do ponto de vista do usuário, mesmo sem banco remoto.

Conclusão: evolução incompatível de `localStorage` precisa de contrato versionado, migração validada, write-before-delete, representação explícita de valores desconhecidos e recovery proporcional.

Ação na Factory: adicionar lifecycle de dados para `local-app` sem promover o produto artificialmente para `persistent-app`.

### 3. Schema por registro não prova invariante da coleção

Zod conseguia validar cada aluno, mas isso não impedia uma coleção/restauração adulterada de conter duas matrículas equivalentes.

Conclusão: unicidade, cardinalidade e conflitos entre registros exigem visão do conjunto.

Ação na Factory: System Engineering passa a diferenciar validação por registro de invariantes cross-record.

### 4. Locator global ficou ambíguo quando a UI cresceu

O formulário possuía “Turma”; ao surgir “Filtrar por turma”, `getByLabel("Turma")` passou a localizar mais de um elemento.

Conclusão: E2E que sobrevive ao crescimento da UI deve escopar seleção à região/form/dialog/row antes de role/label.

Ação na Factory: disciplina browser/E2E registrada em Semantic Verification.

### 5. O teste de migração tinha corrida com hidratação

O E2E semeava `localStorage` enquanto a aplicação ainda podia estar executando sua leitura inicial. O resultado era intermitente e podia parecer bug de migração.

Conclusão: testes que manipulam persistência depois da navegação devem aguardar readiness/hydration ou semear antes da inicialização.

Ação na Factory: regra explícita de sincronização no E2E.

### 6. Projeto legado sem lockfile não possui instalação reproduzível

O CI Executor corretamente recusava `npm ci`, mas não explicava um caminho seguro para recuperar o projeto.

O field test materializou o lockfile em runner limpo com package manager pinado, executou audit/build/testes, versionou o resultado e somente então migrou o CI final para `npm ci`.

Conclusão: ausência de lockfile é estado de recuperação, não autorização para CI permissivo permanente.

Ação na Factory: CI plan passa a expor `materialize-validate-commit-lockfile` sem executar `npm install` automaticamente.

### 7. CLI de Semantic Assurance dependia de `PYTHONPATH`

Em checkout limpo, `python scripts/semantic_assurance.py ...` falhou com `ModuleNotFoundError: engine`.

Conclusão: CLI versionada da Factory deve ser executável diretamente a partir de qualquer cwd sem workaround de ambiente.

Ação na Factory: bootstrap do repo root no script + teste subprocess sem `PYTHONPATH`.

### 8. `pattern: policy` não significa policy engine

O requisito local “backup inválido não substitui dados atuais” foi normalizado como `policy`, e isso bastou para recomendar OPA/Cedar.

Conclusão: o padrão estrutural EARS `policy` é genérico demais para selecionar policy-as-code. OPA/Cedar só deve ser sugerido com sinais explícitos de autorização/access-control/governança compatível.

Ação na Factory: tornar a recomendação dependente de sinais específicos e cobri-la com regressões positiva/negativa.

## O que deliberadamente NÃO virou regra

- não tornar todo `local-app` um app com backend;
- não exigir banco remoto para preservar dados locais;
- não exigir Independent Verification pesada em todo app simples;
- não instalar OPA/Cedar porque existe uma regra de negócio;
- não adicionar nova Skill apenas para este field test;
- não ampliar matriz cross-browser sem requisito de suporte multi-engine;
- não transformar workflow temporário de bootstrap em estado permanente.

## Resultado arquitetural

O principal sinal de qualidade do teste não foi “usar mais tecnologia”. Foi conseguir:

1. ampliar o produto;
2. preservar dados anteriores;
3. capturar novas invariantes;
4. aumentar a evidência executável;
5. manter a classificação `local-app` correta;
6. fechar em CI reproduzível;
7. converter problemas reais em hardenings generalizáveis da Factory.

Essa é a regra que o field test reforça: **a App Factory deve crescer a solução até o requisito real, e parar ali**.
