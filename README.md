# 용인대학교 규정집 관리 시스템

HWP 파일 기반의 규정집을 GitHub에서 체계적으로 관리하는 자동화 시스템입니다.

## 🌟 주요 기능

- ✅ **완전 자동화**: 파일 업로드만으로 모든 처리 자동화
- ✅ **스마트 처리**: 단일/통합 문서 자동 판단 및 처리
- ✅ **자동 백업**: 업데이트 전 자동 백업 (7일 후 자동 정리)
- ✅ **버전 관리**: Git으로 모든 변경 이력 추적
- ✅ **RAG 지원**: AI 챗봇용 데이터 자동 동기화

---

## 🚀 초간단 사용법

### 1. 규정 파일 업로드

```bash
# PDF 권장! (HWP → PDF로 저장)
# PDF는 DOCX를 거쳐 Markdown으로 변환되어 구조가 더 잘 보존됩니다
cp 규정집.pdf regulations_source/new/

# DOCX도 여전히 지원
cp 규정집.docx regulations_source/new/

# Git 커밋 및 푸시
git add regulations_source/new/
git commit -m "규정 업로드"
git push
```

**끝!** GitHub Actions가 자동으로:
- PDF의 경우: **PDF → DOCX → Markdown** (더 나은 품질!)
- DOCX의 경우: **DOCX → Markdown**
- 단일 규정인지 통합 문서인지 판단
- 해당 규정 파일 업데이트
- 백업 생성 및 오래된 백업 정리
- regulations.json 자동 재생성
- RAG 폴더 동기화
- 자동 커밋 및 푸시

### 2. 수동 실행 (선택사항)

```bash
# 통합 스크립트로 한 번에 처리
python scripts/process_regulation.py regulations_source/new/규정집.docx

# regulations.json 재생성
python scripts/regenerate_regulations_db.py

# RAG 폴더 동기화
python scripts/sync_rag_folder.py
```

---

## 📁 핵심 폴더 구조

```
MarkDown/
├── regulations/              # 📚 모든 규정 파일 (Markdown)
│   ├── 1-학교법인/
│   └── 3-학사행정/
│       ├── 1-일반행정/
│       ├── 2-인사보수행정/
│       └── 3-교무행정/
│
├── regulations_source/       # 원본 파일
│   └── new/                 # 📥 새 DOCX 업로드 여기!
│
├── regulations_for_rag/      # 🤖 RAG용 한글 파일명
│
├── scripts/                  # 🛠️ 자동화 스크립트
│   ├── process_regulation.py           # 통합 처리 스크립트
│   ├── regenerate_regulations_db.py    # DB 재생성
│   └── sync_rag_folder.py              # RAG 동기화
│
└── regulations.json          # 📊 규정 매핑 데이터베이스
```

---

## 🔧 시스템 개선사항 (2026-02-13)

### ✨ 새로운 기능

1. **통합 처리 스크립트** (`process_regulation.py`)
   - 단일 규정 / 통합 문서 자동 판단
   - 적절한 처리 방법 자동 선택
   - **하나의 명령으로 모든 파일 처리 가능**

2. **자동 백업 관리**
   - 7일 이상 된 백업 파일 자동 삭제
   - 공간 절약 및 관리 부담 최소화

3. **regulations.json 자동 재생성**
   - 규정 처리 후 자동으로 DB 업데이트
   - 수동 관리 불필요

4. **RAG 폴더 자동 동기화**
   - 규정 코드 파일명 → 한글 제목 파일명
   - AI 챗봇/검색 시스템 연동 간편화

5. **GitHub Actions 개선**
   - 모든 자동화 기능 통합
   - 파일 업로드만으로 완전 자동 처리

---

## 📚 상세 문서

- **[HWP_WORKFLOW.md](./HWP_WORKFLOW.md)** - HWP 파일 처리 상세 가이드
- **[QUICK_START.md](./QUICK_START.md)** - 빠른 시작 가이드 (상세)
- **[PROPOSAL.md](./PROPOSAL.md)** - 시스템 설계 제안서

---

## ❓ 자주 묻는 질문

### Q: PDF와 DOCX 중 어떤 것을 사용해야 하나요?

### Q: 단일 규정과 통합 문서를 어떻게 구분하나요?

A: **PDF를 권장합니다!** 
- PDF → DOCX → Markdown 경로로 변환되어 구조가 더 잘 보존됩니다
- HWP 파일을 한컴오피스에서 PDF로 직접 저장하세요
- DOCX도 여전히 지원하지만, PDF가 표와 서식을 더 잘 유지합니다

### Q: HWP 파일을 어떻게 변환하나요?

A: **한컴오피스에서 PDF로 저장하세요:**
1. HWP 파일 열기
2. 파일 → 다른 이름으로 저장 → PDF
3. "텍스트 선택 가능" 옵션 활성화
4. PDF 파일을 regulations_source/new/에 업로드

A: **자동으로 판단합니다!** `process_regulation.py` 스크립트가 파일을 분석하여:
- 2개 이상의 규정 제목 발견 → 통합 문서로 처리
- 1개 이하 → 단일 규정으로 처리

### Q: 백업 파일이 너무 많이 쌓이지 않나요?

A: **자동으로 정리됩니다!** 7일 이상 된 백업 파일은 자동 삭제됩니다.

### Q: regulations.json은 언제 업데이트하나요?

A: **자동으로 업데이트됩니다!** 규정 처리 후 자동으로 재생성됩니다.

### Q: RAG 폴더는 무엇인가요?

A: AI 챗봇이나 검색 시스템에서 사용하기 쉽도록 규정 파일을 한글 제목으로 복사한 폴더입니다.
- `3-2-11.md` → `보수지급규정.md`

---

## 🔧 기술 스택PDF → DOCX → Markdown 변환 (최적 품질)
- **Python 3**: 자동화 스크립트
- **GitHub Actions**: CI/CD 완전 자동화
- **Git**: 버전 관리

---

## 📝 변경 이력

### 2026-02-13 (v2)
- ✨ **PDF → DOCX → Markdown 2단계 변환** (품질 개선!)
- ✨ PDF 직접 지원 (HWPX 구조 손실 문제 해결)
- 📚 PDF 사용 권장 (표와 서식 더 잘 보존)

### 2026-02-13 (v1)

### 2026-02-13
- ✨ 통합 처리 스크립트 추가
- ✨ 자동 백업 관리 기능
- ✨ regulations.json 자동 재생성
- ✨ RAG 폴더 자동 동기화
- ✨ GitHub Actions 개선

### 2025-01-24
- 초기 시스템 구축
- 스마트 매칭 시스템
- 기본 자동화 기능

---

**마지막 업데이트**: 2026-02-13
