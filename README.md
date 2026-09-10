# sprocketplayer.com

Marketing and support site for Sprocket Player, served by GitHub Pages from `main`.

## Layout

```
templates/pages/*.html      page templates (index, support, privacy)
templates/partials/*.html   shared head, nav, footer
templates/redirect.html     root-level language redirector
i18n/<lang>.json            string catalog per language (en is the source of truth)
build.py                    generates everything below
<lang>/*.html               generated. Do not edit by hand.
index.html, support.html, privacy.html   generated redirectors. Do not edit by hand.
assets/                     CSS, JS, images, screenshots
```

## Editing copy

1. Change the string in `i18n/en.json` (or the language you are translating).
2. Run `python3 build.py`.
3. Commit the templates, catalogs **and** the generated output together.

The build prints how many strings each language has translated. Any key missing from a
language catalog falls back to English, so a partially translated language still builds.

## Adding or changing page structure

Edit the template under `templates/`, add any new strings to `i18n/en.json`, rebuild.
Template syntax is documented at the top of `build.py`.

## How language selection works

- `/` (and `/support.html`, `/privacy.html`) is a tiny page that redirects to the best language:
  a language the visitor previously picked from the switcher, else the browser's language list,
  else English. Without JavaScript it falls through to `/en/`.
- Real content lives at `/en/`, `/fr/`, `/de/`, `/es/`, `/it/`, `/ja/`.
- Every page carries `hreflang` links for all languages plus `x-default`, so search engines
  index each language directly and never land people on the redirector.
- The nav switcher saves the choice and jumps to the same page in the chosen language.

## Screenshots

See `assets/img/screenshots/README.md` for the list of files the pages expect.

## Local preview

Any static server works, for example:

```bash
python3 -m http.server 8765
```

then open http://127.0.0.1:8765/. Pages use root-absolute asset paths, so open them over HTTP
rather than as `file://`.
