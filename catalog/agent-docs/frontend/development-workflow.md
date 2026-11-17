---
title: Frontend Development Workflow
description: Dev server, build, testing and debugging workflow for the generated React frontend, including .default scaffolds and destructive prune warnings.
aliases: [frontend dev server, pnpm dev setup, frontend build steps, customize generated React, prune deletes custom files, frontend lint and type check]
keywords: [pnpm run dev, pnpm run build, VITE_API_DEFAULT_BASE_URL, vite.config.ts, src/custom, .default, .generator-ignore, prune, git clean, mvn clean install, git stash -u, Pandino]
tags: [domain:frontend, layer:frontend, status:platform]
---

# Development Workflow

## ⚠️ CRITICAL: Generated Files and `.default` Scaffolds

Generated files outside `src/custom/` are overwritten on every build, and the checksum check fails the build when you edited one.

**Rules for Generated Code:**
- ❌ **DO NOT** edit any files in `.generated-files/` directories
- ❌ **DO NOT** edit the `.default` scaffold in place; it is regenerated on every build and your edit is lost
- ❌ **DO NOT** modify generated React components directly
- ✅ **DO** use Pandino hooks to customize generated components
- ✅ **DO** create custom components that wrap generated ones
- ✅ **DO** use the documented extension points (see [Hooks](./hooks/README.md))

**What `.default` files are:**
- Hook registration scaffolds under `src/custom/hooks/...` (for example `src/custom/hooks/pages/register<Page>ActionsHook.ts.default`), generated only when the matching hook flag is set in the model
- To use one, **copy it to the same name without `.default`** and implement it; the copy lives in the gitignored `src/custom/` folder and is not touched by regeneration (no `.generator-ignore` entry needed)
- `src/custom/application-customizer.tsx` is a plain generated file (no `.default`), and so are the theme files in `src/theme/`

---

## ⚠️ CRITICAL: `./judo.sh prune -f` Deletes Uncommitted Frontend Customizations

`./judo.sh prune -f` runs `git clean` against `application/frontend-react/` and **permanently deletes every file that is not tracked by git** in that subtree. There is no undo.

This is the exact directory where your custom code lives: Pandino hooks, theme overrides, custom components, and i18n overrides (e.g. under `frontend-react/<app>/src/custom/**`, `.../theme/**`, `.../i18n/**`). If any of those files are new and not yet committed, `prune -f` will erase them.

**Before running `./judo.sh prune -f` (or `prune -y`):**

1. `git status` — verify every custom hook/theme/i18n/component file is either committed or staged, or deliberately disposable.
2. `git stash -u` to snapshot untracked work you want to keep.
3. Never run `./judo.sh prune -y` (auto-confirm) in an agent workflow without a verified clean working tree — treat it as equivalent to `rm -rf` on customer code.
4. Do not use `./judo.sh clean` as a gentler alternative: it stops and removes the postgres and keycloak Docker instances, removes the postgres data and DB volumes and deletes the Karaf runtime directory. To discard generated frontend output without touching your data, regenerate with `./judo.sh build -i` (ignore checksums).

See [Prune (Destructive)](../deployment/build-process.md) for the full reference.

---

## ⚠️ CRITICAL: `./judo.sh prune -f` Deletes Uncommitted Frontend Customizations

`./judo.sh prune -f` runs `git clean` against `application/frontend-react/` and **permanently deletes every file that is not tracked by git** in that subtree. There is no undo.

This is the exact directory where your custom code lives: Pandino hooks, theme overrides, custom components, and i18n overrides (e.g. under `frontend-react/<app>/src/custom/**`, `.../theme/**`, `.../i18n/**`). If any of those files are new and not yet committed, `prune -f` will erase them.

**Before running `./judo.sh prune -f` (or `prune -y`):**

1. `git status` — verify every custom hook/theme/i18n/component file is either committed or staged, or deliberately disposable.
2. `git stash -u` to snapshot untracked work you want to keep.
3. Never run `./judo.sh prune -y` (auto-confirm) in an agent workflow without a verified clean working tree — treat it as equivalent to `rm -rf` on customer code.
4. Do not use `./judo.sh clean` as a gentler alternative: it stops and removes the postgres and keycloak Docker instances, removes the postgres data and DB volumes and deletes the Karaf runtime directory. To discard generated frontend output without touching your data, regenerate with `./judo.sh build -i` (ignore checksums).

See Prune (Destructive) (see `judo-deployment-docs` skill) for the full reference.

---

## Local Development Setup

### Correct Directory for pnpm Commands

**Important**: Commands must be run from the correct frontend module directory:

```bash
cd application/frontend-react/<app>__[actor_fqn]
```

Replace `<app>__[actor_fqn]` with your actual module name (e.g., `<app>__service__admin`).

### Starting Development Server

```bash
# 1. Full build from root (generates all code)
# Navigate to the project's root directory first
mvn clean install

# 2. Navigate to frontend module
cd application/frontend-react/<app>__[actor_fqn]

# 3. Install dependencies
pnpm install

# 4. Set API endpoint
export VITE_API_DEFAULT_BASE_URL=http://localhost:8181

# 5. Start development server
pnpm run dev

# Frontend available at: http://localhost:3000
# Backend API at: http://localhost:8181
```

