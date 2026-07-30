# Coach Tools — iOS setup

Two self-contained web apps, packaged so they install to an iPhone or iPad home
screen and run with no signal.

- `index.html` — launcher with a tile for each tool
- `timer.html` — Gym Timer
- `colour.html` — React: Colour
- `sw.js` — offline cache
- `manifest-*.webmanifest`, `icon-*.png` — home screen icon and app metadata

## 1. Put the folder on a URL

iOS will only install a web app from `https://`. Any static host works; upload
the whole folder, keeping the filenames as they are.

**GitHub Pages** (free, permanent)
1. Create a repository, upload every file in this folder to the root.
2. Settings → Pages → Source: *Deploy from a branch*, branch `main`, folder `/`.
3. Wait a minute, then open `https://<username>.github.io/<repo>/`.

**Cloudflare Pages or Netlify** — create a project, drag the folder into the
deploy box, use the URL it gives you.

**Local network only** — from the folder on a Mac:
`python3 -m http.server 8000`, then open `http://<mac-ip>:8000` on the phone.
Fine for testing, but the service worker and installed-app mode need `https://`,
so the icon won't behave properly.

## 2. Install on the phone

Open the URL **in Safari** (Chrome and Firefox on iOS can't install web apps).

- Tap **Share** → **Add to Home Screen** → **Add**.
- Do it from `index.html` for a launcher icon, or open `timer.html` or
  `colour.html` first to get a separate icon for just that tool. Installing all
  three is fine — each gets its own icon and its own colour scheme.

Launched from the home screen there's no address bar, no tab bar, and no
accidental swipe-back mid-round.

## 3. Offline

The first launch on `https://` caches everything. After that both tools work in
airplane mode. React: Colour pulls two web fonts from Google on first load and
caches them too; if that first load happens offline it falls back to the
system condensed face and still works.

## Notes

- **Sound** — iOS won't play audio until you tap something, so the first tap on
  Start unlocks it. The timer's alarms will be silent if the phone's ringer
  switch is on mute; volume up and ringer on.
- **Screen sleep** — both request a screen wake lock (iOS 16.4+), so the display
  stays on while a session runs.
- **Editing later** — if you change any file, bump `CACHE = 'coach-tools-v1'` in
  `sw.js` to `v2`. Otherwise installed phones keep serving the old cached copy.
