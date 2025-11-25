# 용인대학교 규정집 웹사이트 구축 로드맵

## 🎯 목표

HWP 파일로 관리되는 규정집을 **아름답고 검색 가능한 웹사이트**로 전환

---

## 📊 3가지 구현 옵션 상세 비교

### Option 1: Docusaurus (추천 ⭐⭐⭐⭐⭐)

**데모 사이트**: https://docusaurus.io/

#### 시스템 아키텍처
```
규정 담당자
    ↓ (웹 업로드)
웹 인터페이스 → GitHub → Docusaurus 빌드 → 웹사이트
    ↑ 드래그앤드롭      ↑ 자동             ↑ 자동         ↑ https://regulations.yongin.ac.kr
```

#### 장점
- ✅ **최고 수준의 UX**: Meta가 만든 현대적 디자인
- ✅ **강력한 검색**: Algolia 통합 (무료)
- ✅ **버전 관리**: 과거 규정 버전 자동 관리
- ✅ **다국어 지원**: 한국어/영어 동시 지원
- ✅ **MDX 지원**: 인터랙티브 요소 추가 가능
- ✅ **커뮤니티**: 대규모 사용자 커뮤니티

#### 실제 화면 구성 예시

**홈페이지:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  용인대학교 로고              [검색]  [규정보기]  [개정이력]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

      🎓 용인대학교 규정집

   모든 규정을 한 곳에서 쉽게 검색하세요

      [규정 검색하기]  [카테고리별 보기]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  최근 개정 규정
  • 교직원포상규정 (3-1-9) - 2025-01-24
  • 직제규정 (3-1-1) - 2025-02-06
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**규정 페이지:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[사이드바]                    [본문]

제1편 학교법인                 교직원포상규정
  1-0-1 정관
  1-0-2 시행세칙              제 1 장 총칙

제3편 학사행정                 제1조[목적] ...
  제1장 일반행정
    3-1-1 직제규정            [목차]
  ▼ 3-1-9 포상규정 ◀         - 제1장 총칙
    3-1-10 징계규정           - 제2장 포상의 종류

                              [하단]
                              • 개정일: 2025-01-24
                              • [PDF 다운로드]
                              • [변경 이력 보기]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 구현 단계
1. **Week 1**: Docusaurus 설치 및 기본 설정
2. **Week 2**: regulations/ → docs/ 마이그레이션
3. **Week 3**: 웹 업로드 인터페이스 개발
4. **Week 4**: 테스트 및 배포

#### 소요 시간
- **최소 버전** (Docusaurus만): 1-2일
- **완전 버전** (업로드 포함): 1주일

---

### Option 2: MkDocs Material (간단 ⭐⭐⭐⭐)

**데모 사이트**: https://squidfunk.github.io/mkdocs-material/

#### 시스템 아키텍처
```
규정 담당자 → GitHub → MkDocs 빌드 → GitHub Pages
```

#### 장점
- ✅ **초고속 설정**: 30분이면 완성
- ✅ **아름다운 테마**: Material Design
- ✅ **검색 내장**: 별도 설정 불필요
- ✅ **경량**: 빠른 빌드, 빠른 로딩
- ✅ **간단**: Python 지식만 있으면 OK

#### 단점
- ❌ **고급 기능 제한**: 버전 관리 약함
- ❌ **커스터마이징**: Docusaurus보다 제한적

#### 설정 파일 예시
```yaml
# mkdocs.yml
site_name: 용인대학교 규정집
site_url: https://yongin-regulations.github.io/

theme:
  name: material
  language: ko
  palette:
    primary: indigo
    accent: indigo
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - search.suggest
    - search.highlight

plugins:
  - search:
      lang: ko
  - pdf-export

nav:
  - 홈: index.md
  - 제1편 학교법인:
      - 1-0-1 정관: 1-학교법인/1-0-1.md
  - 제3편 학사행정:
      - 제1장 일반행정:
          - 3-1-1 직제규정: 3-학사행정/1-일반행정/3-1-1.md
          - 3-1-9 포상규정: 3-학사행정/1-일반행정/3-1-9.md
```

#### 구현 단계
1. **Day 1**: MkDocs 설치, 설정
2. **Day 2**: 배포 및 테스트

