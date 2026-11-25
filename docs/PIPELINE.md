# Pipeline: how the whole site is made

There is no back end. The site is a static front end (HTML, JS, one 3D file, images). GitHub Actions builds it and GitHub Pages serves it. Everything you can edit is a plain file in this repo.

## The four layers

1. Content: text and images. Edit in your editor, no tools needed.
2. Front end: React + Three.js + Vite code in web/. Reads the content and the 3D file.
3. Character pipeline: Python scripts in tools/character/ that build web/public/models/me.glb from files in source/.
4. Deploy: .github/workflows/deploy.yml builds web/ and publishes web/dist.

## Repo map

    source/                      inputs to the character pipeline (edit these, then rebuild)
      model/source_me.glb        base head and bust (from Higgsfield image to Meshy 3D)
      face/eyetex.png            face texture crop used for the eyelid patch
      logos/*.png                real logos, plus boopdog_original.png (your exact file)
    tools/character/             character pipeline
      paths.py                   every input and output path, change paths only here
      make_stickers.py           logos to die-cut stickers (off-white border, soft shadow, 512 px)
      build_model.py             eyes, skin, shoulders, base cap, sticker decals
      camera_path.py             camera shots (CFG and STOPS tables), spin timing, focus anchors
      load.py                    helper that reads the source glb
      run_all.sh                 runs everything, writes web/public/models/me.glb
      work/                      scratch output, ignored by git
    web/                         the website
      public/models/me.glb       the finished character (committed so Pages can serve it)
      public/works/covers/       Works cover images
      public/textures/env.hdr    lighting environment (CC0, Poly Haven kloppenheim_06_puresky)
      public/fonts/              Cormorant Upright, Mansalva
      src/App.tsx                hero, About, nav links, spin line
      src/ui/Resume.tsx          resume timeline panels
      src/ui/Works.tsx           works grid and case study viewer
      src/data/works.ts          works list
      src/data/focusPoints.ts    names of camera anchors in the glb
      src/content/works/*.md     case studies
      src/scene/Scene.tsx        camera, lights, eye follow, bloom, blur, spin-line fade
      vite.single.config.ts      builds the double-click single file
    .github/workflows/deploy.yml build and publish to GitHub Pages
    tools/resume/                build_resume_pdf.py makes web/public/resume.pdf (final marketing resume, email only)
    tools/works-art/             art.html + render.js draw the Works covers and case banners from real logos and numbers
    docs/                        this documentation
    HANDOFF.md                   project state and open items

## Character pipeline, in order

1. make_stickers.py: reads source/logos, writes work/stk/*.png (13 stickers: sfu, cloverdale, instagram, facebook, linkedin, tiktok, jaalik, reframes, telus, skechers, boopdog, chatgpt, claude).
2. build_model.py: reads source_me.glb and the stickers.
   - Eyes: cuts socket holes, adds an almond eyelid patch (named lid_patch, never put "eye" in that name), eyeballs eye_L and eye_R.
   - Skin: Sen-style material, base colour 0.83/0.75/0.73, roughness map. No emissive trick.
   - Shoulders widened below y -0.2 and a base cap closes the bottom for the 360 spin.
   - Stickers: projected onto the face as decals. Placement table is the STK list in build_model.py: name, x, y, width, rotation. Change numbers there to move a sticker.
3. camera_path.py: writes the CameraAction clip (24 fps) from scratch. Each shot is a target, a distance, and a yaw and pitch around that target; no data is taken from any other model. The hero shot is solved from the head: hair top at 7 percent and chin at 60 percent of the frame. Stops 1 to 6 are close-ups of the sticker groups (settings in the STOPS table), stop 7 is the wide shot with the SFU sticker on the nose, then a slow drift back during the Works spin. Close-ups are slid sideways so the sticker lands at 28 percent of the screen width and the text sits on the right. Stop k sits at frame 50k, 450 frames total. The 360 spin (manAction) is shifted to start after stop 7. Writes the focus-1 to focus-7 anchors.
4. gltf-transform prune then quantize: 10.7 MB to 3.8 MB.
5. Copy to web/public/models/me.glb.

Check: running run_all.sh from this repo reproduces the shipped me.glb byte for byte (3,789,320 bytes).

## The contract between the glb and the site

The site finds things by name. Do not rename these.
- Camera animation clip: CameraAction (24 fps)
- Empties: focus-1 to focus-7 and focus-works
- Any mesh whose name contains "eye" rotates to follow the cursor (eye_L, eye_R)
- manAction: the 360 spin during Works

## Stop order (must match in three places)

1 Jaalik Tech x Reframes, 2 Telus, 3 Skechers, 4 Cloverdale Paint, 5 Boopdog, 6 AI content production, 7 Simon Fraser University.
Same order in src/ui/Resume.tsx, src/data/focusPoints.ts and the STK table. Add or remove a stop in all three and in the STOPS table of camera_path.py, then rerun run_all.sh.

## Phone version

The same glb and the same page serve phones. Rules in web/src/scene/Scene.tsx (IS_PHONE, NODE_LINE, cam.mobile* settings):
- Phones (touch pointer or width up to 640 px): the text card sits in the lower half, so the timeline reference line moves to 50 percent of the screen and the camera lifts the face into the top half (mobileTimelineShiftY). The sideways offset in the camera path is cancelled (mobileTimelineShift).
- The camera pulls back 20 percent (mobilePullback). Eye follow is off (no cursor). Pixel ratio is capped at 1.25 (App.tsx).
- Text sizes and layout: the max-width 640 px blocks in web/src/styles.css, including the About text block at the end of the file.
- Tested with a 390 x 844 touch emulation: no sideways scrolling, every stop shows its stickers above the card. Not tested on a real phone GPU.

## Build outputs

- npm run build gives web/dist, about 13 MB, separate files. This is what goes live.
- vite.single.config.ts gives web/dist-single/index.html, about 20 MB, everything embedded. Local preview only.
- base is './' so the site works at username.github.io/repo-name and on a custom domain.
