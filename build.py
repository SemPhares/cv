#!/usr/bin/env python3
"""
Build script — converts the Flask/Jinja2 portfolio into a static site
deployable on GitHub Pages.

Output structure:
  docs/
    index.html          ← French version (default)
    en/
      index.html        ← English version
    static/             ← copy of ./static/
    .nojekyll           ← prevents Jekyll processing

Usage:
  python build.py

Then commit the docs/ folder and configure GitHub Pages:
  Settings → Pages → Source: Deploy from branch, folder: /docs
"""

import os
import shutil
import sys

# Allow importing LANGUAGES from app.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import LANGUAGES

from jinja2 import Environment, FileSystemLoader

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR  = os.path.join(BASE_DIR, 'docs')
STATIC_SRC = os.path.join(BASE_DIR, 'static')


def make_url_for(prefix: str):
    """Return a url_for() compatible callable for the given relative prefix."""
    def url_for(endpoint: str, filename: str = '', **kwargs) -> str:
        if endpoint == 'static':
            return f'{prefix}static/{filename}'
        return '#'
    return url_for


def build():
    # ── Clean & recreate docs/ ────────────────────────────────────────────────
    if os.path.exists(DOCS_DIR):
        shutil.rmtree(DOCS_DIR)
    os.makedirs(DOCS_DIR)

    # ── Copy static assets ────────────────────────────────────────────────────
    shutil.copytree(STATIC_SRC, os.path.join(DOCS_DIR, 'static'))

    # ── .nojekyll (GitHub Pages: don't treat the site as a Jekyll project) ────
    open(os.path.join(DOCS_DIR, '.nojekyll'), 'w').close()

    # ── Jinja2 standalone environment ─────────────────────────────────────────
    env = Environment(
        loader=FileSystemLoader(os.path.join(BASE_DIR, 'templates')),
        autoescape=False,   # HTML is already trusted
    )
    template = env.get_template('index.html')

    # ── Per-language configuration ────────────────────────────────────────────
    configs = [
        {
            'lang':         'fr',
            'prefix':       '',             # static/css/style.css
            'lang_fr_url':  'index.html',   # current page
            'lang_en_url':  'en/index.html',
            'cv_url':       'static/folder/CV_Sem_EGLOH%20LOKOH.pdf',
            'out':          os.path.join(DOCS_DIR, 'index.html'),
        },
        {
            'lang':         'en',
            'prefix':       '../',          # ../static/css/style.css
            'lang_fr_url':  '../index.html',
            'lang_en_url':  'index.html',   # current page (en/index.html)
            'cv_url':       '../static/folder/CV_Sem_EGLOH%20LOKOH.pdf',
            'out':          os.path.join(DOCS_DIR, 'en', 'index.html'),
        },
    ]

    for cfg in configs:
        lang = cfg['lang']
        print(f'Rendering [{lang}]…')

        html = template.render(
            texts=LANGUAGES[lang],
            current_lang=lang,
            url_for=make_url_for(cfg['prefix']),
        )

        # Fix language-switcher hrefs
        html = html.replace('href="?lang=fr"', f'href="{cfg["lang_fr_url"]}"')
        html = html.replace('href="?lang=en"', f'href="{cfg["lang_en_url"]}"')

        # Fix CV download route → direct PDF link
        html = html.replace('href="/cv/download"', f'href="{cfg["cv_url"]}"')

        os.makedirs(os.path.dirname(cfg['out']), exist_ok=True)
        with open(cfg['out'], 'w', encoding='utf-8') as f:
            f.write(html)

        rel = os.path.relpath(cfg['out'], BASE_DIR)
        print(f'  → {rel}')

    print('\nBuild complete!')
    print(f'Static site is in: {os.path.relpath(DOCS_DIR, BASE_DIR)}/')
    print('\nDeploy steps:')
    print('  1. git add docs/ && git commit -m "build: static site"')
    print('  2. git push')
    print('  3. GitHub repo → Settings → Pages → Source: /docs')


if __name__ == '__main__':
    build()
