import { motion } from 'framer-motion'
import { SOCIAL_ICONS } from './SocialIcons'
import { FOCUS_POINTS } from '../data/focusPoints'
import { openPanel } from './ContactModals'

const SOCIAL_LINKS = [
  { id: 'linkedin', label: 'LinkedIn', href: 'https://www.linkedin.com/in/tahmidjalal' },
  { id: 'mail', label: 'Email', href: 'mailto:tahmidjalal8@gmail.com' },
]

// 履历数据（双语）。英文为译稿，可按需润色。
interface ResumeGroup {
  heading?: string
  logo?: string
  logoImg?: string
  sub?: string
  link?: string
  items?: string[]
  links?: { id: string; label: string; href: string }[]
}
interface ResumeEntry {
  period: string
  place: string
  role?: string
  logo?: { src: string; alt: string }
  points?: string[]
  groups?: ResumeGroup[]
}
// Résumé entries. Each one lines up, in order, with a camera stop (focus-1 … focus-7)
// in your me.glb. Keep the count equal to FOCUS_POINTS in data/focusPoints.ts.
const RESUME_EN: { title: string; entries: ResumeEntry[] } = {
  title: 'Résumé',
  entries: [
    {
      period: '2022 – Now',
      place: 'Jaalik Tech × Reframes',
      role: 'Founder · digital marketing agency',
      points: [
        'Run paid Meta and TikTok campaigns for small client brands, using audience segmentation and A/B creative testing',
        'Build and maintain Shopify stores and websites with Reframes',
        'Produce social content end to end: strategy, shoot, edit and publishing',
      ],
    },
    {
      period: '2023 – 2025',
      place: 'Telus Communications',
      role: 'Area sales manager · Metro Vancouver',
      points: [
        'Closed 350+ security accounts through consultative, needs-based selling',
        'Served residential and business customers, recommending telecom and security solutions',
        'Consistently met sales targets',
      ],
    },
    {
      period: '2025 – 2026',
      place: 'Skechers',
      role: 'Product specialist · Metro Vancouver',
      points: [
        'Supported product launches through customer outreach and in-store brand messaging',
        'Helped shoppers in a concept store with product selection and presentation',
      ],
    },
    {
      period: '2026 – Now',
      place: 'Cloverdale Paint',
      role: 'Marketing coordinator · Surrey, BC · 82 stores',
      points: [
        'Grew Instagram and Facebook 348% with original, trend-based video, carousel and meme content',
        'Led the Colour of the Year 2027 colour edit booths: 2,500+ attendees in Vancouver and Toronto',
        'Created Canadian by Canadian and 30 Days of Made in Canada',
        'Run geofenced dealer campaigns and manage reputation for 82 locations',
      ],
      groups: [
        {
          heading: 'From my manager',
          items: [
            '“Tahmid stands out as one of the most resourceful and self-directed.”',
          ],
          sub: 'Kevin Skelly, Marketing Manager',
        },
      ],
    },
    {
      period: '2026 – Now',
      place: 'Boopdog',
      role: 'Social media manager',
      points: [
        'Own the brand’s Instagram: strategy, content calendar and publishing',
        'Grow reach and community with consistent, on-brand content',
      ],
    },
    {
      period: 'Ongoing',
      place: 'AI content production',
      role: 'ChatGPT · Claude · Gemini · Higgsfield · ElevenLabs',
      points: [
        'Built a Claude Code and Canva workflow that turns a 1,921-colour database into 4K palette videos',
        'LLM-assisted scripts, captions and campaign concepts',
        'Generative image, video and voice for social and paid creative',
      ],
    },
    {
      period: 'In progress',
      place: 'Simon Fraser University',
      role: 'Bachelor of Science, Information and Interactive Arts and Technology',
      groups: [
        {
          heading: 'Languages',
          items: ['Arabic · English · Bengali · Hindi · Urdu'],
        },
        {
          heading: 'Get in touch',
          items: ['tahmidjalal8@gmail.com'],
          links: SOCIAL_LINKS,
        },
      ],
    },
  ],
}
const RESUME: Record<'en' | 'zh', { title: string; entries: ResumeEntry[] }> = {
  en: RESUME_EN,
  zh: RESUME_EN,
}

