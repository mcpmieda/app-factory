# Project Profiles

Profiles convert validated evidence into conditional defaults for recurring classes of software.

A profile is not a universal stack. It is a tested starting point the Factory may select automatically after understanding the product.

## Selection rule

1. understand the problem first;
2. choose a profile only when the product clearly fits;
3. apply profile defaults conditionally;
4. local project requirements override generic profile defaults;
5. avoid installing optional modules without a demonstrated need.

## Validated profiles

### `web-admin`

Use for administrative systems, CRUDs, dashboards, internal tools and data-oriented management applications.

See `profiles/web-admin/PROFILE.md`.

### `website`, `web-app`, `chrome-extension`, `automation`

Validated by one complete V0.9 pilot each. They provide conditional contracts and gates, not frozen universal stacks. See each profile directory.

## Planned profiles

- API/backend;
- mobile/desktop when evidence is available.

A planned profile must not be treated as validated until it passes a real pilot and review gates comparable to its risk.
