# Project Adoption Gate

## Objetivo

Impedir que um projeto declare uso da **App Factory** mas comece a implementar como um projeto convencional e só incorpore arquitetura, UI, Semantic Verification ou verificação independente depois.

Este gate transforma a adoção da Factory em um estado **durável, machine-readable e verificável antes do código**.

## Quando o gate é obrigatório

O Project Adoption Gate é obrigatório antes de implementação material quando qualquer uma destas condições for verdadeira:

- o usuário pedir explicitamente para usar a App Factory;
- o projeto tiver `.app-factory.json`;
- `AGENTS.md`, `PROJECT_STATE.md`, `PRODUCT.md` ou `ARCHITECTURE.md` declarar governança pela App Factory;
- o projeto tiver sido gerado por starter/template da App Factory;
- o projeto já tiver `.factory/state.json` ou artefatos semânticos que o identifiquem como projeto governado pela Factory.

A ativação universal de `factory-router` por intenção de software **não obriga** um repositório legado externo a adotar permanentemente a Factory para um reparo pequeno. A adoção durável é obrigatória quando a Factory é explicitamente escolhida como processo do projeto ou quando o projeto já está vinculado a ela.

## Regra principal

> Um projeto governado pela App Factory não entra em implementação material enquanto o gate `pre-implementation` não estiver verde.

Antes disso são permitidas apenas ações de preflight/governança: leitura, auditoria, classificação, criação/atualização de `AGENTS.md`, `PROJECT_STATE.md`, `.app-factory.json`, produto/arquitetura, especificações, plano de verificação e demais artefatos necessários para deixar o gate pronto.

Não usar código de produto como forma de descobrir depois qual arquitetura, design system ou contrato deveria ter sido escolhido.

## Fonte durável de adoção

Todo projeto governado deve possuir `.app-factory.json` na raiz.

Campos de governança esperados:

```json
{
  "schemaVersion": 2,
  "governance": "app-factory",
  "factoryBaseline": "vX.Y.Z",
  "adoption": {
    "status": "routed",
    "mode": "new"
  },
  "routing": {
    "scale": "M",
    "risk": "medium",
    "systemLevel": "production-system",
    "profile": "web-admin",
    "apiMode": "lightweight",
    "semanticVerification": "required",
    "semanticDepth": "domain",
    "independentVerification": "adversarial",
    "authoritativeData": "...",
    "identity": "...",
    "authorization": "...",
    "recovery": "..."
  },
  "ui": {
    "enabled": true,
    "designSystem": "shadcn/ui",
    "professionalUiProfile": "professional-default",
    "motionProfile": "ambient",
    "ambientSurfaceProfile": null,
    "constellationIntensity": null,
    "deviation": null
  }
}
```

O manifesto é um resumo de roteamento, não substitui documentação detalhada. `PROJECT_STATE.md`, `PRODUCT.md`, `ARCHITECTURE.md`, specs e código continuam sendo fontes reais do projeto.

## Gate `pre-implementation`

Antes de código funcional/visual novo, verificar:

1. `AGENTS.md` existe e vincula explicitamente o projeto à App Factory e ao `factory-router`;
2. `PROJECT_STATE.md` existe e contém o bloco recuperável de adoção;
3. `.app-factory.json` possui `governance = app-factory` e roteamento completo;
4. escala, risco e `systemLevel` foram classificados;
5. `persistent-app` ou superior possui fonte autoritativa explícita;
6. `multi-user-system` ou superior registra identidade, autorização e recovery proporcionais;
7. API mode foi classificado;
8. Semantic Verification foi classificada antes do código;
9. se Semantic Verification for `required`, `specs/semantic-contract.json` e `specs/verification-plan.json` existem antes da implementação;
10. para `domain`/`formal`, `specs/semantic-assurance.json` existe e está pronto/coerente antes da implementação;
11. Independent Verification mode foi classificado;
12. se houver UI material, design system, Professional UI Profile e Motion Profile estão explicitamente escolhidos;
13. se o perfil for `web-admin`, o default é shadcn/ui; ReUI é seletivo; CSS/HTML ad hoc como base visual exige desvio explícito e justificativa real;
14. se HeroUI for o design system principal, `ambient-constellation strong` é obrigatório por padrão conforme `ui/AMBIENT_CONSTELLATION_PROFILE.md`;
15. antes de criar UI própria, o agente inventaria os arquétipos necessários e pesquisaria o design system/registry/catálogo correspondente.

