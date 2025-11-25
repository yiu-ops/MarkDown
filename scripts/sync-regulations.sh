#!/bin/bash
# regulations/ 폴더를 website/docs/로 동기화

set -e

echo "🔄 regulations/ → website/docs/ 동기화 중..."

# 기존 docs 폴더 백업 (처음에만)
if [ -d "website/docs.backup" ]; then
    echo "⚠️  백업이 이미 존재합니다."
else
    echo "💾 기본 docs 백업 중..."
    cp -r website/docs website/docs.backup
fi

# 기존 docs 폴더 제거
rm -rf website/docs

# regulations를 docs로 복사
cp -r regulations website/docs

echo "✅ 동기화 완료!"
echo "📊 통계:"
find website/docs -name "*.md" -type f | wc -l | xargs echo "  - Markdown 파일:"