#### 소요 시간
- **1-2일**

---

### Option 3: Docsify (최고속 ⭐⭐⭐)

**데모 사이트**: https://docsify.js.org/

#### 시스템 아키텍처
```
규정 담당자 → GitHub → 즉시 배포 (빌드 없음!)
```

#### 장점
- ✅ **빌드 불필요**: Markdown 올리면 끝
- ✅ **즉시 반영**: 변경 즉시 웹사이트 업데이트
- ✅ **초간단**: index.html 하나면 됨
- ✅ **SPA**: 빠른 페이지 전환

#### 단점
- ❌ **SEO 약함**: 검색엔진 최적화 어려움 (규정집은 상관없음)
- ❌ **고급 기능 제한**

#### 설정 파일 예시
```html
<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>용인대학교 규정집</title>
  <link rel="stylesheet" href="//cdn.jsdelivr.net/npm/docsify@4/themes/vue.css">
</head>
<body>
  <div id="app"></div>
  <script>
    window.$docsify = {
      name: '용인대학교 규정집',
      repo: 'https://github.com/yongin/regulations',
      loadSidebar: true,
      subMaxLevel: 3,
      search: {
        placeholder: '규정 검색',
        noData: '검색 결과 없음',
        depth: 6
      }
    }
  </script>
  <script src="//cdn.jsdelivr.net/npm/docsify@4"></script>
  <script src="//cdn.jsdelivr.net/npm/docsify/lib/plugins/search.min.js"></script>
</body>
</html>
```

#### 구현 단계
1. **1시간**: index.html 생성, 배포

#### 소요 시간
- **1-2시간**

---

## 🥇 최종 추천

### **Docusaurus + 웹 업로드 인터페이스**

#### 이유
1. **미래 지향적**: 10년 후에도 사용 가능한 현대적 기술
2. **확장성**: 나중에 기능 추가 쉬움 (API, 알림, 승인 워크플로우 등)
3. **전문성**: 대학 규정집에 어울리는 전문적 외관
4. **검색**: 강력한 검색 기능으로 규정 찾기 쉬움
5. **버전 관리**: 과거 규정 조회 가능

---

## 🚀 구체적 구현 계획

### Phase 1: Docusaurus 기본 사이트 (Day 1-2)

```bash
# 1. 프로젝트 생성
cd /home/user/MarkDown
npx create-docusaurus@latest website classic --typescript

# 2. 폴더 구조
website/
├── docs/                    # regulations/ 복사
├── src/
│   └── pages/
│       └── index.tsx        # 홈페이지
├── docusaurus.config.js
└── sidebars.js

# 3. regulations 동기화 스크립트
cat > sync-regulations.sh << 'EOF'
#!/bin/bash
# regulations/ → website/docs/ 동기화
rsync -av --delete regulations/ website/docs/
EOF

chmod +x sync-regulations.sh

# 4. 로컬 테스트
cd website
npm install
npm start  # http://localhost:3000
```

### Phase 2: 자동 사이드바 생성 (Day 2)

```javascript
// scripts/generate-sidebar.js
const fs = require('fs');
const path = require('path');

function generateSidebar(dir, basePath = '') {
  const items = [];
  const files = fs.readdirSync(dir);

  for (const file of files) {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);

    if (stat.isDirectory()) {
      items.push({
        type: 'category',
        label: file,
        items: generateSidebar(fullPath, path.join(basePath, file))
      });
    } else if (file.endsWith('.md')) {
      const docPath = path.join(basePath, file).replace(/\.md$/, '');
      items.push(docPath);
    }
  }

  return items;
}

const sidebar = {
  regulations: generateSidebar('website/docs')
};

fs.writeFileSync(
  'website/sidebars.js',
  `module.exports = ${JSON.stringify(sidebar, null, 2)};`
);

console.log('✅ 사이드바 자동 생성 완료');
```

### Phase 3: 웹 업로드 인터페이스 (Day 3-4)

#### 간단한 버전: Vercel Function

