# PRODUCT — Template

## Problema
[Qual problema real será resolvido?]

## Usuários
- usuário principal:
- outros perfis:

## Resultado esperado
[O que deve ficar mais simples, rápido, seguro ou possível?]

## Experiência visual
- design system/preferência visual:
- Professional UI Profile: `professional-default` por padrão para UI material, ou exceção justificada:
- density: `compact` / `comfortable` / `spacious` quando relevante:
- surface/emphasis quando relevante:
- Motion Profile: `ambient` por padrão, salvo decisão explícita (`none`, `subtle`, `ambient`, `expressive`):
- exceções relevantes de leitura, densidade, acessibilidade ou desempenho:

`professional-default` é um quality bar, não uma biblioteca. Para admin/dashboard/CRUD, shadcn continua base preferencial e ReUI continua complemento seletivo quando não houver escolha explícita de HeroUI. HeroUI continua alternativa principal e, quando escolhido como **linguagem principal do sistema**, deve ser usado transversalmente. Seguir `ui/UI_POLICY.md`, `ui/PROFESSIONAL_UI_PROFILE.md` e `ui/MOTION_POLICY.md`.

Nenhum efeito ambiental específico é imposto globalmente pela Factory. Atmosfera, fundos especiais e efeitos decorativos só entram quando fizerem sentido para o produto/projeto.

## Fluxos principais
1. ...
2. ...
3. ...

## Escopo
### Incluído
- ...

### Fora do escopo agora
- ...

## Regras de negócio
- ...

## Restrições
- custo:
- ambiente:
- compatibilidade:
- privacidade/segurança:

## Continuidade operacional, quando aplicável
- quais operações críticas podem ser interrompidas por fechamento do navegador, queda de energia/rede ou troca de dispositivo:
- quais dessas operações precisam continuar, retomar ou reconciliar depois da interrupção:
- qual resultado observável o usuário espera ao voltar:

O produto não precisa escolher tecnologia de fila/checkpoint. Essa decisão é arquitetural e segue `core/SYSTEM_ENGINEERING.md`.

## Critérios de sucesso
Defina resultados observáveis, não apenas tarefas técnicas.

## Blocos funcionais
Organize por capacidades completas, não por botões ou arquivos isolados.

### Bloco 1 — [nome]
- comportamento:
- critério de conclusão:

### Bloco 2 — [nome]
- comportamento:
- critério de conclusão:

## Questões que realmente dependem do usuário
Liste somente decisões de produto, preferência, custo ou regra de negócio ainda não resolvidas.
