# Frontend

React + Vite frontend for 智创Agent.

## Local Development

```bash
cd frontend
npm install
npm run dev
```

## Pages

- Student dashboard
- Assignment analysis overview
- Teacher dashboard
- Knowledge base admin

## Module Boundaries

- `src/app`: app shell, routing and providers
- `src/pages`: page-level screens
- `src/features`: business feature modules
- `src/shared/api`: API clients
- `src/shared/components`: reusable components
- `src/shared/types`: shared TypeScript types

The Web frontend is the primary client for the MVP. HarmonyOS is planned as a P1
ArkTS + ArkUI client that reuses backend APIs.
