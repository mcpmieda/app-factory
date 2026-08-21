# Architecture

Astro pre-renders two routes because content is public, changes infrequently and is equal for every visitor. `BaseLayout` owns semantic shell and metadata; pages own content; one global stylesheet owns the local visual language and native CSS motion. There is no client framework or runtime API. Playwright serves the production build and checks desktop, mobile and reduced-motion contexts.

Decision: Astro was selected from its official content/static path; Next.js and the `web-admin` starter would add runtime and patterns this product does not need.
