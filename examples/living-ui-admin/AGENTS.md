# AGENTS.md — Pulse Desk

This project follows **App Factory** (`mcpmieda/app-factory`) and uses the validated `web-admin` profile.

## Start here

1. Invoke/use `factory-router` for software-development work when the App Factory plugin is available.
2. Read `PROJECT_STATE.md` before changing the project.
3. Read `PRODUCT.md` and `ARCHITECTURE.md` for product or structural changes.
4. Activate optional recipes only when the product requires them.
5. Preserve shadcn/ui as the visual foundation; use ReUI only for a justified advanced component.
6. For UI work, follow `ui/UI_POLICY.md` and `ui/MOTION_POLICY.md` from App Factory. Default Motion Profile is `ambient` contextual; attenuate dense admin views and respect `prefers-reduced-motion`.
7. Do not add another design system or motion library only to obtain an effect when the current stack/CSS can provide it cleanly.
8. Verify format, lint, typecheck, tests, build, critical browser behavior and relevant motion/reduced-motion behavior before completion.

## Factory fallback

If the plugin is unavailable, consult `mcpmieda/app-factory` starting at `AGENTS.md`, `core/ENTRYPOINT.md`, `profiles/web-admin/PROFILE.md`, `ui/UI_POLICY.md` and `ui/MOTION_POLICY.md`.

<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->
