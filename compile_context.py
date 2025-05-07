#!/usr/bin/env python3

import os
import glob
from pathlib import Path

# Configuration
HUGO_DIR = './hugo'
OUTPUT_FILE = '/Users/adam/sandbox/prompts-context/context/adamgordonbell.content.md'

# File types to include
INCLUDE_EXTENSIONS = [
    '.md', '.markdown', '.html', '.yml', '.yaml', '.toml', '.json',
    '.css', '.js', '.sh', '.go', '.ts', '.jsx', '.tsx'
]

# Directories to process in order
DIRECTORY_ORDER = [
    'hugo.yaml',           # Config first
    'archetypes',          # Site structure
    'layouts',             # Templates
    'themes',              # Theme config
    'content',             # Content last (usually largest)
    'static',
    'util'
]

def should_include(filepath):
    """Determine if a file should be included in the context"""
    # Skip hidden files
    if os.path.basename(filepath).startswith('.'):
        return False
    
    # Only include specific extensions
    ext = os.path.splitext(filepath)[1].lower()
    return ext in INCLUDE_EXTENSIONS

def get_files_in_order():
    """Get all relevant files in a logical order"""
    result = []
    
    # Process config files first
    config_file = os.path.join(HUGO_DIR, 'hugo.yaml')
    if os.path.exists(config_file):
        result.append(config_file)
    
    # Include theme configuration
    theme_config = os.path.join(HUGO_DIR, 'themes/cascadeofinsights/theme.toml')
    if os.path.exists(theme_config):
        result.append(theme_config)
    
    # Include archetypes (content templates)
    archetypes_dir = os.path.join(HUGO_DIR, 'archetypes')
    if os.path.exists(archetypes_dir):
        for file in sorted(os.listdir(archetypes_dir)):
            filepath = os.path.join(archetypes_dir, file)
            if should_include(filepath):
                result.append(filepath)
                break  # Just include default archetype
    
    # Include layouts for site structure
    layouts_dir = os.path.join(HUGO_DIR, 'layouts')
    if os.path.exists(layouts_dir):
        for root, _, files in os.walk(layouts_dir):
            for file in sorted(files):
                # Include base templates and page types
                if file in ['baseof.html', 'single.html', 'list.html']:
                    filepath = os.path.join(root, file)
                    if should_include(filepath):
                        result.append(filepath)
    
    # Include all partials
    partials_dir = os.path.join(HUGO_DIR, 'layouts/partials')
    if os.path.exists(partials_dir):
        for file in sorted(os.listdir(partials_dir)):
            filepath = os.path.join(partials_dir, file)
            if should_include(filepath):
                result.append(filepath)
    
    # Include shortcodes if they exist
    shortcodes_dir = os.path.join(HUGO_DIR, 'layouts/shortcodes')
    if os.path.exists(shortcodes_dir):
        for file in sorted(os.listdir(shortcodes_dir)):
            filepath = os.path.join(shortcodes_dir, file)
            if should_include(filepath):
                result.append(filepath)
                break  # Just include one shortcode as example
    
    # Include data files
    data_dir = os.path.join(HUGO_DIR, 'data')
    if os.path.exists(data_dir):
        for file in sorted(os.listdir(data_dir)):
            filepath = os.path.join(data_dir, file)
            if should_include(filepath):
                result.append(filepath)
                break  # Just include one data file as example
    
    # Include CSS files 
    css_dir = os.path.join(HUGO_DIR, 'static/css')
    if os.path.exists(css_dir):
        for file in sorted(os.listdir(css_dir)):
            filepath = os.path.join(css_dir, file)
            if should_include(filepath):
                result.append(filepath)
                if len(result) >= 10:  # Avoid too many CSS files
                    break
    
    # Include JS files if they exist
    js_dir = os.path.join(HUGO_DIR, 'static/js')
    if os.path.exists(js_dir):
        for file in sorted(os.listdir(js_dir)):
            filepath = os.path.join(js_dir, file)
            if should_include(filepath):
                result.append(filepath)
                break  # Just include one JS file
    
    # Also check theme assets
    theme_css = os.path.join(HUGO_DIR, 'themes/cascadeofinsights/assets/css')
    if os.path.exists(theme_css):
        for file in sorted(os.listdir(theme_css)):
            if file == 'main.css':
                filepath = os.path.join(theme_css, file)
                if should_include(filepath):
                    result.append(filepath)
                    break
    
    # Include just one blog post as an example
    blog_found = False
    blog_dir = os.path.join(HUGO_DIR, 'content/blog')
    if os.path.exists(blog_dir):
        for file in sorted(os.listdir(blog_dir)):
            filepath = os.path.join(blog_dir, file)
            if should_include(filepath) and not blog_found:
                result.append(filepath)
                blog_found = True
                break
    
    return result

def write_context_file():
    """Write all files to the context file with proper formatting"""
    with open(OUTPUT_FILE, 'w') as output:
        output.write("---\nname: Adam Gordon Bell Webiste\ndescription: hugo site content\n---\n\n")
        
        for filepath in get_files_in_order():
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    
                # Write file header
                output.write(f"---\n{filepath}\n---\n{content}\n\n")
                
                print(f"Added: {filepath}")
            except Exception as e:
                print(f"Error processing {filepath}: {e}")
    
    print(f"\nContext file created at: {OUTPUT_FILE}")

if __name__ == "__main__":
    write_context_file()