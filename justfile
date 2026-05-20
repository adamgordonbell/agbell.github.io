# Hugo site management commands

# List all available commands
default:
    @just --list

# Start Hugo server in background on localhost:1313
start: sync-data
    @hugo server -D > /tmp/hugo-server.log 2>&1 &
    @echo "Hugo server started in background"
    @echo "Server logs at /tmp/hugo-server.log"
    @echo "Run 'just status' to check server status"

# Check Hugo server status
status:
    #!/usr/bin/env bash
    if pgrep -f "hugo server" > /dev/null; then
        echo "Hugo server is running"
        echo ""
        echo "Recent log entries:"
        tail -n 10 /tmp/hugo-server.log
        PORT=$(grep -o "http://localhost:[0-9]\+" /tmp/hugo-server.log | tail -n 1 | cut -d":" -f3)
        echo ""
        echo "Site available at http://localhost:$PORT/"
    else
        echo "Hugo server is not running"
    fi

# Stop Hugo server
stop:
    @pkill -f "hugo server" && echo "Hugo server stopped" || echo "No Hugo server running"

# Sync accomplishments data file from PARA source-of-truth
sync-data:
    @cp ~/para/projects/personal-site/accomplishments.yaml data/accomplishments.yaml
    @echo "Synced accomplishments.yaml from ~/para/projects/personal-site/"

# Pull CoRecursive episodes from corecursive.com → data/corecursive.json
sync-corecursive:
    @python3 scripts/sync-corecursive.py

# Pull CoRecursive newsletter posts from Kit → data/newsletters.json
sync-newsletters:
    @python3 scripts/sync-newsletters.py

# Pull Pulumi blog posts by Adam from ~/sandbox/docs → data/pulumi_blog.json
sync-pulumi-blog:
    @python3 scripts/sync-pulumi-blog.py

# Scrape Earthly blog posts by Adam (frozen archive) → data/earthly_blog.json
sync-earthly-blog:
    @python3 scripts/sync-earthly-blog.py

# Scrape SE Radio episodes hosted by Adam → data/se_radio.json
sync-se-radio:
    @python3 scripts/sync-se-radio.py

# Scrape SE Daily episodes featuring Adam → data/se_daily.json
sync-se-daily:
    @python3 scripts/sync-se-daily.py

# Pull EarthlyTech YouTube videos → data/youtube_earthly.json (~40s, frozen channel)
sync-youtube-earthly:
    @python3 scripts/sync-youtube.py --channel @EarthlyTech --out data/youtube_earthly.json

# Pull PulumiTV videos featuring Adam.
# Auto-detects videos with "Adam Gordon Bell" in description; merges with
# manually curated IDs from config/youtube-pulumi-picks.txt.
sync-youtube-pulumi:
    @python3 scripts/sync-youtube-pulumi.py

# Sync active sources only (Adam still publishes to these).
# Frozen sources (Earthly blog/YouTube, SE Radio, SE Daily) are one-time backfills —
# re-run their individual recipes manually if needed.
sync: sync-data sync-corecursive sync-newsletters sync-pulumi-blog sync-youtube-pulumi

# Backfill every frozen source from scratch — only need to run once.
sync-backfill: sync-earthly-blog sync-se-radio sync-se-daily sync-youtube-earthly

# Build the site locally
build: sync
    hugo --minify

# Show deployment information
publish:
    @echo "The site is deployed via GitHub Actions."
    @echo ""
    @echo "Deployment process:"
    @echo "1. Push changes to the main branch"
    @echo "2. GitHub Actions will build and deploy automatically"
    @echo "3. Site will be live at your GitHub Pages URL"
    @echo ""
    @echo "To build locally and preview:"
    @just build
    @echo "Site built in public/"

# Create a new blog post with today's date
new-post title:
    #!/usr/bin/env bash
    DATE=$(date +%Y-%m-%d)
    SLUG=$(echo "{{title}}" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//' | sed 's/-$//')
    FILENAME="content/blog/${DATE}-${SLUG}.md"
    cat > "$FILENAME" << EOF
    ---
    title: "{{title}}"
    author: "Adam Bell"
    date: $DATE
    tags: []
    ---

    [Your content here]

    <!--more-->

    EOF
    echo "Created new blog post: $FILENAME"
