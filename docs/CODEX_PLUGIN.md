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

`1.0.0-rc.1` — **release candidate aguardando revisão final**.

O Codex CLI oficial `0.149.0` reconhece o marketplace local, instala a App Factory e descobre as 11 Skills, incluindo `factory-router`. A auditoria V1 compara SHA-256 de todas as Skills entre o checkout limpo e o cache instalado e rejeita omissão, duplicação, divergência ou pacote pesado.

## Marketplace local com fonte única

O arquivo `.agents/plugins/marketplace.json` aponta a entrada `app-factory` para `./`, isto é, a própria raiz do repositório. O checkout continua sendo a única fonte mantida. Na instalação, o Codex cria um cache derivado; ele não é editado e a auditoria exige hashes idênticos ao `skills/` de origem.

Para registrar a origem em um Codex CLI que exponha os comandos de plugins:

```text
codex --enable plugins plugin marketplace add <raiz-do-repositorio>
codex --enable plugins plugin add app-factory@app-factory-local
```

O Codex/ChatGPT Desktop pode exigir reinstalação/reinício e nova conversa para carregar alterações do plugin.

## Validação reproduzível

Execute:

```text
python scripts/validate_factory.py
python scripts/validate_skills.py
python scripts/validate_plugin.py
python scripts/validate_v1_bootstrap.py
```

No piloto também foi usado o validador oficial do `plugin-creator`.

As evidências completas estão em:

`research/V0.2_CODEX_PLUGIN_PILOT.md` (piloto histórico) e `research/V1.0_FINAL_AUDIT.md` (gate atual).

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

Nenhum arquivo do Core ou Skill é mantido como segunda fonte. O cache de instalação é uma cópia derivada do checkout limpo e deve ter hashes idênticos; `scripts/validate_v1_bootstrap.py` prova essa relação em um `CODEX_HOME` temporário, sem alterar a configuração global do usuário.

## MCP e hooks

Não adicionar MCP ou hooks por padrão nesta fase.

Eles só entram quando houver caso concreto em que:

- MCP forneça ferramenta/dados que Skills e ferramentas existentes não cubram;
- hook automatize proteção real e simples.

Plugins com hooks exigem revisão/confiança do usuário; portanto a Factory deve manter hooks raros, claros e auditáveis.
