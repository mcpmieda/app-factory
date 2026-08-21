# Architecture

An official Vite vanilla-TypeScript scaffold bundles one isolated-world content script as an IIFE. MV3 declaratively injects it only on the local test host. Native DOM APIs are sufficient; popup, service worker, storage and named permissions would add attack surface without value. Styles and handlers are created by bundled JavaScript, with no inline script, `eval`, remote code or relaxed CSP.

Vitest proves reversible DOM behavior. Playwright follows its official extension path: build the unpacked extension, launch bundled Chromium with a persistent context, visit the controlled HTTP fixture and exercise the injected control. `archiver` creates the validation ZIP from `dist/` so the manifest remains at archive root.
