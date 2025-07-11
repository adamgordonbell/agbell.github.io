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
- [x] Create a "hakyll" subfolder and move all Hakyll-specific files there (preserving CNAME and this plan file at root)
- [x] Create a "hugo" folder with a fresh Hugo installation
- [x] Create new utility functions for Hugo (similar to current util/functions but for Hugo)
- [x] Set up basic Hugo site structure with minimal theme
- [x] Port templates from Hakyll to Hugo format
- [x] Migrate content (posts, pages) to Hugo
- [x] Port CSS and styling
- [x] Set up images directory in Hugo static folder
- [x] Update .gitignore for both Hakyll and Hugo
- [x] Configure tags, pagination, and other features in Hugo
- [x] Test the site locally
- [x] Add background mode to Hugo server with log file and status check
- [x] Update deployment process (removing CircleCI dependency, adding GitHub Actions build)
- [x] Configure blog to be under /blog/ path
- [x] Ensure top-level page matches the original Hakyll content
- [x] Fix image rendering by enabling raw HTML in markdown content
- [x] Fix home page layout to match original Hakyll site (remove sidebar from home page)
- [x] Fix Markdown links not rendering inside HTML content by converting to HTML links
- [x] Update baseURL to use adamgordonbell.com instead of agbell.github.io
- [x] Configure blog permalinks to maintain consistent URL structure
- [x] Add custom CSS to better match original Hakyll styling and font sizes
- [x] Simplify font handling by removing custom fonts and font loading scripts

## Notes
- Hakyll dependencies are complex and running the Hakyll site is not necessary
- We can use the markdown input as reference for porting ( or find rendered output in master git branch )
- The current util/functions is Hakyll-specific and will be moved to the hakyll subfolder
- New Hugo-specific utility functions will be created
- CircleCI will not be used for the new setup, a github actions build that supports hosting result on github static pages will be used instead.