"""Reproducible, dependency-free runtime builder. Browser QA dependencies are separate."""
from pathlib import Path
import sys,re,hashlib,json,shutil
D=Path(sys.argv[1]); source=Path(__file__).parent
s=(D/'Luna-Raum.html').read_text()
assert 'Luna.version' in s and 'detailedMesh' in s
s=s.replace(', .55, 2.8',', .35, 6').replace(',.55,2.8)',',.35,6)')
s=s.replace('<title>LUNA RAUM 2 · Detailplanung · EDV Hausleitner</title>','<title>LUNA RAUM 3 · Atelier · EDV Hausleitner</title>')
# Sidebar suppression in presentation uses actual IDs/classes instead of a new shell.
extra=(source/'studio.js').read_text()
s=s.replace('// Render an interactive Canvas plan first;',extra+'\n// Render an interactive Canvas plan first;')
# Guard unsupported schematic constructs in the parts model.
s=s.replace("if(t.kind==='gap')continue;const inside", "if(t.kind==='gap'||t.equipment==='hood')continue;const inside")
s=s.replace("add(t.drawers>0?'Auszugsfront':'Türfront',fronts,fw,fh,19,finishFor(c).name)","if(!t.shelf)add(t.drawers>0?'Auszugsfront':'Türfront',fronts,fw,fh,19,finishFor(c).name)")
(D/'Luna-Raum.html').write_text(s)
(D/'runtime.js').write_text(s[s.index("'use strict';"):s.rindex('</script>')])
q=(D/'qa_v2.py').read_text().replace('Luna.version===\"2.0.0\"','Luna.version===\"3.0.0\"').replace('LUNA RAUM 2.0.0','LUNA RAUM 3.0.0').replace("'version-2'","'version-3'")
q=q.replace("'document.documentElement.dataset.ready === \"true\"'","'() => document.documentElement.dataset.ready === \"true\"'").replace("'Luna.gpu.ready || !Luna.gpu.initializing'","'() => Luna.gpu.ready || !Luna.gpu.initializing'")
(D/'qa_v3_legacy.py').write_text(q)
shutil.copy2(source/'studio.js',D/'studio.js')
shutil.copy2(source/'upgrade.py',D/'upgrade.py')
print('LUNA3_SHA256',hashlib.sha256(s.encode()).hexdigest())
