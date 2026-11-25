import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { RESUME_DOC } from '../data/resumeDoc'

// Email and resume pop-ups. Anything on the page can open them with openPanel('email') or openPanel('resume').
export const EMAIL = 'tahmidjalal8@gmail.com'
export const LINKEDIN = 'https://www.linkedin.com/in/tahmidjalal'
const RESUME_PDF = `${import.meta.env.BASE_URL}resume.pdf`

type Panel = 'email' | 'resume'
export function openPanel(p: Panel) {
  window.dispatchEvent(new CustomEvent('tj:panel', { detail: p }))
}

// A PDF embedded as a data: URL (double-click build) cannot be opened directly in a new tab,
// so it is turned into a temporary blob first.
async function pdfUrl(): Promise<string> {
  if (!RESUME_PDF.startsWith('data:')) return RESUME_PDF
  const blob = await (await fetch(RESUME_PDF)).blob()
  return URL.createObjectURL(new Blob([blob], { type: 'application/pdf' }))
}

function EmailPanel() {
  const [copied, setCopied] = useState(false)
  const copy = async () => {
    try {
      await navigator.clipboard.writeText(EMAIL)
    } catch {
      const t = document.createElement('textarea')
      t.value = EMAIL
      document.body.appendChild(t)
      t.select()
      document.execCommand('copy')
      t.remove()
    }
    setCopied(true)
    setTimeout(() => setCopied(false), 1800)
  }
  return (
    <div className="pop-email">
      <div className="pop-kicker">Get in touch</div>
      <h2 className="pop-title">Let’s talk</h2>
      <p className="pop-lead">Open to marketing roles in Metro Vancouver. The fastest way to reach me is email.</p>
      <button className="pop-address" onClick={copy} aria-label={`Copy ${EMAIL}`}>
        {EMAIL}
        <span className="pop-copy">{copied ? 'Copied' : 'Copy'}</span>
      </button>
      <div className="pop-actions">
        <a className="pop-btn primary" href={`mailto:${EMAIL}?subject=Hello%20TJ`}>
          Open in mail app
        </a>
        <a
          className="pop-btn"
          href={`https://mail.google.com/mail/?view=cm&to=${EMAIL}&su=Hello%20TJ`}
          target="_blank"
          rel="noopener noreferrer"
        >
          Write in Gmail
        </a>
        <a className="pop-btn" href={LINKEDIN} target="_blank" rel="noopener noreferrer">
          LinkedIn
        </a>
      </div>
    </div>
  )
}

function ResumePanel() {
  const r = RESUME_DOC
  const openPdf = async () => window.open(await pdfUrl(), '_blank', 'noopener')
  return (
    <div className="pop-resume">
      <div className="pop-resume-bar">
        <span className="pop-kicker">Resume</span>
        <div className="pop-actions">
          <a className="pop-btn primary" href={RESUME_PDF} download="TJ-Mohammed-Tahmid-Jalal-resume.pdf">
            Download PDF
          </a>
          <button className="pop-btn" onClick={openPdf}>
            Open PDF
          </button>
        </div>
      </div>
      <article className="cv">
        <header>
          <h2>{r.name}</h2>
          <p className="cv-line">{r.line}</p>
          <p className="cv-contact">
            <button className="cv-link" onClick={() => openPanel('email')}>{EMAIL}</button>
            <span> · </span>
            <a className="cv-link" href={LINKEDIN} target="_blank" rel="noopener noreferrer">linkedin.com/in/tahmidjalal</a>
          </p>
        </header>
        <p className="cv-summary">{r.summary}</p>
        <h3>Experience</h3>
        {r.jobs.map((j) => (
          <section key={j.org} className="cv-job">
            <div className="cv-job-head">
              <strong>{j.org}</strong>
              <span>{j.role}</span>
              <em>{j.when}</em>
            </div>
            <ul>
              {j.points.map((p) => (
                <li key={p}>{p}</li>
              ))}
            </ul>
          </section>
        ))}
        <h3>Skills</h3>
        <dl className="cv-skills">
          {r.skills.map(([k, v]) => (
            <div key={k}>
              <dt>{k}</dt>
              <dd>{v}</dd>
            </div>
          ))}
        </dl>
        <h3>Education and languages</h3>
        <p>{r.education}</p>
        <p>{r.languages}</p>
        <p className="cv-ref">{r.references}</p>
      </article>
    </div>
  )
}

export default function ContactModals() {
  const [panel, setPanel] = useState<Panel | null>(null)
  useEffect(() => {
    const on = (e: Event) => setPanel((e as CustomEvent<Panel>).detail)
    const key = (e: KeyboardEvent) => e.key === 'Escape' && setPanel(null)
    window.addEventListener('tj:panel', on)
    window.addEventListener('keydown', key)
    return () => {
      window.removeEventListener('tj:panel', on)
      window.removeEventListener('keydown', key)
    }
  }, [])
  useEffect(() => {
    document.documentElement.style.overflow = panel ? 'hidden' : ''
  }, [panel])
  return (
    <AnimatePresence>
      {panel && (
        <motion.div
          key="pop"
          className="pop-backdrop"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={() => setPanel(null)}
        >
          <motion.div
            className={`pop-card ${panel === 'resume' ? 'is-resume' : ''}`}
            role="dialog"
            aria-modal="true"
            aria-label={panel === 'email' ? 'Email TJ' : 'TJ resume'}
            initial={{ opacity: 0, y: 18, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 10, scale: 0.99 }}
            transition={{ duration: 0.32, ease: [0.22, 1, 0.36, 1] }}
            onClick={(e) => e.stopPropagation()}
          >
            <button className="pop-close" onClick={() => setPanel(null)} aria-label="Close">
              ✕
            </button>
            {panel === 'email' ? <EmailPanel /> : <ResumePanel />}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
