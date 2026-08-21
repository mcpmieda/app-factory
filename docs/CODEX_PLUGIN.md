# Codex Plugin — modo experimental

A App Factory pode ser empacotada diretamente como plugin do ecossistema OpenAI sem duplicar as Skills.

## Estrutura

```text
app-factory/
├── .codex-plugin/
│   └── plugin.json
├── skills/
├── core/
├── policies/
├── templates/
└── ...
```

O manifest aponta `skills` para `./skills/`, que já é a fonte portátil usada pelos outros agentes.

## Por que usar a raiz como plugin

- evita cópia de Skills;
- reduz risco de divergência entre Codex e outros agentes;
- preserva Core/policies/templates no mesmo repositório;
- mantém o plugin como adaptador fino, não como nova fonte de verdade.

## Estado

`0.2.0-alpha` — manifest compatível com o esquema atual e marketplace local
adicionado para o piloto da Issue #3. A promoção para estável depende da revisão
das evidências do piloto.

## Marketplace local sem cópia

O arquivo `.agents/plugins/marketplace.json` aponta a entrada `app-factory`
para `./`, isto é, a própria raiz do repositório. Assim, o host lê
`.codex-plugin/plugin.json` e `skills/` diretamente da fonte portátil, sem criar
`plugins/app-factory`, copiar Skills ou duplicar `core/`.

Para registrar a origem em um Codex CLI que exponha os comandos de plugins:

```text
codex plugin marketplace add <raiz-do-repositorio>
codex plugin add app-factory@app-factory-local
```

O Codex/ChatGPT Desktop precisa ser reiniciado e o smoke test deve ser feito em
uma nova conversa para carregar a instalação atualizada.

## Teste necessário

Em uma fase executada no Codex/local:

1. clonar/abrir `mcpmieda/app-factory`;
2. validar que o plugin é reconhecido por marketplace/local install;
3. confirmar descoberta das Skills;
4. invocar pelo menos `app-planner`, `tool-router`, `ui-builder` e `verification`;
5. confirmar que nenhuma Skill precisa duplicar o Core;
6. registrar incompatibilidades;
7. somente depois promover a versão do plugin.

Execute também os validadores versionados:

```text
python scripts/validate_factory.py
python scripts/validate_skills.py
python scripts/validate_plugin.py
```

As evidências executáveis do piloto estão em
`research/V0.2_CODEX_PLUGIN_PILOT.md`.

## MCP e hooks

Não adicionar MCP ou hooks por padrão nesta fase.

Eles só entram quando houver caso concreto em que:

- MCP forneça ferramenta/dados que Skills e ferramentas existentes não cubram;
- hook automatize proteção real e simples.

Plugins com hooks exigem revisão/confiança do usuário; portanto a Factory deve manter hooks raros, claros e auditáveis.
