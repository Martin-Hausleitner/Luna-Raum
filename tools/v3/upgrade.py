"""Reproducible runtime builder; browser GPU flags are QA-only."""
from pathlib import Path
import sys,re,hashlib,json,shutil
D=Path(sys.argv[1]); source=Path(__file__).parent
s=(D/'Luna-Raum.html').read_text();assert 'Luna.version' in s and 'detailedMesh' in s
s=s.replace(',.55,2.8)',',.35,6)')
s=s.replace('<title>LUNA RAUM 2 · Detailplanung · EDV Hausleitner</title>','<title>LUNA RAUM 3 · Atelier · EDV Hausleitner</title>')
extra=(source/'studio.js').read_text().replace('.presentation3 .inspector','.presentation3 #inspector').replace('.presentation3 #projectHeader','.presentation3 .projectbar')
extra=extra.replace('SERVICES[s.type].name||s.type','SERVICES[s.type].name||SERVICES[s.type].label||s.type')
s=s.replace('// Render an interactive Canvas plan first;',extra+'\n// Render an interactive Canvas plan first;')
s=s.replace("if(t.kind==='gap')continue;const inside", "if(t.kind==='gap'||t.equipment==='hood')continue;const inside")
s=s.replace("add(t.drawers>0?'Auszugsfront':'Türfront',fronts,fw,fh,19,finishFor(c).name)","if(!t.shelf)add(t.drawers>0?'Auszugsfront':'Türfront',fronts,fw,fh,19,finishFor(c).name)")
s=s.replace('const d=await a.requestDevice();this.device=d;', 'this.adapter=a;const d=await a.requestDevice();this.device=d;')
(D/'Luna-Raum.html').write_text(s);(D/'runtime.js').write_text(s[s.index("'use strict';"):s.rindex('</script>')])
def qa_patch(q):
 q=q.replace('headless=True','headless=False').replace('executable_path=p.chromium.executable_path',"executable_path='/usr/bin/google-chrome'").replace('executable_path=a.browser',"executable_path='/usr/bin/google-chrome'")
 q=q.replace("'--use-angle=swiftshader'","'--use-angle=swiftshader','--enable-gpu','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'").replace("'--disable-vulkan-surface'","'--use-vulkan=swiftshader'")
 return q
q=(D/'qa_v2.py').read_text().replace('Luna.version===\"2.0.0\"','Luna.version===\"3.0.0\"').replace('LUNA RAUM 2.0.0','LUNA RAUM 3.0.0').replace("'version-2'","'version-3'")
(D/'qa_v3_legacy.py').write_text(qa_patch(q));(D/'qa_studio.py').write_text(qa_patch((source/'qa_studio.py').read_text()))
shutil.copy2(source/'studio.js',D/'studio.js');shutil.copy2(source/'upgrade.py',D/'upgrade.py')
print('LUNA3_SHA256',hashlib.sha256(s.encode()).hexdigest())
