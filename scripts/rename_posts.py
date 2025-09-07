#!/usr/bin/env python3
import os
import re
from datetime import datetime

def rename_posts():
    post_dir = '/home/bervianto/Documents/Projects/blog/content/post'
    
    for filename in os.listdir(post_dir):
        if filename.endswith('.md') and filename != '_index.md' and not filename.startswith('20'):
            filepath = os.path.join(post_dir, filename)
            
            # Read file to get date
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract date from frontmatter
            date_match = re.search(r'date:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})', content)
            if date_match:
                date_str = date_match.group(1)
                new_filename = f"{date_str}-{filename}"
                new_filepath = os.path.join(post_dir, new_filename)
                
                os.rename(filepath, new_filepath)
                print(f"Renamed: {filename} -> {new_filename}")

if __name__ == "__main__":
    rename_posts()
