"""Build the site: index.html plus a/ with every asset as its own cached file.

Run: python3 build.py
Images are converted to WebP (the name mask stays lossless), each file gets a
content hash in its name, so browsers may cache it forever.
"""
import hashlib, io, pathlib, shutil
from PIL import Image

R = pathlib.Path(__file__).parent
F, I, P = R / 'assets/fonts', R / 'assets/img', R / 'assets/img/proj'
OUT = R / 'a'
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()


def emit(data: bytes, stem: str, ext: str) -> str:
    h = hashlib.sha1(data).hexdigest()[:10]
    name = f'{stem}.{h}.{ext}'
    (OUT / name).write_bytes(data)
    return 'a/' + name


def font(fn):
    p = F / fn
    return emit(p.read_bytes(), p.stem, 'woff2')


def webp(p, q=80, max_w=None, lossless=False):
    im = Image.open(p)
    im = im.convert('RGBA' if im.mode in ('RGBA', 'LA', 'P') and 'A' in im.getbands() or im.mode == 'RGBA' else 'RGB')
    if max_w and im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    b = io.BytesIO()
    if lossless:
        im.save(b, 'WEBP', lossless=True, quality=100, method=6, exact=True)
    else:
        im.save(b, 'WEBP', quality=q, method=6)
    return emit(b.getvalue(), p.stem, 'webp')


def raw(p):
    return emit(p.read_bytes(), p.stem, p.suffix[1:])


rep = {
    'F_BANTLEY': font('bantley.woff2'), 'F_CINZEL': font('cinzel_lat.woff2'),
    'F_NR300': font('newsreader-latin-300-normal.woff2'), 'F_NR400': font('newsreader-latin-400-normal.woff2'),
    'F_NR300I': font('newsreader-latin-300-italic.woff2'), 'F_NR400I': font('newsreader-latin-400-italic.woff2'),
    'F_SP300': font('spectral-cyrillic-300-normal.woff2'), 'F_SP400': font('spectral-cyrillic-400-normal.woff2'),
    'F_SP300I': font('spectral-cyrillic-300-italic.woff2'), 'F_SP400I': font('spectral-cyrillic-400-italic.woff2'),
    'F_FORUM': font('forum-cyrillic-400-normal.woff2'), 'F_GV': font('great-vibes-cyrillic-400-normal.woff2'),
    'PF_CORM': font('cormorant-garamond-latin-500-normal.woff2'), 'PF_DM': font('dm-sans-latin-400-normal.woff2'),
    'PF_PLAY': font('playfair-display-latin-400-normal.woff2'), 'PF_INTER': font('inter-latin-400-normal.woff2'),
    'PF_PRATA': font('prata-latin-400-normal.woff2'), 'PF_GOLOS': font('golos-text-latin-400-normal.woff2'),
    'PF_ZEN': font('zen-kaku-gothic-new-latin-400-normal.woff2'), 'PF_SHIP': font('shippori-mincho-latin-400-normal.woff2'),
    'PARD': webp(I / 'pard2.png', 90),
    'MASK': webp(I / 'bant_mask.png', lossless=True),  # data image: must stay exact
    'BGSOFT': webp(I / 'bgsoft.png', 90), 'RELIEF': webp(I / 'relief.jpg', 86),
    'DUNE1': webp(I / 'dune1.png', 88), 'DUNE2': webp(I / 'dune2.png', 88), 'AMBER': webp(I / 'amber.png', 90),
    'FAV': raw(I / 'fav.png'), 'FAV180': raw(I / 'fav180.png'),
    'META': (I / 'bant_meta.json').read_text(),
    'TEMPO': webp(P / 'tp0.jpg', 80, 1400), 'USTY': webp(P / 'usty_cover.jpg', 80, 1400),
}
for k in ['SAV0', 'SAV1', 'SAV2', 'SAV3', 'PL0', 'PL1', 'PL2', 'US1', 'US2', 'US3', 'TP1', 'TP2', 'TP3', 'YO0', 'YO1', 'YO2']:
    rep[k] = webp(P / (k.lower() + '.jpg'), 80, 1400)

s = (R / 'src/index.src.html').read_text()
for k, v in rep.items():
    s = s.replace('{{' + k + '}}', v)
assert '{{' not in s, s[s.index('{{'):s.index('{{') + 40]
(R / 'index.html').write_text(s)
tot = sum(f.stat().st_size for f in OUT.iterdir())
print('index.html', len(s.encode()) // 1024, 'KB; assets', len(list(OUT.iterdir())), 'files', tot // 1024, 'KB')
