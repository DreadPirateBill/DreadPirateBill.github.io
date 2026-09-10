#!/usr/bin/env python3
"""
Static site builder for sprocketplayer.com.

    python3 build.py

Reads  templates/pages/*.html      one template per page
       templates/partials/*.html   shared fragments ({{> name}})
       templates/redirect.html     the root-level language redirector
       i18n/<lang>.json            one flat string catalog per language

Writes /<lang>/<page>.html for every language in LANGS, and a small
redirector at /<page>.html that forwards to the visitor's language.

Template syntax (deliberately tiny, no dependencies):
    {{key.name}}                 a string from the catalog
    {{> partial}}                include templates/partials/partial.html
    {{> partial a="key" b="key"}} include with named arguments; inside the
                                 partial, {{$a}} resolves to the catalog
                                 string for that key
    {{lang}} {{page}} {{page_path}} {{site}}   built-in variables
    {{hreflang}}                 <link rel="alternate"> block for this page
    {{lang_options}}             <option> list for the language switcher

Catalog keys beginning with "_" are ignored (use them for notes).
Missing keys in a non-English catalog fall back to English, and the build
prints a per-language coverage summary so you can see what still needs
translating.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "https://sprocketplayer.com"
DEFAULT_LANG = "en"

# Order here is the order in the language switcher.
LANGS = {
    "en": "English",
    "fr": "Français",
    "de": "Deutsch",
    "es": "Español",
    "it": "Italiano",
    "ja": "日本語",
}

PAGES = ["index", "support", "privacy"]

TPL_PAGES = ROOT / "templates" / "pages"
TPL_PARTIALS = ROOT / "templates" / "partials"
TPL_REDIRECT = ROOT / "templates" / "redirect.html"
I18N = ROOT / "i18n"

TOKEN = re.compile(r"\{\{\s*(.*?)\s*\}\}")


def load_catalog(lang: str) -> dict:
    path = I18N / f"{lang}.json"
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    return {k: v for k, v in data.items() if not k.startswith("_")}


def page_path(page: str) -> str:
    """URL path segment for a page: '' for index, 'support.html' otherwise."""
    return "" if page == "index" else f"{page}.html"


def hreflang_block(page: str) -> str:
    lines = []
    for lang in LANGS:
        lines.append(f'<link rel="alternate" hreflang="{lang}" href="{SITE}/{lang}/{page_path(page)}">')
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}/{page_path(page)}">')
    return "\n".join(lines)


def lang_options(current: str) -> str:
    out = []
    for code, name in LANGS.items():
        sel = " selected" if code == current else ""
        out.append(f'<option value="{code}"{sel}>{name}</option>')
    return "\n".join(out)


class Renderer:
    def __init__(self, lang: str, page: str, strings: dict, en: dict):
        self.lang = lang
        self.page = page
        self.strings = strings
        self.en = en
        self.missing: set[str] = set()
        self.builtins = {
            "lang": lang,
            "page": page,
            "page_path": page_path(page),
            "site": SITE,
            "hreflang": hreflang_block(page),
            "lang_options": lang_options(lang),
        }

    def lookup(self, key: str) -> str:
        if key in self.builtins:
            return self.builtins[key]
        if key in self.strings:
            return self.strings[key]
        if key in self.en:
            self.missing.add(key)
            return self.en[key]
        raise KeyError(f"[{self.lang}/{self.page}] unknown template key: {key}")

    def render(self, text: str, args: dict | None = None) -> str:
        args = args or {}

        def sub(m: re.Match) -> str:
            expr = m.group(1)
            if expr.startswith(">"):
                return self.include(expr[1:].strip())
            if expr.startswith("$"):
                name = expr[1:]
                if name not in args:
                    raise KeyError(f"[{self.lang}/{self.page}] partial argument not supplied: ${name}")
                return self.lookup(args[name])
            return self.lookup(expr)

        return TOKEN.sub(sub, text)

    def include(self, spec: str) -> str:
        parts = spec.split()
        name, rest = parts[0], parts[1:]
        args = {}
        for item in rest:
            k, _, v = item.partition("=")
            args[k] = v.strip('"')
        path = TPL_PARTIALS / f"{name}.html"
        if not path.exists():
            raise FileNotFoundError(f"partial not found: {path}")
        return self.render(path.read_text(encoding="utf-8"), args)


def build() -> int:
    en = load_catalog(DEFAULT_LANG)
    if not en:
        print(f"error: {I18N / 'en.json'} is missing or empty", file=sys.stderr)
        return 1

    redirect_tpl = TPL_REDIRECT.read_text(encoding="utf-8")
    coverage = {}
    written = 0

    for lang in LANGS:
        strings = load_catalog(lang)
        missing_total: set[str] = set()
        out_dir = ROOT / lang
        out_dir.mkdir(exist_ok=True)

        for page in PAGES:
            tpl = (TPL_PAGES / f"{page}.html").read_text(encoding="utf-8")
            r = Renderer(lang, page, strings, en)
            html = r.render(tpl)
            (out_dir / f"{page}.html").write_text(html, encoding="utf-8")
            missing_total |= r.missing
            written += 1

        used_keys = set(en.keys())
        translated = len(used_keys) - len(missing_total) if lang != DEFAULT_LANG else len(used_keys)
        coverage[lang] = (translated, len(used_keys))

    # Root-level redirectors: /index.html, /support.html, /privacy.html
    for page in PAGES:
        r = Renderer(DEFAULT_LANG, page, en, en)
        r.builtins["lang_list_json"] = json.dumps(list(LANGS.keys()))
        r.builtins["lang_links"] = "\n".join(
            f'<li><a href="/{code}/{page_path(page)}" lang="{code}">{name}</a></li>' for code, name in LANGS.items()
        )
        (ROOT / f"{page}.html").write_text(r.render(redirect_tpl), encoding="utf-8")
        written += 1

    print(f"built {written} files")
    for lang, (done, total) in coverage.items():
        note = "" if done == total else f"  ({total - done} keys falling back to English)"
        print(f"  {lang}: {done}/{total} strings translated{note}")
    return 0


if __name__ == "__main__":
    sys.exit(build())
