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

## Gates e recovery

Validar manifest, typecheck/test/build/audit, estrutura do ZIP, carga real, ação/reversão e console. Mudança de host/API exige security/privacy/store review e rollback de versão. Living UI só se houver UI; usar feedback curto e reduced motion, nunca instalar design system por isso.

Evidence: `examples/chrome-extension-pilot/` and `research/V0.9_UNIVERSAL_VALIDATION.md`.
