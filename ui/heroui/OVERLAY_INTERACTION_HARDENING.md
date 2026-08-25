# HeroUI — hardening de overlays, navegação e QA de interação

Data da consolidação: **2026-08-25**.

Este contrato complementa o catálogo HeroUI v3 e o `ui-builder`. Ele existe para impedir regressões comuns quando componentes acessíveis de coleção, navegação e overlay são combinados em shells administrativos.

## 1. Semântica antes da aparência

Não usar um componente de **seleção** apenas porque ele se parece com uma lista clicável.

- navegação real deve preservar semântica de navegação (`Link`, `<a href>`, router link ou primitive equivalente);
- ação real deve preservar semântica de ação (`Button`, command/action item ou primitive equivalente);
- `ListBox`, `Select`, `ComboBox` e coleções semelhantes devem continuar sendo usados quando a interação principal for seleção/collection behavior;
- dentro de `Popover`, `Drawer`, `Dropdown` ou outro overlay, não trocar automaticamente links/buttons por itens de seleção se isso mudar propagação de eventos, foco, activation behavior ou fechamento do overlay;
- aparência HeroUI não exige sacrificar a semântica correta: usar Surface/Popover/Drawer e primitives HeroUI ao redor de links/buttons semânticos quando necessário.

### Gate

Se um clique visualmente correto não concluir a navegação/ação com ponteiro real, considerar a composição reprovada mesmo que `element.click()` ou disparo sintético funcione.

## 2. Uma fonte de estado por overlay

Drawer, Popover, Modal e overlays controlados devem possuir **uma única fonte de verdade**.

Evitar combinar, para o mesmo overlay:

- estado interno do trigger;
- `onPress` manual que também abre/fecha;
- `isOpen`/`onOpenChange` externos;
- listeners globais de rota que fecham o overlay em paralelo.

Quando o componente oferecer state object/hook oficial, como `useOverlayState`, preferir um state owner explícito no root e compartilhar apenas as operações necessárias.

### Gate

Abrir → interagir → navegar → fechar deve resultar em um único fluxo de transição, sem dupla atualização, overlay órfão, foco preso ou recuperação concorrente do React.

## 3. Fechar na mesma interação que navega

Quando selecionar um item dentro de Drawer/Popover deve navegar e fechar o overlay:

1. executar o fechamento no mesmo handler da interação do usuário;
2. deixar a navegação semântica ocorrer normalmente;
3. usar listeners globais de rota apenas como fallback quando houver motivo concreto;
4. não depender de `hashchange`, `popstate` ou equivalente como caminho primário de fechamento quando isso puder competir com a renderização da nova rota.

Essa regra reduz atualizações concorrentes e elimina estados intermediários em que a rota já mudou, mas o portal/backdrop continua ativo.

## 4. QA com ponteiro real

Para overlays animados, não assumir que `mounted === hittable`.

O harness deve:

- aguardar o alvo possuir área visível dentro da viewport;
- confirmar hit-testing no ponto de clique (`elementFromPoint()` ou equivalente do harness/browser);
- tolerar somente o tempo normal da animação de entrada/saída;
- disparar eventos de ponteiro/mouse reais pelo navegador quando possível;
- reprovar se o alvo nunca se tornar atingível;
- não substituir isso por `element.click()` como prova de usabilidade.

Essa checagem separa falhas reais de interação de falsos negativos produzidos enquanto Drawer/Popover ainda está entrando na viewport.

## 5. Erros não tratados fazem parte do gate visual

QA de UI deve observar também:

- erros/exceções não tratados da página ou runtime;
- `console.error` relevante ao fluxo;
- root desmontado/recriado inesperadamente;
- overlay/backdrop persistente após navegação;
- foco preso ou portal visualmente órfão.

O mecanismo de captura deve ser compatível com o browser/harness escolhido. Exemplos:

- Playwright: evento `pageerror`/equivalente;
- WebDriver/harness próprio: hook de erro não tratado suportado pelo ambiente;
- Chromium + CDP: `Runtime.exceptionThrown` pode ser usado como adaptador adicional, não como requisito universal.

Uma tela que “parece pronta” depois de o framework se recuperar de uma exceção não passa automaticamente. A causa deve ser isolada e a reprodução repetida após a correção.

## 6. Performance de interação: protocolo antes do threshold

Runners e browsers headless têm jitter. Para transições de rota/overlay:

- definir antes da medição o ambiente, viewport, estado de cache, condição de rede quando relevante, rota inicial e marcas exatas de início/fim;
- preferir SLO/contrato do projeto ou baseline observado no mesmo perfil de execução;
- coletar múltiplas amostras do mesmo fluxo;
- usar mediana como métrica principal de latência sustentada e registrar distribuição suficiente para detectar regressão;
- registrar também maior long task quando o browser fornecer essa métrica e erros não tratados;
- investigar picos isolados somente quando se repetem ou aparecem junto de long task/jank;
- não mascarar regressão real escolhendo apenas a melhor amostra;
- não aplicar números de outro produto/hardware como gate global da Factory.

### Exemplo de perfil, não default universal

Em um shell administrativo **já montado**, com dados locais estáveis, mesma máquina/runner, mesma viewport e clique físico medido de pointer-down até rota selecionada/overlay estabilizado, uma bateria anterior usou:

- três amostras por rota/interação;
- mediana de navegação desktop `<= 350 ms`;
- interação mobile com Drawer/Popover `<= 500 ms`;
- long task máxima `<= 200 ms`.

Esses números são apenas exemplo de um contrato local. Outro projeto deve derivar thresholds de seu SLO ou baseline reproduzível.

## 7. Harness deve modelar a aplicação real

Antes de declarar regressão:

- verificar o tipo real do elemento (`Button` pode navegar via `onPress` sem existir `<a>`);
- não usar classes genéricas compartilhadas entre login e shell autenticado como prova de autorização;
- para portal/overlay, verificar visibilidade dos ancestrais e hit-testing, não apenas a existência do nó;
- quando o teste falhar, capturar screenshot, DOM/estado relevante e erros não tratados antes de alterar a aplicação.

O harness é código de produção de evidência: seletor errado não deve virar “correção” desnecessária no produto.

## 8. Segurança no browser QA

- não criar cookie falso, bypass de identidade, redução de capability ou sessão artificial no domínio oficial;
- QA autenticado automatizado só pode usar fixture local/isolada ou ambiente de teste autorizado e explicitamente separado da produção;
- smoke do domínio oficial sem sessão deve confirmar que APIs protegidas continuam negando acesso e que rotas internas não expõem shell administrativo;
- deployment para validação não equivale a autorização de produção.

## Checklist obrigatório para shell HeroUI com overlays

- [ ] link é link e ação é Button/command apropriado;
- [ ] coleção de seleção não foi usada apenas como substituto visual de navegação;
- [ ] overlay tem uma única fonte de estado;
- [ ] navegação fecha overlay na mesma interação quando aplicável;
- [ ] ponteiro real consegue atingir o alvo após a animação;
- [ ] teclado/foco continuam funcionando;
- [ ] zero erro/exceção não tratado no fluxo aprovado, usando o hook compatível com o browser/harness;
- [ ] `console.error` relevante ao fluxo está zerado;
- [ ] protocolo de performance e thresholds do projeto estão definidos antes de medir;
- [ ] múltiplas amostras foram usadas quando latência é gate;
- [ ] reduced-motion foi verificado;
- [ ] smoke oficial não usa autenticação artificial;
- [ ] falha de harness foi descartada antes de alterar a aplicação.
