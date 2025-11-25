# 용인대학교 규정집 관리 시스템

HWP 파일 기반의 규정집을 GitHub에서 체계적으로 관리하는 자동화 시스템입니다.

## 🌟 주요 기능

- ✅ **자동 변환**: DOCX → Markdown 자동 변환
- ✅ **스마트 매칭**: 규정 코드 또는 제목으로 자동 매칭
- ✅ **자동화**: GitHub Actions로 완전 자동화
- ✅ **버전 관리**: Git으로 모든 변경 이력 추적
- ✅ **백업**: 업데이트 전 자동 백업
- ✅ **유연성**: 규정 코드 변경에도 대응 가능

---

## 📁 폴더 구조

```
MarkDown/
├── regulations/              # 📚 모든 규정 파일 (Markdown)
│   ├── 1-학교법인/
│   ├── 2-학칙/
│   ├── 3-학사행정/
│   │   ├── 1-일반행정/     # 3-1-X.md
│   │   ├── 2-인사보수행정/  # 3-2-X.md
│   │   ├── 3-교무행정/      # 3-3-X.md
│   │   ├── 4-학생행정/
│   │   └── 5-대학원/
│   ├── 4-부속기관/
│   ├── 5-위원회/
│   └── 6-기타/
│
├── regulations_source/       # 원본 파일 보관소
│   ├── new/                 # 📥 새로운 DOCX 업로드 여기!
│   ├── hwp/                 # HWP 원본
│   ├── docx/                # DOCX 변환 파일
│   └── history/             # 처리 완료 파일
│       └── 2025/
│
├── scripts/                  # 🛠️ 자동화 스크립트
│   ├── smart_update.py      # 스마트 규정 업데이트
│   └── batch_smart_update.py # 일괄 처리
│
├── .github/workflows/        # GitHub Actions
│   └── auto-update-regulations.yml
│
├── regulations.json          # 📊 규정 매핑 데이터베이스
├── README.md                 # 이 파일
├── QUICK_START.md           # 빠른 시작 가이드
└── HWP_WORKFLOW.md          # 상세 워크플로우
```

---

## 🚀 빠른 시작 (3가지 방법)

### 방법 1: 완전 자동화 (추천 ⭐)

**규정 담당 부서에서 DOCX 파일을 받으면:**

```bash
# 1. DOCX 파일을 regulations_source/new/ 폴더에 저장
cp 교직원포상규정.docx regulations_source/new/

# 2. Git에 커밋 및 푸시
git add regulations_source/new/
git commit -m "규정 업로드: 교직원포상규정"
git push

# 3. GitHub Actions가 자동으로:
#    - DOCX → MD 변환
#    - 해당 규정 파일 업데이트
#    - 자동 커밋
```

**소요 시간**: 1분 (GitHub Actions 실행 시간 별도)

---

### 방법 2: 수동 실행

```bash
# regulations_source/new/에 DOCX 파일들을 저장한 후

# 일괄 처리
python3 scripts/batch_smart_update.py

# Git 커밋
git add regulations/
git commit -m "규정 업데이트 - $(date +%Y-%m-%d)"
git push
```

**소요 시간**: 2-3분

---

### 방법 3: 개별 파일 처리

```bash
# 단일 파일 처리
python3 scripts/smart_update.py regulations_source/new/교직원포상규정.docx

# 스크립트가 알려주는 Git 명령 실행
git add <파일>
git commit -m "..."
git push
```

---

## 🤖 스마트 매칭 시스템

### 규정 코드 기반 매칭

파일명에 규정 코드를 포함하면 자동으로 해당 규정에 매칭됩니다:

```
✅ 3-1-9_교직원포상규정.docx     → regulations/3-학사행정/1-일반행정/3-1-9.md
✅ 3-2-11_보수지급규정.docx      → regulations/3-학사행정/2-인사보수행정/3-2-11.md
```

### 제목 기반 매칭 (규정 코드가 없을 때)

파일명에 코드가 없어도 DOCX의 제목으로 자동 매칭:

```
✅ 교직원포상규정.docx           → 제목 추출 → "교직원포상규정" 검색 → 매칭
✅ 보수지급규정_개정.docx        → 제목 추출 → "보수지급규정" 검색 → 매칭
```

**유사도 매칭**: 60% 이상 유사한 제목도 매칭 가능 (확인 메시지 표시)

---

## 📊 regulations.json

모든 규정의 메타데이터를 관리하는 데이터베이스 파일:

```json
{
  "version": "1.0",
  "total_regulations": 35,
  "regulations": [
    {
      "code": "3-1-9",
      "title": "교직원포상규정",
      "title_normalized": "교직원포상규정",
      "category": "3-학사행정/1-일반행정",
      "path": "regulations/3-학사행정/1-일반행정/3-1-9.md",
      "filename": "3-1-9.md"
    }
  ]
}
```

**용도**:
- 스마트 매칭 시스템의 검색 데이터베이스
- 규정 목록 및 구조 파악
- 규정 코드 변경 시 중앙 관리

**업데이트**: 새 규정 추가 시 자동 업데이트 또는 수동으로 재생성:

