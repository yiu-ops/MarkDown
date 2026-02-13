#!/usr/bin/env python3
"""
regulations.json 재생성 스크립트

regulations/ 폴더의 모든 MD 파일을 스캔하여
regulations.json 파일을 다시 생성합니다.
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

def extract_title_from_md(filepath):
    """MD 파일에서 첫 번째 헤딩(제목) 추출"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#'):
                    # # 제거하고 제목만 추출
                    title = re.sub(r'^#+\s*', '', line).strip()
                    if title:
                        return title
        return None
    except Exception as e:
        print(f"⚠️  {filepath} 읽기 실패: {e}")
        return None

def normalize_title(title):
    """제목 정규화 (공백, 특수문자 제거, 소문자 변환)"""
    if not title:
        return ""
    return re.sub(r'[\s\.\·\-]', '', title).lower()

def scan_regulations(regulations_dir='regulations'):
    """regulations 폴더를 스캔하여 모든 규정 파일 정보 수집"""
    regulations = []
    
    for root, dirs, files in os.walk(regulations_dir):
        # 백업 파일 제외
        files = [f for f in files if f.endswith('.md') and '.backup.' not in f]
        
        for file in files:
            filepath = os.path.join(root, file)
            relative_path = os.path.relpath(filepath, start='.')
            
            # 규정 코드 (파일명에서 .md 제거)
            code = file.replace('.md', '')
            
            # 제목 추출
            title = extract_title_from_md(filepath)
            
            if not title:
                print(f"⚠️  제목 없음: {relative_path}")
                continue
            
            # 카테고리 (regulations/ 이후 경로)
            category = os.path.dirname(relative_path).replace('regulations/', '').replace('regulations\\', '')
            
            regulations.append({
                "code": code,
                "title": title,
                "title_normalized": normalize_title(title),
                "category": category,
                "path": relative_path.replace('\\', '/'),  # Windows 경로 → Unix 경로
                "filename": file
            })
    
    return regulations

def save_regulations_db(regulations, output_file='regulations.json'):
    """regulations.json 파일 저장"""
    # 코드 순으로 정렬
    regulations_sorted = sorted(regulations, key=lambda x: x['code'])
    
    data = {
        "version": "1.0",
        "last_updated": datetime.now().strftime('%Y-%m-%d'),
        "total_regulations": len(regulations_sorted),
        "regulations": regulations_sorted
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {output_file} 생성 완료: {len(regulations_sorted)}개 규정")

def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("🔄 regulations.json 재생성")
    print("=" * 60)
    print()
    
    # 프로젝트 루트 확인
    if not os.path.exists('regulations'):
        print("❌ regulations 폴더를 찾을 수 없습니다.")
        print("   프로젝트 루트 디렉토리에서 실행하세요.")
        return 1
    
    # 규정 파일 스캔
    print("📂 regulations 폴더 스캔 중...")
    regulations = scan_regulations()
    
    if not regulations:
        print("❌ 규정 파일을 찾을 수 없습니다.")
        return 1
    
    print(f"📊 발견된 규정: {len(regulations)}개")
    print()
    
    # 카테고리별 통계
    categories = {}
    for reg in regulations:
        cat = reg['category']
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += 1
    
    print("📁 카테고리별 통계:")
    for cat, count in sorted(categories.items()):
        print(f"   {cat}: {count}개")
    print()
    
    # regulations.json 저장
    save_regulations_db(regulations)
    print()
    print("✅ 완료!")
    
    return 0

if __name__ == '__main__':
    import sys
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  사용자가 중단했습니다.")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
