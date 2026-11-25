# Edit guide

Open the repo folder in your editor (VS Code). Run npm run dev inside web/ and the page refreshes as you save.

## Change text

- Hero name label, About paragraph, nav links, spin line: web/src/App.tsx. The spin line is const SPIN_LINE near the top. Write your own words, no song lyrics.
- Resume entries: web/src/ui/Resume.tsx. Each entry has period, place, role and groups of bullet points. Keep the order the same as the camera stops.
- Degree line: the Simon Fraser University entry in Resume.tsx (Bachelor of Science, Information and Interactive Arts and Technology).

## Change Works

- List: web/src/data/works.ts. 8 sections (events, campaigns, social, paid, reputation, web, ai, agency). Each item has name, meta, tags and a slug.
- Case study: web/src/content/works/<slug>.md. Frontmatter (title, banner, year, role, tags), then the story: a number row (<div class="case-stats">), The brief, What I did, Result, and optional manager quote (<blockquote class="case-quote">).
- Real photos: each case lists its photo slots as ![Photo: what to show](/works/<slug>/photo-1.jpg). Save your file with that exact name in web/public/works/<slug>/ (jpg, under 500 KB, crop or blur anything internal). A slot with no file is hidden on the live site. To see the empty slots while editing, run npm run dev or open the page with ?slots at the end of the address.
- Covers (web/public/works/covers/<section>.jpg, 1200 px wide) and case banners (web/public/works/<slug>/banner.jpg, 1680 x 720) are handmade-style still-life art made with Higgsfield (GPT Image 2.6, 2k high, 2 credits each), one consistent style: paint chips, paper, painter's tape, sage green backdrop, window light, no text. Replace any of them with a real photo of the same size whenever you have one. Keep each under 500 KB.
- Section intro under each card title: blurb in web/src/data/works.ts.
- The older code-drawn versions are still in tools/works-art (node tools/works-art/render.js writes them to tools/works-art/out, never over the photos).
- Videos go on YouTube (unlisted) and are linked, not stored.

## Email and resume pop-ups

- Email and Resume buttons (top right, timeline, end of page) open pop-ups: web/src/ui/ContactModals.tsx. The email pop-up has copy, mail app, Gmail and LinkedIn. The resume pop-up shows the resume as a page plus Download PDF and Open PDF.
- Resume text in the pop-up: web/src/data/resumeDoc.ts. The PDF: tools/resume/build_resume_pdf.py. Change both together.
- Closing section at the end of the page (Let's work together): Closing in web/src/App.tsx.

## Resume PDF

web/public/resume.pdf is generated: edit the text in tools/resume/build_resume_pdf.py, then run python3 tools/resume/build_resume_pdf.py (pip install reportlab). One page, email only. Or drop in your own PDF, but check it has no phone number.

## Change a logo or sticker

1. Replace the file in source/logos/ (boopdog_original.png is your exact Boopdog file, a 212 px wide one is soft, use a larger file for a sharper sticker).
2. bash tools/character/run_all.sh
3. Check in npm run dev, then commit web/public/models/me.glb.

## Move or resize a sticker

Edit the STK table in tools/character/build_model.py (name, x, y, width, rotation), run run_all.sh.

## Change the face, eyes or skin

Edit the numbers in build_model.py (eye patch IN_X, OUT_X, HU, HL near line 70; skin colour BF near line 206), run run_all.sh. Rules set by TJ: keep skin tone matching the Higgsfield render, natural almond eyes, no smile, no long neck.

## Change camera, light or eye follow

- Camera shots: tools/character/camera_path.py. In STOPS each row is a sticker group, a distance, a yaw angle and a pitch. Bigger distance = wider shot. Change CFG.stop_screen_x to move where the sticker sits across the screen. Run run_all.sh and look.
- Eye follow, light and blur: web/src/scene/Scene.tsx (eye gain 1.7, crossEye 18, focusBokeh 1.2).
- Lighting file: web/public/textures/env.hdr (CC0). Any equirectangular .hdr from polyhaven.com works, keep it under 5 MB.

## Phone settings

web/src/scene/Scene.tsx, the cam block: mobilePullback (how far the camera backs off), mobileTimelineShiftY (how high the face sits, bigger = higher), and NODE_LINE for phones (0.5 = text card starts at mid screen). Text sizes: the max-width 640 px blocks at the end of web/src/styles.css. Test in Chrome: open dev tools, device toolbar, pick iPhone 14.

## Take Cloverdale out (if approval is not in yet)

1. Delete the Cloverdale entry in web/src/ui/Resume.tsx and its name from web/src/data/focusPoints.ts.
2. Remove the Cloverdale row from the STK table in tools/character/build_model.py and from STOPS in camera_path.py, lower the stop count there, run run_all.sh.
3. Remove Cloverdale items from web/src/data/works.ts and the matching case study files. Rebuild and push.

## Change colours and fonts

web/src/styles.css. Fonts are in web/public/fonts.

## Add a new camera stop

1. Add the entry in Resume.tsx. 2. Add 'focus-8' in focusPoints.ts. 3. Add a sticker row in the STK table of build_model.py and a logo in make_stickers.py. 4. Add a row to STOPS in camera_path.py (the stop count follows the table). 5. Run run_all.sh.

## Set up the Python side once

    pip install -r tools/character/requirements.txt
    (node is already needed for the website)
