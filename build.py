"""Build index.html: inline every {{KEY}} in src/index.src.html as a base64 data URI.
Run: python3 build.py"""
import base64, pathlib
R = pathlib.Path(__file__).parent
F, I, P = R / 'assets/fonts', R / 'assets/img', R / 'assets/img/proj'
b64 = lambda p: base64.b64encode(p.read_bytes()).decode()
img = lambda p: ('data:image/png;base64,' if p.suffix == '.png' else 'data:image/jpeg;base64,') + b64(p)
rep = {
    'F_BANTLEY': b64(F / 'bantley.woff2'), 'F_CINZEL': b64(F / 'cinzel_lat.woff2'),
    'F_NR300': b64(F / 'newsreader-latin-300-normal.woff2'), 'F_NR400': b64(F / 'newsreader-latin-400-normal.woff2'),
    'F_NR300I': b64(F / 'newsreader-latin-300-italic.woff2'), 'F_NR400I': b64(F / 'newsreader-latin-400-italic.woff2'),
    'F_SP300': b64(F / 'spectral-cyrillic-300-normal.woff2'), 'F_SP400': b64(F / 'spectral-cyrillic-400-normal.woff2'),
    'F_SP300I': b64(F / 'spectral-cyrillic-300-italic.woff2'), 'F_SP400I': b64(F / 'spectral-cyrillic-400-italic.woff2'),
    'F_FORUM': b64(F / 'forum-cyrillic-400-normal.woff2'), 'F_GV': b64(F / 'great-vibes-cyrillic-400-normal.woff2'),
    'PF_CORM': b64(F / 'cormorant-garamond-latin-500-normal.woff2'), 'PF_DM': b64(F / 'dm-sans-latin-400-normal.woff2'),
    'PF_PLAY': b64(F / 'playfair-display-latin-400-normal.woff2'), 'PF_INTER': b64(F / 'inter-latin-400-normal.woff2'),
    'PF_PRATA': b64(F / 'prata-latin-400-normal.woff2'), 'PF_GOLOS': b64(F / 'golos-text-latin-400-normal.woff2'),
    'PF_ZEN': b64(F / 'zen-kaku-gothic-new-latin-400-normal.woff2'), 'PF_SHIP': b64(F / 'shippori-mincho-latin-400-normal.woff2'),
    'PARD': img(I / 'pard2.png'), 'MASK': img(I / 'bant_mask.png'), 'BGSOFT': img(I / 'bgsoft.png'),
    'RELIEF': img(I / 'relief.jpg'), 'DUNE1': img(I / 'dune1.png'), 'DUNE2': img(I / 'dune2.png'),
    'AMBER': img(I / 'amber.png'), 'FAV': img(I / 'fav.png'), 'FAV180': img(I / 'fav180.png'),
    'META': (I / 'bant_meta.json').read_text(),
    'TEMPO': img(P / 'tp0.jpg'), 'USTY': img(P / 'usty_cover.jpg'),
}
for k in ['SAV0', 'SAV1', 'SAV2', 'SAV3', 'PL0', 'PL1', 'PL2', 'US1', 'US2', 'US3', 'TP1', 'TP2', 'TP3', 'YO0', 'YO1', 'YO2']:
    rep[k] = img(P / (k.lower() + '.jpg'))
s = (R / 'src/index.src.html').read_text()
for k, v in rep.items():
    s = s.replace('{{' + k + '}}', v)
assert '{{' not in s, s[s.index('{{'):s.index('{{') + 40]
(R / 'index.html').write_text(s)
print('index.html', len(s) // 1024, 'KB')
