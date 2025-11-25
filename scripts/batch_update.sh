#!/bin/bash
# regulations_source/new/ 폴더의 모든 DOCX/MD 파일을 일괄 처리

set -e

NEW_DIR="regulations_source/new"

if [ ! -d "$NEW_DIR" ]; then
    echo "❌ $NEW_DIR 폴더가 없습니다."
    echo "💡 mkdir -p $NEW_DIR 명령으로 폴더를 생성하세요."
    exit 1
fi

# 처리할 파일 개수 확인
FILE_COUNT=$(find "$NEW_DIR" -type f \( -name "*.docx" -o -name "*.md" \) | wc -l)

if [ "$FILE_COUNT" -eq 0 ]; then
    echo "❌ $NEW_DIR 폴더에 처리할 파일이 없습니다."
    echo ""
    echo "💡 사용 방법:"
    echo "   1. 개정된 규정 파일을 $NEW_DIR/ 폴더에 저장"
    echo "   2. 파일명 형식: <규정코드>_제목.docx"
    echo "      예: 3-1-9_교직원포상규정_20250124.docx"
    echo "   3. 이 스크립트 실행"
    exit 0
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 일괄 업데이트 시작"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "처리할 파일: $FILE_COUNT 개"
echo ""

SUCCESS=0
FAILED=0

# regulations_source/new/ 폴더의 모든 DOCX/MD 파일 처리
for file in "$NEW_DIR"/*.docx "$NEW_DIR"/*.md; do
    # 파일이 실제로 존재하는지 확인 (glob 패턴이 매칭 안 되면 문자열 그대로 반환됨)
    [ -f "$file" ] || continue

    filename=$(basename "$file")
    filename_noext="${filename%.*}"

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "처리중: $filename"

    # 파일명에서 규정 코드 추출
    # 형식: 3-1-9_... 또는 3-1-9-... 또는 3_1_9...
    code=$(echo "$filename_noext" | grep -oP '^\d+-\d+-\d+' || echo "$filename_noext" | grep -oP '^\d+_\d+_\d+' | tr '_' '-' || echo "")

    if [ -z "$code" ]; then
        echo "⚠️  파일명에서 규정 코드를 추출할 수 없습니다: $filename"
        echo "   파일명을 '3-1-9_제목.docx' 형식으로 변경하세요."
        ((FAILED++))
        continue
    fi

    echo "   규정 코드: $code"

    # 개정일 추출 시도 (파일명에 날짜가 있으면)
    revision_date=$(echo "$filename_noext" | grep -oP '\d{8}' | sed 's/\([0-9]\{4\}\)\([0-9]\{2\}\)\([0-9]\{2\}\)/\1-\2-\3/')
    if [ -z "$revision_date" ]; then
        revision_date=$(date +%Y-%m-%d)
    fi

    # 규정 업데이트
    if ./scripts/update_regulation.sh "$code" "$file" "$revision_date 개정"; then
        echo "✅ 성공: $filename → $code.md"
        ((SUCCESS++))

        # 처리된 파일을 history로 이동
        mkdir -p "regulations_source/history/$(date +%Y)"
        mv "$file" "regulations_source/history/$(date +%Y)/"
    else
        echo "❌ 실패: $filename"
        ((FAILED++))
    fi
    echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 처리 결과"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 성공: $SUCCESS 개"
echo "❌ 실패: $FAILED 개"
echo ""

if [ "$SUCCESS" -gt 0 ]; then
    echo "💡 다음 단계:"
    echo "   git status                    # 변경된 파일 확인"
    echo "   git add regulations/          # 모든 변경사항 추가"
    echo "   git commit -m \"규정 일괄 개정 - $(date +%Y-%m-%d)\""
    echo "   git push"
fi
