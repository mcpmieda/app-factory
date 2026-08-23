# API templates

Use estes arquivos somente em projetos onde `core/API_ENGINEERING.md` classificar a interface como `contract` ou `governed`.

## OpenAPI — gate recomendado

1. Copie `redocly.yaml` para a raiz do projeto quando Redocly CLI for o linter escolhido.
2. Fixe a versao do Redocly CLI no package manager/CI do projeto.
3. Valide o contrato, por exemplo:

```bash
npx @redocly/cli@<versao-fixada> lint api/openapi.yaml
```

4. Quando houver consumidores que dependam de compatibilidade, compare a baseline com a revisao usando oasdiff ou equivalente:

```bash
oasdiff breaking base-openapi.yaml api/openapi.yaml
```

5. Quando risco/valor justificar, execute Schemathesis contra ambiente de teste/preview, nunca fuzz destrutivo contra producao:

```bash
uvx schemathesis@<versao-fixada> run api/openapi.yaml --url http://127.0.0.1:8000 --mode all
```

Os comandos sao exemplos de integracao, nao dependencias universais. Adapte paths, autenticacao, runtime e versoes ao projeto. `skills/api-engineering` decide quais gates realmente entram.
