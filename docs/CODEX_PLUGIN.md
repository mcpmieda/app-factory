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
├── engine/
├── policies/
├── templates/
└── ...
```

O manifest aponta `skills` para `./skills/`, que já é a fonte portátil usada pelos outros agentes. O runtime V1.1 em `engine/` é neutro e não depende do Codex.

## Por que usar a raiz como plugin

- evita cópia de Skills;
- reduz risco de divergência entre Codex e outros agentes;
- preserva Core/engine/policies/templates no mesmo repositório;
- mantém o plugin como adaptador fino, não como nova fonte de verdade.

## Estado

`1.1.0` — **V1.1 estável**.

O Codex CLI oficial `0.149.0` reconhece o marketplace local, instala a App Factory e descobre as **13 Skills**, incluindo `factory-router`, `context-engine` e `autonomy-engine`. O bootstrap isolado compara SHA-256 de todas as Skills entre checkout limpo e cache instalado e rejeita omissão, duplicação, divergência ou pacote pesado.

A V1.1 também reduz a dependência operacional do Codex: o Task Router prefere agente atual + GitHub/CI quando essa rota consegue implementar e provar o trabalho. Codex continua sendo um executor importante para runtime/browser/debug/migrations interativos, mas não é mais o destino automático de qualquer tarefa com testes ou múltiplos arquivos.

## Marketplace local com fonte única

O arquivo `.agents/plugins/marketplace.json` aponta a entrada `app-factory` para `./`, isto é, a própria raiz do repositório. O checkout continua sendo a única fonte mantida. Na instalação, o Codex cria um cache derivado; ele não é editado e a auditoria exige hashes idênticos ao `skills/` de origem.

Para registrar a origem em um Codex CLI que exponha os comandos de plugins:

```text
codex --enable plugins plugin marketplace add <raiz-do-repositorio>
codex --enable plugins plugin add app-factory@app-factory-local
```

O Codex/ChatGPT Desktop pode exigir reinstalação/reinício e nova conversa para carregar alterações do plugin.

## Runtime autônomo

Quando houver checkout/runtime disponível, os agentes compartilham a mesma interface:

```text
python scripts/factory.py --root <projeto> context
python scripts/factory.py --root <projeto> resume
python scripts/factory.py --root <projeto> next
python scripts/factory.py --root <projeto> record <evento>
```

O usuário normalmente não executa esses comandos; o agente/adaptador faz isso internamente.

## Validação reproduzível

Execute:

```text
python scripts/validate_factory.py
python scripts/validate_skills.py
python scripts/validate_plugin.py
python scripts/validate_v1_1.py
python scripts/validate_v1_bootstrap.py
python scripts/validate_v1_release.py
```

As evidências completas estão em:

- `research/V0.2_CODEX_PLUGIN_PILOT.md` — piloto histórico;
- `research/V1.0_FINAL_AUDIT.md` — auditoria da primeira release estável;
- `research/V1.1_AUTONOMOUS_CONTEXT_VALIDATION.md` — validação do runtime autônomo.

## Resultado arquitetural

```text
APP FACTORY CORE + ENGINE
(portátil)
      │
      ├── Skills abertas
      ├── Context/Autonomy runtime
      ├── core/policies/templates
      └── scripts/testes
      │
      ├──────── current-agent + GitHub/CI
      │
      ▼
ADAPTADOR/EXECUTOR CODEX
      ├── plugin.json
      └── marketplace local
```

Nenhum arquivo do Core ou Skill é mantido como segunda fonte. O cache de instalação é uma cópia derivada do checkout limpo e deve ter hashes idênticos; `scripts/validate_v1_bootstrap.py` prova essa relação em um `CODEX_HOME` temporário, sem alterar a configuração global do usuário.

## MCP e hooks

Não adicionar MCP ou hooks por padrão. Eles só entram quando houver caso concreto em que MCP forneça ferramenta/dados ausentes ou um hook automatize proteção real e simples. Hooks devem permanecer raros, claros e auditáveis.
