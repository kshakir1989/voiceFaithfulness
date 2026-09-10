# Spec architecture diagram scaffold

Copy into every new Spec Kit app at init. Agents MUST keep the diagram current as Spec Kit artifacts change.

## Install into a new app

```bash
APP=apps/<name>
mkdir -p "$APP"
cp templates/spec-architecture/spec-architecture.mmd "$APP/"
cp templates/spec-architecture/spec-architecture.html "$APP/"
cp templates/spec-architecture/render-spec-architecture.mjs "$APP/"
# Replace APP_NAME in .mmd and .html with the app folder name
# Then render:
cd "$APP" && node render-spec-architecture.mjs
```

Or from the monorepo root:

```bash
node templates/spec-architecture/scaffold.mjs apps/<name>
```

## Files

| File | Purpose |
|------|---------|
| `spec-architecture.mmd` | Mermaid source (edit this when dependencies change) |
| `spec-architecture.html` | HTML preview used to generate the PNG |
| `render-spec-architecture.mjs` | Writes `spec-architecture.png` (uses Playwright from `apps/value` if needed) |
| `scaffold.mjs` | Copies files into `apps/<name>` and substitutes the app name |

## Keep current

Whenever assess artifacts, `specs/`, constitution, extensions, or implementation surfaces are added or their dependencies change:

1. Update `spec-architecture.mmd` and the Mermaid block in `spec-architecture.html`
2. Run `node render-spec-architecture.mjs` from the app directory
