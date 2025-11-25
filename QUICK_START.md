# 빠른 시작 가이드 - 규정 업데이트 방법

## 🎯 개요

HWP 파일로 받은 개정 규정을 GitHub에 업데이트하는 방법입니다.

---

## 📝 방법 1: 단일 규정 업데이트 (가장 많이 사용)

### Step 1: HWP 파일을 DOCX로 변환

**온라인 변환기 사용 (추천)**
1. https://www.zamzar.com/convert/hwp-to-docx/ 접속
2. HWP 파일 업로드
3. DOCX 파일 다운로드

**또는 한컴오피스 사용**
- HWP 파일 열기 → 다른 이름으로 저장 → DOCX 선택

### Step 2: 변환된 DOCX 파일을 regulations_source/new/ 폴더에 저장

```bash
# 파일명 형식: <규정코드>_제목.docx
# 예시:
regulations_source/new/3-1-9_교직원포상규정.docx
```

### Step 3: 업데이트 스크립트 실행

```bash
./scripts/update_regulation.sh 3-1-9 regulations_source/new/3-1-9_교직원포상규정.docx "2025-01-24 개정"
```

### Step 4: Git 커밋 (스크립트가 안내하는 명령 실행)

```bash
git add <파일경로>
git commit -m "개정: 교직원포상규정 (3-1-9) - 2025-01-24 개정"
git push
```

**완료! 🎉**

---

## 📦 방법 2: 여러 규정 한 번에 업데이트

### Step 1: 모든 DOCX 파일을 regulations_source/new/ 폴더에 저장

```bash
regulations_source/new/
├── 3-1-9_교직원포상규정.docx
├── 3-1-1_직제규정.docx
└── 3-2-11_보수지급규정.docx
```

**중요**: 파일명 앞에 반드시 규정 코드 포함 (예: `3-1-9_`)

### Step 2: 일괄 처리 스크립트 실행

```bash
./scripts/batch_update.sh
```

스크립트가 자동으로:
- 모든 파일을 MD로 변환
- 해당 규정 파일 업데이트
- 처리된 파일을 history 폴더로 이동

### Step 3: Git 커밋

```bash
git status                    # 변경된 파일 확인
git add regulations/          # 모든 변경사항 추가
git commit -m "규정 일괄 개정 - 2025-01-24"
git push
```

---

## 🔍 규정 코드 찾기

규정 코드를 모르는 경우:

### 방법 1: 규정 제목으로 검색
```bash
find regulations -name "*.md" -exec grep -l "교직원포상규정" {} \;
```

### 방법 2: 모든 규정 목록 보기
```bash
find regulations -name "*.md" -type f | sort
```

### 방법 3: INDEX.md 파일 확인
```bash
cat docs/INDEX.md
```

---

## 🛠️ 문제 해결

### Q1: "규정 파일을 찾을 수 없습니다" 오류

**원인**: 규정 코드가 잘못되었거나 해당 규정이 아직 생성되지 않음

**해결**:
```bash
# 존재하는 모든 규정 확인
find regulations -name "*.md" | sort

# 새 규정인 경우 수동으로 파일 생성
mkdir -p regulations/적절한폴더/
cp temp.md regulations/적절한폴더/3-X-X.md
```

### Q2: DOCX 변환 품질이 낮음

**원인**: HWP → DOCX 변환 시 서식 손실

**해결**:
1. 다른 온라인 변환기 사용
2. 한컴오피스에서 직접 DOCX 저장
3. 변환 후 수동으로 MD 파일 정리

### Q3: 한글이 깨짐

**원인**: 인코딩 문제

**해결**:
```bash
# UTF-8로 변환
iconv -f euc-kr -t utf-8 원본.md > 변환.md
```

---

## 📋 체크리스트

업데이트 전 확인사항:

- [ ] HWP 파일을 DOCX로 변환했는가?
- [ ] 파일명에 규정 코드가 포함되어 있는가?
- [ ] regulations_source/new/ 폴더에 파일을 저장했는가?
- [ ] 규정 코드가 정확한가?

업데이트 후 확인사항:

- [ ] 변환된 MD 파일이 올바른가?
- [ ] Git 커밋 메시지가 명확한가?
- [ ] 백업 파일이 생성되었는가?
- [ ] 원격 저장소에 푸시했는가?

---

## 💡 팁

### 1. 파일명 규칙
```
좋은 예:
- 3-1-9_교직원포상규정_20250124.docx
- 3-2-11_보수지급규정.docx

나쁜 예:
- 교직원포상규정.docx  (규정 코드 없음)
- 포상규정_3-1-9.docx  (규정 코드가 앞에 없음)
```

### 2. 개정일 자동 추출

파일명에 날짜(YYYYMMDD)를 포함하면 자동 추출:
- `3-1-9_교직원포상규정_20250124.docx` → "2025-01-24 개정"

### 3. 백업 파일 관리

업데이트 시 자동으로 백업 파일이 생성됩니다:
- `3-1-9.md.backup.20250124_153045`

문제가 없으면 삭제:
```bash
find regulations -name "*.backup.*" -delete
```

### 4. 변환 전 미리보기

DOCX를 MD로 변환하고 확인한 후 업데이트:
```bash
./scripts/convert_to_md.sh 파일.docx temp.md
cat temp.md  # 확인
./scripts/update_regulation.sh 3-1-9 temp.md
```

---

## 📞 도움이 필요하면

1. **HWP_WORKFLOW.md**: 상세한 워크플로우 설명
2. **PROPOSAL.md**: 전체 시스템 설계
3. **스크립트 사용법**:
   ```bash
   ./scripts/update_regulation.sh              # 사용법 보기
   ./scripts/batch_update.sh                   # 사용법 보기
   ```

---

## 🚀 더 빠르게: 즐겨찾기 명령

자주 사용하는 명령을 alias로 등록:

```bash
# ~/.bashrc 또는 ~/.zshrc에 추가
alias reg-update='./scripts/update_regulation.sh'
alias reg-batch='./scripts/batch_update.sh'
alias reg-list='find regulations -name "*.md" | sort'
```

사용:
```bash
reg-update 3-1-9 파일.docx "개정사유"
reg-batch
reg-list
```
