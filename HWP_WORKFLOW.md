# HWP 파일 → GitHub 업데이트 워크플로우

## 📋 상황 분석

- **규정 담당 부서**: HWP 파일로만 작업
- **개정 규정 배포**: HWP 형식
- **GitHub 저장소**: 마크다운(MD) 형식으로 관리

## 🔄 제안 워크플로우

### 방법 1: 수동 변환 (권장 - 가장 확실함)

```
개정된 HWP 파일 수령
    ↓
HWP를 DOCX로 변환 (한컴오피스 또는 온라인 변환기)
    ↓
DOCX를 MD로 변환 (pandoc)
    ↓
해당 규정 파일 업데이트 (예: 3-1-1.md)
    ↓
Git 커밋 및 푸시
```

**장점**: 변환 품질 확인 가능, 단계별 검증
**단점**: 수작업 필요

---

### 방법 2: 반자동화 스크립트 (권장)

전용 스크립트를 만들어 변환 과정 간소화

```bash
# 사용 예시
./scripts/update_regulation.sh 3-1-1 새로운규정.hwp "개정 사유"
```

**스크립트가 자동 수행:**
1. HWP → DOCX 변환 안내 (수동)
2. DOCX → MD 자동 변환
3. 해당 규정 파일 자동 업데이트
4. 메타데이터 자동 갱신
5. Git 커밋 템플릿 생성

---

### 방법 3: 전체 자동화 (고급, 선택사항)

GitHub에 전용 웹 인터페이스 구축

```
규정 담당자가 웹 페이지에서 HWP 업로드
    ↓
서버에서 자동 변환 (hwp2txt, pandoc)
    ↓
변환 결과 미리보기
    ↓
승인 후 자동 커밋
```

**장점**: 규정 담당자가 직접 업데이트 가능
**단점**: 초기 개발 비용 높음

---

## 🛠️ 실무 권장 방안: 방법 2 (반자동화)

### 단계별 가이드

#### Step 1: HWP 파일 준비
```
받은 파일: regulations_source/교직원포상규정_개정_20250124.hwp
```

#### Step 2: HWP → DOCX 변환

**옵션 A: 한컴오피스 사용 (Windows)**
- HWP 파일 열기 → 다른 이름으로 저장 → DOCX 선택

**옵션 B: 온라인 변환기 (추천)**
- https://www.zamzar.com/convert/hwp-to-docx/
- https://convertio.co/kr/hwp-docx/
- https://www.freeconvert.com/hwp-to-docx

**옵션 C: 리눅스 명령줄 도구**
```bash
# hwp5txt 도구 설치 (한글 hwp 파일 처리)
pip install olefile pyhwp

# 변환
hwp5txt 교직원포상규정_개정_20250124.hwp > temp.txt
```

#### Step 3: DOCX → MD 변환 (자동)

```bash
# 변환 스크립트 실행
./scripts/convert_to_md.sh regulations_source/교직원포상규정_개정_20250124.docx

# 또는 pandoc 직접 사용
pandoc -f docx -t markdown regulations_source/교직원포상규정_개정_20250124.docx -o temp.md
```

#### Step 4: 해당 규정 파일 업데이트

```bash
# 변환된 MD 파일을 해당 규정 파일로 복사
cp temp.md regulations/3-학사행정/1-일반행정/3-1-9.md

# 또는 스크립트 사용
./scripts/update_regulation.sh 3-1-9 temp.md "2025-01-24 개정"
```

#### Step 5: Git 커밋

```bash
git add regulations/3-학사행정/1-일반행정/3-1-9.md
git commit -m "개정: 교직원포상규정 (3-1-9) - 2025-01-24"
git push
```

---

## 📁 권장 디렉토리 구조

```
MarkDown/
├── regulations/              # MD 파일 (GitHub 관리)
│   ├── 3-학사행정/
│   │   └── 1-일반행정/
│   │       └── 3-1-9.md
│
├── regulations_source/       # 원본 파일 보관 (Git에서 제외 가능)
│   ├── hwp/                  # 받은 HWP 파일
│   │   └── 교직원포상규정_개정_20250124.hwp
│   ├── docx/                 # 변환된 DOCX
│   │   └── 교직원포상규정_개정_20250124.docx
│   └── history/              # 이전 버전 보관
│       └── 2024/
│
├── scripts/
│   ├── convert_to_md.sh      # DOCX → MD 변환
│   ├── update_regulation.sh  # 규정 업데이트 자동화
│   └── hwp_to_docx.sh        # HWP → DOCX 변환 안내
│
└── docs/
    └── HWP_WORKFLOW.md       # 이 문서
```

---

## 🔧 제공할 스크립트

