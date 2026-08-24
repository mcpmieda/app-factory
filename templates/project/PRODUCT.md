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
- Ambient Surface Profile: [não aplicável / `ambient-constellation`]:
- Constellation Intensity: [`strong` quando explicitamente solicitada ou quando HeroUI for linguagem principal / não aplicável]:
- dense content strategy: [quando constelação ativa: superfícies limpas + assinatura no shell/header/perímetro]:
- reduced motion: [quando constelação ativa: fallback constelar estático]:
- exceções relevantes de leitura, densidade, acessibilidade ou desempenho:

`professional-default` é um quality bar, não uma biblioteca. Para admin/dashboard/CRUD, shadcn continua base preferencial e ReUI continua complemento seletivo quando não houver escolha explícita de HeroUI. HeroUI continua alternativa principal e, quando escolhido como **linguagem principal do sistema**, herda `ambient-constellation` com intensidade `strong` por padrão. Seguir `ui/UI_POLICY.md`, `ui/PROFESSIONAL_UI_PROFILE.md`, `ui/MOTION_POLICY.md` e `ui/AMBIENT_CONSTELLATION_PROFILE.md` quando aplicável.

Pedidos como `ambient constellation`, `ambient constellarion`, `ambiente de constelação` ou equivalente ativam o perfil automaticamente. Não obrigar o usuário a escolher detalhes técnicos de radius, shadow, spacing, density, partículas ou animação.

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
