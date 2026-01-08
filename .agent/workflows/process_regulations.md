---
description: Process archive regulation file (docx) to update individual regulation markdown files
---

# 규정집 아카이브 처리 및 업데이트 워크플로우

이 워크플로우는 `archive` 폴더에 업로드된 통합 규정집 파일(`.docx`)을 처리하여 개별 규정 파일들을 자동으로 업데이트합니다.

## 사전 준비

1. **Pandoc 설치 확인**: 시스템에 Pandoc이 설치되어 있어야 합니다.
2. **파일 준비**: 최신 규정집 파일(`.docx`)을 `d:\Github\MarkDown\MarkDown\archive` 폴더에 복사하세요.

## 실행 방법

터미널에서 다음 명령어를 실행하세요:

```powershell
# 프로젝트 루트로 이동
cd d:\Github\MarkDown\MarkDown

# 처리 스크립트 실행
.\scripts\process_archive.ps1
```

## 처리 과정

1. **파일 감지**: `archive` 폴더에서 가장 최근에 수정된 `.docx` 파일을 찾습니다.
2. **변환**: Pandoc을 사용하여 `.docx`를 `output.md`로 변환합니다.
3. **분리 및 업데이트**:
   - `output.md`를 분석하여 개별 규정 단위로 분리합니다.
   - 기존 규정 파일과 비교하여 변경 사항이 있는 경우에만 업데이트합니다.
   - 기존 파일은 `.backup` 파일로 백업됩니다.
4. **리포트**: 변경 사항이 감지되면 `update_report.html` 파일이 생성되고 자동으로 열립니다.

## 문제 해결

- **Pandoc 오류**: Pandoc이 설치되어 있는지 확인하세요 (`pandoc --version`).
- **규정 미감지**: `regulations.json`에 등록된 규정 제목과 문서 내의 제목이 일치하는지 확인하세요.
