# Migration Plan: Hakyll to Hugo

## Overview
This document outlines the plan to migrate the site from Hakyll (Haskell-based) to Hugo (Go-based) static site generator.

## Goals
- Simplify site maintenance by moving to Hugo
- Remove complex Haskell dependencies
- Preserve all existing content and functionality
- Maintain same visual style and user experience

## Approach
- Move existing Hakyll site to a subfolder for reference
- Create a new Hugo site from scratch
- Port content, templates, and styling to Hugo
- Use the existing HTML output as a reference without needing to run the Hakyll site

## Tasks
- [ ] Create a "hakyll" subfolder and move all Hakyll-specific files there (preserving CNAME and this plan file at root)
- [ ] Create a "hugo" folder with a fresh Hugo installation
- [ ] Create new utility functions for Hugo (similar to current util/functions but for Hugo)
- [ ] Set up basic Hugo site structure with minimal theme
- [ ] Port templates from Hakyll to Hugo format
- [ ] Migrate content (posts, pages) to Hugo
- [ ] Port CSS and styling
- [ ] Configure tags, pagination, and other features in Hugo
- [ ] Test the site locally
- [ ] Update deployment process (removing CircleCI dependency, adding gha build)

## Notes
- Hakyll dependencies are complex and running the Hakyll site is not necessary
- We can use the markdown input as reference for porting ( or find rendered output in master git branch )
- The current util/functions is Hakyll-specific and will be moved to the hakyll subfolder
- New Hugo-specific utility functions will be created
- CircleCI will not be used for the new setup, a github actions build that supports hosting result on github static pages will be used instead.