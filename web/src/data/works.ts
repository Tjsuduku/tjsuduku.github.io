// 作品集数据（双语）。5 大板块 → 点击展开作品详情。
// 纯数据驱动：增删板块 / 作品只改本文件，Works.jsx 仅负责渲染。
//
// 板块字段：
//   id        唯一标识（用于 framer layoutId 共享元素动画）
//   no        编号 '01'…'05'
//   title     板块标题
//   tagline   索引行右侧一句话
//   items[]   扁平作品列表：{ name, meta?, tags?, link? }
//             点击 item 弹出全屏详情，可补充可选媒体/文案字段：
//             { image?, video?, year?, desc? }（缺省时媒体用占位、简介回退 meta/标签）
//   groups[]  分组作品（与 items 二选一）：{ heading, items: string[] }
//   awards[]  奖项 chip（可选）
//   footer    底部技术/备注一行（可选）

export interface WorkListItem {
  name: string
  meta?: string
  tags?: string[]
  link?: string
  slug?: string
}

export interface WorkGroup {
  heading: string
  items: string[]
}

export interface WorkSection {
  id: string
  no: string
  title: string
  tagline: string
  blurb?: string
  items?: WorkListItem[]
  groups?: WorkGroup[]
  awards?: string[]
  footer?: string
}

export interface WorksLang {
  title: string
  closeLabel: string
  openLabel: string
  hint: string
  awardsLabel: string
  visitLabel: string
  detailPlaceholder: string
  phImageLabel: string
  phButtonLabel: string
  countLabel: (n: number) => string
  sections: WorkSection[]
}