### Hot Module Replacement (HMR)

Vite provides instant hot module replacement:
- Edit files in `src/custom/`
- Changes reflect immediately in browser
- No rebuild needed
- React state is preserved when possible

**What triggers HMR:**
- Changes to `.tsx` and `.ts` files
- CSS/style changes
- Custom hook modifications
- Component updates

**What requires full reload:**
- Changes to `vite.config.ts`
- Changes to environment variables
- Package.json modifications
- New dependencies added

## Build Process

### Development Build

```bash
cd application/frontend-react/<app>__[actor_fqn]

# Build only (no code generation)
pnpm run build

# Output: dist/ directory with optimized bundles
```

### Full Build with Code Generation

```bash
# From project root
# Navigate to the project's root directory first

# Full build (generates code + builds frontend)
mvn clean install

# Auto-deploys to Karaf if server running
```

`./judo.sh generate` does not regenerate frontend sources. Frontend files (including a generated component restored by reverting a `.generator-ignore` entry or an edit) are regenerated by the frontend build: `./judo.sh build -f -i` (`-f` builds the frontend, `-i` ignores checksum errors and updates checksums).

### Production Build

```bash
# From frontend module
cd application/frontend-react/<app>__[actor_fqn]

# Production build
pnpm run build

# Creates optimized bundle in dist/
# Assets are hashed for cache busting
# Code is minified and tree-shaken
```

### Build Output

**Frontend JAR Location:**
```
application/frontend-react/<app>__[actor_fqn]/target/<app>__[actor_fqn]-*.jar
```

**What's included in JAR:**
- Compiled React bundles
- Static assets (images, fonts)
- Internationalization files
- Manifest.json
- Index.html

### Auto-Deploy to Karaf

When Karaf server is running, builds automatically deploy:

```bash
# Check Karaf status
./judo.sh status

# If running, JAR deploys automatically after build
# Monitor deployment:
tail -f application/.karaf/data/log/karaf.log
```

## Testing

### Linting and Code Quality

**ESLint** - Enforces code quality rules:
```bash
cd application/frontend-react/<app>__[actor_fqn]

# Check for lint errors
pnpm run lint

# Auto-fix lint issues
pnpm run lint:fix
```

**Configuration:** `.eslintrc.json`

### Code Formatting

**Prettier** - Ensures consistent code formatting:
```bash
cd application/frontend-react/<app>__[actor_fqn]

# Format code
pnpm run format

# Check formatting without changes
pnpm run format:check
```

**Configuration:** `.prettierrc`

### TypeScript Type Checking

```bash
cd application/frontend-react/<app>__[actor_fqn]

# Run type checker
pnpm run type-check

# Or use watch mode
pnpm run type-check:watch
```

**Configuration:** `tsconfig.json`

### Pre-Commit Checklist

Before committing code:

```bash
cd application/frontend-react/<app>__[actor_fqn]

# 1. Run linter
pnpm run lint

# 2. Format code
pnpm run format

# 3. Type check
pnpm run type-check

# 4. Build to verify no errors
pnpm run build
```

## Debugging

### Browser DevTools

**React Developer Tools:**
- Install React DevTools browser extension
- Inspect component hierarchy
- View props and state
- Profile component performance

**Network Tab:**
- Monitor API calls
- Check request/response payloads
- Verify headers and status codes
- Debug authentication issues

**Console:**
- View error messages
- Check log output
- Debug JavaScript issues
- Inspect variables

### Vite Debug Mode

```bash
cd application/frontend-react/<app>__[actor_fqn]

# Start dev server with debugging
pnpm run dev --debug

# Shows detailed build information
# Logs module resolution
# Displays HMR updates
```

### Source Maps

Development builds include source maps:
- Original TypeScript source in DevTools
- Set breakpoints in original code
- Step through TypeScript line by line

**Enable in DevTools:**
1. Open DevTools
2. Go to Sources tab
3. Navigate to `webpack://` or `vite://`
4. Find your source files in `src/custom/`

### Common Debugging Scenarios

**Hook not firing:**
```typescript
// Add console logs to verify execution
export const myHook: TableRowHighlightingHook = () => {
  console.log('Hook registered');

  return () => {
    console.log('Hook executing');
    return [...];
  };
};
```

**API call failing:**
```typescript
// Check network tab
// Verify VITE_API_DEFAULT_BASE_URL is set
console.log('API URL:', import.meta.env.VITE_API_DEFAULT_BASE_URL);
```

**Component not rendering:**
```typescript
// Add logging to component lifecycle
export const MyComponent: FC = () => {
  console.log('Component rendering');

  useEffect(() => {
    console.log('Component mounted');
  }, []);

  return <div>Content</div>;
};
```

## Environment Configuration

### Environment Variables

**Available Variables:**
- `VITE_API_DEFAULT_BASE_URL` - Backend API URL (required)
- Custom variables must start with `VITE_`

**Setting Variables:**

