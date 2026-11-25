# GitHub plan: from this folder to a live site

You push to GitHub yourself. This is the order.

## One time

1. Create an empty repo on github.com, for example tj-3d-resume. Public (free Pages needs public unless you have a paid plan). Do not add a README or licence there.
2. In the project folder:

        git init -b main
        git add .
        git commit -m "TJ 3D resume"
        git remote add origin https://github.com/<your-username>/tj-3d-resume.git
        git push -u origin main

3. On GitHub: Settings, Pages, Source = GitHub Actions. (Do this once. The workflow is already in .github/workflows/deploy.yml.)
4. Open the Actions tab. The Deploy to GitHub Pages run takes about 2 minutes. When it is green the site is at:

        https://<your-username>.github.io/tj-3d-resume/

5. Put that link on your resume, LinkedIn and email signature.

## Before you push (checklist)

- web/public/resume.pdf is already in the repo (email only). Re-run tools/resume/build_resume_pdf.py after text changes.
- No phone number anywhere: search the repo for the digits.
- Kevin Skelly's approval (see docs/APPROVALS-AND-LICENSES.md, email text included). Cloverdale content: public or approved only. No internal sales numbers, customer names or ad account IDs in images.
- Licences are handled: env.hdr is CC0 (Poly Haven), camera path is original, logos are identification only. Details in docs/APPROVALS-AND-LICENSES.md.
- Open the live link on your phone and on a second computer. Software-rendered checks cannot show real GPU speed.

## What to keep out of git

Already in .gitignore: node_modules, dist, tools/character/work, local preview index.html, _tmp, Claude outputs. The 20 MB single-file index.html stays on your computer only.

## Update routine

    edit a file, npm run dev to check
    git add . && git commit -m "what changed" && git push

Every push to main rebuilds and republishes. Changed a logo, sticker, eye or skin: run tools/character/run_all.sh first and commit the new web/public/models/me.glb.

## Custom domain (optional)

Buy a domain, then Settings, Pages, Custom domain. Add the DNS records GitHub shows. Because base is './' no code change is needed.

## If the build fails

Actions tab, open the red run, read the failing step. Usual causes: a TypeScript error (run npm run build locally to see it), or package-lock.json out of sync (run npm install in web/ and commit the lock file).

## Before publishing publicly

The camera is now fully original. The only open item is Kevin's approval.
