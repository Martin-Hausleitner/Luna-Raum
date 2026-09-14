"""Package only the reviewed application and its evidence; no temporary builds as runtime."""
from pathlib import Path
import sys,shutil,json,hashlib
c=Path(sys.argv[1]);dest=Path(sys.argv[2]);dest.mkdir(parents=True,exist_ok=True)
r=json.loads((c/'qa/v3-regression/test-results.json').read_text());s=json.loads((c/'qa/atelier/studio-results.json').read_text());v=json.loads((c/'qa/release/release-results.json').read_text())
assert r['failed']==s['failed']==v['failed']==0
blob=(c/'Luna-Raum.html').read_bytes();assert b"Luna.version='3.0.0'" in blob
(dest/'Luna-Raum.html').write_bytes(blob);shutil.copy2(c/'LICENSE',dest/'LICENSE');(dest/'.nojekyll').touch()
root=Path(__file__).resolve().parents[1];readme=(root/'docs/ATELIER-V3.md').read_text();old=(c/'README.md').read_text();at=old.find('## Reference projects, provenance and MIT credits');readme+='\n\n'+old[at:] if at>=0 else ''
readme+='\n## Recorded release checks\n\nLocal browser: '+str(r['passed'])+' regression + '+str(s['passed'])+' camera/pixel/export + '+str(v['passed'])+' pointer/release checks. See `qa/` for the individual results and screenshots. This does not establish target-device hardware frame rate.\n'
(dest/'README.md').write_text(readme)
f=json.loads((c/'qa/atelier/features.json').read_text());assert len(f)>=50
(dest/'FEATURES.md').write_text('# LUNA RAUM 3 · Funktionsverzeichnis\n\n'+str(len(f))+' Erweiterungen gegenüber der ursprünglich ausgelieferten Version 1. Die zuvor nicht fertig ausgelieferte Detailversion 2 ist darin enthalten.\n\n'+'\n'.join(str(i+1)+'. '+n for i,n in enumerate(f))+'\n\nDemo: keine BIM-, CNC-, Bestell- oder freigegebenen Fertigungsdaten.\n')
shutil.copytree(c/'qa/release',dest/'qa',dirs_exist_ok=True);shutil.copytree(c/'qa/v3-regression',dest/'qa/regression',dirs_exist_ok=True);shutil.copytree(c/'qa/atelier',dest/'qa/atelier',dirs_exist_ok=True)
(dest/'tests').mkdir(exist_ok=True)
for name,new in [('qa_v3_legacy.py','regression.py'),('qa_studio.py','studio.py')]:shutil.copy2(c/name,dest/'tests'/new)
shutil.copy2(root/'tools/qa_release_v3.py',dest/'tests/release.py');shutil.copytree(c/'original',dest/'tests/original',dirs_exist_ok=True)
manifest={'version':'3.0.0','runtime':'Luna-Raum.html','bytes':len(blob),'sha256':hashlib.sha256(blob).hexdigest(),'features':len(f),'regression':r['passed'],'studio':s['passed'],'release':v['passed'],'bootMs':r['gpu']['stats']['bootMs'],'browser':r['browser'],'gpuVerification':'software WebGPU; not a hardware 60-fps guarantee'}
(dest/'RELEASE.json').write_text(json.dumps(manifest,indent=2));print(json.dumps(manifest,indent=2))
