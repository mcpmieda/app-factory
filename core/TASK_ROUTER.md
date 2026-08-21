# Task Router — escolha de executor

A Factory escolhe o executor pela capacidade necessária para provar o trabalho, não pela palavra "código" nem por preferência de fornecedor.

## Regra principal — current-agent first

Antes de fazer handoff, tente a rota mais leve que preserve segurança e verificabilidade:

1. **agente atual + ferramentas diretas** — leitura, raciocínio, arquivos, GitHub, conectores disponíveis;
2. **GitHub + CI** — branch/PR e Actions como executor remoto para lint, typecheck, testes, build e outros gates reproduzíveis;
3. **executor leve disponível** — shell/sandbox/ACP/outro backend quando necessário e seguro;
4. **Codex ou agente local completo** — quando a tarefa realmente depende de checkout interativo, servidor/browser local, debugging, migrations ou coordenação que o caminho anterior não consegue provar.

Nunca reduza Definition of Done só para evitar Codex. Também não use Codex por reflexo quando GitHub/CI já fornece prova suficiente.

## ChatGPT / agente com GitHub

Pode permanecer no ambiente atual quando ele consegue:

- entender produto e arquitetura;
- pesquisar/comparar soluções;
- editar arquivos e branches com segurança;
- abrir/revisar PRs;
- acionar ou observar CI;
- ler logs e corrigir falhas;
- repetir o ciclo até os gates ficarem verdes.

Múltiplos arquivos, por si só, não obrigam handoff se o agente consegue coordenar as alterações e o CI prova o resultado.

## GitHub Actions como executor remoto

Use CI quando comandos determinísticos podem provar o trabalho sem ambiente interativo, por exemplo:

- lint/format/typecheck;
- testes unitários/integrados;
- build;
- Playwright headless;
- banco efêmero/migrations testáveis;
- validadores e smoke tests.

O agente deve ler o resultado, corrigir e rerodar automaticamente dentro do limite de reparo aplicável.

## Quando Codex/local continua sendo a escolha correta

Preferir um executor local completo quando houver necessidade real de:

- browser interativo ou inspeção visual/manual que CI não cobre;
- debugging de processo/servidor local;
- dependências/serviços locais difíceis de reproduzir no CI;
- migrations com ambiente real ou investigação delicada;
- refatoração ampla cujo feedback rápido de terminal é essencial;
- operação em muitos arquivos/binários não suportada pelas ferramentas atuais;
- falha repetida em que o current-agent/CI atingiu o limite de reparo.

## Heurística

1. O agente atual consegue editar e provar via GitHub/CI? → fique no agente atual.
2. Precisa apenas executar comandos determinísticos? → prefira CI ou sandbox disponível.
3. Precisa observar/interagir com runtime local? → executor local/Codex.
4. Precisa de decisão/raciocínio/revisão? → agente atual.
5. A rota atual falhou repetidamente? → mude estratégia/executor antes de envolver o usuário.
6. Existe decisão de produto/custo/risco/credencial? → usuário quando realmente necessário.

## Comunicação

Não exponha roteamento interno a cada passo. Informe troca de ambiente apenas quando o usuário precisa agir ou quando ela muda materialmente custo/risco.

Quando houver handoff, registre fase, contexto/fingerprint, Issue/PR e critérios de conclusão no GitHub.

## Portabilidade

O Core fala em capacidades (`current agent`, `CI`, `local executor`, `browser executor`) e adaptadores mapeiam essas capacidades para ChatGPT, Codex, Claude Code, Cursor, ACP ou outra ferramenta disponível.
