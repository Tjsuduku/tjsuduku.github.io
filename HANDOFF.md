# TJ 3D portfolio: handoff (state as of 2026-11-22)

## Goal
Scroll-driven 3D resume following Sen Zheng's open-source site (github.com/dayinji/sen-3d-resume, MIT) with TJ's own head, stickers and content. Hosted free on GitHub Pages. TJ pushes to GitHub himself.

## State: final build done
- Desktop and phone both work. Phone tested with a 390 x 844 touch emulation (no sideways scroll, face in the top half, text card below). Not tested on a real GPU or phone: open the live link on your own phone.
- Camera path is original (tools/character/camera_path.py). Lighting file is CC0 (Poly Haven). resume.pdf exists, email only.
- Boopdog entry is trimmed to Social media manager with two bullets. Hero label says TJ. SFU degree: Bachelor of Science, Information and Interactive Arts and Technology.
- npm run build passes. Double-click preview: index.html at the repo root (local only, not in git, under 25 MB).
- Docs: README.md, docs/PIPELINE.md, docs/EDIT-GUIDE.md, docs/GITHUB-PLAN.md, docs/APPROVALS-AND-LICENSES.md.
- Skill: tj-3d-portfolio (updated with this state).

## Works (2026-11-22)
- Rebuilt from TJ's final resume and Kevin's signed letter: 8 sections, 17 case studies (brief, what I did, result, number row).
- Covers and banners: handmade-style still-life art from Higgsfield (TJ approved, 50 credits used, about 2,896 left). Real photos can replace any of them.
- Email and Resume open pop-ups (ContactModals.tsx); closing call to action after Works; section intros (blurb) on each Works card; page title now TJ (Mohammed Tahmid Jalal).
- Real photos still needed: each case lists its slots (see docs/EDIT-GUIDE.md, Change Works). Empty slots are hidden on the live site.
- Kevin approved quoting him (per TJ): one line on the Cloverdale timeline card, one in the Toronto case, one in 30 Days. His phone, email and the line about the role ending are never shown.
- Timeline and resume.pdf now follow the final marketing resume. Degree stays BSc Information and Interactive Arts and Technology (TJ's correction); his PDF resumes still say BA Communication.

## Only open item before going public
Real work photos. Kevin's approval to quote him is confirmed by TJ; confirm he is also fine with the Cloverdale work and numbers shown. Email text is in docs/APPROVALS-AND-LICENSES.md. If slow, use "Take Cloverdale out" in docs/EDIT-GUIDE.md, publish, add back later.

## Smaller open items
- Telus, Skechers, Boopdog bullets were partly written by Claude: TJ to confirm wording.
- Real work images for case studies and numbers for 30 Days of Made in Canada, Ads Manager, BCAA (placeholders show until then).
- Boopdog sticker is soft: source PNG is 212 px wide. A larger file in source/logos/boopdog_original.png then run_all.sh fixes it.
- Check Higgsfield and Meshy plan terms allow portfolio use.
- Normal map skipped (seams). Side profile limited by the 3D model (a new Meshy model is a paid run, quote credits first).

## Rules TJ set (keep following)
- Brief and direct. Follow Sen's method. Small tweaks are OK.
- Character looks like the Higgsfield render: no skin tone change, no long neck, natural almond eyes, no smile.
- Quote Higgsfield credit cost before paid generation (about 2,950 credits left).
- Give a double-click index.html after each major step, under 25 MB.
- Email only, never the phone number.
- Only public or Kevin approved Cloverdale work. No internal sales numbers, customer names or ad account IDs.
- No song lyrics. TJ asked for a Kendrick Lamar line on the spin and was declined, including after "I have permission". SPIN_LINE in web/src/App.tsx holds an original line. TJ can type his own text there himself.
- Deliverable docs in plain text style, sentence case.

## Stops (Resume.tsx = focusPoints.ts = STK table = STOPS table)
1 Jaalik Tech x Reframes, 2 Telus, 3 Skechers, 4 Cloverdale Paint, 5 Boopdog, 6 AI content production, 7 Simon Fraser University (wide, SFU on the nose), then the Works spin with SPIN_LINE.

## Rebuild commands
    bash tools/character/run_all.sh                      character, stickers, camera into web/public/models/me.glb
    python3 tools/resume/build_resume_pdf.py             resume.pdf
    cd web && npm run dev                                live preview
    cd web && npm run build                              production build (web/dist)
    cd web && npx vite build -c vite.single.config.ts && cp dist-single/index.html ../index.html     double-click file

## GitHub
Create empty public repo, push, Settings then Pages then Source = GitHub Actions. Full steps: docs/GITHUB-PLAN.md.
