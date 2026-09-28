#!/usr/bin/env python3
"""Read-only WhatsApp artifact inventory. Never extracts archives or decrypts content."""
from __future__ import annotations
import argparse, hashlib, json, re, zipfile
from datetime import datetime, timezone
from pathlib import Path

CRYPT = re.compile(r"^msgstore(?:[-.]|).*\.crypt\d*$", re.I)
EXPORT_PATTERNS = [
    re.compile(r"^WhatsApp Chat with .+\.txt$", re.I),
    re.compile(r"^WhatsApp[- _]?Chat mit .+\.txt$", re.I),
    re.compile(r"^Chat de WhatsApp con .+\.txt$", re.I),
    re.compile(r"^Discussion WhatsApp avec .+\.txt$", re.I),
    re.compile(r"^Chat WhatsApp con .+\.txt$", re.I),
]
LEVELDB_NAME = re.compile(r"^(?:CURRENT|LOCK|LOG(?:\.old)?|MANIFEST-\d+|\d+\.(?:ldb|sst|log))$", re.I)
MAX_MEMBERS = 5000
MAX_OFFSETS = 32


def is_export_name(name: str) -> bool:
    return any(p.match(name) for p in EXPORT_PATTERNS)


def is_whatsapp_leveldb_path(path: Path) -> bool:
    s = str(path).lower().replace('\\', '/')
    return ('web.whatsapp.com' in s or 'whatsapp' in s) and ('indexeddb' in s or '.indexeddb.leveldb' in s)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def exact_hits(path: Path, identifiers: list[str]) -> dict[str, dict]:
    if not identifiers:
        return {}
    needles = {}
    for ident in identifiers:
        encs = []
        for enc in ('utf-8', 'utf-16le', 'utf-16be'):
            try:
                b = ident.encode(enc)
                if b and b not in encs:
                    encs.append(b)
            except UnicodeEncodeError:
                pass
        needles[ident] = encs
    found = {i: {'count': 0, 'offsets': []} for i in identifiers}
    overlap = max((len(n) for xs in needles.values() for n in xs), default=1) - 1
    pos = 0; tail = b''
    with path.open('rb') as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk: break
            data = tail + chunk
            base = pos - len(tail)
            for ident, encs in needles.items():
                seen = set()
                for needle in encs:
                    start = 0
                    while True:
                        idx = data.find(needle, start)
                        if idx < 0: break
                        absolute = base + idx
                        if absolute >= 0 and absolute not in seen:
                            seen.add(absolute)
                            found[ident]['count'] += 1
                            if len(found[ident]['offsets']) < MAX_OFFSETS:
                                found[ident]['offsets'].append(absolute)
                        start = idx + 1
            pos += len(chunk)
            tail = data[-overlap:] if overlap > 0 else b''
    return {k: v for k, v in found.items() if v['count']}


def inspect(path: Path, identifiers: list[str]) -> dict:
    st = path.stat()
    item = {
        'path': str(path), 'name': path.name, 'size_bytes': st.st_size,
        'modified_utc': datetime.fromtimestamp(st.st_mtime, timezone.utc).isoformat(),
        'sha256': sha256(path), 'kind': 'other'
    }
    if CRYPT.match(path.name):
        item['kind'] = 'encrypted_whatsapp_database'
        item['note'] = 'Encrypted WhatsApp backup filename; contents/key not decrypted.'
    elif is_export_name(path.name):
        item['kind'] = 'possible_whatsapp_text_export'
        item['note'] = 'Multilingual WhatsApp export filename recognized; message body intentionally not read.'
    elif LEVELDB_NAME.match(path.name) and is_whatsapp_leveldb_path(path):
        item['kind'] = 'whatsapp_chromium_leveldb_component'
    elif path.suffix.lower() == '.zip':
        item['kind'] = 'zip_archive'
        try:
            with zipfile.ZipFile(path) as zf:
                all_infos = zf.infolist()
                infos = all_infos[:MAX_MEMBERS]
                members, unsafe = [], []
                for info in infos:
                    name = info.filename
                    normalized = name.replace('\\', '/')
                    if normalized.startswith('/') or re.match(r'^[A-Za-z]:', normalized) or '..' in normalized.split('/'):
                        unsafe.append(name)
                    members.append({'name': name, 'size_bytes': info.file_size})
                item['zip_members'] = members
                item['zip_member_count_listed'] = len(members)
                item['zip_member_count_total'] = len(all_infos)
                item['unsafe_member_paths'] = unsafe
                item['contains_possible_whatsapp_export'] = any(is_export_name(Path(m['name']).name) for m in members)
                item['contains_possible_database_backup'] = any(CRYPT.match(Path(m['name']).name) for m in members)
        except (zipfile.BadZipFile, OSError) as e:
            item['zip_error'] = str(e)
    hits = exact_hits(path, identifiers)
    if hits:
        item['exact_identifier_hits'] = hits
    return item


def candidate(path: Path) -> bool:
    n = path.name
    return bool(CRYPT.match(n) or is_export_name(n) or n.lower().endswith('.zip') or (LEVELDB_NAME.match(n) and is_whatsapp_leveldb_path(path)))


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('path', type=Path, help='File or directory to inventory (read-only)')
    p.add_argument('--identifier', action='append', default=[], help='Exact JID/LID/phone/string to locate in recognized artifacts; repeatable')
    p.add_argument('--json', action='store_true', help='Emit JSON')
    args = p.parse_args()
    root = args.path.expanduser()
    if not root.exists(): p.error(f'Path not found: {root}')
    candidates = [root] if root.is_file() else sorted(x for x in root.rglob('*') if x.is_file() and candidate(x))
    results = []
    for f in candidates:
        try: results.append(inspect(f, args.identifier))
        except (PermissionError, OSError) as e: results.append({'path': str(f), 'error': str(e)})
    out = {'read_only': True, 'files': results}
    if args.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        if not results: print('No recognized WhatsApp artifacts found.')
        for x in results:
            print(f"{x.get('kind','error')}: {x.get('path')}")
            if 'size_bytes' in x: print(f"  size={x['size_bytes']} modified_utc={x['modified_utc']} sha256={x['sha256']}")
            if x.get('contains_possible_whatsapp_export'): print('  ZIP contains a possible WhatsApp text export; no extraction performed.')
            if x.get('contains_possible_database_backup'): print('  ZIP contains a possible encrypted WhatsApp database; no extraction performed.')
            if x.get('exact_identifier_hits'):
                for ident, h in x['exact_identifier_hits'].items(): print(f"  exact-hit {ident!r}: count={h['count']} offsets={h['offsets']}")
            if x.get('unsafe_member_paths'): print(f"  WARNING: unsafe ZIP paths flagged ({len(x['unsafe_member_paths'])}); do not extract blindly.")
            if x.get('error') or x.get('zip_error'): print(f"  error={x.get('error') or x.get('zip_error')}")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
