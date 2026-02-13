#!/usr/bin/env python3
"""
일괄 스마트 업데이트 스크립트

regulations_source/new/ 폴더의 모든 PDF/DOCX 파일을 자동 처리

사용법:
    python3 scripts/batch_smart_update.py
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def find_regulation_files(directory):
    """특정 디렉토리에서 모든 PDF/DOCX 파일 찾기"""
    files = []
    if os.path.exists(directory):
        for file in os.listdir(directory):
            # PDF 또는 DOCX 파일만, 임시 파일 제외
            if (file.endswith('.pdf') or file.endswith('.docx')) and not file.startswith('~'):
                files.append(os.path.join(directory, file))
    return sorted(files)

def main():
    new_dir = "regulations_source/new"

    print("=" * 80)
    print("📦 일괄 스마트 업데이트 시작")
    print("=" * 80)
    print(f"📁 대상 폴더: {new_dir}")
    print()

    if not os.path.exists(new_dir):
        print(f"❌ {new_dir} 폴더가 없습니다.")
        print(f"❌ {new_dir} 폴더를 생성하세요.")
        sys.exit(1)

    # PDF/DOCX 파일 검색
    files = find_regulation_files(new_dir)

    if not files:
        print(f"❌ {new_dir} 폴더에 처리할 PDF/DOCX 파일이 없습니다.")
        print()
        print("💡 사용 방법:")
        print(f"   1. 개정된 규정 파일(PDF 또는 DOC X)을 {new_dir}/ 폴더에 저장")
        print("   2. (선택) 파일명에 규정 코드 포함: <코드>_제목.pdf")
        print("   3. 이 스크립트 실행")
        sys.exit(0)

    print(f"발견한 파일: {len(files)}개")
    for f in files:
        print(f"  - {os.path.basename(f)}")
    print()

    # 처리
    success_count = 0
    failed_count = 0
    failed_files = []

    for i, file in enumerate(files, 1):
        print("=" * 80)
        print(f"[{i}/{len(files)}] {os.path.basename(file)}")
        print("=" * 80)

        try:
            result = subprocess.run(
                ['python3', 'scripts/smart_update.py', file],
                capture_output=False,
                text=True
            )

            if result.returncode == 0:
                success_count += 1
                print(f"✅ 성공")
            else:
                failed_count += 1
                failed_files.append(os.path.basename(file))
                print(f"❌ 실패")
        except Exception as e:
            failed_count += 1
            failed_files.append(os.path.basename(file))
            print(f"❌ 오류: {e}")

        print()

    # 결과 요약
    print("=" * 80)
    print("📊 처리 결과")
    print("=" * 80)
    print(f"✅ 성공: {success_count}개")
    print(f"❌ 실패: {failed_count}개")

    if failed_files:
        print()
        print("실패한 파일:")
        for f in failed_files:
            print(f"  - {f}")

    print()

    if success_count > 0:
        print("💡 다음 단계:")
        print("   git status                    # 변경된 파일 확인")
        print("   git add regulations/          # 모든 변경사항 추가")
        print(f"   git commit -m \"규정 일괄 개정 - {datetime.now().strftime('%Y-%m-%d')}\"")
        print("   git push")
        print()

        # 백업 파일 정리 안내
        print("💡 백업 파일 정리:")
        print("   find regulations -name '*.backup.*' -mtime +7 -delete  # 7일 이상 된 백업 삭제")

if __name__ == "__main__":
    main()