// 履历条目依次对应 glb 里的聚焦锚点（相机停靠点），顺序须与 entries 一致。
// 名单是唯一真源，见 data/focusPoints.ts（Scene.tsx 也从那里取）。
const POINT_ORDER = FOCUS_POINTS

const EASE = [0.22, 1, 0.36, 1]
const containerV = {
  hidden: {},
  show: { transition: { staggerChildren: 0.09, delayChildren: 0.04 } },
}
const itemV = {
  hidden: { opacity: 0, y: 26 },
  show: { opacity: 1, y: 0, transition: { duration: 0.75, ease: EASE } },
}

function Group({ group }: { group: ResumeGroup }) {
  const heading = group.link ? (
    <a className="about-link" href={group.link} target="_blank" rel="noopener noreferrer">
      {group.heading}
    </a>
  ) : (
    <span>{group.heading}</span>
  )

  return (
    <motion.div className="tl-group" variants={itemV}>
      <div className="tl-group-head">
        {group.logoImg && (
          <span className="tl-group-logo">
            <img src={group.logoImg} alt={group.heading || ''} loading="lazy" />
          </span>
        )}
        {heading}
        {group.sub && <span className="tl-group-sub">{group.sub}</span>}
      </div>
      {group.items && (
        <ul className="tl-points">
          {group.items.map((it, i) => (
            <li key={i}>{it}</li>
          ))}
        </ul>
      )}
      {group.links && (
        <div className="tl-logos">
          {group.links.map((l) => {
            const Icon = SOCIAL_ICONS[l.id as keyof typeof SOCIAL_ICONS]
            return (
              <a
                key={l.id}
                className="tl-logo"
                href={l.href}
                {...(l.href.startsWith('mailto:')
                  ? { onClick: (e: { preventDefault: () => void }) => { e.preventDefault(); openPanel('email') } }
                  : { target: '_blank', rel: 'noopener noreferrer' })}
                aria-label={l.label}
                title={l.label}
              >
                <Icon />
              </a>
            )
          })}
        </div>
      )}
    </motion.div>
  )
}

function Entry({ entry, index }: { entry: ResumeEntry; index: number }) {
  return (
    <motion.div
      className="tl-entry"
      data-point={POINT_ORDER[index]}
      variants={containerV}
      initial="hidden"
      whileInView="show"
      viewport={{ once: true, margin: '-12% 0px -12% 0px' }}
    >
      <motion.span className="tl-dot" variants={itemV} aria-hidden="true" />
      {/* tl-body 包住文字内容（点保持在外做时间轴标记）：移动端可给它加卡片衬底，
          且它紧贴内容高度，不含 tl-entry 用于排布的大 padding。
          用普通 div（非 motion）：framer 变体经 React context 穿透它，叶子元素仍是
          tl-entry 的直接 stagger 子级，入场动画与包裹前完全一致。 */}
      <div className="tl-body">
        <motion.div className="tl-period" variants={itemV}>
          {entry.period}
        </motion.div>
        <motion.div className="tl-head" variants={itemV}>
          {entry.logo && (
            <span className="tl-logo-chip">
              <img src={entry.logo.src} alt={entry.logo.alt} loading="lazy" />
            </span>
          )}
          <h3 className="tl-place">{entry.place}</h3>
        </motion.div>
        {entry.role && (
          <motion.div className="tl-role" variants={itemV}>
            {entry.role}
          </motion.div>
        )}
        {entry.points && (
          <motion.ul className="tl-points" variants={itemV}>
            {entry.points.map((p, i) => (
              <li key={i}>{p}</li>
            ))}
          </motion.ul>
        )}
        {entry.groups && entry.groups.map((g, i) => <Group key={i} group={g} />)}
      </div>
    </motion.div>
  )
}

export default function Resume({ lang }: { lang: 'en' | 'zh' }) {
  const data = RESUME[lang]
  return (
    <section className="resume" lang={lang}>
      <motion.h2
        className="resume-title"
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: '-10% 0px' }}
        transition={{ duration: 0.7, ease: EASE }}
      >
        {data.title}
      </motion.h2>
      <div className="timeline">
        {data.entries.map((e, i) => (
          <Entry key={i} entry={e} index={i} />
        ))}
      </div>
    </section>
  )
}
