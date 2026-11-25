# TJ 3D resume

Scroll-driven 3D portfolio for TJ (Mohammed Tahmid Jalal), marketing coordinator. Static site, no server or database. Hosted free on GitHub Pages, rebuilt automatically on every push to main.

Built on the open-source sen-3d-resume by Sen Zheng (MIT, see LICENSE and NOTICE): https://github.com/dayinji/sen-3d-resume

## Run it on your computer

    cd web
    npm install
    npm run dev          live preview at http://localhost:5173
    npm run build        production build into web/dist

Double-click preview (one 20 MB file, no server): cd web, then
    npx vite build -c vite.single.config.ts && cp dist-single/index.html ../index.html

## Where to change things

    What                         File
    Hero text, About, spin line  web/src/App.tsx
    Resume timeline text         web/src/ui/Resume.tsx
    Works sections and links     web/src/data/works.ts
    Case study pages             web/src/content/works/*.md
    Camera stops (keep in sync)  web/src/data/focusPoints.ts
    Cover images                 web/public/works/covers/*.jpg
    Resume file                  web/public/resume.pdf (made by tools/resume/build_resume_pdf.py)
    3D character                 web/public/models/me.glb (generated)
    Logos / stickers             source/logos/ then rebuild the character
    Colours, fonts, spin line    web/src/styles.css
    Eye, light, blur, phone      web/src/scene/Scene.tsx
    Camera shots                 tools/character/camera_path.py

## Docs

- docs/PIPELINE.md   every part of the system and how the 3D character is built
- docs/EDIT-GUIDE.md   how to change each thing, step by step
- docs/GITHUB-PLAN.md   push, go live, custom domain, update routine
- docs/APPROVALS-AND-LICENSES.md   licences, what needs Kevin's approval, email text
- HANDOFF.md   state of the project, rules, open items

## Rules for this site

Email only, never the phone number. Works on desktop and phone. Only public or Kevin Skelly approved Cloverdale work. No internal sales numbers, customer names or ad account IDs. No song lyrics.
