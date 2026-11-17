# theming.md — index

Pull-only condensed map. Source: catalog/agent-docs/frontend/theming.md.

## Overview

- MUI theming. Two layers:
  1. Actor palette (model-driven): `ActorType` carries 7 colours (`primaryColor`, `secondaryColor`, `backgroundColor`, `paperBackgroundColor`, `textPrimaryColor`, `textSecondaryColor`, `subtitleColor`) plus `applicationLogo`. Generator renders `src/theme/palette.ts`. Rendered at generation time; no runtime brand data.
  2. Component sub-themes: a `subTheme` name on a UI widget selects a `SubThemeHook` service that returns partial MUI overrides, applied via nested `ThemeProvider`.
- Brand palette: edit `ActorType` in the ESM model, NOT `palette.ts`. Editing `palette.ts` needs a `.generator-ignore` entry and loses cross-actor consistency.
- Logo is a plain `<img>` limited to 100% `maxHeight`/`maxWidth`; give SVG logos explicit `width` and `height`.
- Logo image, icon, subtitle overridable in code via `CustomLogoPropsHook` (see ui-hooks).
- Authoring: `judo-model-cli` skill, `ui-mutations.md` → "Visual Language → Theming & colors" and Recipes 18 (sub-theme card colours) and 19 (row highlighting).

## Color Palette

- File `src/theme/palette.ts`. Exports `paletteThemeLight` and `paletteThemeDark` (`createTheme`).
- Light: `mode: 'light'`; primary/secondary with main/light/dark/contrastText; error, warning, info, success main; background default/paper; text primary/secondary/disabled.
- Dark: `mode: 'dark'`; background `#121212`/`#1e1e1e`; light-tinted primary and secondary.

## Customizing Theme

- Prefer model (ActorType colours); regenerating updates palette.
- Hand-edit `palette.ts`: 1) edit in `application/frontend-react/<app>__[actor_fqn]`; 2) `echo "src/theme/palette.ts" >> .generator-ignore`; 3) change `primary.main` / `secondary.main` in `createTheme`; 4) `pnpm run dev` (HMR).

## Advanced Theme Customization

- Typography: `fontFamily` (array joined by `,`), `h1`/`h2` size and weight, `button.textTransform: 'none'`.
- Component overrides: `components.MuiButton` (`styleOverrides` root/contained, `defaultProps.disableElevation`), `MuiCard` (`borderRadius`, `boxShadow`), `MuiTextField` (`defaultProps.variant: 'outlined'`).
- Spacing: `spacing: 8` (default 8px unit). Breakpoints `values`: xs 0, sm 600, md 960, lg 1280, xl 1920.

## Theme Override Fragments

- Generated `src/theme/index.tsx` is assembled from fragments. Override by same-named file in `actor/src/theme/` override dir (see `./README.md#template-override-process`).
- `index.ts.mui-<component>.fragment.hbs` for: app-bar, autocomplete, avatar, button, card, chip, data-grid, data-grid-pro, dialog, divider, drawer, form-control, icon, input-base, list, paper, radio, select, stack, tab, text-field, tooltip.
- `index.ts.extra-components.fragment.hbs`, `index.ts.theme-options.fragment.hbs`.
- `palette.ts.extra-imports.fragment.hbs`, `palette.ts.extra-attributes.fragment.hbs`, `palette.ts.extra-palette-attributes.fragment.hbs`.
- Prefer a fragment over `.generator-ignore` of `index.tsx` when changing one component.

## Sub-Themes for Components

- Widgets with a `subTheme` name are wrapped in `SubThemeWrapper`. It looks up a Pandino service under `SUB_THEME_HOOK_INTERFACE_KEY` (value `'SubThemeHook'`) with matching `name` property, calls it with parent theme, deep-merges result into that subtree.
- Generator emits scaffold per sub-theme: `src/custom/hooks/sub-themes/register<Name>SubThemeHook.tsx.default`. Remove `.default`; call register fn from `application-customizer.tsx`.
- Registration: `context.registerService<SubThemeHook>(SUB_THEME_HOOK_INTERFACE_KEY, fn, { name: '<toSafeCamelCase of model sub-theme name>' })`.
- Function signature `(parentTheme: Theme, data?: any)`; `data` is the wrapped widget's data (e.g. status colour).
- Example: `MuiPaper` root `background: alpha(parentTheme.palette.secondary.main, 0.97)`.
- Use cases: highlight dashboard card or status field; different palette or table style (`MuiDataGrid` `styleOverrides`) for admin sections.

## CSS-in-JS Styling

- Emotion. Use `sx` prop or `styled(Component)(({ theme }) => ...)`. `useTheme()` for theme values in code.
- `sx` palette refs: `'primary.main'`, `'primary.contrastText'`, `'primary.dark'`; `padding: 2`, `borderRadius: 1`, `'&:hover'`.

## Responsive Styling

- `sx` breakpoint objects: `width: { xs, sm, md, lg, xl }`, `padding: { xs, sm, md }`, `display: { xs: 'block', md: 'flex' }`.
- `useMediaQuery(theme.breakpoints.down('sm'))`; `theme.breakpoints.between('sm', 'md')`.

## Dark Mode Toggle

- Example `ThemeToggle` (`src/custom/components/ThemeToggle.tsx`) with `useState`; the toggle does not actually switch the theme; the source leaves switching logic as a comment.
- Source's "Register in AppBar" example uses an `appBarComponents` field on `applicationCustomizer`. This conflicts with the Pandino service registration in ui-hooks (`CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY`); verify before use.

## Custom Fonts

- Put font files in `public/fonts/` (e.g. `CustomFont.woff2`).
- `src/theme/typography.ts` (generator-emitted): `typography.fontFamily: 'CustomFont, Roboto, Arial, sans-serif'`; `MuiCssBaseline` `styleOverrides` string with `@font-face` `src: url('/fonts/CustomFont.woff2') format('woff2')`.
- Hand-editing `typography.ts` requires `echo "src/theme/typography.ts" >> .generator-ignore`.
- Font URL is absolute from `public/` (`/fonts/...`), not `./fonts/...`.

## Global Styles

- `CssBaseline` inside `ThemeProvider theme={paletteThemeLight}`.
- `GlobalStyles styles={{ body, '*::-webkit-scrollbar', '*::-webkit-scrollbar-thumb' }}`.

## Best Practices

- Use theme variables (`'primary.main'`), not hex.
- `sx` for one-off styles; `styled` for reused styles.
- Use theme spacing units (`theme.spacing(2)` = 16px at 8px unit).
- Use breakpoints in `sx`.

## Troubleshooting

- Theme changes not applying: `rm -rf node_modules/.cache` then `pnpm run dev`.
- Custom fonts not loading: font file under `public/fonts/`; use `/fonts/...`.
- Sub-theme not working: `name` in `registerService(..., { name })` must equal `toSafeCamelCase` of the model sub-theme name (see `Sub Theme Name:` comment in scaffold); remove `.default` and call the register fn from `application-customizer.tsx`.

## Related Documentation

- MUI docs: theming, palette, typography, breakpoints.
- [Development Workflow](./development-workflow.md)
- [Main README](./README.md)
