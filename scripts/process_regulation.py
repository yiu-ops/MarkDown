#!/usr/bin/env python3
"""
통합 규정 처리 스크립트

기능:
- PDF/DOCX 파일을 자동으로 분석
- 단일 규정인지 통합 문서(여러 규정)인지 자동 판단
- 적절한 처리 스크립트 자동 호출

사용법:
    python scripts/process_regulation.py <FILE_PATH>
    python scripts/process_regulation.py regulations_source/new/규정집.pdf
    python scripts/process_regulation.py regulations_source/new/규정집.docx
"""

import os
import sys
import json
import re
import subprocess
import tempfile
from pathlib import Path

# 프로젝트 루트로 이동
script_dir = Path(__file__).parent
project_root = script_dir.parent
os.chdir(project_root)

def load_regulations_db():
    """regulations.json 파일 로드"""
    json_path = project_root / 'regulations.json'
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['regulations']
    except Exception as e:
        print(f"❌ regulations.json 로드 실패: {e}")
        sys.exit(1)

def normalize_title(title):
    """제목 정규화 (공백 제거, 소문자 변환)"""
    return re.sub(r'[\s\.\·\-]', '', title).lower()

def convert_to_md(input_path):
    """PDF/DOCX를 임시 MD 파일로 변환"""
    # 파일 확장자 확인
    ext = os.path.splitext(input_path)[1].lower()
    
    temp_files_to_cleanup = []
    
    try:
        # PDF의 경우 DOCX를 중간 단계로 사용
        if ext == '.pdf':
            print(f"📄 PDF → DOCX → Markdown 변환 중 (더 나은 품질): {input_path}")
            
            # 1단계: PDF → DOCX (pdf2docx 패키지 사용)
            temp_docx = tempfile.NamedTemporaryFile(mode='w', suffix='.docx', 
                                                     delete=False, encoding='utf-8')
            temp_docx_path = temp_docx.name
            temp_docx.close()
            temp_files_to_cleanup.append(temp_docx_path)
            
            print("   1/2: PDF → DOCX 변환...")
            try:
                from pdf2docx import Converter
                cv = Converter(input_path)
                cv.convert(temp_docx_path)
                cv.close()
                print("   ✅ PDF → DOCX 변환 완료")
            except Exception as e:
                print(f"❌ PDF → DOCX 변환 실패: {e}")
                for f in temp_files_to_cleanup:
                    try:
                        os.unlink(f)
                    except:
                        pass
                sys.exit(1)
            
            # 2단계: DOCX → Markdown
            input_file = temp_docx_path
            input_format = 'docx'
            print("   2/2: DOCX → Markdown 변환...")
            
        elif ext == '.docx':
            print(f"📄 DOCX를 Markdown으로 변환 중: {input_path}")
            input_file = input_path
            input_format = 'docx'
        else:
            print(f"❌ 지원하지 않는 파일 형식: {ext}")
            print("   지원 형식: .pdf, .docx")
            sys.exit(1)
        
        # 임시 MD 파일 생성
        temp_md = tempfile.NamedTemporaryFile(mode='w', suffix='.md', 
                                               delete=False, encoding='utf-8')
        temp_md_path = temp_md.name
        temp_md.close()
        
        result = subprocess.run(
            ['pandoc', '-f', input_format, '-t', 'markdown', input_file, '-o', temp_md_path],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode != 0:
            print(f"❌ Pandoc 변환 실패: {result.stderr}")
            for f in temp_files_to_cleanup:
                try:
                    os.unlink(f)
                except:
                    pass
            sys.exit(1)
        
        # 중간 파일 정리
        for f in temp_files_to_cleanup:
            try:
                os.unlink(f)
            except:
                pass
            
        return temp_md_path
        
    except FileNotFoundError:
        print("❌ Pandoc이 설치되어 있지 않습니다.")
        print("   설치: https://pandoc.org/installing.html")
        for f in temp_files_to_cleanup:
            try:
                os.unlink(f)
            except:
                pass
        sys.exit(1)

def analyze_md_content(md_path, regulations):
    """MD 파일 내용을 분석하여 규정 개수 판단"""
    print("🔍 파일 내용 분석 중...")
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 제목 매핑 생성 (정규화된 제목 -> 원본 제목)
    title_map = {}
    for reg in regulations:
        normalized = normalize_title(reg['title'])
        title_map[normalized] = reg['title']
    
    lines = content.splitlines()
    found_titles = set()  # 중복 방지
    
    # 방법 1: Markdown 헤딩에서 찾기 (# 제목)
    for line in lines:
        if line.strip().startswith('#'):
            title = re.sub(r'^#+\s*', '', line.strip())
            normalized = normalize_title(title)
            if normalized in title_map:
                found_titles.add(title_map[normalized])
    
    # 방법 2: 일반 텍스트에서 규정 제목 매칭 (PDF 변환 후 헤딩이 없는 경우)
    if len(found_titles) < 3:
        print("   📝 헤딩에서 제목을 찾지 못해 전체 텍스트 검색 중...")
        for line in lines:
            line_normalized = normalize_title(line)
            # 라인이 규정 제목과 정확히 일치하거나 매우 유사한 경우
            for norm_title, orig_title in title_map.items():
                # 정확히 일치하거나 라인이 제목으로 끝나는 경우
                if norm_title == line_normalized:
                    found_titles.add(orig_title)
                # 라인 내에 제목이 포함된 경우 (짧은 라인만)
                elif len(line.strip()) < 80 and norm_title in line_normalized:
                    found_titles.add(orig_title)
    
    # 방법 3: 규정/규칙 패턴으로 추가 탐지
    if len(found_titles) < 3:
        print("   📝 규정 패턴 기반 검색 중...")
        # 일반적인 규정 패턴: "XXX규정", "XXX규칙", "XXX지침", "XXX정관", "XXX내규"
        reg_pattern = re.compile(r'^[\s\d\.\-]*(.{2,30}(?:규정|규칙|지침|정관|내규|행동강령))[\s]*$')
        for line in lines:
            match = reg_pattern.match(line.strip())
            if match:
                potential_title = match.group(1).strip()
                norm_potential = normalize_title(potential_title)
                if norm_potential in title_map:
                    found_titles.add(title_map[norm_potential])
    
    print(f"📊 발견된 규정 제목: {len(found_titles)}개")
    if found_titles:
        for title in list(found_titles)[:5]:  # 최대 5개만 표시
            print(f"   - {title}")
        if len(found_titles) > 5:
            print(f"   ... 외 {len(found_titles) - 5}개")
    
    return len(found_titles)

def process_single_regulation(input_path):
    """단일 규정 처리 (smart_update.py 호출)"""
    print("\n✅ 단일 규정으로 판단 → smart_update.py 실행")
    print("=" * 60)
    
    smart_update_script = project_root / 'scripts' / 'smart_update.py'
    
    result = subprocess.run(
        [sys.executable, str(smart_update_script), input_path],
        cwd=project_root
    )
    
    return result.returncode

def process_multiple_regulations(input_path):
    """통합 문서 처리 (split_and_update.py 호출)"""
    print("\n✅ 통합 문서(여러 규정)로 판단 → split_and_update.py 실행")
    print("=" * 60)
    
    # 1. PDF/DOCX → MD 변환
    temp_md_path = convert_to_md(input_path)
    
    # 2. split_and_update.py 실행
    split_update_script = project_root / 'scripts' / 'split_and_update.py'
    
    result = subprocess.run(
        [sys.executable, str(split_update_script), temp_md_path],
        cwd=project_root
    )
    
    # 3. 임시 파일 정리
    try:
        os.unlink(temp_md_path)
    except:
        pass
    
    return result.returncode

def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("🚀 규정 처리 통합 스크립트")
    print("=" * 60)
    
    # 인자 확인
    if len(sys.argv) < 2:
        print("\n사용법:")
        print(f"  python {sys.argv[0]} <FILE_PATH>")
        print("\n예시:")
        print(f"  python {sys.argv[0]} regulations_source/new/규정집.pdf")
        print(f"  python {sys.argv[0]} regulations_source/new/규정집.docx")
        print(f"  python {sys.argv[0]} regulations_source/new/교직원포상규정.pdf")
        sys.exit(1)
    
    input_path = sys.argv[1]
    
    # 파일 존재 확인
    if not os.path.exists(input_path):
        print(f"❌ 파일을 찾을 수 없습니다: {input_path}")
        sys.exit(1)
    
    # 파일 형식 확인
    ext = os.path.splitext(input_path)[1].lower()
    if ext not in ['.pdf', '.docx']:
        print(f"❌ 지원하지 않는 파일 형식: {ext}")
        print("   지원 형식: .pdf, .docx")
        sys.exit(1)
    
    print(f"📁 입력 파일: {input_path}")
    
    # regulations.json 로드
    regulations = load_regulations_db()
    print(f"📚 규정 데이터베이스: {len(regulations)}개 규정 로드됨")
    
    # PDF/DOCX → MD 변환 (분석용)
    temp_md_path = convert_to_md(input_path)
    
    # 내용 분석
    regulation_count = analyze_md_content(temp_md_path, regulations)
    
    # 임시 파일 정리
    try:
        os.unlink(temp_md_path)
    except:
        pass
    
    # 판단 및 처리
    if regulation_count >= 2:
        # 2개 이상 → 통합 문서
        return process_multiple_regulations(input_path)
    elif regulation_count == 1:
        # 1개 → 단일 규정
        return process_single_regulation(input_path)
    else:
        # 0개 → 매칭 실패, 단일 규정으로 간주 (smart_update가 제목 기반 매칭 시도)
        print("\n⚠️  regulations.json에서 매칭되는 제목을 찾지 못했습니다.")
        print("   단일 규정으로 간주하여 제목 기반 매칭을 시도합니다.")
        return process_single_regulation(input_path)

if __name__ == '__main__':
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