```javascript
// api/upload.js (Vercel Serverless Function)
const { Octokit } = require("@octokit/rest");
const formidable = require('formidable');
const fs = require('fs');
const { exec } = require('child_process');

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // 1. 파일 업로드 처리
  const form = new formidable.IncomingForm();

  form.parse(req, async (err, fields, files) => {
    if (err) {
      return res.status(500).json({ error: '파일 업로드 실패' });
    }

    const { code, title, category, reason } = fields;
    const docxFile = files.file;

    // 2. DOCX → MD 변환
    const mdPath = `/tmp/${Date.now()}.md`;

    exec(`pandoc -f docx -t markdown "${docxFile.filepath}" -o "${mdPath}"`, async (error) => {
      if (error) {
        return res.status(500).json({ error: 'DOCX 변환 실패' });
      }

      const mdContent = fs.readFileSync(mdPath, 'utf8');

      // 3. GitHub에 업로드
      const octokit = new Octokit({
        auth: process.env.GITHUB_TOKEN
      });

      // regulations.json에서 매칭
      let targetPath;
      if (code) {
        // 코드 기반 매칭
        targetPath = `regulations/${category}/${code}.md`;
      } else {
        // 제목 기반 매칭 (regulations.json 활용)
        const regulationsDb = JSON.parse(
          fs.readFileSync('regulations.json', 'utf8')
        );
        const matched = regulationsDb.regulations.find(
          r => r.title.includes(title) || title.includes(r.title)
        );
        if (matched) {
          targetPath = matched.path;
        } else {
          return res.status(404).json({ error: '매칭되는 규정을 찾을 수 없습니다' });
        }
      }

      // 4. GitHub에 커밋
      try {
        await octokit.repos.createOrUpdateFileContents({
          owner: 'yongin',
          repo: 'regulations',
          path: targetPath,
          message: `개정: ${title} - ${reason}`,
          content: Buffer.from(mdContent).toString('base64'),
        });

        res.status(200).json({
          success: true,
          message: '규정 업데이트 완료',
          path: targetPath
        });
      } catch (error) {
        res.status(500).json({ error: 'GitHub 업로드 실패' });
      }

      // 5. 임시 파일 삭제
      fs.unlinkSync(mdPath);
    });
  });
}
```

#### 프론트엔드: React 업로드 페이지

```tsx
// upload-page/src/App.tsx
import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [code, setCode] = useState('');
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('');
  const [reason, setReason] = useState('');
  const [status, setStatus] = useState('');

  const { getRootProps, getInputProps } = useDropzone({
    accept: {
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    },
    onDrop: (acceptedFiles) => {
      setFile(acceptedFiles[0]);
    }
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!file) {
      alert('파일을 선택하세요');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('code', code);
    formData.append('title', title);
    formData.append('category', category);
    formData.append('reason', reason);

    setStatus('업로드 중...');

    try {
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData
      });

      const result = await response.json();

      if (result.success) {
        setStatus(`✅ ${result.message}`);
        // 폼 초기화
        setFile(null);
        setCode('');
        setTitle('');
        setReason('');
      } else {
        setStatus(`❌ ${result.error}`);
      }
    } catch (error) {
      setStatus(`❌ 오류: ${error.message}`);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: '50px auto', padding: 20 }}>
      <h1>📄 용인대학교 규정 업로드</h1>

      <form onSubmit={handleSubmit}>
        <div {...getRootProps()} style={{
          border: '2px dashed #ccc',
          padding: 40,
          textAlign: 'center',
          cursor: 'pointer',
          marginBottom: 20
        }}>
          <input {...getInputProps()} />
          {file ? (
            <p>✅ {file.name}</p>
          ) : (
            <p>DOCX 파일을 드래그하거나 클릭하세요</p>
          )}
        </div>

        <div style={{ marginBottom: 15 }}>
          <label>규정 코드 (선택):</label>
          <input
            type="text"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="예: 3-1-9"
            style={{ width: '100%', padding: 8 }}
          />
        </div>

        <div style={{ marginBottom: 15 }}>
          <label>규정 제목 (선택):</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="파일에 제목이 없으면 입력"
            style={{ width: '100%', padding: 8 }}
          />
        </div>

        <div style={{ marginBottom: 15 }}>
          <label>카테고리:</label>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            style={{ width: '100%', padding: 8 }}
            required
          >
            <option value="">선택하세요</option>
            <option value="1-학교법인">제1편 학교법인</option>
            <option value="3-학사행정/1-일반행정">제3편 > 제1장 일반행정</option>
            <option value="3-학사행정/2-인사보수행정">제3편 > 제2장 인사보수행정</option>
          </select>
        </div>

        <div style={{ marginBottom: 15 }}>
          <label>개정 사유:</label>
          <textarea
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            placeholder="예: 2025-01-24 개정"
            style={{ width: '100%', padding: 8, height: 80 }}
          />
        </div>

        <button type="submit" style={{
          width: '100%',
          padding: 15,
          backgroundColor: '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: 5,
          fontSize: 16,
          cursor: 'pointer'
        }}>
          업로드
        </button>
      </form>

      {status && (
        <div style={{
          marginTop: 20,
          padding: 15,
          backgroundColor: status.startsWith('✅') ? '#d4edda' : '#f8d7da',
          borderRadius: 5
        }}>
          {status}
        </div>
      )}
    </div>
  );
}

export default App;
```

