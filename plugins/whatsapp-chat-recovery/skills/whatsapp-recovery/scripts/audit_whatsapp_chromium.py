#!/usr/bin/env python3
"""Read-only structural triage for copied WhatsApp Web Chromium IndexedDB/LevelDB artifacts."""
from __future__ import annotations
import argparse, hashlib, json, re
from datetime import datetime, timezone
from pathlib import Path

LEVELDB = re.compile(r"^(?:CURRENT|LOCK|LOG(?:\.old)?|MANIFEST-\d+|\d+\.(?:ldb|sst|log))$", re.I)
SST_FOOTER = bytes.fromhex('57fb808b247547db')
MAX_OFFSETS = 64


def sha256(p: Path) -> str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()


def hits(p: Path, identifiers: list[str]) -> dict:
    needles={i:[i.encode('utf-8'),i.encode('utf-16le'),i.encode('utf-16be')] for i in identifiers}
    out={i:{'count':0,'offsets':[]} for i in identifiers}
    overlap=max((len(b) for xs in needles.values() for b in xs),default=1)-1
    pos=0; tail=b''
    with p.open('rb') as f:
        while True:
            chunk=f.read(1024*1024)
            if not chunk: break
            data=tail+chunk; base=pos-len(tail)
            for ident,encs in needles.items():
                local=set()
                for n in encs:
                    s=0
                    while True:
                        k=data.find(n,s)
                        if k<0: break
                        a=base+k
                        if a>=0 and a not in local:
                            local.add(a); out[ident]['count']+=1
                            if len(out[ident]['offsets'])<MAX_OFFSETS: out[ident]['offsets'].append(a)
                        s=k+1
            pos+=len(chunk); tail=data[-overlap:] if overlap>0 else b''
    return {k:v for k,v in out.items() if v['count']}


def classify(p: Path) -> str:
    n=p.name.lower()
    if n=='current': return 'leveldb_current'
    if n.startswith('manifest-'): return 'leveldb_manifest'
    if n.endswith(('.ldb','.sst')): return 'leveldb_sstable'
    if re.match(r'^\d+\.log$',n): return 'leveldb_wal'
    if n=='log' or n=='log.old': return 'leveldb_operational_log'
    if n=='lock': return 'leveldb_lock'
    return 'other'


def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('path',type=Path)
    ap.add_argument('--identifier',action='append',default=[])
    ap.add_argument('--json',action='store_true')
    a=ap.parse_args(); root=a.path.expanduser()
    if not root.exists(): ap.error(f'Path not found: {root}')
    files=[root] if root.is_file() else sorted(p for p in root.rglob('*') if p.is_file() and LEVELDB.match(p.name))
    results=[]
    for p in files:
        st=p.stat(); item={'path':str(p),'name':p.name,'kind':classify(p),'size_bytes':st.st_size,'modified_utc':datetime.fromtimestamp(st.st_mtime,timezone.utc).isoformat(),'sha256':sha256(p)}
        if item['kind']=='leveldb_sstable':
            try:
                with p.open('rb') as f:
                    if st.st_size>=8: f.seek(-8,2); item['sstable_footer_magic_ok']=(f.read(8)==SST_FOOTER)
                    else: item['sstable_footer_magic_ok']=False
            except OSError: item['sstable_footer_magic_ok']=False
        h=hits(p,a.identifier)
        if h: item['exact_identifier_hits']=h
        results.append(item)
    summary={
      'read_only':True,
      'root':str(root),
      'file_count':len(results),
      'kinds':{},
      'identifier_files':sum(1 for x in results if x.get('exact_identifier_hits')),
      'files':results
    }
    for x in results: summary['kinds'][x['kind']]=summary['kinds'].get(x['kind'],0)+1
    if a.json: print(json.dumps(summary,indent=2,ensure_ascii=False))
    else:
        print(f"read_only=True files={summary['file_count']} identifier_files={summary['identifier_files']}")
        print('kinds='+json.dumps(summary['kinds'],ensure_ascii=False))
        for x in results:
            extra=''
            if 'sstable_footer_magic_ok' in x: extra+=f" sstable_footer_magic_ok={x['sstable_footer_magic_ok']}"
            print(f"{x['kind']}: {x['path']} size={x['size_bytes']} sha256={x['sha256']}{extra}")
            for ident,h in x.get('exact_identifier_hits',{}).items(): print(f"  exact-hit {ident!r}: count={h['count']} offsets={h['offsets']}")
    return 0

if __name__=='__main__': raise SystemExit(main())
