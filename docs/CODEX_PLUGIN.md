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

O manifest aponta `skills` para `./skills/`, que já é a fonte portátil usada pelos outros agentes. O runtime V1.4 em `engine/` é neutro e não depende do Codex.

## Estado

`1.4.0` — **V1.4 estável**, com System Engineering e API Engineering como governance hardenings sobre a mesma baseline de engines.

O plugin descobre as **17 Skills** diretamente de `skills/`, incluindo `factory-router`, `api-engineering`, `semantic-verification`, `context-engine`, `autonomy-engine`, `execution-router` e `learning-engine`. O bootstrap isolado compara SHA-256 das Skills entre checkout limpo e cache instalado e rejeita omissão, duplicação, divergência ou pacote pesado.

Adicionar uma Skill à fonte `skills/` não exige manter uma segunda lista dentro do plugin; essa fonte única é intencional.

## Papel do Codex

Codex não é destino automático para tarefa com código, múltiplos arquivos ou testes. A Execution Fabric seleciona por capacidade:

1. agente atual + ferramentas;
2. GitHub Actions / CI;
3. sandbox leve disponível;
4. executor local completo.

Aprendizado local pode otimizar somente os backends leves que já são capazes/elegíveis. `local_full` não é promovido sobre um backend leve capaz apenas porque teve score histórico melhor.

Codex é uma implementação possível de `local_full` e continua indicado quando browser/runtime/debug/migrations interativos ou outra capacidade local forem realmente necessários.

## Governança não depende do Codex

`core/SYSTEM_ENGINEERING.md`, `core/API_ENGINEERING.md` e `core/SEMANTIC_VERIFICATION.md` pertencem ao núcleo portátil. Um projeto deve receber a mesma classificação arquitetural, governança de API e prova semântica independentemente de ser executado por Codex, ChatGPT, CI ou outro agente compatível.

API Engineering continua condicional: o plugin não instala OpenAPI, Redocly, Pact ou outras ferramentas apenas porque a Skill existe. `api-engineering` escolhe os contratos/gates que o projeto realmente precisa.

## Learning Engine não depende do Codex

`.factory/learning.json` contém apenas metadados técnicos allowlisted de execução e fica fora do Git por padrão. Não há envio de telemetria externa. O mesmo runtime pode ser usado por outro agente compatível; se o arquivo local não existir em outra máquina, o roteamento baseline continua funcionando normalmente.

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
python scripts/factory.py --root <projeto> learning-status
python scripts/factory.py --root <projeto> learning-recommend verify
python scripts/factory.py --root <projeto> gates
```

O usuário normalmente não executa esses comandos; o agente/adaptador faz isso internamente.

## Validação reproduzível

```text
python scripts/validate_factory.py
python scripts/validate_skills.py
python scripts/validate_plugin.py
python scripts/validate_system_engineering.py
python scripts/validate_api_engineering.py
python scripts/validate_v1_1.py
python scripts/validate_v1_2.py
python scripts/validate_v1_3.py
python scripts/validate_v1_4.py
python scripts/validate_v1_bootstrap.py
python scripts/validate_v1_release.py
```

## Resultado arquitetural

```text
APP FACTORY CORE + ENGINE
(portátil)
      │
      ├── System Engineering
      ├── API Engineering (condicional)
      ├── Semantic Verification
      ├── Context Engine
      ├── Autonomy Engine
      ├── Execution Fabric
      ├── Learning Engine (local-only)
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
