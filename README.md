# Coach tools

Two standalone class tools. Each file runs on its own — no build step, no
dependencies, no server-side code.

```
├─ gym-timer-ios.html          interval / round timer
├─ react-colour-trainer.html   reaction colour cues
├─ manifest-timer.json
├─ manifest-react.json
├─ manifest-home.json          for your own index.html — see below
├─ build-icons.py              regenerates everything in icons/
└─ icons/                      12 PNGs, 3 apps x 4 sizes
```

## Your home page

There is deliberately **no index.html here**, so uploading this won't overwrite
the one you already have. To use the whistle icon, paste this into its `<head>`:

```html
<link rel="apple-touch-icon" href="icons/icon-home-180.png">
<link rel="icon" href="icons/icon-home-192.png">
<link rel="manifest" href="manifest-home.json">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Coach Tools">
<meta name="theme-color" content="#0B1B3E">
```

Then edit `manifest-home.json` — change `name` and `short_name` to whatever
should appear under the icon. If you don't want a home page icon at all, delete
`manifest-home.json` and the four `icon-home-*.png` files.

## Icons

| File | Used by |
|---|---|
| `icon-*-180.png` | iPhone / iPad home screen |
| `icon-*-192.png` | Android home screen, browser tab |
| `icon-*-512.png` | Android splash screen, app switcher |
| `icon-*-512-maskable.png` | Android adaptive icon (cropped to a circle or squircle) |

To change a colour or shape, edit the drawing functions near the top of
`build-icons.py` and run `python3 build-icons.py`. It rewrites every size into
`icons/` from a single 2048px master, so all four stay in sync. Needs Pillow
(`pip install Pillow`); nothing else.

## Notes

- Home screen icons are captured at "Add to Home Screen". Changing the files
  later won't update an existing shortcut — delete it and re-add.
- Manifests only load over http(s). Opening the HTML off the filesystem works
  for the pages themselves, but Android won't read the manifest.
- Both pages use `wakeLock` to stop the screen sleeping mid-session. Safari
  only grants it over https.
