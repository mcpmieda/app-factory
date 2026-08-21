# Selective ReUI recipe

This recipe records a justified decision to evaluate a ReUI component. It intentionally installs no component or dependency by itself.

## Apply safely

1. Name the concrete advanced interaction that shadcn composition does not cover efficiently, such as a data grid with column filtering/visibility, Kanban or calendar.
2. Install only that component from the official ReUI registry.
3. Inspect every generated file and dependency.
4. Remove drag-and-drop, virtualization, Base UI or other modules that the selected component does not use.
5. Keep shadcn as the design-system foundation.
6. Run format, lint, typecheck, tests, build and browser checks after installation.

If the requirement is only a modest searchable table, do not install ReUI; native responsive table/card composition is simpler.
