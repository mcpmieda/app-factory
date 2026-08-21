# Codex Plugin — adaptador validado

A App Factory pode ser empacotada diretamente como plugin do ecossistema OpenAI sem duplicar as Skills.

## Estrutura

```text
app-factory/
├── .codex-plugin/
│   └── plugin.json
├── .agents/plugins/
│   └── marketplace.json
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

`0.2.0-alpha` — **validado em piloto real na Issue #3 em 2026-08-21**.

O Codex CLI oficial `0.149.0` reconheceu o marketplace local, instalou e habilitou a App Factory, descobriu as 10 Skills e ativou explicitamente `app-planner`, `tool-router`, `ui-builder` e `verification` em smoke test. Os hashes das quatro Skills na origem e no cache instalado foram idênticos.

A versão continua `alpha` porque a V0.2 ainda precisa ser integrada ao `main` e o starter `web-admin` ainda será usado como segundo piloto antes da V1.

## Marketplace local sem cópia

O arquivo `.agents/plugins/marketplace.json` aponta a entrada `app-factory` para `./`, isto é, a própria raiz do repositório. Assim, o host lê `.codex-plugin/plugin.json` e `skills/` diretamente da fonte portátil, sem criar uma segunda árvore de `skills/` ou `core/`.

Para registrar a origem em um Codex CLI que exponha os comandos de plugins:

```text
codex plugin marketplace add <raiz-do-repositorio>
codex plugin add app-factory@app-factory-local
```

O Codex/ChatGPT Desktop pode exigir reinstalação/reinício e nova conversa para carregar alterações do plugin.

## Validação reproduzível

Execute:

```text
python scripts/validate_factory.py
python scripts/validate_skills.py
python scripts/validate_plugin.py
```

No piloto também foi usado o validador oficial do `plugin-creator`.

As evidências completas estão em:

`research/V0.2_CODEX_PLUGIN_PILOT.md`

## Resultado arquitetural

O piloto confirmou o desenho:

```text
APP FACTORY CORE
(portátil)
      │
      ├── Skills abertas
      ├── core/policies/templates
      └── scripts/testes
      │
      ▼
ADAPTADOR CODEX
      ├── plugin.json
      └── marketplace local
```

Nenhum arquivo do Core precisou ser duplicado ou alterado para satisfazer o Codex.

## MCP e hooks

Não adicionar MCP ou hooks por padrão nesta fase.

Eles só entram quando houver caso concreto em que:

- MCP forneça ferramenta/dados que Skills e ferramentas existentes não cubram;
- hook automatize proteção real e simples.

Plugins com hooks exigem revisão/confiança do usuário; portanto a Factory deve manter hooks raros, claros e auditáveis.