**Development (Linux/Mac):**
```bash
export VITE_API_DEFAULT_BASE_URL=http://localhost:8181
pnpm run dev
```

**Development (Windows):**
```cmd
set VITE_API_DEFAULT_BASE_URL=http://localhost:8181
pnpm run dev
```

**Using .env file:**
```bash
# Create .env.local (not committed to git)
echo "VITE_API_DEFAULT_BASE_URL=http://localhost:8181" > .env.local

# Start dev server (reads .env.local automatically)
pnpm run dev
```

**Accessing in Code:**
```typescript
const apiUrl = import.meta.env.VITE_API_DEFAULT_BASE_URL;
console.log('API URL:', apiUrl);
```

### Build Configuration

**Vite Configuration:** `vite.config.ts`

Common customizations:
- Build output directory
- Port configuration
- Proxy settings
- Plugin configuration

**Example Proxy Setup:**
```typescript
// vite.config.ts
export default defineConfig({
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8181',
        changeOrigin: true,
      }
    }
  }
});
```

## Common Development Tasks

### Accessing Generated Services

```typescript
import { AddressServiceImpl } from '~/services/data-axios/AddressServiceImpl';
import { judoAxiosProvider } from '~/services/data-axios/JudoAxiosProvider';

const addressServiceImpl = new AddressServiceImpl(judoAxiosProvider);

const fetchAddresses = async () => {
  const addresses = await addressServiceImpl.listAddresses({
    page: 0,
    size: 20,
  });
  return addresses;
};
```

### Adding Custom Components

```bash
# Create custom component
mkdir -p src/custom/components
cat > src/custom/components/MyComponent.tsx << 'EOF'
import { FC } from 'react';
import { Card, CardContent, Typography } from '@mui/material';

export const MyComponent: FC = () => {
  return (
    <Card>
      <CardContent>
        <Typography>Custom Component</Typography>
      </CardContent>
    </Card>
  );
};
EOF

# Protect from regeneration
# No .generator-ignore entry needed — MyComponent.tsx is a brand-new hand-written
# component (case 3); the generator never emits this path. See frontend
# README.md → Understanding .generator-ignore.
```

### Testing After Regeneration

```bash
# 1. Regenerate code
# Navigate to the project's root directory first
mvn clean install

# 2. Verify customizations not overwritten
cd application/frontend-react/<app>__[actor_fqn]
git diff src/custom/

# 3. Reinstall dependencies if needed
pnpm install

# 4. Start dev server
pnpm run dev

# 5. Test functionality
# - Navigate to customized pages
# - Verify hooks executing
# - Check custom components rendering
```

## Troubleshooting

### "Vite dev server won't start"

**Check API URL:**
```bash
echo $VITE_API_DEFAULT_BASE_URL
# Should output: http://localhost:8181
```

**Verify port availability:**
```bash
# Check if port 3000 is in use
lsof -i :3000

# Kill process if needed
kill -9 <PID>
```

**Delete node_modules and reinstall:**
```bash
cd application/frontend-react/<app>__[actor_fqn]
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

### "Changes not deploying to Karaf"

**Check JAR built successfully:**
```bash
ls -lh target/*.jar
# Should show recent JAR file
```

**Verify Karaf is running:**
```bash
./judo.sh status
```

**Check Karaf logs:**
```bash
tail -f application/.karaf/data/log/karaf.log
# Look for deployment messages
```

**Force redeploy:**
```bash
# Stop Karaf
./judo.sh stop

# Rebuild
mvn clean install

# Start Karaf
./judo.sh start
```

### "Type errors after regeneration"

**Update type definitions:**
```bash
cd application/frontend-react/<app>__[actor_fqn]
pnpm install
```

**Check for breaking changes:**
```bash
# Review generated type definitions
grep -r "export interface" src/services/data-api/model/
```

**Clear TypeScript cache:**
```bash
# Delete TypeScript build info
rm -rf node_modules/.cache
pnpm run type-check
```

### "Build fails with checksum mismatch"

See [README](./README.md) for detailed checksum error handling.

## Performance Tips

### Development Server

**Optimize HMR:**
- Keep `src/custom/` files small and focused
- Avoid circular dependencies
- Use lazy loading for large components

**Reduce bundle size:**
- Import only what you need from Material-UI
  ```typescript
  // Good
  import { Button } from '@mui/material';

  // Bad (imports entire library)
  import * as mui from '@mui/material';
  ```

### Production Build

**Analyze bundle size:**
```bash
# Build with bundle analyzer
pnpm run build -- --analyze

# Opens visualization of bundle contents
```

**Optimization strategies:**
- Code splitting (automatic with Vite)
- Tree shaking (remove unused code)
- Lazy loading routes
- Optimize images

## Related Documentation

- [Main README](./README.md) - Overview and architecture
- [Theming](./theming.md) - Customize appearance
- [Internationalization](./i18n.md) - Translations
- [Hook System](./hooks/README.md) - Customization hooks
- [Build and Deployment](./build-and-deployment.md) - Maven build modes, base href, MUI license
- [Error Handling](./error-handling.md) - HTTP error handling in the generated frontend
