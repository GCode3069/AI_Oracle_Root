"""
Credential discovery and validation tool for the SCARIFY repo.
Saves a JSON report to tools/credentials_report.json (non-secret: masks values).
Usage: python tools/validate_credentials.py --root .
"""
import os
import json
import argparse
from pathlib import Path

MASK_HEAD = 4
MASK_TAIL = 4

COMMON_EXT = ['.json', '.env', '.key', '.pem', '.txt']
KEYWORDS = ['credential', 'credentials', 'client', 'secret', 'token', 'key', 'auth']

def mask_value(v: str) -> str:
    if not v:
        return v
    if len(v) <= MASK_HEAD + MASK_TAIL:
        return v[:MASK_HEAD] + '...' + v[-MASK_TAIL:]
    return v[:MASK_HEAD] + '...' + v[-MASK_TAIL:]

def inspect_json(path: Path):
    try:
        raw = path.read_text(encoding='utf-8')
        data = json.loads(raw)
        summary = {
            'path': str(path),
            'type': 'json',
            'keys': list(data.keys()) if isinstance(data, dict) else None,
            'service_account': bool(data.get('type') == 'service_account') if isinstance(data, dict) else False
        }
        # mask obvious secrets
        secrets = {}
        for k, v in (data.items() if isinstance(data, dict) else []):
            if any(tok in k.lower() for tok in ('secret', 'key', 'token', 'private', 'client')):
                try:
                    secrets[k] = mask_value(str(v))
                except Exception:
                    secrets[k] = '***'
        summary['secrets'] = secrets
        return summary
    except Exception as e:
        return {'path': str(path), 'type': 'json', 'error': str(e)}

def inspect_env(path: Path):
    out = {'path': str(path), 'type': 'env', 'keys': [], 'secrets': {}}
    try:
        for line in path.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                k, v = line.split('=', 1)
                out['keys'].append(k.strip())
                if any(tok in k.lower() for tok in ('secret', 'key', 'token', 'password', 'client')):
                    out['secrets'][k.strip()] = mask_value(v.strip())
            else:
                out.setdefault('invalid_lines', []).append(line)
    except Exception as e:
        out['error'] = str(e)
    return out

def inspect_keyfile(path: Path):
    try:
        content = path.read_text(encoding='utf-8').strip()
        return {'path': str(path), 'type': 'key', 'length': len(content), 'nonempty': bool(content)}
    except Exception as e:
        return {'path': str(path), 'type': 'key', 'error': str(e)}

def gather_credentials(root: Path):
    results = []
    for dirpath, dirnames, filenames in os.walk(root):
        pdir = Path(dirpath)
        # skip virtual envs
        if 'venv' in pdir.parts or '.git' in pdir.parts:
            continue
        for fname in filenames:
            fpath = pdir / fname
            lname = fname.lower()
            try:
                if fpath.suffix == '.json' or any(k in lname for k in KEYWORDS) and fpath.suffix in ('.json', '.txt'):
                    results.append(inspect_json(fpath) if fpath.suffix == '.json' else {'path': str(fpath), 'type': fpath.suffix})
                elif fpath.suffix == '.env':
                    results.append(inspect_env(fpath))
                elif fpath.suffix in ('.key', '.pem') or 'key' in lname:
                    results.append(inspect_keyfile(fpath))
                elif 'token' in lname and fpath.suffix in ('.json', '.txt'):
                    results.append(inspect_json(fpath) if fpath.suffix == '.json' else inspect_keyfile(fpath))
                else:
                    # heuristics: filenames that match known credentials patterns
                    if any(tok in lname for tok in KEYWORDS):
                        if fpath.suffix == '.json':
                            results.append(inspect_json(fpath))
                        else:
                            results.append({'path': str(fpath), 'type': fpath.suffix or 'file'})
            except Exception as e:
                results.append({'path': str(fpath), 'error': str(e)})
    return results

def main():
    parser = argparse.ArgumentParser(description='Scan repository for credential files and validate them')
    parser.add_argument('--root', default='.', help='Root path to scan')
    parser.add_argument('--out', default='tools/credentials_report.json', help='Output JSON report path')
    args = parser.parse_args()

    root = Path(args.root).resolve()
    report = {'root': str(root), 'items': []}
    items = gather_credentials(root)
    report['items'] = items
    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(f"WROTE: {outp}")

if __name__ == '__main__':
    main()
