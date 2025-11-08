# Hugo site management commands

# List all available commands
default:
    @just --list

# Start Hugo server in background on localhost:1313
start:
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

# Build the site locally
build:
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
