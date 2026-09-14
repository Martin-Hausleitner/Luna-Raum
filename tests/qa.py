#!/usr/bin/env python3
"""LUNA RAUM browser QA. Python + Playwright are TEST dependencies only.
Usage: python tests/qa.py --url file:///.../Luna-Raum.html --out qa
       python tests/qa.py --url https://OWNER.github.io/Luna-Raum/ --out qa/live
No npm, package installation, server or framework is used by the product.
"""
import argparse, json, pathlib, time, hashlib, platform, sys
from playwright.sync_api import sync_playwright
ap=argparse.ArgumentParser();ap.add_argument('--url');ap.add_argument('--content');ap.add_argument('--browser');ap.add_argument('--out',default='qa');ap.add_argument('--shots-only',action='store_true');ap.add_argument('--live',action='store_true');args=ap.parse_args()
out=pathlib.Path(args.out);out.mkdir(parents=True,exist_ok=True);checks=[];errors=[];requests=[]
def record(name,ok,detail=''):
 checks.append({'test':name,'pass':bool(ok),'detail':detail})
 print(('PASS ' if ok else 'FAIL ')+name, detail,flush=True)
def test(name,fn):
 try: v=fn();record(name,v if isinstance(v,bool) else bool(v),'' if isinstance(v,bool) else v)
 except Exception as e: record(name,False,str(e)[:350])