// Works shown after the 360 spin. Every item with a slug opens src/content/works/<slug>.md.
// Covers and banners are drawn in code (tools/works-art), not AI. Real photos go in public/works/<slug>/.
const WORKS_EN: WorksLang = {
  title: 'Works',
  closeLabel: 'Back',
  openLabel: 'Explore',
  hint: 'Keep scrolling',
  awardsLabel: 'Highlights',
  visitLabel: 'View',
  detailPlaceholder: 'Case study coming soon.',
  phImageLabel: 'Image / Video',
  phButtonLabel: 'Link',
  countLabel: (n) => `${n} projects`,
  sections: [
    {
      id: 'events',
      no: '01',
      title: 'Events',
      tagline: 'Colour of the Year 2027 · 2,500+ attendees',
      blurb: "Cloverdale's Colour of the Year 2027 launch, built as colour edit booths where designers bring their clients. I led the creative and ran both cities on site.",
      items: [
        { name: 'Colour edit booth · Vancouver', meta: '1,000+ attendees', tags: ['Event marketing', 'Creative lead'], slug: 'coty-vancouver' },
        { name: 'Toronto launch, run on site', meta: '1,500+ attendees', tags: ['Product launch', 'Travelled to run it'], slug: 'coty-toronto' },
      ],
      awards: ['Worked directly with the president and CEO'],
    },
    {
      id: 'campaigns',
      no: '02',
      title: 'Campaigns',
      tagline: 'Buy Canadian · Partnerships',
      blurb: 'Two buy-Canadian campaigns I came up with, plus a partnership with BCAA. Built to reach people who never think about paint.',
      items: [
        { name: 'Canadian by Canadian', meta: 'Reached beyond the paint industry', tags: ['Own concept'], slug: 'canadian-by-canadian' },
        { name: '30 Days of Made in Canada', meta: '30 businesses · November', tags: ['Own concept', 'Web', 'Social'], slug: 'made-in-canada' },
        { name: 'BCAA Fan Club VIP', meta: 'Partnership + member email', tags: ['Partnership', 'Email'], slug: 'bcaa' },
      ],
    },
    {
      id: 'social',
      no: '03',
      title: 'Social',
      tagline: '348% Instagram + Facebook growth',
      blurb: 'Organic social for a paint brand with 82 stores: video first, trend-led, planned on a calendar. Plus three LinkedIn pages for three professional audiences.',
      items: [
        { name: 'Instagram and Facebook growth', meta: '348%', tags: ['Organic social'], slug: 'social-growth' },
        { name: 'Top posts', meta: '50K to 100K+ views', tags: ['Video', 'Carousel', 'Meme'], slug: 'top-reels' },
        { name: 'Three LinkedIn pages', meta: '~12K followers', tags: ['Industrial', 'Corporate', 'Specifier'], slug: 'linkedin-pages' },
      ],
      footer: 'Formats: reels · carousels · memes · content calendars',
    },
    {
      id: 'paid',
      no: '04',
      title: 'Paid and Dealer',
      tagline: 'Meta Ads · Geofencing · Retargeting',
      blurb: 'Meta campaigns for authorized dealers across Canada, geofenced and targeted by location, age and job title, on small budgets tuned for cost per click.',
      items: [
        { name: 'Geofenced dealer campaigns', meta: 'Budgets around $2,000', tags: ['Meta Ads', 'Geofencing'], slug: 'dealer-campaigns' },
        { name: 'Ontario dealer awareness', meta: '$500 / month', tags: ['Dealer marketing', 'Community'], slug: 'global-building-supplies' },
      ],
      footer: 'Targeting: location · age · job title · CPC and CPM optimization',
    },
    {
      id: 'reputation',
      no: '05',
      title: 'Reputation',
      tagline: '82 locations · 80–150 reviews a week',
      blurb: 'Every Google review across 82 stores, answered every week, with complaints followed up with stores and HR until they are resolved.',
      items: [
        { name: 'Google review management', meta: '80–150 a week', tags: ['Google Business Profile'], slug: 'reputation' },
        { name: 'Turning launch criticism into content', meta: 'Negative to positive', tags: ['Community management'], slug: 'feedback-to-content' },
      ],
    },
    {
      id: 'web',
      no: '06',
      title: 'Web and Content',
      tagline: 'Website · intranet · SEO · labels',
      blurb: 'The owned channels behind every campaign: website, staff intranet, SEO blog, monthly sales and product labels.',
      items: [
        { name: 'Website, intranet and SEO blogs', meta: 'Sitefinity CMS', tags: ['Web', 'SEO', 'Labels'], slug: 'web-content' },
      ],
      footer: 'Also: monthly sale campaigns · product labels · video production and editing',
    },
    {
      id: 'ai',
      no: '07',
      title: 'AI Production',
      tagline: 'Workflow automation · generative content',
      blurb: 'AI built into the work, not instead of it: an automated colour-to-video pipeline, and AI-assisted scripts, visuals and sound.',
      items: [
        { name: 'Colour database to 4K palette videos', meta: '1,921 colours', tags: ['Claude Code', 'Canva'], slug: 'ai-automation' },
        { name: 'AI in everyday content', meta: 'Brief to finished asset', tags: ['ChatGPT', 'Claude', 'Gemini'], slug: 'ai-content' },
      ],
      footer: 'Tools: ChatGPT · Claude · Claude Code · Gemini · Higgsfield · ElevenLabs · Canva · Adobe Creative Suite',
    },
    {
      id: 'agency',
      no: '08',
      title: 'Agency and Clients',
      tagline: 'Jaalik Tech × Reframes · Boopdog',
      blurb: 'My own agency since 2022 and client work on the side: paid social, Shopify stores and Instagram for small brands.',
      items: [
        { name: 'Jaalik Tech × Reframes', meta: 'Since 2022', tags: ['Paid social', 'Shopify'], slug: 'jaalik-reframes' },
        { name: 'Boopdog', meta: 'Social media manager', tags: ['Instagram'], slug: 'boopdog' },
      ],
    },
  ],
}

export const WORKS: Record<'zh' | 'en', WorksLang> = {
  en: WORKS_EN,
  zh: WORKS_EN,
}

// Section covers (left image of each card), drawn by tools/works-art. A missing file falls back to a numbered panel.
export const SECTION_COVERS: Record<string, string> = {
  events: `${import.meta.env.BASE_URL}works/covers/events.jpg`,
  campaigns: `${import.meta.env.BASE_URL}works/covers/campaigns.jpg`,
  social: `${import.meta.env.BASE_URL}works/covers/social.jpg`,
  paid: `${import.meta.env.BASE_URL}works/covers/paid.jpg`,
  reputation: `${import.meta.env.BASE_URL}works/covers/reputation.jpg`,
  web: `${import.meta.env.BASE_URL}works/covers/web.jpg`,
  ai: `${import.meta.env.BASE_URL}works/covers/ai.jpg`,
  agency: `${import.meta.env.BASE_URL}works/covers/agency.jpg`,
}

// 统计一个板块的作品数（items 或 groups 求和），用于索引行 hover 显示
export function sectionCount(section: WorkSection): number {
  if (section.items) return section.items.length
  if (section.groups) return section.groups.reduce((n, g) => n + g.items.length, 0)
  return 0
}
