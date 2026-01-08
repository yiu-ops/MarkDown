#!/usr/bin/env python3
"""
Regulation Split and Update Script

This script processes a monolithic markdown file containing multiple regulations,
splits it into individual regulation files based on titles defined in regulations.json,
and updates the existing files if changes are detected. It also generates a diff report.
"""

import os
import sys
import json
import re
import difflib
from datetime import datetime
from pathlib import Path

# Set stdout to UTF-8 to avoid UnicodeEncodeError on Windows
sys.stdout.reconfigure(encoding='utf-8')

def load_regulations_db(project_root):
    """Load regulations.json database."""
    json_path = os.path.join(project_root, 'regulations.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['regulations']
    except Exception as e:
        print(f"Error loading regulations.json: {e}")
        sys.exit(1)

def normalize_line(line):
    """Normalize line for comparison (ignore whitespace differences)."""
    return line.strip()

def split_markdown_content(content, regulations):
    """
    Split the monolithic markdown content into individual regulations.
    Returns a dictionary {regulation_code: content_lines}
    """
    lines = content.splitlines()
    split_result = {}
    current_code = None
    current_content = []
    
    # Create a mapping of title -> regulation info for fast lookup
    # We use normalized titles (strip spaces) for better matching
    title_map = {}
    for reg in regulations:
        # Map exact title
        title_map[reg['title'].strip()] = reg
        # Map normalized title (remove spaces)
        title_map[reg['title'].replace(' ', '')] = reg

    for line in lines:
        stripped_line = line.strip()
        
        # Check if this line is a start of a new regulation
        # We check both exact match and space-removed match
        is_new_reg = False
        matched_reg = None
        
        if stripped_line in title_map:
            matched_reg = title_map[stripped_line]
            is_new_reg = True
        elif stripped_line.replace(' ', '') in title_map:
            matched_reg = title_map[stripped_line.replace(' ', '')]
            is_new_reg = True
            
        if is_new_reg:
            # Save previous regulation if exists
            if current_code:
                split_result[current_code] = current_content
            
            # Start new regulation
            current_code = matched_reg['code']
            current_content = [line] # Include the title line
            print(f"Found regulation start: {matched_reg['title']} ({current_code})")
        else:
            # Append to current regulation
            if current_code:
                current_content.append(line)
    
    # Save the last regulation
    if current_code:
        split_result[current_code] = current_content
        
    return split_result

def generate_diff_html(old_lines, new_lines, title):
    """Generate a simple HTML diff snippet."""
    diff = difflib.HtmlDiff().make_table(old_lines, new_lines, context=True, numlines=3)
    return f"<h3>{title}</h3>\n{diff}<br>"

def update_files(split_result, regulations, project_root):
    """Update files and generate report."""
    updated_count = 0
    unchanged_count = 0
    diff_report = []
    
    reg_map = {r['code']: r for r in regulations}
    
    print("\nChecking for updates...")
    
    for code, new_lines in split_result.items():
        if code not in reg_map:
            continue
            
        reg_info = reg_map[code]
        file_path = os.path.join(project_root, reg_info['path'])
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        old_lines = []
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                old_lines = f.read().splitlines()
        
        # Compare content
        # Join and split to ensure consistent newline handling
        new_content_str = '\n'.join(new_lines)
        old_content_str = '\n'.join(old_lines)
        
        if new_content_str.strip() != old_content_str.strip():
            print(f"  [UPDATE] {reg_info['title']} ({code})")
            
            # Generate diff
            diff_html = generate_diff_html(old_lines, new_lines, f"{reg_info['title']} ({code})")
            diff_report.append(diff_html)
            
            # Backup existing file
            if os.path.exists(file_path):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_path = f"{file_path}.backup.{timestamp}"
                try:
                    os.rename(file_path, backup_path)
                    print(f"    Backup created: {os.path.basename(backup_path)}")
                except OSError as e:
                    print(f"    Error creating backup: {e}")
            
            # Write new content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content_str)
                # Add a newline at end of file if missing
                if not new_content_str.endswith('\n'):
                    f.write('\n')
            
            updated_count += 1
        else:
            unchanged_count += 1
            
    return updated_count, unchanged_count, diff_report

def main():
    if len(sys.argv) < 2:
        print("Usage: python split_and_update.py <input_markdown_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)
        
    # Determine project root (assuming script is in scripts/ folder)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    print(f"Project Root: {project_root}")
    print(f"Input File: {input_file}")
    
    # Load regulations
    regulations = load_regulations_db(project_root)
    print(f"Loaded {len(regulations)} regulations from database.")
    
    # Read input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Split content
    print("\nSplitting content...")
    split_result = split_markdown_content(content, regulations)
    print(f"Found {len(split_result)} regulations in input file.")
    
    # Update files
    updated, unchanged, diff_report = update_files(split_result, regulations, project_root)
    
    print("\n" + "="*50)
    print(f"Summary:")
    print(f"  Updated: {updated}")
    print(f"  Unchanged: {unchanged}")
    print("="*50)
    
    # Save diff report if there are updates
    if diff_report:
        report_path = os.path.join(project_root, 'update_report.html')
        html_content = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table.diff { border-collapse: collapse; width: 100%; font-family: monospace; font-size: 12px; }
                table.diff td { padding: 2px 5px; border: 1px solid #ddd; }
                table.diff th { background-color: #f0f0f0; }
                .diff_add { background-color: #e6ffec; }
                .diff_chg { background-color: #fff5b1; }
                .diff_sub { background-color: #ffebe9; }
            </style>
        </head>
        <body>
            <h1>Regulation Update Report</h1>
            <p>Generated at: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
            <hr>
        """ + "\n".join(diff_report) + """
        </body>
        </html>
        """
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"\nDiff report saved to: {report_path}")

if __name__ == "__main__":
    main()
