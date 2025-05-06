# Codebase Memory

## Project Planning
- Refactoring plans and documentation are maintained in `plan.md` at the root of the repository

## Build Commands
- `source ./util/functions && start` - Start development server on localhost:8000
- `source ./util/functions && build` - Build the static site
- `source ./util/functions && publish` - Clean, build and publish the site
- `source ./util/functions && new_post` - Create a new blog post with proper formatting
- `source ./util/functions && lint` - Run linter on the codebase

## Project Structure
- Hakyll-based static site generator written in Haskell
- Blog posts in `posts/` directory (markdown format)
- Draft posts go in `posts/drafts/`
- Template files in `templates/` directory

## Code Style
- Uses `OverloadedStrings` language extension
- Haskell imports grouped with qualified imports after standard ones
- Function names use camelCase
- Context composition uses the monoid operator `<>` 
- Error handling follows Hakyll/Haskell conventions with MonadFail

## Deployment
- CircleCI deploys the site to GitHub Pages
- Main branch is `hakyll`, production branch is `master`