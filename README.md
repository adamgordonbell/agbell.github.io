# Adam Gordon Bell's Website

This is my blog. [Find it here](https://agbell.github.io)

## Technology

This blog is built with Hugo, a fast static site generator written in Go.

## Features

* Draft posts
* Post teasers with "read more" functionality
* Tag support and tag cloud
* Pagination
* Responsive design
* Comments via Disqus

## Development

### Setup

1. Clone this repository
2. Make sure you have Hugo installed (https://gohugo.io/installation/)

### Running Locally

```bash
source ./hugo/util/functions && start
```

Check server status:
```bash
source ./hugo/util/functions && status
```

Stop the server:
```bash
source ./hugo/util/functions && stop
```

### Creating New Posts

```bash
source ./hugo/util/functions && new_post
```

### Deployment

The site is automatically deployed via GitHub Actions when changes are pushed to the master branch.

## History

This blog was originally built with Hakyll (Haskell-based static site generator) but has been migrated to Hugo for easier maintenance.
