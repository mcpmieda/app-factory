# Product

## Outcome

Define the user, problem and first complete administrative flow for **Web Admin Starter**.

## Experience

- visual system: shadcn/ui baseline unless product requirements override it;
- advanced admin UI: ReUI only when a concrete component justifies it;
- Professional UI Profile: `professional-default`;
- default admin density/surface/emphasis: `comfortable + layered + balanced`, adjustable to the real task;
- Motion Profile: `ambient` contextual by default;
- dense data/reading views: attenuate motion to `subtle`;
- reduced motion: mandatory for non-essential movement.

`professional-default` is a quality bar, not a package. Reach it with the current design system before considering another library. Preserve hierarchy, spacing rhythm, typography, semantic color, complete states, responsive behavior and accessibility. Use progressive disclosure rather than showing every option at once.

For medium/large UI, identify the needed archetypes before implementation: shell, page header, stats, search/command, filters, data view, form, detail/inspector and feedback states. Calendar, Kanban, chart or other advanced patterns enter only when the product needs them.

Use motion to communicate interaction, data changes, state, attention and navigation. Ambient effects are appropriate for login, waiting, empty states, headers and spacious surfaces when they do not compete with the task.

## First slice

Record the primary entity, required fields, list/search/create/edit behavior and observable success criteria before implementation.

## Non-goals

- optional infrastructure without a product requirement;
- real user data or production credentials in examples;
- multiple design systems;
- copying proprietary commercial templates/assets without an applicable project license;
- continuous decorative animation in dense administrative screens.
