# Context Engine

O Context Engine reduz releitura de repositório sem transformar a Factory em um índice pesado ou dependente de fornecedor.

## Objetivo

Gerar um mapa compacto, portátil e incremental do projeto para que um agente consiga responder rapidamente:

- qual é a stack;
- quais arquivos são importantes;
- quais símbolos e imports existem nos arquivos de código;
- o que mudou desde a última leitura;
- qual é o estado Git disponível;
- quais partes do repositório merecem ser abertas em detalhe para a tarefa atual.

O mapa é uma ajuda de navegação, nunca substitui a leitura do arquivo real quando a decisão depende do conteúdo completo.

## Interface

A partir da raiz do projeto:

```bash
python scripts/factory.py context
```

Em projetos que consomem a App Factory por plugin/adaptador, o agente pode chamar o runtime equivalente sem expor o comando ao usuário.

Saída padrão:

- `.factory/context/repo-map.json` — mapa legível por máquina;
- `.factory/context/SUMMARY.md` — resumo curto para agentes/pessoas.

`.factory/context/` é cache regenerável e não deve ser usado como fonte histórica de verdade. O estado durável continua no GitHub e em documentos como `PROJECT_STATE.md`.

## Incrementalidade

Cada arquivo textual mapeado recebe SHA-256. Em uma atualização:

1. arquivos com o mesmo hash reutilizam os metadados anteriores;
2. arquivos novos ou alterados são reprocessados;
3. arquivos removidos aparecem no delta;
4. um fingerprint global representa a fotografia lógica atual.

O motor ainda precisa ler bytes suficientes para calcular hashes, mas evita reextrair símbolos/imports/stack de arquivos sem mudança.

## Segurança e escopo

Por padrão não indexar:

- `.git` e metadados de IDE;
- `node_modules`, vendors e ambientes virtuais;
- builds, caches, coverage e resultados de teste;
- `.factory` para impedir loops do próprio runtime;
- `.env*`, chaves privadas, credenciais conhecidas e keystores;
- binários e arquivos grandes acima do limite configurado.

Não colocar conteúdo integral de arquivos no mapa. Guardar apenas metadados, hashes, símbolos/imports e classificação necessária à navegação.

## Portabilidade

O engine usa Python stdlib e caminhos relativos. Não depende de Codex, ChatGPT, MCP ou API proprietária.

Um adaptador de agente pode usar o mapa, mas o Core não deve depender do adaptador.

## Quando atualizar

Atualize no início de uma retomada e quando houver suspeita de mudança externa no repositório. O `Autonomy Engine` chama o refresh automaticamente no `resume`/`next` e força reconciliação quando o fingerprint mudou durante uma fase ativa.
