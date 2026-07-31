# Coach Tools

Three static pages. No build step, no dependencies, no server-side code.

```
├─ index.html                    launcher
├─ timer.html                    interval / round timer
├─ colour.html                   reaction colour cues
├─ sw.js                         offline cache
├─ manifest-launcher.webmanifest
├─ manifest-timer.webmanifest
├─ manifest-colour.webmanifest
├─ build-icons.py                regenerates everything in icons/
└─ icons/                        12 PNGs, 3 apps x 4 sizes
```

## After you change a file

Bump `CACHE` in `sw.js` — `coach-tools-v6` to `v7`, and so on. Installed phones
key their cache off that string; without a bump they keep serving the old copy
and your change looks like it silently didn't work.

If you add or rename a file, also update the `CORE` list in `sw.js`.

## Renaming a page

Three places, all together:

1. the `href` in `index.html`
2. the entry in `CORE` in `sw.js`
3. `start_url` in that page's manifest

Then bump `CACHE`. Note that anyone who already added the page to their home
screen has the old URL baked in — they need to delete the shortcut and re-add it.

## Icons

| File | Used by |
|---|---|
| `icon-*-180.png` | iPhone / iPad home screen |
| `icon-*-192.png` | Android home screen, browser tab |
| `icon-*-512.png` | Android splash screen, app switcher |
| `icon-*-512-maskable.png` | Android adaptive icon (cropped to a circle or squircle) |

To change a colour or shape, edit the drawing functions at the top of
`build-icons.py` and run `python3 build-icons.py`. It rewrites all 12 files from
a single 2048px master so every size stays in sync. Needs Pillow
(`pip install Pillow`); nothing else.

Home screen icons are captured at "Add to Home Screen" — changing the files
later won't update an existing shortcut.

## Serving

Needs http(s), not `file://`. Manifests, service workers and `wakeLock` (which
stops the screen sleeping mid-session) all require it. GitHub Pages is fine.
