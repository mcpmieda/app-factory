# Codex Plugin — adaptador validado

A App Factory pode ser empacotada diretamente como plugin do ecossistema OpenAI sem duplicar as Skills.

## Estrutura

```text
app-factory/
├── .codex-plugin/plugin.json
├── .agents/plugins/marketplace.json
├── skills/
├── core/
├── engine/
├── policies/
├── templates/
└── ...
```

O manifest aponta `skills` para `./skills/`, que já é a fonte portátil usada pelos outros agentes. O runtime V1.2 em `engine/` é neutro e não depende do Codex.

## Estado

`1.2.0` — **V1.2 estável**.

O Codex CLI oficial `0.149.0` reconhece o marketplace local, instala a App Factory e descobre as **14 Skills**, incluindo `factory-router`, `context-engine`, `autonomy-engine` e `execution-router`. O bootstrap isolado compara SHA-256 de todas as Skills entre checkout limpo e cache instalado e rejeita omissão, duplicação, divergência ou pacote pesado.

## Papel do Codex na V1.2

Codex deixa de ser destino automático para qualquer tarefa com código, múltiplos arquivos ou testes. A Execution Fabric seleciona por capacidade:

1. agente atual + ferramentas;
2. GitHub Actions / CI;
3. sandbox leve disponível;
4. executor local completo.

Codex é um possível backend `local_full` e continua indicado quando browser/runtime/debug/migrations interativos ou outra capacidade local forem realmente necessários.

Essa separação evita que o Core fique dependente de um único fornecedor ou ambiente.

## Marketplace local com fonte única

O arquivo `.agents/plugins/marketplace.json` aponta a entrada `app-factory` para `./`, isto é, a própria raiz do repositório. O checkout continua sendo a única fonte mantida. Na instalação, o Codex cria um cache derivado; ele não é editado e a auditoria exige hashes idênticos ao `skills/` de origem.

Para registrar a origem em um Codex CLI que exponha os comandos de plugins:

```text
codex --enable plugins plugin marketplace add <raiz-do-repositorio>
codex --enable plugins plugin add app-factory@app-factory-local
```

O Codex/ChatGPT Desktop pode exigir reinstalação/reinício e nova conversa para carregar alterações do plugin.

## Runtime portátil

Quando houver checkout/runtime disponível, os agentes compartilham a mesma interface:

```text
python scripts/factory.py --root <projeto> context
python scripts/factory.py --root <projeto> resume
python scripts/factory.py --root <projeto> next
python scripts/factory.py --root <projeto> route verify
python scripts/factory.py --root <projeto> execution-status
python scripts/factory.py --root <projeto> gates
```

O usuário normalmente não executa esses comandos; o agente/adaptador faz isso internamente.

## Validação reproduzível

```text
python scripts/validate_factory.py
python scripts/validate_skills.py
python scripts/validate_plugin.py
python scripts/validate_v1_1.py
python scripts/validate_v1_2.py
python scripts/validate_v1_bootstrap.py
python scripts/validate_v1_release.py
```

## Resultado arquitetural

```text
APP FACTORY CORE + ENGINE
(portátil)
      │
      ├── Context Engine
      ├── Autonomy Engine
      ├── Execution Fabric
      ├── Skills/policies/templates
      └── testes/validadores
      │
      ├── current_agent
      ├── github_ci
      ├── sandbox (opcional)
      └── local_full (opcional)
                 │
                 └── Codex pode ser um adaptador
```

Nenhum arquivo do Core ou Skill é mantido como segunda fonte. O cache de instalação é derivado do checkout limpo e deve ter hashes idênticos; `scripts/validate_v1_bootstrap.py` prova essa relação em um `CODEX_HOME` temporário.

## MCP e hooks

Não adicionar MCP ou hooks por padrão. Eles só entram quando houver caso concreto em que MCP forneça ferramenta/dados ausentes ou um hook automatize proteção real e simples. Hooks devem permanecer raros, claros e auditáveis.