```bash
# 수동 재생성
python3 << 'EOF'
import os, json, re

def extract_title_from_md(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return re.sub(r'^#+\s*', '', f.readline().strip())
    except:
        return None

def normalize_title(title):
    return re.sub(r'[\s\.\·\-]', '', title).lower()

regulations = []
for root, dirs, files in os.walk('regulations'):
    for file in files:
        if file.endswith('.md'):
            filepath = os.path.join(root, file)
            title = extract_title_from_md(filepath)
            if title:
                regulations.append({
                    "code": file.replace('.md', ''),
                    "title": title,
                    "title_normalized": normalize_title(title),
                    "category": root.replace('regulations/', ''),
                    "path": filepath,
                    "filename": file
                })

with open('regulations.json', 'w', encoding='utf-8') as f:
    json.dump({
        "version": "1.0",
        "last_updated": "$(date +%Y-%m-%d)",
        "total_regulations": len(regulations),
        "regulations": sorted(regulations, key=lambda x: x['code'])
    }, f, ensure_ascii=False, indent=2)
EOF
```

---

## 🔄 업데이트 워크플로우

### 전체 프로세스

```
HWP 파일 수령 (규정 담당 부서)
    ↓
HWP → DOCX 변환 (온라인 변환기 또는 한컴오피스)
    ↓
regulations_source/new/ 폴더에 업로드
    ↓
Git 커밋 및 푸시
    ↓
GitHub Actions 자동 실행
    ↓
스마트 매칭 시스템:
  1. 파일명에서 코드 추출
  2. 없으면 DOCX에서 제목 추출
  3. regulations.json에서 검색
  4. 매칭된 규정 찾기
    ↓
DOCX → MD 변환 (Pandoc)
    ↓
regulations/X-X/X-X-X.md 업데이트
    ↓
백업 파일 생성 (X-X-X.md.backup.YYYYMMDD_HHMMSS)
    ↓
원본 DOCX → regulations_source/history/ 이동
    ↓
Git 자동 커밋 및 푸시
    ↓
완료 ✅
```

---

## 🛠️ 유지보수

### 규정 코드 변경

규정 코드가 변경되면 `regulations.json`과 파일명을 업데이트:

```bash
# 1. 파일 이름 변경
mv regulations/3-학사행정/1-일반행정/3-1-9.md regulations/3-학사행정/1-일반행정/3-1-99.md

# 2. regulations.json 재생성
python3 scripts/regenerate_db.py  # 또는 위의 수동 재생성 코드

# 3. Git 커밋
git add regulations/ regulations.json
git commit -m "규정 코드 변경: 3-1-9 → 3-1-99"
git push
```

### 백업 파일 정리

```bash
# 7일 이상 된 백업 파일 삭제
find regulations -name '*.backup.*' -mtime +7 -delete

# 모든 백업 파일 목록 확인
find regulations -name '*.backup.*' -ls
```

### 아카이브 정리

```bash
# 오래된 아카이브 파일 정리 (예: 3년 이상)
find regulations_source/history -name '*.docx' -mtime +1095 -delete
```

---

## 📚 문서

- **[QUICK_START.md](./QUICK_START.md)** - 빠른 시작 가이드
- **[HWP_WORKFLOW.md](./HWP_WORKFLOW.md)** - HWP 파일 처리 상세 워크플로우
- **[PROPOSAL.md](./PROPOSAL.md)** - 시스템 설계 제안서

---

## ❓ FAQ

### Q1: HWP 파일을 직접 변환할 수 없나요?

현재는 DOCX 중간 단계가 필요합니다. HWP → MD 직접 변환 도구는 품질이 낮습니다.
추천: https://www.zamzar.com/convert/hwp-to-docx/

### Q2: 규정 코드가 자주 변경되는데 어떻게 하나요?

제목 기반 매칭을 사용하세요. 파일명에 코드 없이 업로드하면 제목으로 자동 매칭됩니다.

### Q3: GitHub Actions가 실행 안 됩니다.

1. `.github/workflows/auto-update-regulations.yml` 파일 확인
2. GitHub 저장소 Settings → Actions → 활성화 확인
3. 수동 실행: Actions 탭 → "자동 규정 업데이트" → Run workflow

### Q4: 변환 품질이 나쁩니다.

1. 다른 HWP → DOCX 변환기 사용
2. 한컴오피스에서 직접 DOCX 저장
3. 변환 후 MD 파일 수동 수정

### Q5: 새로운 규정을 추가하려면?

```bash
# 1. 적절한 폴더에 MD 파일 생성
mkdir -p regulations/적절한폴더/
echo "# 새 규정 제목" > regulations/적절한폴더/X-X-X.md

# 2. regulations.json 재생성
python3 scripts/regenerate_db.py

# 3. Git 커밋
git add regulations/ regulations.json
git commit -m "새 규정 추가: X-X-X"
git push
```

---

## 🔧 기술 스택

- **Pandoc**: DOCX → Markdown 변환
- **Python 3**: 자동화 스크립트
- **GitHub Actions**: CI/CD 자동화
- **Git**: 버전 관리

---

## 📞 문의

시스템 관련 문의:
- GitHub Issues 생성
- 또는 시스템 관리자에게 연락

---

## 📝 라이선스

용인대학교 내부 사용 목적

---

**마지막 업데이트**: 2025-01-24
