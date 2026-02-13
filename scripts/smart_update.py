#!/usr/bin/env python3
"""
스마트 규정 업데이트 스크립트

기능:
1. DOCX 파일을 MD로 자동 변환
2. 규정 코드 또는 제목으로 자동 매칭
3. 해당 규정 파일 자동 업데이트
4. Git 커밋 메시지 자동 생성

사용법:
    python3 scripts/smart_update.py regulations_source/new/교직원포상규정.docx
    python3 scripts/smart_update.py regulations_source/new/3-1-9_교직원포상규정.docx
"""

import os
import sys
import json
import re
import subprocess
import difflib
from pathlib import Path
from datetime import datetime

# regulations.json 로드
def load_regulations_db():
    """regulations.json 파일 로드"""
    with open('regulations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['regulations']

def extract_code_from_filename(filename):
    """파일명에서 규정 코드 추출"""
    # 패턴: 3-1-9 또는 3_1_9
    match = re.search(r'(\d+-\d+-\d+)', filename)
    if match:
        return match.group(1)

    match = re.search(r'(\d+_\d+_\d+)', filename)
    if match:
        return match.group(1).replace('_', '-')

    return None

def extract_title_from_docx(docx_path):
    """DOCX 파일에서 제목 추출 (첫 번째 단락)"""
    try:
        # pandoc을 사용하여 제목 추출
        result = subprocess.run(
            ['pandoc', '-f', 'docx', '-t', 'plain', docx_path],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )

        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line and len(line) > 2:  # 의미 있는 첫 줄
                    return line
        return None
    except Exception as e:
        print(f"⚠️  제목 추출 실패: {e}")
        return None

def normalize_title(title):
    """제목 정규화"""
    normalized = re.sub(r'[\s\.\·\-]', '', title)
    return normalized.lower()

def find_regulation_by_code(regulations, code):
    """규정 코드로 검색"""
    for reg in regulations:
        if reg['code'] == code:
            return reg
    return None

def find_regulation_by_title(regulations, title):
    """제목으로 검색 (유사도 기반)"""
    normalized_search = normalize_title(title)

    # 정확한 매칭 먼저 시도
    for reg in regulations:
        if reg['title_normalized'] == normalized_search:
            return reg, 1.0  # 100% 일치

    # 부분 매칭 시도
    best_match = None
    best_ratio = 0.0

    for reg in regulations:
        # 제목 포함 여부 확인
        if normalized_search in reg['title_normalized'] or reg['title_normalized'] in normalized_search:
            ratio = difflib.SequenceMatcher(None, normalized_search, reg['title_normalized']).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = reg

    # 유사도 기반 검색
    if best_match is None:
        for reg in regulations:
            ratio = difflib.SequenceMatcher(None, normalized_search, reg['title_normalized']).ratio()
            if ratio > best_ratio and ratio > 0.6:  # 60% 이상 유사도
                best_ratio = ratio
                best_match = reg

    return best_match, best_ratio

def convert_docx_to_md(docx_path):
    """DOCX를 MD로 변환"""
    temp_md = f"/tmp/regulation_temp_{os.getpid()}.md"

    try:
        result = subprocess.run(
            ['pandoc', '-f', 'docx', '-t', 'markdown', docx_path, '-o', temp_md],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return temp_md
        else:
            print(f"❌ Pandoc 변환 실패: {result.stderr}")
            return None
    except Exception as e:
        print(f"❌ 변환 중 오류: {e}")
        return None

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
        print(f"🗑️  오래된 백업 파일 {deleted_count}개 정리됨 ({days}일 이상)")

def update_regulation_file(target_path, source_md):
    """규정 파일 업데이트"""
    # 백업 생성
    backup_path = f"{target_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    try:
        # 백업
        if os.path.exists(target_path):
            subprocess.run(['cp', target_path, backup_path], check=True)
            print(f"💾 백업 생성: {backup_path}")

        # 파일 업데이트
        subprocess.run(['cp', source_md, target_path], check=True)
        
        # 오래된 백업 정리
        cleanup_old_backups(target_path, days=7)

        return True, backup_path
    except Exception as e:
        print(f"❌ 파일 업데이트 실패: {e}")
        return False, None

def main():
    if len(sys.argv) < 2:
        print("사용법: python3 scripts/smart_update.py <docx파일>")
        print("\n예시:")
        print("  python3 scripts/smart_update.py regulations_source/new/교직원포상규정.docx")
        print("  python3 scripts/smart_update.py regulations_source/new/3-1-9_교직원포상규정.docx")
        sys.exit(1)

    docx_file = sys.argv[1]

    if not os.path.exists(docx_file):
        print(f"❌ 파일을 찾을 수 없습니다: {docx_file}")
        sys.exit(1)

    print("=" * 80)
    print("🤖 스마트 규정 업데이트 시작")
    print("=" * 80)
    print(f"📄 원본 파일: {docx_file}")
    print()

    # 1. regulations.json 로드
    regulations = load_regulations_db()
    print(f"📚 규정 데이터베이스 로드: {len(regulations)}개 규정")
    print()

    # 2. 규정 코드 추출 시도
    filename = os.path.basename(docx_file)
    code = extract_code_from_filename(filename)

    matched_regulation = None
    match_method = None
    match_confidence = 0.0

    if code:
        print(f"🔍 파일명에서 코드 추출: {code}")
        matched_regulation = find_regulation_by_code(regulations, code)
        if matched_regulation:
            match_method = "코드"
            match_confidence = 1.0
            print(f"✅ 규정 매칭 성공 (코드 기반)")

    # 3. 코드로 못 찾으면 제목으로 검색
    if not matched_regulation:
        print("🔍 DOCX 파일에서 제목 추출 중...")
        title = extract_title_from_docx(docx_file)

        if title:
            print(f"   제목: {title}")
            matched_regulation, match_confidence = find_regulation_by_title(regulations, title)
            if matched_regulation:
                match_method = "제목"
                print(f"✅ 규정 매칭 성공 (제목 기반, 유사도: {match_confidence*100:.1f}%)")
        else:
            print("⚠️  제목 추출 실패")

    if not matched_regulation:
        print("\n❌ 매칭되는 규정을 찾을 수 없습니다.")
        print("\n💡 다음을 확인하세요:")
        print("   1. 파일명에 규정 코드 포함 (예: 3-1-9_제목.docx)")
        print("   2. DOCX 파일의 첫 줄이 올바른 규정 제목인지 확인")
        print("   3. regulations.json에 해당 규정이 등록되어 있는지 확인")
        sys.exit(1)

    print()
    print(f"🎯 매칭된 규정:")
    print(f"   코드: {matched_regulation['code']}")
    print(f"   제목: {matched_regulation['title']}")
    print(f"   경로: {matched_regulation['path']}")
    print(f"   매칭 방법: {match_method}")
    if match_confidence < 1.0:
        print(f"   매칭 신뢰도: {match_confidence*100:.1f}%")
    print()

    # 확신도가 낮으면 확인
    if match_confidence < 0.8:
        response = input(f"⚠️  매칭 신뢰도가 낮습니다 ({match_confidence*100:.1f}%). 계속하시겠습니까? (y/N): ")
        if response.lower() != 'y':
            print("취소되었습니다.")
            sys.exit(0)

    # 4. DOCX → MD 변환
    print("🔄 DOCX → MD 변환 중...")
    temp_md = convert_docx_to_md(docx_file)

    if not temp_md:
        print("❌ 변환 실패")
        sys.exit(1)

    print(f"✅ 변환 완료: {temp_md}")
    print()

    # 5. 규정 파일 업데이트
    print(f"📝 규정 파일 업데이트 중...")
    success, backup_path = update_regulation_file(matched_regulation['path'], temp_md)

    if not success:
        sys.exit(1)

    print(f"✅ 업데이트 완료: {matched_regulation['path']}")
    print()

    # 6. 임시 파일 삭제
    os.remove(temp_md)

    # 7. Git 커밋 안내
    print("=" * 80)
    print("📝 Git 커밋 명령:")
    print("=" * 80)
    print()
    print(f"git add {matched_regulation['path']}")
    print(f"git commit -m \"개정: {matched_regulation['title']} ({matched_regulation['code']}) - {datetime.now().strftime('%Y-%m-%d')}\"")
    print("git push")
    print()
    print("=" * 80)
    print()
    print(f"💡 백업 파일: {backup_path}")
    print(f"   문제가 없으면 삭제: rm \"{backup_path}\"")
    print()

    # 처리된 파일을 history로 이동
    year = datetime.now().strftime('%Y')
    history_dir = f"regulations_source/history/{year}"
    os.makedirs(history_dir, exist_ok=True)

    history_path = os.path.join(history_dir, os.path.basename(docx_file))
    subprocess.run(['mv', docx_file, history_path])
    print(f"📦 원본 파일 아카이브: {history_path}")
    print()
    print("✅ 모든 작업 완료!")

if __name__ == "__main__":
    main()
