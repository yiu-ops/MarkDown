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

def normalize_title(title):
    """제목 정규화 (공백, 특수문자 제거)"""
    return re.sub(r'[\s\.\·\-\(\)\[\]\:：]', '', title).lower()

def split_markdown_content(content, regulations):
    """
    Split the monolithic markdown content into individual regulations.
    Returns a dictionary {regulation_code: content_lines}
    
    PDF 변환 후에도 규정을 찾을 수 있도록 여러 매칭 방법 사용:
    1. 정확한 제목 매칭
    2. 정규화된 제목 매칭 (공백/특수문자 무시)
    3. 라인 내 제목 포함 여부 (짧은 라인만)
    """
    lines = content.splitlines()
    split_result = {}
    current_code = None
    current_content = []
    
    # Create a mapping for fast lookup
    # exact_title -> reg, normalized_title -> reg
    exact_map = {}
    normalized_map = {}
    for reg in regulations:
        exact_map[reg['title'].strip()] = reg
        exact_map[reg['title'].replace(' ', '')] = reg
        normalized_map[normalize_title(reg['title'])] = reg

    def find_matching_regulation(line):
        """라인에서 규정 제목을 찾는 함수"""
        stripped = line.strip()
        
        # Markdown 헤딩 처리 (# 제목)
        if stripped.startswith('#'):
            stripped = re.sub(r'^#+\s*', '', stripped)
        
        # 방법 1: 정확한 매칭
        if stripped in exact_map:
            return exact_map[stripped]
        if stripped.replace(' ', '') in exact_map:
            return exact_map[stripped.replace(' ', '')]
        
        # 방법 2: 정규화된 매칭
        normalized = normalize_title(stripped)
        if normalized in normalized_map:
            return normalized_map[normalized]
        
        # 방법 3: 짧은 라인에서 부분 매칭 (제목이 포함된 경우)
        if len(stripped) < 80:
            for norm_title, reg in normalized_map.items():
                if norm_title == normalized:
                    return reg
                # 라인이 규정 제목으로 끝나는 경우
                if normalized.endswith(norm_title) and len(norm_title) > 4:
                    return reg
        
        return None

    for line in lines:
        matched_reg = find_matching_regulation(line)
        
        if matched_reg:
            # Save previous regulation if exists
            if current_code:
                split_result[current_code] = current_content
            
            # Start new regulation
            current_code = matched_reg['code']
            current_content = [line]  # Include the title line
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

def sanitize_for_mdx(content):
    """Sanitize content for Docusaurus MDX compatibility."""
    # Remove style attributes from HTML tags (causes MDX errors)
    # style="width: 9%" -> ""
    content = re.sub(r' style="[^"]*"', '', content)
    
    # Fix MDX nesting issues: Ensure block tags inside table cells have newlines
    # </td> after </p> or </blockquote> should be on new line
    content = re.sub(r'(</p>|</blockquote>)</td>', r'\1\n</td>', content)
    
    # <td> before <p> or <blockquote> should be on new line
    # Handle <td> with attributes (e.g. <td rowspan="2">)
    content = re.sub(r'(<td[^>]*>)(<p>|<blockquote>)', r'\1\n\2', content)
    
    # Replace <br> with <br /> if needed (Pandoc usually does this, but just in case)
    # But be careful not to double replace
    
    return content

def cleanup_old_backups(target_path, days=7):
    """오래된 백업 파일 정리 (기본 7일)"""
    import time
    import glob
    
    # 백업 파일 패턴
    backup_pattern = f"{target_path}.backup.*"
    backup_files = glob.glob(backup_pattern)
    
    if not backup_files:
        return
    
    current_time = time.time()
    deleted_count = 0
    
    for backup_file in backup_files:
        try:
            # 파일 수정 시간 확인
            file_age_days = (current_time - os.path.getmtime(backup_file)) / 86400
            
            if file_age_days > days:
                os.remove(backup_file)
                deleted_count += 1
        except Exception as e:
            # 삭제 실패해도 계속 진행
            pass
    
    if deleted_count > 0:
        print(f"    🗑️  오래된 백업 {deleted_count}개 정리 ({days}일 이상)")

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
        
        # Sanitize for MDX
        new_content_str = sanitize_for_mdx(new_content_str)
        
        # Re-split to lines for diffing (after sanitization)
        new_lines_sanitized = new_content_str.splitlines()
        
        old_content_str = '\n'.join(old_lines)
        
        if new_content_str.strip() != old_content_str.strip():
            print(f"  [UPDATE] {reg_info['title']} ({code})")
            
            # Generate diff
            diff_html = generate_diff_html(old_lines, new_lines_sanitized, f"{reg_info['title']} ({code})")
            diff_report.append(diff_html)
            
            # Backup existing file
            if os.path.exists(file_path):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_path = f"{file_path}.backup.{timestamp}"
                try:
                    os.rename(file_path, backup_path)
                    print(f"    Backup created: {os.path.basename(backup_path)}")
                    
                    # 오래된 백업 정리
                    cleanup_old_backups(file_path, days=7)
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
        # Create reports directory
        reports_dir = os.path.join(project_root, 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_filename = f'update_report_{timestamp}.html'
        report_path = os.path.join(reports_dir, report_filename)
        
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