### 1. convert_to_md.sh
```bash
#!/bin/bash
# DOCX를 MD로 변환

DOCX_FILE=$1
OUTPUT_MD=${2:-output.md}

pandoc -f docx -t markdown "$DOCX_FILE" -o "$OUTPUT_MD"
echo "✓ 변환 완료: $OUTPUT_MD"
```

### 2. update_regulation.sh
```bash
#!/bin/bash
# 규정 업데이트 자동화

CODE=$1           # 예: 3-1-9
SOURCE_FILE=$2    # 예: temp.md 또는 temp.docx
REVISION_NOTE=$3  # 예: "2025-01-24 개정"

# DOCX인 경우 MD로 변환
if [[ $SOURCE_FILE == *.docx ]]; then
    ./scripts/convert_to_md.sh "$SOURCE_FILE" temp.md
    SOURCE_FILE="temp.md"
fi

# 규정 파일 경로 찾기 (자동 매핑)
TARGET_FILE=$(find regulations -name "${CODE}.md")

if [ -z "$TARGET_FILE" ]; then
    echo "❌ 규정 파일을 찾을 수 없습니다: $CODE"
    exit 1
fi

# 파일 업데이트
cp "$SOURCE_FILE" "$TARGET_FILE"

# Git 커밋 템플릿 생성
TITLE=$(head -n 1 "$TARGET_FILE")
echo "✓ 업데이트 완료: $TARGET_FILE"
echo ""
echo "Git 커밋 명령:"
echo "git add $TARGET_FILE"
echo "git commit -m \"개정: $TITLE ($CODE) - $REVISION_NOTE\""
echo "git push"
```

### 3. batch_update.sh (여러 규정 한 번에 업데이트)
```bash
#!/bin/bash
# 여러 규정을 한 번에 업데이트

# regulations_source/new/ 폴더의 모든 DOCX 파일 처리
for docx in regulations_source/new/*.docx; do
    filename=$(basename "$docx" .docx)

    # 파일명에서 규정 코드 추출 (예: 3-1-9_교직원포상규정.docx)
    code=$(echo "$filename" | grep -oP '^\d+-\d+-\d+')

    if [ -n "$code" ]; then
        echo "처리중: $filename (코드: $code)"
        ./scripts/update_regulation.sh "$code" "$docx" "$(date +%Y-%m-%d) 개정"
    fi
done
```

---

## 🎯 가장 실용적인 방법 (단순화)

**규정 담당 부서에 요청할 사항:**
1. HWP 파일명에 규정 코드 포함해서 전달
   - 예: `3-1-9_교직원포상규정_20250124.hwp`
2. 가능하면 DOCX로도 함께 전달 (HWP 저장 시 DOCX도 함께 저장)

**GitHub 관리자 작업:**
1. 받은 파일을 `regulations_source/new/` 폴더에 저장
2. (HWP인 경우) 온라인 변환기로 DOCX 변환
3. 스크립트 실행: `./scripts/update_regulation.sh 3-1-9 파일.docx "개정사유"`
4. Git 푸시

**소요 시간**: 규정 1개당 2-3분

---

## 🚀 더 나아가기 (선택사항)

### 옵션 1: Dropbox/Google Drive 연동
```
규정 담당 부서가 공유 폴더에 HWP 업로드
    ↓
GitHub Actions가 자동 감지
    ↓
자동 변환 및 커밋
```

### 옵션 2: 이메일 자동화
```
규정 담당 부서가 특정 이메일로 HWP 첨부 발송
    ↓
서버가 이메일 감지 및 첨부파일 추출
    ↓
자동 변환 및 PR 생성
```

### 옵션 3: 웹 업로드 인터페이스
- 간단한 웹페이지 제작
- 규정 담당자가 직접 HWP 업로드
- 변환 결과 미리보기 후 승인

---

## 📝 .gitignore 설정

```gitignore
# 원본 파일은 Git에서 제외 (용량 절약)
regulations_source/hwp/
regulations_source/docx/

# 임시 파일
temp.md
temp.docx
*.tmp

# 한글 작업 파일
*.hwp
*.~hwp
```

---

## ❓ 의사결정 필요

1. **변환 방법**: 수동 vs 반자동 vs 전자동?
2. **원본 파일 보관**: HWP 원본도 Git에 포함? (용량 문제)
3. **규정 담당 부서 협조**: 파일명 규칙 적용 가능?
4. **변환 품질**: 변환 후 검토 프로세스 필요?

---

**지금 바로 시작하려면:**

1. `regulations_source/` 폴더 구조 생성
2. 기본 스크립트 3개 작성
3. 테스트: 샘플 HWP 파일로 전체 워크플로우 검증

어떻게 진행하시겠습니까?
