"""Browser acceptance for the user-requested public LUNA RAUM demo. No private data."""
import sys,json,pathlib
from playwright.sync_api import sync_playwright
url=sys.argv[1];out=pathlib.Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,ok,detail=None):
 checks.append(dict(name=name,passed=bool(ok),detail=detail));print('PASS' if ok else 'FAIL',name,detail or '',flush=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=p.chromium.executable_path,headless=True,args=['--enable-unsafe-webgpu','--use-angle=swiftshader','--enable-features=Vulkan','--disable-vulkan-surface'])
 page=b.new_page(viewport={'width':1920,'height':1080},accept_downloads=True);page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(url);page.wait_for_timeout(3000);ev=page.evaluate
 check('version-3',ev('Luna.version === "3.0.0"'))
 check('50-additions-minimum',ev('Luna.studio.features.length>=50'),ev('Luna.studio.features.length'))
 ev('Luna.debug.loadScene("studio");Luna.apps.open("room");Luna.debug.setView("3d")');page.wait_for_timeout(300)
 check('gpu-ready',ev('Luna.gpu.ready'),ev('Luna.gpu.reason'));page.screenshot(path=str(out/'02-room-3d.png'))
 pixels=ev('''()=>{const g=Luna.gpu,c=document.querySelector('#gpuCanvas');g.render(performance.now());const cv=document.createElement('canvas');cv.width=c.width;cv.height=c.height;const x=cv.getContext('2d');x.drawImage(c,0,0);const d=x.getImageData(0,0,cv.width,cv.height).data;let n=0;for(let i=0;i<d.length;i+=4)if(d[i+3]>128&&d[i]<200)n++;return {dark:n,total:cv.width*cv.height,fraction:n/(cv.width*cv.height)}}''')
 check('visible-kitchen-pixels',pixels['fraction']>.06,pixels)
 ev('Luna.debug.setSelected(Luna.store.state.cabinets.find(c=>c.wall==="I").id)');page.click('#focus3');page.wait_for_timeout(200);check('module-focus',ev('camera.zoom===2.8 && Math.abs(Luna.studio.state.panX)>.01'));page.screenshot(path=str(out/'20-focus.png'))
 ev('camera.home();Luna.gpu.invalidate(true)');page.click('#projection3');page.wait_for_timeout(200);check('perspective-matrix',ev('Luna.studio.state.perspective && camera.vp[15]!==1'));page.screenshot(path=str(out/'21-perspective.png'))
 ev('camera.home();Luna.gpu.invalidate(true)');page.click('#present3');page.wait_for_timeout(250);check('presentation-mode',ev('Luna.studio.state.present'));page.screenshot(path=str(out/'22-presentation.png'));page.keyboard.press('Escape');check('escape-restores-workbench',ev('!Luna.studio.state.present'))
 page.click('#orbit3');before=ev('camera.yaw');page.wait_for_timeout(400);after=ev('camera.yaw');page.click('#orbit3');check('real-auto-orbit',after>before and ev('!Luna.studio.state.orbit'))
 ev('Luna.studio.saveBookmark("Kameratest");camera.yaw=1.8;Luna.studio.restoreBookmark(0)');check('save-restore-camera',ev('Luna.studio.state.bookmarks.length===1 && camera.yaw!==1.8'))
 price=ev('Luna.takeoff.calculate().sum');ev('Luna.studio.applyStyle(1)');check('style-package',ev('Luna.store.state.finish==="sage" && Luna.store.state.settings.handles==="brass"'));ev('Luna.debug.undo()');check('undo-style',abs(ev('Luna.takeoff.calculate().sum')-price)<.001)
 page.click('#helpButton3');page.fill('#featureSearch3','Insel');n=page.locator('#featureList3 li:visible').count();check('feature-search',4<=n<20);page.screenshot(path=str(out/'23-features.png'));page.click('#detailCancel')
 with page.expect_download() as d:page.click('#report3')
 d.value.save_as(str(out/'Gespraechsblatt.txt'));check('report-download',len((out/'Gespraechsblatt.txt').read_text())>500)
 ev('Luna.debug.loadScene("studio");Luna.apps.open("takeoff")');page.wait_for_timeout(200);page.screenshot(path=str(out/'05-aufmass.png'))
 ev('Luna.apps.open("room");Luna.debug.setView("3d");camera.home();Luna.gpu.invalidate(true)');page.wait_for_timeout(200)
 with page.expect_download() as d:page.click('#pngExport')
 d.value.save_as(str(out/'24-export-kitchen.png'));check('png-download',(out/'24-export-kitchen.png').stat().st_size>10000)
 ev('Luna.store.state.forceCanvas=true;Luna.debug.refresh()');page.wait_for_timeout(200);page.screenshot(path=str(out/'09-canvas-fallback.png'));check('canvas-is-plan',ev('Luna.debug.effectiveView==="plan"'))
 page.reload();page.wait_for_timeout(2000);ev('Luna.studio.readBookmarks()');check('bookmarks-persist',ev('Luna.studio.state.bookmarks.length===1'))
 page.set_viewport_size({'width':390,'height':844});page.wait_for_timeout(200);check('mobile-overflow',ev('document.documentElement.scrollWidth<=innerWidth'));page.screenshot(path=str(out/'25-mobile.png'))
 check('javascript-errors',not errors,errors)
 report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors,browser=b.version,url=url,softwareGPU=True)
 (out/'studio-results.json').write_text(json.dumps(report,indent=2));(out/'features.json').write_text(json.dumps(ev('Luna.studio.features'),ensure_ascii=False,indent=2));b.close()
 assert report['failed']==0,report
