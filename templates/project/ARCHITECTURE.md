# ARCHITECTURE — Template

## Contexto
[Resumo técnico do sistema e ambiente]

## Escolhas principais
- frontend:
- backend:
- banco:
- autenticação:
- deploy:
- design system:
- Professional UI Profile: `professional-default` por padrão para UI material / exceção justificada:
- density: `compact` / `comfortable` / `spacious` quando relevante:
- surface: `flat` / `layered` / `immersive` quando relevante:
- emphasis: `quiet` / `balanced` / `bold` quando relevante:
- Motion Profile: `ambient` por padrão (`none`, `subtle`, `ambient`, `expressive`):
- motion implementation: recursos nativos do design system / CSS / biblioteca especializada somente se necessário:
- testes:
- semantic depth: [não aplicável / `scenario` / `domain` / `formal`]
- Independent Verification: `baseline` / `independent` / `adversarial` / `release`
- executor de verificação determinística: `github_ci` / self-hosted / local equivalente / não aplicável

Para cada escolha importante, registrar motivo curto e evitar tecnologia sem necessidade.

Interfaces devem seguir `ui/UI_POLICY.md`, `ui/PROFESSIONAL_UI_PROFILE.md` e `ui/MOTION_POLICY.md`:

- `professional-default` define o quality bar, não instala biblioteca;
- admin/dashboard/CRUD continua preferindo shadcn como base e ReUI seletivo quando não houver preferência explícita por HeroUI;
- escolha explícita de HeroUI para o sistema inteiro prevalece sobre o default administrativo e deve permanecer transversal;
- nenhum efeito ambiental específico é obrigatório por design system;
- `prefers-reduced-motion` é obrigatório para movimento não essencial.

## Componentes

```mermaid
flowchart LR
  U[Usuário] --> A[Aplicação]
  A --> B[Backend/API]
  B --> D[(Dados)]
```

Adapte ou remova o diagrama quando não ajudar. Se não houver API formal, não rotule uma função interna como API apenas para preencher o desenho.

## Fluxo de dados
- ...

## Limites e contratos
- schema/dados:
- integrações:
- permissões:

### Semantic Assurance, quando `domain`/`formal`
- semantic contract: `specs/semantic-contract.json`
- semantic assurance: `specs/semantic-assurance.json`
- vocabulário/entidades/relações/estados que afetam arquitetura:
- restrições importantes:
- semantic diff/baseline:
- formalizações selecionadas: [não aplicável / kind + artefato + gate]

Use `core/SEMANTIC_ASSURANCE.md`. Não replique aqui o glossário/requisito inteiro.

### API, quando aplicável
- modo de governança: `none` / `lightweight` / `contract` / `governed`
- consumidores/owner:
- protocolo/estilo:
- fonte de verdade do contrato:
- caminho do contrato:
- compatibilidade/depreciação:
- gates de contrato/runtime:

Use `core/API_ENGINEERING.md`. Para API relevante/complexa, use também `API.md`.

### Independent Verification, quando acima de `baseline`
- modo: `independent` / `adversarial` / `release`
- checks `required`:
- checks `advisory`:
- ambiente/alvo efêmero:
- thresholds/budgets baseados em baseline real:
- exceções/suppressions:
- workflow/config autoritativo:

Use `core/INDEPENDENT_VERIFICATION.md` e detalhe a matriz em `VERIFICATION.md`.

## Configuração por ambiente
Separar valores variáveis da lógica. Nunca registrar segredos.

## Segurança
- autenticação:
- autorização:
- dados sensíveis:
- secrets:
- privilégio mínimo:

## UI profissional, quando aplicável
- inventário de arquétipos: shell / page-header / stats / search-command / filters / data-view / form / detail-inspector / feedback / outros realmente necessários:
- componentes reutilizados do design system/registry:
- componentes próprios justificados:
- estados críticos: loading / empty / error / success / disabled / permission denied / outros:
- estratégia mobile para dados densos:
- ação destrutiva/primary action:
- visual QA executado:

Não copiar templates/ativos proprietários de referências comerciais para a Factory ou projeto sem licença explícita aplicável.

## Acessibilidade e movimento
- reduced motion:
- reduced transparency progressive enhancement:
- teclado/foco:
- telas/fluxos onde motion precisa ser atenuado:
- sinais de atenção que precisam encerrar/reduzir após interação:
- ausência de flash/strobe:
- axe-core/Playwright: [não aplicável / advisory / required conforme VERIFICATION.md]

## Continuidade de operações críticas

Preencher para `persistent-app` ou superior quando a interrupção do cliente puder causar efeito parcial, duplicidade, inconsistência ou perda de progresso.

- operação crítica:
- risco se navegador/cliente fechar, energia/rede cair ou usuário trocar de dispositivo:
- ponto em que o comando passa a ser considerado aceito pelo servidor:
- identificador estável da operação/job/lote quando necessário:
- estado/checkpoint durável fora do navegador:
- estratégia de idempotência:
- estratégia para escrita de resultado ambíguo (reconciliar antes de repetir):
- progresso por item/unidade para operações em massa:
- retomada/reconciliação/compensação:
- status consultável pelo cliente depois da interrupção:
- regra para responder: **foi executada? até onde chegou? o que ainda falta?**
- comportamento quando a interrupção ocorre antes do servidor aceitar o comando:
- teste de interrupção/retomada executado:

Não adote fila/job por reflexo. Se a operação for curta, atômica e segura para repetição, documente por que mecanismo mais simples é suficiente. O requisito é sobrevivência e determinismo conforme `core/SYSTEM_ENGINEERING.md`.

## Observabilidade
Definir apenas o necessário para diagnosticar falhas e comportamento. Para operações duráveis, manter correlação suficiente para localizar uma operação sem registrar secrets/dados sensíveis desnecessários.

## Recuperação
Em sistemas existentes ou mudanças de risco, registrar baseline, backup/migration e rollback adequados. Quando operações críticas puderem sobreviver ao cliente, incluir retomada/reconciliação e estado server-side na estratégia de recovery.

## Decisões substituídas
Não manter alternativas antigas como se ainda fossem vigentes. Referenciar decisão histórica quando necessário.
