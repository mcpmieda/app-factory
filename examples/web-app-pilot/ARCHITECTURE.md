# Architecture

Vite + React is the smallest official scaffold that fits a stateful end-user interaction and produces static deployable assets. Zod is the single validation contract. State stays local because no component outside the booking journey consumes it; data is static and no persistence is necessary. Vitest/Testing Library test validation and UI recovery; Playwright tests the production build across desktop, mobile and reduced motion.

Anti-default: Next.js, the web-admin starter, dashboard navigation, shadcn/ReUI, database and auth were intentionally excluded. A real booking backend is a separate product decision because it introduces concurrency, authorization and operational risk.
