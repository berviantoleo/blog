#!/usr/bin/env python3
import os
import re

# Tag ID to name mapping (based on common tag patterns)
TAG_MAPPING = {
    "656f4c3dc26ff09a8160c4e1": "personal",
    "5f8072b8f829251669389949": "reflection", 
    "659a7cba7f2e4b55d01f48b0": "mental-health",
    "56744721958ef13879b94a60": "productivity",
    "651046abdae1474f642209fc": "work",
    "5c367cefe38e4a8e2d890061": "discussion",
    "647720708a9f5d90982e6851": "kualitatif",
    "647720708a9f5d90982e6852": "kuantitatif", 
    "647720708a9f5d90982e6853": "diskusi",
    "642d943e311bf43ae8ed9d6c": "philosophy",
    "642d943e311bf43ae8ed9d96": "human-nature"
}

def fix_tags_in_file(filepath):
    """Fix tag IDs in a markdown file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find tags section
    lines = content.split('\n')
    new_lines = []
    in_tags = False
    
    for line in lines:
        if line.strip() == 'tags:':
            in_tags = True
            new_lines.append(line)
        elif in_tags and line.startswith('  - '):
            # Extract tag ID
            tag_id = line.strip()[2:]  # Remove "- "
            # Map to tag name if exists
            tag_name = TAG_MAPPING.get(tag_id, tag_id)
            new_lines.append(f"  - {tag_name}")
        elif in_tags and not line.startswith('  '):
            # End of tags section
            in_tags = False
            new_lines.append(line)
        else:
            new_lines.append(line)
    
    # Write back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

def main():
    post_dir = '/home/bervianto/Documents/Projects/blog/content/post'
    
    for filename in os.listdir(post_dir):
        if filename.endswith('.md') and filename != '_index.md':
            filepath = os.path.join(post_dir, filename)
            fix_tags_in_file(filepath)
            print(f"Fixed tags in: {filename}")

if __name__ == "__main__":
    main()
