#!/bin/bash
# 규정 파일을 업데이트하는 스크립트

set -e

CODE=$1           # 예: 3-1-9
SOURCE_FILE=$2    # 예: temp.md 또는 temp.docx
REVISION_NOTE=$3  # 예: "2025-01-24 개정"

if [ -z "$CODE" ] || [ -z "$SOURCE_FILE" ]; then
    echo "사용법: $0 <규정코드> <원본파일> [개정사유]"
    echo ""
    echo "예시:"
    echo "  $0 3-1-9 regulations_source/new/교직원포상규정.docx \"2025-01-24 개정\""
    echo "  $0 3-1-1 temp.md \"직제 개편\""
    exit 1
fi

if [ ! -f "$SOURCE_FILE" ]; then
    echo "❌ 원본 파일을 찾을 수 없습니다: $SOURCE_FILE"
    exit 1
fi

echo "🔍 규정 코드: $CODE"
echo "📁 원본 파일: $SOURCE_FILE"

# DOCX인 경우 MD로 변환
TEMP_MD="/tmp/regulation_temp_$$.md"
if [[ $SOURCE_FILE == *.docx ]]; then
    echo "🔄 DOCX → MD 변환 중..."
    ./scripts/convert_to_md.sh "$SOURCE_FILE" "$TEMP_MD"
    SOURCE_FILE="$TEMP_MD"
elif [[ $SOURCE_FILE == *.md ]]; then
    cp "$SOURCE_FILE" "$TEMP_MD"
else
    echo "❌ 지원하지 않는 파일 형식입니다. (.docx 또는 .md만 가능)"
    exit 1
fi

# 규정 파일 경로 찾기
TARGET_FILE=$(find . -name "${CODE}.md" -type f | grep -v archive | head -1)

if [ -z "$TARGET_FILE" ]; then
    echo "❌ 규정 파일을 찾을 수 없습니다: $CODE.md"
    echo ""
    echo "💡 현재 존재하는 규정 파일:"
    find . -name "*.md" -type f | grep -E "[0-9]-[0-9]-[0-9]\.md" | sort
    rm -f "$TEMP_MD"
    exit 1
fi

echo "🎯 대상 파일: $TARGET_FILE"

# 백업 생성
BACKUP_FILE="${TARGET_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
cp "$TARGET_FILE" "$BACKUP_FILE"
echo "💾 백업 생성: $BACKUP_FILE"

# 파일 업데이트
cp "$TEMP_MD" "$TARGET_FILE"
rm -f "$TEMP_MD"

echo "✅ 업데이트 완료!"
echo ""

# 규정 제목 추출
TITLE=$(head -n 1 "$TARGET_FILE" | sed 's/^#* *//')

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 Git 커밋 명령:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "git add \"$TARGET_FILE\""

if [ -n "$REVISION_NOTE" ]; then
    echo "git commit -m \"개정: $TITLE ($CODE) - $REVISION_NOTE\""
else
    echo "git commit -m \"개정: $TITLE ($CODE) - $(date +%Y-%m-%d)\""
fi

echo "git push"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 백업 파일을 삭제하려면: rm \"$BACKUP_FILE\""