## Gate de UI — evitar o caso “React + CSS próprio”

Em UI material, “React existe” não é uma decisão de design system.

Para `web-admin`:

- default: **shadcn/ui**;
- ReUI: somente complemento avançado justificado;
- HeroUI: override transversal quando explicitamente escolhido ou claramente mais adequado;
- `custom`, `native`, `plain CSS`, `CSS/HTML`, `hand-rolled` ou equivalente só podem ser base visual com `ui.deviation` não vazio explicando por que o perfil validado não serve.

Uma restrição como “a stack existente usa React/Vite” **não é** por si só justificativa para ignorar shadcn/HeroUI: bibliotecas e primitives podem ser integradas à stack existente sem reconstruir infraestrutura quando compatíveis.

O gate deve falhar se o projeto registrar `web-admin` + UI habilitada + design system ad hoc sem desvio explícito.

## HeroUI

Quando `ui.designSystem` contiver HeroUI:

```text
Professional UI Profile: professional-default
Motion Profile: ambient
Ambient Surface Profile: ambient-constellation
Constellation Intensity: strong
```

São aceitas exceções somente com justificativa explícita de produto, marca, acessibilidade ou plataforma. Reduced motion altera o movimento, não apaga automaticamente a identidade constelar.

## Semantic-before-code

Quando Semantic Verification for necessária, a ordem é:

```text
intenção
→ routing/adoption
→ semantic contract
→ semantic assurance quando domain/formal
→ verification plan
→ pre-implementation gate verde
→ implementação
```

Criar a spec depois que o código já existe é recuperação de processo, não conformidade com o fluxo normal.

## Independent Verification

O modo (`baseline`, `independent`, `adversarial`, `release`) deve ser escolhido antes da implementação para que a arquitetura e o Definition of Done já saibam qual evidência será necessária.

O gate não obriga a executar scanners antes do código. Ele obriga a **decidir a matriz** antes do código. Execução ocorre nas fases de verificação/release conforme `core/INDEPENDENT_VERIFICATION.md`.

## Gate `delivery`

Além do pre-implementation, antes de entregar/concluir:

- Semantic Verification `required` exige evidência rastreável atual;
- risco `medium`/`high`/`critical` com Semantic Verification exige `specs/review-evidence.json` atual;
- Independent Verification acima de `baseline` exige `VERIFICATION.md` ou equivalente recuperável;
- UI material exige browser/visual QA proporcional quando a capacidade existir;
- Change Hygiene precisa estar consolidado em código existente;
- documentação arquitetural/estado não pode contradizer o stack/design system atual.

## Recuperação de projetos já iniciados

Se um projeto governado já tiver código e falhar no gate:

1. **não apagar/reconstruir automaticamente** o que funciona;
2. auditar o estado atual;
3. materializar adoção/roteamento faltantes;
4. classificar diferenças entre o que a Factory teria escolhido e o que existe;
5. registrar dívida/desvio real;
6. corrigir no próximo bloco seguro quando necessário;
7. não declarar retrospectivamente que o gate estava verde.

Isso distingue recuperação honesta de “compliance retroativo”.

## Ferramenta executável

Use:

```bash
python scripts/project_adoption_gate.py init --project <repo> ...
python scripts/project_adoption_gate.py check --project <repo> --phase pre-implementation
python scripts/project_adoption_gate.py check --project <repo> --phase delivery
```

`init` preserva conteúdo existente e adiciona/atualiza somente o bloco gerenciado de adoção em `AGENTS.md`/`PROJECT_STATE.md` e os campos de governança em `.app-factory.json`.

`check` é somente leitura.

## Regra para agentes

Quando o gate for aplicável, o agente deve executá-lo **antes da primeira alteração funcional/visual**. Não pedir ao usuário para preencher campos técnicos que a Factory consegue classificar sozinha.

Se o ambiente não puder executar o script, aplique o mesmo checklist manualmente e registre os mesmos campos no repositório antes da implementação.
