import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: '용인대학교 규정집',
  tagline: '용인대학교 제규정 통합 관리 시스템',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://parkseihuan.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/MarkDown/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'Parkseihuan', // Usually your GitHub org/user name.
  projectName: 'MarkDown', // Usually your repo name.

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  // Markdown configuration to handle legacy content
  markdown: {
    parseFrontMatter: async (params) => {
      const result = await params.defaultParseFrontMatter(params);
      return result;
    },
  },

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'ko',
    locales: ['ko'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.js',
          routeBasePath: 'docs',
          // 수정 링크 제거
          editUrl: undefined,
        },
        blog: false, // 블로그 기능 비활성화
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: '용인대학교 규정집',
      logo: {
        alt: '용인대학교 로고',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'regulationsSidebar',
          position: 'left',
          label: '📚 규정 보기',
        },
        {
          type: 'search',
          position: 'right',
        },
        {
          href: 'https://github.com/Parkseihuan/MarkDown',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: '규정집',
          items: [
            {
              label: '홈',
              to: '/docs/intro',
            },
            {
              label: '제1편 학교법인',
              to: '/docs/1-학교법인/1-0-1',
            },
            {
              label: '제3편 학사행정',
              to: '/docs/3-학사행정/1-일반행정/3-1-1',
            },
          ],
        },
        {
          title: '용인대학교',
          items: [
            {
              label: '대학 홈페이지',
              href: 'https://www.yongin.ac.kr',
            },
            {
              label: '포털',
              href: 'https://portal.yongin.ac.kr',
            },
          ],
        },
        {
          title: '기타',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/Parkseihuan/MarkDown',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} 용인대학교. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
