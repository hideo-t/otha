"""Check every local asset/anchor and the contact and staging invariants."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import sys
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'i18n'))
import config

errors = []
pages = [ROOT / 'index.html'] + [ROOT / lang / 'index.html' for lang in config.LANGS]
for page in pages:
    soup = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
    ids = [e['id'] for e in soup.select('[id]')]
    if len(ids) != len(set(ids)):
        errors.append(f'{page}: duplicate ids')
    for el in soup.select('[href], [src]'):
        url = urlsplit(el.get('href', el.get('src', '')))
        if url.scheme or url.netloc:
            continue
        path = unquote(url.path)
        if path.startswith('/'):
            if config.BASE and not path.startswith(config.BASE + '/'):
                errors.append(f'{page}: wrong base: {path}')
                continue
            target = ROOT / path[len(config.BASE):].lstrip('/')
        else:
            target = page.parent / path if path else page
        if target.is_dir():
            target /= 'index.html'
        if not target.is_file():
            errors.append(f'{page}: missing: {path}')
        elif url.fragment and target.suffix == '.html':
            other = BeautifulSoup(target.read_text(encoding='utf-8'), 'html.parser')
            if not other.find(id=unquote(url.fragment)):
                errors.append(f'{page}: missing anchor: {url.fragment}')
    for selector in ['form', '[data-info]', '[data-link]']:
        if soup.select(selector):
            errors.append(f'{page}: obsolete contact element: {selector}')
    if len(soup.select('a[href="tel:+81989171536"]')) != 2:
        errors.append(f'{page}: phone links')
    for value in ['900-0015', '098-917-1547']:
        if value not in soup.get_text():
            errors.append(f'{page}: missing {value}')
    if len(soup.select('.check')) != 13:
        errors.append(f'{page}: checklist count')
    robots = soup.find('meta', attrs={'name': 'robots'})
    if config.NOINDEX and (not robots or robots.get('content') != 'noindex,nofollow'):
        errors.append(f'{page}: staging robots')
    if not config.NOINDEX and robots and 'noindex' in robots.get('content', ''):
        errors.append(f'{page}: production still noindex')
    canonical = soup.select_one('link[rel="canonical"]')
    rel = page.relative_to(ROOT).as_posix().removesuffix('index.html')
    if not canonical or canonical['href'] != config.SITE + config.BASE + '/' + rel:
        errors.append(f'{page}: incorrect canonical')
    print(f'Checked {page.relative_to(ROOT)}')
if errors:
    print('\n'.join(errors))
    sys.exit(1)
print('PASS: all assets, anchors, contact details and staging settings')
