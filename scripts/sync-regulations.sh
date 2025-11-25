#!/bin/bash
# regulations/ 폴더를 website/docs/로 동기화
# Docusaurus는 폴더명의 숫자 접두사를 자동 제거하므로, 복사 시 미리 제거

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
mkdir -p website/docs

# regulations 폴더 복사 (숫자 접두사 제거)
for dir in regulations/*/; do
    if [ -d "$dir" ]; then
        dirname=$(basename "$dir")
        # 숫자 접두사 제거 (예: "1-학교법인" → "학교법인")
        newname=$(echo "$dirname" | sed 's/^[0-9]*-//')

        # 하위 폴더가 있는 경우 재귀적으로 복사
        mkdir -p "website/docs/$newname"

        # 2단계 폴더 처리
        for subdir in "$dir"*/; do
            if [ -d "$subdir" ]; then
                subdirname=$(basename "$subdir")
                newsubname=$(echo "$subdirname" | sed 's/^[0-9]*-//')
                mkdir -p "website/docs/$newname/$newsubname"
                cp -r "$subdir"* "website/docs/$newname/$newsubname/" 2>/dev/null || true
            fi
        done

        # 1단계 폴더의 파일 복사
        cp "$dir"*.md "website/docs/$newname/" 2>/dev/null || true
    fi
done

# intro.md 복사
if [ -f "website/docs.backup/intro.md" ]; then
    cp website/docs.backup/intro.md website/docs/intro.md
else
    echo "# 용인대학교 규정집" > website/docs/intro.md
fi

echo "✅ 동기화 완료!"
echo "📊 통계:"
find website/docs -name "*.md" -type f | wc -l | xargs echo "  - Markdown 파일:"
