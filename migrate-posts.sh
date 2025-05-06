#!/bin/bash

# Create directory if it doesn't exist
mkdir -p hugo/content/posts

# Process each post file
for file in hakyll/posts/*.md; do
  filename=$(basename "$file")
  date_part=${filename:0:10}
  
  # Extract front matter
  title=$(grep -m 1 'title:' "$file" | sed 's/title: *//')
  author=$(grep -m 1 'author:' "$file" | sed 's/author: *//')
  tags=$(grep -m 1 'tags:' "$file" | sed 's/tags: *//')
  
  # Create new front matter
  echo "Processing $filename..."
  
  # Create new file with Hugo front matter
  cat > "hugo/content/posts/$filename" << EOF
---
title: "$title"
author: "$author"
date: $date_part
tags: [$tags]
---
$(tail -n +6 "$file")
EOF

  echo "Migrated $filename"
done

# Now process pages
mkdir -p hugo/content

for file in hakyll/pages/*.md; do
  filename=$(basename "$file")
  pagename=${filename%.md}
  
  # Extract front matter
  title=$(grep -m 1 'title:' "$file" | sed 's/title: *//')
  description=$(grep -m 1 'description:' "$file" | sed 's/description: *//')
  
  # Create new file with Hugo front matter
  echo "Processing page $filename..."
  
  cat > "hugo/content/$pagename.md" << EOF
---
title: "$title"
url: "/$pagename/"
description: "$description"
---
$(tail -n +6 "$file")
EOF

  echo "Migrated page $filename"
done

echo "Migration complete!"