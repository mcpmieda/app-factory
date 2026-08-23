# Chrome Extension Profile

Status: `validated`

## Quando usar

Uma capacidade pequena que precisa agir no contexto do navegador/página e cujo valor não cabe melhor em site, app ou bookmarklet controlado.

## Defaults comprovados

- Manifest V3, TypeScript e bundle local CSP-safe;
- superfície mínima: content script ou mecanismo único suficiente;
- ação observável, previsível e reversível;
- teste da extensão unpacked em Chromium com contexto persistente;
- ZIP reproduzível somente como artefato de validação/release.

Vite vanilla é uma opção comprovada; popup/service worker/framework visual não são defaults.

## Condicionais e anti-defaults

Cada API e match pattern precisa de justificativa. Preferir hosts específicos/permissões opcionais quando aplicável. Não usar `<all_urls>`, remote code, secrets, storage, clipboard, tabs ou background por conveniência.

## Independent Verification

Aplique `core/INDEPENDENT_VERIFICATION.md` proporcionalmente sem tratar extensão pequena como sistema web completo.

- extensão simples/baixo risco pode permanecer `baseline`;
- permissões sensíveis, integrações externas, storage compartilhado ou alto impacto podem elevar para `independent`/`adversarial`;
- Trivy/Semgrep são candidatos para supply-chain/SAST;
- StrykerJS pode verificar força de testes de lógica crítica de forma seletiva;
- axe-core/Lighthouse só entram se houver UI web relevante e baseline que justifique;
- ZAP/Schemathesis entram somente se a extensão também consumir/expor uma superfície HTTP/API cuja arquitetura justificar esses gates.

Scanners não substituem teste real da extensão unpacked, revisão de permissões/CSP, store/privacy review ou regressão contra a página-alvo. A política permanece `free-only`.

## Gates e recovery

Validar manifest, typecheck/test/build/audit, estrutura do ZIP, carga real, ação/reversão e console. Mudança de host/API exige security/privacy/store review e rollback de versão. Living UI só se houver UI; usar feedback curto e reduced motion, nunca instalar design system por isso.

Quando Independent Verification selecionar checks `required`, executá-los em CI/runner equivalente e registrar exceções explicitamente. Ferramenta não executada não vira `pass`.

Evidence: `examples/chrome-extension-pilot/` and `research/V0.9_UNIVERSAL_VALIDATION.md`.
