#!/usr/bin/env python3
import json
import os
from datetime import datetime
import re

def clean_filename(title):
    """Convert title to a clean filename"""
    # Remove special characters and replace spaces with hyphens
    filename = re.sub(r'[^\w\s-]', '', title.lower())
    filename = re.sub(r'[-\s]+', '-', filename)
    return filename.strip('-')

def convert_html_to_markdown(html_content):
    """Basic HTML to Markdown conversion"""
    if not html_content:
        return ""
    
    # Replace common HTML tags with Markdown equivalents
    content = html_content
    
    # Headers
    content = re.sub(r'<h2[^>]*id="[^"]*"[^>]*>(.*?)</h2>', r'## \1', content)
    content = re.sub(r'<h3[^>]*id="[^"]*"[^>]*>(.*?)</h3>', r'### \1', content)
    content = re.sub(r'<h4[^>]*id="[^"]*"[^>]*>(.*?)</h4>', r'#### \1', content)
    
    # Paragraphs
    content = re.sub(r'<p>(.*?)</p>', r'\1\n', content)
    
    # Blockquotes
    content = re.sub(r'<blockquote>\s*<p>(.*?)</p>\s*</blockquote>', r'> \1\n', content)
    
    # Lists
    content = re.sub(r'<ol>', '', content)
    content = re.sub(r'</ol>', '', content)
    content = re.sub(r'<ul>', '', content)
    content = re.sub(r'</ul>', '', content)
    content = re.sub(r'<li><p>(.*?)</p></li>', r'- \1', content)
    content = re.sub(r'<li>(.*?)</li>', r'- \1', content)
    
    # Links
    content = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', content)
    
    # Images
    content = re.sub(r'<img[^>]*src="([^"]*)"[^>]*alt="([^"]*)"[^>]*/?>', r'![\2](\1)', content)
    content = re.sub(r'<img[^>]*src="([^"]*)"[^>]*/?>', r'![](\1)', content)
    
    # Strong/Bold
    content = re.sub(r'<strong>(.*?)</strong>', r'**\1**', content)
    content = re.sub(r'<b>(.*?)</b>', r'**\1**', content)
    
    # Emphasis/Italic
    content = re.sub(r'<em>(.*?)</em>', r'*\1*', content)
    content = re.sub(r'<i>(.*?)</i>', r'*\1*', content)
    
    # Code
    content = re.sub(r'<code>(.*?)</code>', r'`\1`', content)
    
    # Horizontal rule
    content = re.sub(r'<hr\s*/?>', '---', content)
    
    # Clean up extra whitespace
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    content = content.strip()
    
    return content

def convert_article_to_hugo(article):
    """Convert a single article to Hugo format"""
    title = article.get('title', 'Untitled')
    date = article.get('createdAt', article.get('dateAdded', ''))
    slug = article.get('slug', clean_filename(title))
    cover_image = article.get('coverImage', '')
    tags = [tag.get('name', tag) if isinstance(tag, dict) else str(tag) for tag in article.get('tags', [])]
    
    # Use contentMarkdown if available, otherwise convert HTML content
    content = article.get('contentMarkdown', '')
    if not content:
        content = convert_html_to_markdown(article.get('content', ''))
    
    # Create frontmatter
    frontmatter = f"""---
title: "{title}"
date: {date}
slug: {slug}"""
    
    if cover_image:
        frontmatter += f"\ncover: {cover_image}"
    
    if tags:
        frontmatter += "\ntags:"
        for tag in tags:
            frontmatter += f"\n  - {tag}"
    
    frontmatter += "\n---\n\n"
    
    return frontmatter + content

def main():
    # Read the JSON file
    json_file = '/home/bervianto/Downloads/626b22336072cdb96d148b90-articles.json'
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    articles = data.get('posts', [])
    
    # Create output directory
    output_dir = '/home/bervianto/Documents/Projects/blog/content/post'
    os.makedirs(output_dir, exist_ok=True)
    
    converted_count = 0
    
    for article in articles:
        # Skip deleted articles
        if not article.get('isActive', True):
            continue
            
        title = article.get('title', 'Untitled')
        slug = article.get('slug', clean_filename(title))
        
        # Create filename
        filename = f"{slug}.md"
        filepath = os.path.join(output_dir, filename)
        
        # Skip if file already exists
        if os.path.exists(filepath):
            print(f"Skipping {filename} - already exists")
            continue
        
        # Convert article
        try:
            hugo_content = convert_article_to_hugo(article)
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(hugo_content)
            
            print(f"Converted: {filename}")
            converted_count += 1
            
        except Exception as e:
            print(f"Error converting {title}: {e}")
    
    print(f"\nConversion complete! Converted {converted_count} articles.")

if __name__ == "__main__":
    main()
