#!/usr/bin/env python3
"""Validate public routes, local links/assets, privacy constraints and publication readiness."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
CONFIG = json.loads((ROOT / 'site.json').read_text())
PRODUCTION = '--production' in sys.argv


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = set()
        self.links = []
        self.h1 = 0
        self.forms = []
        self.scripts = []
        self.feed(text)

    def handle_starttag(self, tag, values):
        attrs = dict(values)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'Duplicate ID: {attrs["id"]}'
            self.ids.add(attrs['id'])
        if tag == 'h1':
            self.h1 += 1
        if tag == 'a' and attrs.get('href'):
            self.links.append(attrs['href'])
        if tag in ('img', 'source'):
            if tag == 'img':
                assert 'alt' in attrs and 'width' in attrs and 'height' in attrs, attrs
            if attrs.get('src'):
                self.links.append(attrs['src'])
            for candidate in attrs.get('srcset', '').split(','):
                if candidate.strip():
                    self.links.append(candidate.strip().split()[0])
        if tag == 'link' and attrs.get('href'):
            self.links.append(attrs['href'])
        if tag == 'form':
            self.forms.append(attrs)
        if tag == 'script':
            self.scripts.append(attrs)


def resolve(url, origin):
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc:
        return None, parsed.fragment
    p = ROOT / unquote(parsed.path).lstrip('/') if parsed.path.startswith('/') else origin.parent / unquote(parsed.path)
    if not parsed.path:
        p = origin
    if p.is_dir():
        p = p / 'index.html'
    return p, parsed.fragment


def main():
    documents = {}
    for p in ROOT.rglob('*.html'):
        text = p.read_text()
        assert 'FluxBar' not in text and 'ZUGZWANG' not in text, p
        d = Document(text)
        assert d.h1 == 1, f'{p}: expected exactly one main heading'
        assert not d.scripts, f'{p}: no script or tracker should be needed'
        documents[p] = d
    for origin, document in documents.items():
        for url in document.links:
            assert 'j3ffwin5tonone/Schafkopf/' not in url, 'Private source repo must not be linked'
            target, fragment = resolve(url, origin)
            if target is None:
                continue
            assert target.is_file(), f'{origin.relative_to(ROOT)}: missing {url}'
            if fragment:
                assert target in documents and fragment in documents[target].ids, f'Broken anchor: {url}'
    for route in ('schafkopf', 'schafkopf/support', 'schafkopf/datenschutz', 'datenschutz', 'impressum', 'kontakt', 'kontakt/danke'):
        assert (ROOT / route / 'index.html').is_file(), route
    imprint = (ROOT / 'impressum/index.html').read_text()
    assert CONFIG['provider']['vat_id'] in imprint and '§ 5 DDG' in imprint
    assert 'TMG' not in imprint and 'RStV' not in imprint
    assert (ROOT / 'CNAME').read_text().strip() == 'fluxbar.app'
    form = documents[ROOT / 'kontakt/index.html'].forms
    assert len(form) == 1 and form[0]['method'].lower() == 'post'
    assert (ROOT / 'assets/fonts/FIGTREE-LICENSE.txt').is_file()
    if PRODUCTION:
        assert CONFIG['form']['avv_confirmed'], 'Form.taxi processing agreement is not confirmed'
        assert re.fullmatch(r'https://form\.taxi/s/[A-Za-z0-9_-]+', CONFIG['form']['endpoint'] or ''), 'Real Form.taxi endpoint missing'
        assert form[0]['action'] == CONFIG['form']['endpoint']
        assert '<fieldset disabled>' not in (ROOT / 'kontakt/index.html').read_text(), 'Form is disabled'
    print(f'Validated {len(documents)} HTML files: routes, links, anchors, image variants, provider data and privacy constraints.')
    if not PRODUCTION:
        print('Draft check only: real form endpoint and owner confirmation remain required before publication.')


if __name__ == '__main__':
    main()
