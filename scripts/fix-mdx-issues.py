#!/usr/bin/env python3
"""
MDX 컴파일 오류를 자동으로 수정하는 스크립트

수정 항목:
1. Pandoc 속성 구문 제거 ({.underline}, {.class} 등)
2. HTML 태그 내 마크다운 구문 정리
3. 누락된 이미지 참조 제거
"""

import re
import os
from pathlib import Path

def fix_pandoc_attributes(content):
    """Pandoc 속성 구문 제거"""
    # {.underline}, {.class} 등 제거
    content = re.sub(r'\{\.[\w-]+\}', '', content)
    # {#id .class key=value} 형태도 제거
    content = re.sub(r'\{[#\.][\w\s="\'-]*\}', '', content)
    # {width="..." height="..."} 같은 이미지 속성 제거
    content = re.sub(r'\{[\w\s=".\-:]+\}', '', content)
    return content

def fix_html_markdown_mix(content):
    """HTML 태그 내 마크다운 구문 정리"""
    # <td>~~text~~</td> → <td>text</td> (strikethrough 제거)
    content = re.sub(r'<td>~~(.+?)~~</td>', r'<td>\1</td>', content)
    # <td>**text**</td> → <td>text</td> (bold 제거)
    content = re.sub(r'<td>\*\*(.+?)\*\*</td>', r'<td>\1</td>', content)
    # <td>*text*</td> → <td>text</td> (italic 제거)
    content = re.sub(r'<td>\*(.+?)\*</td>', r'<td>\1</td>', content)

    # HTML 태그에서 style 속성 제거 (React는 style을 객체로 기대함)
    # 모든 HTML 태그의 style 속성 제거
    content = re.sub(r'<(\w+)\s+style="[^"]*"([^>]*)>', r'<\1\2>', content)
    content = re.sub(r'<(\w+)\s+style=\'[^\']*\'([^>]*)>', r'<\1\2>', content)
    # 자동 닫기 태그도 처리
    content = re.sub(r'<(\w+)\s+style="[^"]*"\s*/>', r'<\1 />', content)
    content = re.sub(r'<(\w+)\s+style=\'[^\']*\'\s*/>', r'<\1 />', content)

    # HTML 태그 내의 ~ 문자를 HTML 엔티티로 변환 (strikethrough로 해석되지 않도록)
    def replace_tilde_in_tag(match):
        tag_content = match.group(0)
        # ~ 문자를 &#126;으로 변환
        return tag_content.replace('~', '&#126;')

    # <td>...</td>, <th>...</th> 등의 태그 내용 처리
    content = re.sub(r'<t[dh][^>]*>.*?</t[dh]>', replace_tilde_in_tag, content, flags=re.DOTALL)

    return content

def fix_broken_images(content):
    """누락된 이미지 참조 제거 또는 주석 처리"""
    # ![alt](media/image.wmf){width="..." height="..."} 형태를 주석으로 변환
    content = re.sub(
        r'!\[([^\]]*)\]\(media/[\w\.]+\)\{[^}]*\}',
        r'<!-- 이미지: \1 (원본 파일 누락) -->',
        content
    )
    # ![alt](media/image.wmf) 형태도 주석으로 변환 (속성 없는 경우)
    content = re.sub(
        r'!\[([^\]]*)\]\(media/[\w\.]+\)',
        r'<!-- 이미지: \1 (원본 파일 누락) -->',
        content
    )
    return content

def fix_acorn_expression_errors(content):
    """acorn 파서 오류 유발 패턴 제거"""
    # 중괄호가 포함된 표현식 이스케이프
    # 예: {value} → \{value\}
    lines = content.split('\n')
    fixed_lines = []
    in_code_block = False

    for line in lines:
        # 코드 블록 추적
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            fixed_lines.append(line)
            continue

        # 코드 블록 안이 아닐 때만 처리
        if not in_code_block:
            # 테이블이나 일반 텍스트에서 JSX로 오해될 수 있는 패턴 수정
            # 하지만 이미 {.class} 형태는 위에서 제거했으므로
            # 여기서는 남은 { } 패턴만 확인
            pass

        fixed_lines.append(line)

    return '\n'.join(fixed_lines)

def fix_markdown_file(filepath):
    """마크다운 파일 수정"""
    print(f"📝 수정 중: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 수정 적용
    content = fix_pandoc_attributes(content)
    content = fix_html_markdown_mix(content)
    content = fix_broken_images(content)
    content = fix_acorn_expression_errors(content)

    # 변경사항이 있을 때만 저장
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   ✅ 수정 완료")
        return True
    else:
        print(f"   ⏭️  변경사항 없음")
        return False

def main():
    """메인 실행"""
    regulations_dir = Path('/home/user/MarkDown/regulations')

    # 문제가 있는 것으로 확인된 파일들
    problem_files = [
        '3-학사행정/3-교무행정/3-3-5.md',
        '3-학사행정/2-인사보수행정/3-2-11.md',
        '3-학사행정/2-인사보수행정/3-2-17.md',
        '3-학사행정/2-인사보수행정/3-2-21.md',
        '3-학사행정/2-인사보수행정/3-2-28.md',
    ]

    print('🔧 MDX 컴파일 오류 자동 수정 시작...\n')

    fixed_count = 0
    for rel_path in problem_files:
        filepath = regulations_dir / rel_path
        if filepath.exists():
            if fix_markdown_file(filepath):
                fixed_count += 1
        else:
            print(f"⚠️  파일 없음: {filepath}")

    print(f'\n✨ 완료! {fixed_count}개 파일 수정됨')

    # 모든 마크다운 파일도 검사 (추가 문제 발견 가능)
    print('\n🔍 전체 마크다운 파일 검사 중...')
    all_md_files = list(regulations_dir.rglob('*.md'))
    additional_fixed = 0

    for filepath in all_md_files:
        rel_path = filepath.relative_to(regulations_dir)
        if str(rel_path) not in problem_files:
            if fix_markdown_file(filepath):
                additional_fixed += 1

    if additional_fixed > 0:
        print(f'\n🎯 추가로 {additional_fixed}개 파일 수정됨')
    else:
        print('\n✅ 다른 파일은 모두 정상입니다')

if __name__ == '__main__':
    main()
