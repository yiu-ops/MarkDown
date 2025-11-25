#!/usr/bin/env node
/**
 * regulations/ 폴더 구조를 분석하여 Docusaurus 사이드바 자동 생성
 */

const fs = require('fs');
const path = require('path');

// 한글 폴더명 → 표시명 매핑 (숫자 접두사 제거된 버전)
const folderNameMap = {
  '학교법인': '제1편 학교법인',
  '학칙': '제2편 학칙',
  '학사행정': '제3편 학사행정',
  '일반행정': '제1장 일반행정',
  '인사보수행정': '제2장 인사보수행정',
  '교무행정': '제3장 교무행정',
  '학생행정': '제4장 학생행정',
  '대학원': '제5장 대학원',
  '부속기관': '제4편 부속기관',
  '부설연구소': '제2장 부설연구소',
  '부설기관': '제3장 부설기관',
  '위원회': '제5편 위원회',
  '기타': '제6편 기타'
};

// MD 파일에서 제목 추출
function getTitleFromMd(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const firstLine = content.split('\n')[0];
    // 마크다운 헤더 제거
    const title = firstLine.replace(/^#+\s*/, '').trim();
    return title;
  } catch (error) {
    return null;
  }
}

// 디렉토리를 재귀적으로 스캔하여 사이드바 항목 생성
function generateSidebarItems(dir, basePath = '') {
  const items = [];

  try {
    const files = fs.readdirSync(dir).sort();

    for (const file of files) {
      const fullPath = path.join(dir, file);
      const stat = fs.statSync(fullPath);

      if (stat.isDirectory()) {
        // 디렉토리인 경우 - 카테고리로 추가
        const label = folderNameMap[file] || file;
        const subItems = generateSidebarItems(fullPath, path.join(basePath, file));

        if (subItems.length > 0) {
          items.push({
            type: 'category',
            label: label,
            collapsed: false, // 기본적으로 펼쳐진 상태
            items: subItems
          });
        }
      } else if (file.endsWith('.md')) {
        // MD 파일인 경우
        const docPath = path.join(basePath, file)
          .replace(/\.md$/, '')
          .replace(/\\/g, '/');

        // 파일에서 제목 추출
        const title = getTitleFromMd(fullPath);
        const fileCode = file.replace('.md', '');

        items.push({
          type: 'doc',
          id: docPath,
          label: title ? `${fileCode} ${title}` : fileCode
        });
      }
    }
  } catch (error) {
    console.error(`Error scanning ${dir}:`, error.message);
  }

  return items;
}

// 메인 실행
const docsDir = path.join(__dirname, '../website/docs');

console.log('📖 사이드바 생성 중...');
console.log(`📁 스캔 경로: ${docsDir}`);

const sidebarItems = generateSidebarItems(docsDir);

// sidebars.js 생성
const sidebarConfig = {
  regulationsSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: '🏠 홈'
    },
    ...sidebarItems
  ]
};

const outputPath = path.join(__dirname, '../website/sidebars.js');
const outputContent = `/**
 * 용인대학교 규정집 사이드바
 *
 * 자동 생성됨 - scripts/generate-sidebar.js
 * 수동 수정하지 마세요!
 */

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = ${JSON.stringify(sidebarConfig, null, 2)};

module.exports = sidebars;
`;

fs.writeFileSync(outputPath, outputContent);

console.log('✅ 사이드바 생성 완료!');
console.log(`📄 출력: ${outputPath}`);
console.log(`📊 총 ${sidebarItems.length}개 항목`);
