import { defineConfig, type Plugin } from 'vite'
import react from '@vitejs/plugin-react'
import { viteSingleFile } from 'vite-plugin-singlefile'
import fs from 'node:fs'

// Double-click build: embeds glb + env.hdr as base64 so index.html works from file://
const b64 = (p: string, mime: string) => `data:${mime};base64,${fs.readFileSync(p).toString('base64')}`
const embed: Plugin = {
  name: 'embed-assets',
  transform(code, id) {
    if (/src\/data\/works\.ts$/.test(id)) {
      return code.replace(/`\$\{import\.meta\.env\.BASE_URL\}works\/covers\/(\w+)\.jpg`/g, (m: string, n: string) =>
        fs.existsSync(`public/works/covers/${n}.jpg`) ? JSON.stringify(b64(`public/works/covers/${n}.jpg`, 'image/jpeg')) : m)
    }
    if (/src\/ui\/ContactModals\.tsx$/.test(id)) {
      return code.replace('`${import.meta.env.BASE_URL}resume.pdf`', JSON.stringify(b64('public/resume.pdf', 'application/pdf')))
    }
    if (/src\/content\/works\/.*\.md/.test(id)) {
      // case-study banners and photos: embed the files that exist, leave the rest as paths (they show as empty slots)
      return code.replace(/\/works\/[\w./-]+\.(jpg|jpeg|png|webp)/g, (m: string, ext: string) =>
        fs.existsSync(`public${m}`) ? b64(`public${m}`, ext === 'png' ? 'image/png' : ext === 'webp' ? 'image/webp' : 'image/jpeg') : m)
    }
    if (!/src\/scene\/(Scene|Env)\.tsx$/.test(id)) return null
    return code
      .replaceAll('`${import.meta.env.BASE_URL}models/me.glb`', JSON.stringify(b64('public/models/me.glb', 'model/gltf-binary')))
      .replaceAll('`${import.meta.env.BASE_URL}textures/env.hdr`', JSON.stringify(b64('public/textures/env.hdr', 'application/octet-stream')))
  },
}

export default defineConfig({
  base: './',
  plugins: [react(), embed, viteSingleFile()],
  build: { outDir: 'dist-single', emptyOutDir: false, assetsInlineLimit: 100000000, chunkSizeWarningLimit: 100000 },
})
