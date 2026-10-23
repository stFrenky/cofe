#!/usr/bin/env python3
"""Inline every asset from src/assets into src/template.html -> index.html (single self-contained file)."""
import base64, pathlib, re, sys
root = pathlib.Path(__file__).parent
tpl = (root / 'src' / 'template.html').read_text(encoding='utf-8')
assets = root / 'src' / 'assets'
mime = {'.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.webp': 'image/webp'}
def data_uri(name):
    for ext, m in mime.items():
        f = assets / f'{name}{ext}'
        if f.exists():
            return f'data:{m};base64,' + base64.b64encode(f.read_bytes()).decode()
    sys.exit(f'missing asset: {name}')
out = re.sub(r'__ASSET_([a-z_]+)__', lambda m: data_uri(m.group(1)), tpl)
three = (assets / 'three.js').read_text(encoding='utf-8').strip()
out = out.replace("__THREE__", three)
(root / 'index.html').write_text(out, encoding='utf-8')
print('index.html', round(len(out.encode()) / 1024), 'KB')
