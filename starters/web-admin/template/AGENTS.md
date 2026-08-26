# AGENTS.md — Web Admin Starter

This project follows **App Factory** (`mcpmieda/app-factory`) and uses the validated `web-admin` profile.

## Start here

1. Invoke/use `factory-router` for software-development work when the App Factory plugin is available.
2. Before material feature/UI implementation, read `core/PROJECT_ADOPTION_GATE.md`, load `project-adoption`, upgrade/materialize `.app-factory.json` routing metadata and require the `pre-implementation` gate to pass. Starter generation is scaffolding, not proof that routing/semantic/system decisions are complete.
3. Read `PROJECT_STATE.md` before changing the project.
4. Read `PRODUCT.md` and `ARCHITECTURE.md` for product or structural changes.
5. Activate optional recipes only when the product requires them.
6. Preserve shadcn/ui as the visual foundation unless the product explicitly adopts HeroUI as the transversal design system; use ReUI only for a justified advanced component in the shadcn variant.
7. React + CSS/custom/native UI is not an implicit fallback design system. If it must become the visual foundation, record a concrete `ui.deviation` in `.app-factory.json` before implementation.
8. For UI work, follow `ui/UI_POLICY.md`, `ui/PROFESSIONAL_UI_PROFILE.md` and `ui/MOTION_POLICY.md` from App Factory. Default quality bar is `professional-default`; default Motion Profile is `ambient` contextual; attenuate dense admin views and respect `prefers-reduced-motion`.
9. If HeroUI becomes the primary design system, use it transversally and consult `ui/heroui/README.md`; do not infer any mandatory environmental effect from the design-system choice.
10. `professional-default` does not authorize adding another design system merely for appearance.
11. Before building medium/large UI, inventory needed archetypes (shell, header, stats, search/command, filters, data view, form, detail, feedback) and reuse the current registry/design system first.
12. Do not add another design system or motion library only to obtain an effect when the current stack/CSS can provide it cleanly.
13. When Semantic Verification is required, materialize the contract/assurance/verification plan required by the selected depth before product code.
14. For critical persistent operations, apply `core/SYSTEM_ENGINEERING.md`: after server acceptance, closing the browser or losing the client must not destroy the only progress record when that could cause partial effects, duplication, inconsistency or lost progress.
15. Verify visual hierarchy, loading/empty/error states, desktop/mobile, keyboard/focus, format, lint, typecheck, tests, build, critical browser behavior and relevant motion/reduced-motion behavior before completion.
16. Before delivery, run the Project Adoption Gate in `delivery` phase or prove the equivalent checklist.

## Factory fallback

If the plugin is unavailable, consult `mcpmieda/app-factory` starting at `AGENTS.md`, `core/ENTRYPOINT.md`, `core/PROJECT_ADOPTION_GATE.md`, `core/SYSTEM_ENGINEERING.md`, `profiles/web-admin/PROFILE.md`, `ui/UI_POLICY.md`, `ui/PROFESSIONAL_UI_PROFILE.md` and `ui/MOTION_POLICY.md`.

<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->