with sync_playwright() as p:
 options={'headless':True}
 if args.browser:options['executable_path']=args.browser
 options['args']=['--enable-unsafe-webgpu']
 if platform.system()=='Linux':options['args']+=['--no-sandbox','--use-angle=swiftshader']
 b=p.chromium.launch(**options); context=b.new_context(viewport={'width':1600,'height':1000},device_scale_factor=1,accept_downloads=True);page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:requests.append(r.url))
 def load():
  if args.content:page.set_content(pathlib.Path(args.content).read_text())
  else:page.goto(args.url,wait_until='load')
  page.wait_for_function('document.documentElement.dataset.ready === "true"');page.wait_for_timeout(1000)
 def ev(s):return page.evaluate(s)
 def reset(name='berger'):
  ev('Luna.debug.loadScene('+json.dumps(name)+')');page.wait_for_timeout(80)
 def app(n):ev('Luna.apps.open('+json.dumps(n)+')');page.wait_for_timeout(100)
 def shot(n):
  page.wait_for_timeout(200);page.screenshot(path=str(out/n))
 load();gpu=ev('({ready:Luna.gpu.ready,reason:Luna.gpu.reason,stats:Luna.gpu.stats})');record('shell-first-view-under-700ms',gpu['stats']['bootMs']<=700,gpu['stats']['bootMs']);record('runtime-started',ev('Object.keys(Luna).includes("apps")'))
 if not args.shots_only:
  test('eight-engine-namespaces',lambda:ev('["theme","wm","store","room","gpu","place","takeoff","apps"].every(k=>!!Luna[k])'))
  test('twelve-required-catalog-modules',lambda:ev('Luna.debug.catalog.length===12'))
  test('default-room-dimensions',lambda:ev('JSON.stringify(Luna.store.state.room)==="{\\"w\\":4200,\\"d\\":3600,\\"h\\":2600}"'))
  test('floor-area-15.12',lambda:abs(ev('Luna.takeoff.calculate().floor')-15.12)<1e-9)
  test('gross-walls-40.56',lambda:abs(ev('Luna.takeoff.calculate().gross')-40.56)<1e-9)
  test('openings-area-3.57',lambda:abs(ev('Luna.takeoff.calculate().openings')-3.57)<1e-9)
  test('net-walls-36.99',lambda:abs(ev('Luna.takeoff.calculate().wall')-36.99)<1e-9)
  test('berger-counts',lambda:ev('JSON.stringify(Luna.takeoff.calculate().count)==="{\\"base\\":4,\\"wall\\":2,\\"tall\\":1,\\"gap\\":1}"'))
  test('berger-run-4200',lambda:ev('Luna.takeoff.calculate().runs[0].length===4200'))
  test('worktop-3.60lm',lambda:ev('Luna.takeoff.calculate().top===3.6'))
  test('plinth-4.20lm',lambda:ev('Luna.takeoff.calculate().plinth===4.2'))
  test('oak-demo-total-3981.80',lambda:abs(ev('Luna.takeoff.calculate().sum')-3981.8)<1e-6)
  test('no-default-collisions',lambda:ev('Luna.place.collisions().bad.size===0'))
  test('canvas-fallback-plan-drawn',lambda:ev('(()=>{Luna.store.state.forceCanvas=true;Luna.debug.setView("3d");Luna.gpu.render(performance.now());return Luna.debug.effectiveView==="plan"&&Luna.debug.plan.s>0})()'))
  test('canvas-badge-truthful',lambda:page.locator('#gpuBadge').inner_text()=='Canvas · Grundriss')
  ev('Luna.store.state.forceCanvas=false;Luna.debug.setView("plan")');page.wait_for_timeout(100)
  test('wall-dimension-click',lambda:ev('(()=>{const p=Luna.debug.plan;return Luna.gpu.pick(p.x+2100*p.s,p.y-32)==="wall:A"})()'))
  test('wall-selection-dimension-text',lambda:(ev('Luna.debug.selectWall("B")') or '3 600 mm' in page.locator('#selection').inner_text()))
  reset();app('catalog');page.locator('#placeWall').select_option('B');page.locator('[data-type="base600"]').click()
  test('catalog-button-adds-600',lambda:ev('Luna.store.state.cabinets.length===9&&Luna.store.state.cabinets.at(-1).type==="base600"'))
  test('snap-to-wall-next-free-slot',lambda:ev('Luna.store.state.cabinets.at(-1).wall==="B"&&Luna.store.state.cabinets.at(-1).offset===600'))
  test('quantities-update-after-place',lambda:ev('Luna.takeoff.calculate().count.base===5'))
  test('new-run-selected-after-place',lambda:'Wand B' in page.locator('#runSelect').inner_text())
  ev('Luna.debug.undo()');test('undo-placement',lambda:ev('Luna.store.state.cabinets.length===8'))
  ev('Luna.debug.redo()');test('redo-placement',lambda:ev('Luna.store.state.cabinets.length===9'))
  ev('Luna.place.move(Luna.store.state.cabinets.at(-1).id,"A",1400)');test('aabb-collision-detected',lambda:ev('Luna.place.collisions().bad.size>=2'))
  test('collision-warning-visible',lambda:page.locator('#collisionNotice').is_visible())
  ev('Luna.debug.undo()');test('undo-clears-collision',lambda:ev('Luna.place.collisions().bad.size===0'))
  ev('Luna.place.move(Luna.store.state.cabinets.at(-1).id,"B",735)');test('100mm-rounding',lambda:ev('Luna.store.state.cabinets.at(-1).offset===700'))
  ev('Luna.debug.setSelected(Luna.store.state.cabinets.at(-1).id)');page.locator('#drawing').focus();page.keyboard.press('ArrowRight');test('keyboard-100mm-move',lambda:ev('Luna.store.state.cabinets.at(-1).offset===800'))
  page.keyboard.press('Delete');test('keyboard-delete',lambda:ev('Luna.store.state.cabinets.length===8'))
  reset('empty');test('empty-room-zero-cabinet-takeoff',lambda:ev('Luna.takeoff.calculate().count.base===0&&Luna.takeoff.calculate().sum===0&&Luna.takeoff.calculate().floor>0'))
  for wall in 'ABCD':
   ev('Luna.place.add("base600",'+json.dumps(wall)+')')
   test('place-on-wall-'+wall,lambda wall=wall:ev('Luna.store.state.cabinets.some(c=>c.wall==='+json.dumps(wall)+')'))
  test('four-wall-bounds-within-room',lambda:ev('Luna.store.state.cabinets.every(c=>{const b=Luna.place.bounds(c);return b.min[0]>=0&&b.min[2]>=0&&b.max[0]<=4200&&b.max[2]<=3600})'))
  reset();before=ev('Luna.takeoff.calculate().sum');page.locator('[data-finish="white"]').click();test('white-price-lower-and-live',lambda:ev('Luna.takeoff.calculate().sum')<before);test('white-finish-persisted-state',lambda:ev('Luna.store.state.finish==="white"'))
  ev('Luna.debug.applyRoom(4500,3800,2700)');test('room-edit-updates-areas',lambda:abs(ev('Luna.takeoff.calculate().floor')-17.1)<1e-9)
  ev('Luna.debug.applyRoom(1400,1200,2000)');test('opening-outside-room-edit-rejected',lambda:ev('Luna.store.state.room.w===4500'))
  reset();ev('Luna.debug.showOpening()');page.locator('#opType').select_option('door');page.locator('#opWall').select_option('B');page.locator('#opOffset').fill('1400');page.locator('#openingForm button[type=submit]').click();test('door-form-adds-opening',lambda:ev('Luna.store.state.openings.length===3&&Luna.store.state.openings.at(-1).sill===0'))
  test('door-changes-net-wall-area',lambda:abs(ev('Luna.takeoff.calculate().wall')-35.10)<1e-6)
  ev('Luna.debug.showOpening()');page.locator('#opWall').select_option('A');page.locator('#opOffset').fill('1800');page.locator('#openingForm button[type=submit]').click();test('overlapping-opening-form-rejected',lambda:page.locator('#openingDialog').is_visible() and 'überschneidet' in page.locator('#openingError').inner_text());page.locator('#opCancel').click()
  reset('lshape');test('lshape-runs-3000-plus-2400',lambda:ev('Luna.takeoff.calculate().runs.map(r=>r.length).sort().join(",")==="2400,3000"'));test('lshape-no-collisions',lambda:ev('Luna.place.collisions().bad.size===0'));test('lshape-worktop-5.44',lambda:abs(ev('Luna.takeoff.calculate().top')-5.44)<1e-9)
  reset();app('talk');page.locator('#noteText').fill('Wasseranschluss: 600 mm ab Fertigfußboden.');page.locator('#noteForm button').click();test('local-note-add',lambda:ev('Luna.store.state.notes.length===3'))
  page.locator('[data-note-toggle]').last.click();test('note-mark-done',lambda:ev('Luna.store.state.notes.at(-1).done===true'))
  page.locator('[data-note-edit]').last.click();page.locator('#noteText').fill('Wasser 650 mm');page.locator('#noteForm button').click();test('note-edit',lambda:ev('Luna.store.state.notes.at(-1).text==="Wasser 650 mm"'))
  page.locator('[data-note-delete]').last.click();test('note-delete',lambda:ev('Luna.store.state.notes.length===2'))
  test('not-teams-disclosure',lambda:'not Teams' in page.locator('#pageTalk').inner_text())
  test('json-roundtrip',lambda:ev('(()=>{const a=JSON.stringify(Luna.store.state);return JSON.stringify(Luna.store.validate(JSON.parse(a)))===a})()'))
  test('json-invalid-schema-rejected',lambda:ev('(()=>{try{Luna.store.validate({schema:"x"});return false}catch{return true}})()'))
  test('json-invalid-catalog-rejected',lambda:ev('(()=>{const s=JSON.parse(JSON.stringify(Luna.store.state));s.cabinets[0].type="unknown";try{Luna.store.validate(s);return false}catch{return true}})()'))
  test('json-duplicate-ids-rejected',lambda:ev('(()=>{const s=JSON.parse(JSON.stringify(Luna.store.state));s.cabinets[1].id=s.cabinets[0].id;try{Luna.store.validate(s);return false}catch{return true}})()'))
  test('json-overlapping-openings-rejected',lambda:ev('(()=>{const s=JSON.parse(JSON.stringify(Luna.store.state));s.openings.push({...s.openings[0],id:"duplicate-geometry"});try{Luna.store.validate(s);return false}catch{return true}})()'))
  test('csv-bom-and-semicolon',lambda:ev('Luna.takeoff.csv().startsWith("\\uFEFF")&&Luna.takeoff.csv().includes(";")'))
  test('csv-takeoff-values',lambda:ev('Luna.takeoff.csv().includes("36,99")&&Luna.takeoff.csv().includes("3.981,80")==false&&Luna.takeoff.csv().includes("3 981,80")'))
  app('takeoff');test('takeoff-report-visible',lambda:page.locator('#pageTakeoff table').count()==2)
  if not args.content:
   with page.expect_download() as dl:page.locator('#takeoffCSV').click()
   dl.value.save_as(str(out/'export-Aufmass.csv'));record('csv-download-real-file',(out/'export-Aufmass.csv').stat().st_size>500)
   with page.expect_download() as dl:page.locator('#exportProject').click()
   dl.value.save_as(str(out/'export-Projekt.json'));record('json-download-real-file',json.loads((out/'export-Projekt.json').read_text())['schema']=='luna.raum.v1')
   page.reload(wait_until='load');page.wait_for_timeout(1200);test('localstorage-after-reload',lambda:ev('localStorage.getItem("luna.raum.v1")!==null&&Luna.store.state.cabinets.length===8'))
  app('settings');page.locator('#settingCanvas').check();test('force-canvas-setting',lambda:ev('Luna.store.state.forceCanvas===true'));page.locator('#settingCanvas').uncheck();test('restore-gpu-preference',lambda:ev('Luna.store.state.forceCanvas===false'))
  for view in ['plan','A','B','C','D']:
   ev('Luna.debug.setView('+json.dumps(view)+')');page.wait_for_timeout(70);test('render-view-'+view,lambda view=view:ev('Luna.debug.effectiveView')==view)
  app('room');page.locator('#minimize').click();test('window-minimize-to-desktop',lambda:page.locator('#window').is_hidden());page.locator('#desktopIcons [data-app=room]').click();test('desktop-icon-restores-app',lambda:page.locator('#window').is_visible());page.locator('#maximize').click();test('window-maximize',lambda:'maximized' in page.locator('#window').get_attribute('class'));page.locator('#maximize').click();page.locator('#closeWindow').click();test('window-close-keeps-state',lambda:ev('Luna.store.state.cabinets.length===8'));page.locator('#startButton').click();test('start-menu-opens',lambda:page.locator('#startmenu').is_visible());page.locator('#startApps [data-app=room]').click();test('start-menu-launches-room',lambda:page.locator('#window').is_visible() and page.locator('#startmenu').is_hidden())
  test('no-unrelated-branding-on-surface',lambda:all(x not in page.locator('body').inner_text() for x in ['Aster','Stratum','Converge']))
  test('required-footer-visible',lambda:page.locator('#footer').is_visible() and 'not a BIM model' in page.locator('#footer').inner_text())
  test('no-runtime-network-dependencies',lambda:all(u.startswith(args.url or 'about:') or u.startswith('data:') for u in requests))
  for width,height in [(1440,900),(834,1112),(390,844)]:
   page.set_viewport_size({'width':width,'height':height});page.wait_for_timeout(130);test('no-horizontal-overflow-'+str(width),lambda:ev('document.documentElement.scrollWidth<=innerWidth'))
   if width==390:shot('10-mobile.png')
  page.set_viewport_size({'width':1600,'height':1000})
  reset();app('room');ev('Luna.debug.setView("3d")');page.wait_for_timeout(700)
  if ev('Luna.gpu.ready'):
   bm=ev('Luna.gpu.benchmark(180)');(out/'orbit-performance.json').write_text(json.dumps(bm,indent=2));record('webgpu-native-pipeline',True,bm);record('orbit-target-60fps',bm['fps']>=55,bm['fps'])
  else:record('webgpu-native-pipeline',False,gpu['reason'])
 reset();app('room');ev('Luna.debug.setView("3d")');page.wait_for_timeout(4500)
 page.locator('#minimize').click();shot('01-desktop.png');page.locator('#desktopIcons [data-app=room]').click();page.wait_for_timeout(300);shot('02-room-3d.png')
 page.locator('[data-view=plan]').click();shot('03-plan.png');page.locator('[data-view=A]').click();shot('04-elevation.png');app('takeoff');shot('05-aufmass.png')
 app('catalog');ev('Luna.debug.setView("3d")');page.locator('#placeWall').select_option('B');page.locator('[data-type=base600]').click();page.wait_for_timeout(4500);shot('06-catalog.png')
 reset('empty');app('room');ev('Luna.debug.setView("plan")');page.wait_for_timeout(4500);shot('07-empty-room.png')
 reset();app('settings');page.wait_for_timeout(4500);shot('08-settings.png')
 app('room');ev('Luna.store.state.forceCanvas=true;Luna.debug.setView("3d")');shot('09-canvas-fallback.png');ev('Luna.store.state.forceCanvas=false;Luna.debug.setView("3d")')
 record('no-javascript-errors',not errors,errors);report={'url':args.url or 'about:blank with local inline HTML','browser':b.version,'host':platform.platform(),'viewport':[1600,1000],'gpu':gpu,'checks':checks,'passed':sum(c['pass'] for c in checks),'failed':sum(not c['pass'] for c in checks),'errors':errors,'requests':requests,'screenshots':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in out.glob('*.png')}};(out/'test-results.json').write_text(json.dumps(report,indent=2,ensure_ascii=False));print(json.dumps({'passed':report['passed'],'failed':report['failed'],'gpu':gpu},indent=2),flush=True);b.close()
