# development-workflow.md — index

Pull-only condensed map. Source: catalog/agent-docs/frontend/development-workflow.md.

## ⚠️ CRITICAL: Generated Files and `.default` Scaffolds
- Generated files outside `src/custom/` are overwritten each build; checksum check fails the build if edited.
- DO NOT edit `.generated-files/` dirs, the `.default` scaffold in place, or generated React components.
- DO use Pandino hooks (`hooks/README.md`), custom components wrapping generated ones, documented extension points.
- `.default` files: hook scaffolds under `src/custom/hooks/...` (e.g. `src/custom/hooks/pages/register<Page>ActionsHook.ts.default`), generated only when the matching model hook flag is set.
- To use one: copy without `.default` suffix and implement. Copy lives in gitignored `src/custom/`; no `.generator-ignore` entry needed.
- `src/custom/application-customizer.tsx` and `src/theme/*` are plain generated files (no `.default`).

## ⚠️ CRITICAL: `./judo.sh prune -f` Deletes Uncommitted Frontend Customizations
- `prune -f` runs `git clean` on `application/frontend-react/`; deletes every untracked file there. No undo.
- Covers `frontend-react/<app>/src/custom/**`, `.../theme/**`, `.../i18n/**`.
- Before `prune -f` / `prune -y`: `git status`; `git stash -u` to snapshot untracked work.
- Never `prune -y` in an agent workflow without a verified clean tree (≈ `rm -rf`).
- `./judo.sh clean` is not gentler: removes postgres and keycloak Docker instances, DB volumes and Karaf runtime dir. To discard generated frontend output safely: `./judo.sh build -i`.
- Reference: `../deployment/build-process.md` (Prune).

## ⚠️ CRITICAL: `./judo.sh prune -f` Deletes Uncommitted Frontend Customizations
- Source repeats the section above verbatim (duplicate `##`); same rules apply. Reference: "Prune (Destructive)" via `judo-deployment-docs` skill.

## Local Development Setup
- pnpm commands run from `application/frontend-react/<app>__[actor_fqn]` (e.g. `<app>__service__admin`).
- Steps: `mvn clean install` at project root → `cd` into frontend module → `pnpm install` → `export VITE_API_DEFAULT_BASE_URL=http://localhost:8181` → `pnpm run dev`.
- Frontend at `http://localhost:3000`; backend API `http://localhost:8181`.
- HMR: edits in `src/custom/` (`.tsx`, `.ts`, CSS, hooks, components) reflect immediately; state preserved when possible.
- Full reload needed for: `vite.config.ts`, env vars, `package.json`, new dependencies.

## Build Process
- Dev build: `pnpm run build` in module (no codegen) → `dist/`.
- Full build with codegen: `mvn clean install` at root; auto-deploys to Karaf if running.
- `./judo.sh generate` does NOT regenerate frontend sources. Use `./judo.sh build -f -i` (`-f` frontend, `-i` ignore checksum errors and update checksums). Applies after reverting a `.generator-ignore` entry or an edit.
- Production build: `pnpm run build`; hashed assets; minified, tree-shaken.
- Frontend JAR: `application/frontend-react/<app>__[actor_fqn]/target/<app>__[actor_fqn]-*.jar` — contains bundles, static assets, i18n files, manifest.json, index.html.
- Auto-deploy: if Karaf running (`./judo.sh status`), JAR deploys after build; watch `application/.karaf/data/log/karaf.log`.

## Testing
- ESLint: `pnpm run lint`, `pnpm run lint:fix`; config `.eslintrc.json`.
- Prettier: `pnpm run format`, `pnpm run format:check`; config `.prettierrc`.
- TypeScript: `pnpm run type-check`, `pnpm run type-check:watch`; config `tsconfig.json`.
- Pre-commit order: `lint` → `format` → `type-check` → `build`.

## Debugging
- Browser: React DevTools (props, state, profiling); Network tab (API calls, status, auth); Console.
- `pnpm run dev --debug`: build info, module resolution, HMR updates.
- Source maps in dev builds: DevTools Sources → `webpack://` or `vite://` → `src/custom/`.
- Scenarios: hook not firing (log in hook factory and returned fn); API failing (check `VITE_API_DEFAULT_BASE_URL` via `import.meta.env`); component not rendering (log render/mount).

## Environment Configuration
- Variables: `VITE_API_DEFAULT_BASE_URL` (backend URL, required). Custom vars must start with `VITE_`.
- Set via `export` (Linux/Mac), `set` (Windows cmd), or `.env.local` (not committed; read by dev server).
- Access in code: `import.meta.env.VITE_API_DEFAULT_BASE_URL`.
- `vite.config.ts`: build output dir, port, proxy, plugins. Example proxy `/api` → `http://localhost:8181`, port 3000.

## Common Development Tasks
- Generated services: import `AddressServiceImpl` from `~/services/data-axios/AddressServiceImpl` and `judoAxiosProvider` from `~/services/data-axios/JudoAxiosProvider`; `new AddressServiceImpl(judoAxiosProvider)`; e.g. `listAddresses({page, size})`.
- Custom components: create under `src/custom/components/`. Brand-new hand-written component needs no `.generator-ignore` entry (generator never emits that path); see frontend README "Understanding .generator-ignore".
- Test after regeneration: `mvn clean install`; `git diff src/custom/`; `pnpm install` if needed; `pnpm run dev`; check customized pages, hooks, components.

## Troubleshooting
- Vite won't start: check `echo $VITE_API_DEFAULT_BASE_URL`; port 3000 in use (`lsof -i :3000`); reinstall with `rm -rf node_modules pnpm-lock.yaml && pnpm install`.
- Changes not deploying to Karaf: JAR built (`ls target/*.jar`); `./judo.sh status`; karaf.log; force redeploy: `./judo.sh stop` → `mvn clean install` → `./judo.sh start`.
- Type errors after regeneration: `pnpm install`; review `src/services/data-api/model/`; clear `node_modules/.cache` then `pnpm run type-check`.
- Checksum mismatch build failure: see frontend `README.md`.

## Performance Tips
- Dev: keep `src/custom/` files small; avoid circular deps; lazy-load large components.
- Import only needed MUI symbols (`import { Button } from '@mui/material'`, not `import * as mui`).
- Production: bundle analysis `pnpm run build -- --analyze`; code splitting, tree shaking, lazy routes, image optimization.

## Related Documentation
- `README.md` (overview), `theming.md`, `i18n.md`, `hooks/README.md`, `build-and-deployment.md` (Maven modes, base href, MUI license), `error-handling.md` (HTTP errors in generated frontend).
