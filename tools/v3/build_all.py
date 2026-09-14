"""Rebuild LUNA RAUM from the reviewed v1 base and checked v2 source bundle."""
from pathlib import Path
import sys,base64,gzip,hashlib,json,shutil,subprocess
root=Path(__file__).resolve().parents[2];build=Path(sys.argv[1] if len(sys.argv)>1 else root/'candidate');build.mkdir(parents=True,exist_ok=True)
payload=json.loads((root/'tools/v2/source.bundle.json').read_text());names=['source.00.b64','source.01.b64','source.02.b64','source.03.b64'];assert payload['chunks']==names
chunks=[(root/'tools/v2'/n).read_text().strip() for n in names];chunks[0]=chunks[0].replace('VcaFdwRrr','VcaFfwRrr',1)
raw=gzip.decompress(base64.b64decode(''.join(chunks),validate=True));assert hashlib.sha256(raw).hexdigest()==payload['source_sha256']
base=root/'dev/v2/base.html'
if not base.exists():base=root/'Luna-Raum.html'
blob=base.read_bytes();assert hashlib.sha256(blob).hexdigest()==payload['base_sha256'],'Base changed; do not silently rebase'
(build/'base.html').write_bytes(blob)
allowed=['early.js','extension.js','mesh-v2.js','shader.wgsl','style-v2.css','build.py','qa_v2.py','README.md']
for name,text in json.loads(raw).items():
 assert name in allowed and Path(name).name==name
 (build/name).write_text(text)
(build/'original/qa').mkdir(parents=True,exist_ok=True);shutil.copy2(root/'qa/export-Projekt.json',build/'original/qa/export-Projekt.json');shutil.copy2(root/'LICENSE',build/'LICENSE')
subprocess.run([sys.executable,str(root/'tools/v2/repair_candidate.py'),str(build)],check=True)
subprocess.run([sys.executable,str(build/'build.py')],check=True)
subprocess.run([sys.executable,str(root/'tools/v3/upgrade.py'),str(build)],check=True)
