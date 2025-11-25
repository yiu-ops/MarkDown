#!/bin/bash
# DOCX를 MD로 변환하는 스크립트

set -e

DOCX_FILE=$1
OUTPUT_MD=${2:-output.md}

if [ -z "$DOCX_FILE" ]; then
    echo "사용법: $0 <docx파일> [출력md파일]"
    echo "예시: $0 규정.docx 3-1-9.md"
    exit 1
fi

if [ ! -f "$DOCX_FILE" ]; then
    echo "❌ 파일을 찾을 수 없습니다: $DOCX_FILE"
    exit 1
fi

echo "📄 변환 중: $DOCX_FILE → $OUTPUT_MD"

# pandoc으로 변환
pandoc -f docx -t markdown "$DOCX_FILE" -o "$OUTPUT_MD"

echo "✅ 변환 완료: $OUTPUT_MD"
echo ""
echo "📊 파일 정보:"
wc -l "$OUTPUT_MD" | awk '{print "  - 라인 수: " $1}'
du -h "$OUTPUT_MD" | awk '{print "  - 파일 크기: " $1}'
