#!/usr/bin/env python3
"""
RAG 폴더 동기화 스크립트

regulations/ 폴더의 규정 파일들을 regulations_for_rag/ 폴더로 복사합니다.
파일명을 규정 코드(3-2-11.md)에서 한글 제목(보수지급규정.md)으로 변경합니다.
"""

import os
import json
import shutil
from pathlib import Path

def load_regulations_db(json_path='regulations.json'):
    """regulations.json 파일 로드"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['regulations']
    except Exception as e:
        print(f"❌ regulations.json 로드 실패: {e}")
        return None

def sync_rag_folder(regulations, output_dir='regulations_for_rag'):
    """RAG 폴더로 파일 동기화"""
    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)
    
    success_count = 0
    fail_count = 0
    skip_count = 0
    
    print(f"📂 {len(regulations)}개 규정 파일 동기화 중...")
    print("=" * 60)
    
    for reg in regulations:
        source_file = reg['path']
        
        # 한글 파일명 생성 (원본 제목 사용, normalized 말고)
        korean_filename = f"{reg['title']}.md"
        destination_file = os.path.join(output_dir, korean_filename)
        
        # 소스 파일 존재 확인
        if not os.path.exists(source_file):
            print(f"⚠️  소스 파일 없음: {source_file}")
            fail_count += 1
            continue
        
        try:
            # 파일 복사
            shutil.copy2(source_file, destination_file)
            print(f"✅ {reg['code']} → {korean_filename}")
            success_count += 1
        except Exception as e:
            print(f"❌ 복사 실패 ({reg['code']}): {e}")
            fail_count += 1
    
    return success_count, fail_count, skip_count

def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("🔄 RAG 폴더 동기화")
    print("=" * 60)
    print()
    
    # regulations.json 로드
    regulations = load_regulations_db()
    
    if not regulations:
        print("❌ regulations.json을 로드할 수 없습니다.")
        return 1
    
    print(f"📚 {len(regulations)}개 규정 로드됨")
    print()
    
    # 동기화 실행
    success, fail, skip = sync_rag_folder(regulations)
    
    # 결과 출력
    print()
    print("=" * 60)
    print("📊 동기화 완료")
    print("=" * 60)
    print(f"✅ 성공: {success}개")
    if fail > 0:
        print(f"❌ 실패: {fail}개")
    if skip > 0:
        print(f"⏭️  건너뜀: {skip}개")
    print()
    
    return 0 if fail == 0 else 1

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