### Phase 4: GitHub Actions 통합 (Day 5)

```yaml
# .github/workflows/deploy-docusaurus.yml
name: Docusaurus 빌드 및 배포

on:
  push:
    branches:
      - main
    paths:
      - 'regulations/**'
      - 'website/**'
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: 체크아웃
        uses: actions/checkout@v4

      - name: Node.js 설정
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: npm
          cache-dependency-path: website/package-lock.json

      - name: regulations/ → website/docs/ 동기화
        run: |
          rm -rf website/docs
          cp -r regulations website/docs

      - name: 사이드바 자동 생성
        run: |
          node scripts/generate-sidebar.js

      - name: 의존성 설치
        run: |
          cd website
          npm ci

      - name: Docusaurus 빌드
        run: |
          cd website
          npm run build

      - name: GitHub Pages 배포
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./website/build
          cname: regulations.yongin.ac.kr  # 커스텀 도메인 (선택)
```

---

## 📅 전체 일정

### Week 1: Docusaurus 사이트 구축
- ✅ Day 1-2: Docusaurus 설정, regulations 마이그레이션
- ✅ Day 3: 사이드바 자동 생성, 검색 설정
- ✅ Day 4: 디자인 커스터마이징 (로고, 색상 등)
- ✅ Day 5: GitHub Pages 배포, 도메인 연결

### Week 2: 웹 업로드 인터페이스
- ✅ Day 1-2: React 업로드 페이지 개발
- ✅ Day 3: Vercel Functions (백엔드) 개발
- ✅ Day 4: GitHub API 연동
- ✅ Day 5: 테스트 및 버그 수정

### Week 3: 테스트 및 문서화
- ✅ Day 1-2: 전체 시스템 통합 테스트
- ✅ Day 3: 사용자 매뉴얼 작성
- ✅ Day 4-5: 규정 담당 부서 교육

---

## 💰 예상 비용

| 항목 | 무료 옵션 | 유료 옵션 |
|------|----------|----------|
| **웹사이트 호스팅** | GitHub Pages (무료) | Vercel Pro ($20/월) |
| **업로드 서버** | Vercel Free (월 100GB) | Vercel Pro (무제한) |
| **검색** | Docusaurus 기본 (무료) | Algolia DocSearch (무료) |
| **도메인** | regulations.github.io | regulations.yongin.ac.kr ($10/년) |
| **빌드/배포** | GitHub Actions (무료) | - |
| **총 비용** | **$0/월** | **$20/월 + $10/년** |

**추천**: 무료 옵션으로 충분합니다!

---

## ✅ 체크리스트

구현 전 확인사항:

- [ ] GitHub Pages 활성화 (Settings → Pages)
- [ ] 커스텀 도메인 준비 (선택)
- [ ] Node.js 18+ 설치
- [ ] Pandoc 설치 (DOCX 변환용)
- [ ] GitHub Personal Access Token 생성 (웹 업로드용)

---

## 🎯 최종 결정

어떤 옵션을 선택하시겠습니까?

1. **Option 1**: Docusaurus 완전 버전 (웹 업로드 포함) - **추천!**
2. **Option 2**: Docusaurus 기본 버전 (업로드 나중에)
3. **Option 3**: MkDocs Material (빠르고 간단)
4. **Option 4**: Docsify (최고속)

선택해주시면 바로 구현 시작하겠습니다!
