"""Check the explicit public file list, inert UI, and absence of live integrations."""
from pathlib import Path, PurePosixPath
import json
import re
import sys

ROOT = Path(__file__).resolve().parent.parent


def public_files():
    names = json.loads((ROOT / 'public-files.json').read_text(encoding='utf-8'))
    if names != sorted(set(names)):
        raise ValueError('Public file list must be sorted and unique')
    for name in names:
        path = PurePosixPath(name)
        if path.is_absolute() or '..' in path.parts or ':' in name or '\\' in name:
            raise ValueError('Invalid public path')
        target = ROOT / name
        if not target.is_file() or target.is_symlink() or not target.resolve().is_relative_to(ROOT):
            raise ValueError(f'Missing or unsafe public file: {name}')
    return names


def check():
    names = public_files()
    for name in names:
        path = ROOT / name
        if path.suffix in {'.png'}:
            continue
        content = path.read_text(encoding='utf-8')
        if re.search(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', content):
            raise ValueError(f'Private key marker in {name}')
        if re.search(r'(?im)^\s*(?:password|api_key|access_token|wifi_ssid)\s*[:=]\s*[\"\'][^\"\']+', content):
            raise ValueError(f'Nonempty credential assignment in {name}')
    app = '\n'.join((ROOT / name).read_text(encoding='utf-8') for name in names
                    if name.startswith('main/') and name.endswith(('.c', '.h', '.txt')))
    for token in ('esp_http_client', 'esp_wifi_', 'esp_netif_', 'nvs_open', 'codex_link',
                  'pocket_cloud', 'pocket_wifi_', 'jsmn', 'https://', 'http://'):
        if token in app:
            raise ValueError('Live integration found in application')
    html = (ROOT / 'preview/index.html').read_text(encoding='utf-8')
    if re.search(r'<script|<iframe|\b(?:src|href)=[\"\'](?:https?:)?//', html, re.I):
        raise ValueError('Preview must be static and use local assets')
    for image in re.findall(r'<img[^>]+src="([^"]+)"', html):
        if not (ROOT / 'preview' / image).is_file():
            raise ValueError('Missing preview image')
    generator = (ROOT / 'tools/build_assets.py').read_text(encoding='utf-8')
    if 'home  /  phone  /  office' not in generator or 'YOUR QR HERE' not in generator:
        raise ValueError('Missing sanitized placeholders')
    if 'codex_audio' in (ROOT / 'partitions.csv').read_text(encoding='utf-8'):
        raise ValueError('Removed integration still has a partition')
    print(f'Public source: PASS ({len(names)} allowlisted files; offline application and preview)')
    return names


if __name__ == '__main__':
    try:
        check()
    except (OSError, ValueError) as error:
        print(f'Public source: FAIL: {error}', file=sys.stderr)
        raise SystemExit(1)
