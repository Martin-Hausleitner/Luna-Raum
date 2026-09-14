"""Release browser checks; all screenshots come from the actual supplied URL."""
from pathlib import Path
import sys,json,hashlib
from playwright.sync_api import sync_playwright
url=sys.argv[1];out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True);checks=[];errors=[]
def ck(n,v,d=None):
 checks.append({'name':n,'passed':bool(v),'detail':d});print(n,v,d or '',flush=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/google-chrome',headless=False,args=['--enable-unsafe-webgpu','--use-angle=swiftshader','--enable-gpu','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--enable-features=Vulkan','--use-vulkan=swiftshader'])
 page=b.new_page(viewport={'width':1920,'height':1080});page.on('pageerror',lambda e:errors.append(str(e)));page.goto(url);page.wait_for_function('() => Luna.gpu.ready || !Luna.gpu.initializing',timeout=60000);ev=page.evaluate
 ck('actual-webgpu-ready',ev('Luna.gpu.ready'),ev('Luna.gpu.reason'))
 def shot(n):page.wait_for_timeout(400);page.screenshot(path=str(out/n))
 ev('Luna.debug.loadScene("studio");Luna.apps.open("room");Luna.debug.setView("3d")');shot('02-room-3d.png')
 box=page.locator('#drawing').bounding_box();x=box['x']+box['width']*.64;y=box['y']+box['height']*.58
 page.keyboard.down('Shift');page.mouse.move(x,y);page.mouse.down();page.mouse.move(x+100,y+30,steps=8);page.mouse.up();page.keyboard.up('Shift');ck('shift-drag-pans',ev('Math.abs(Luna.studio.state.panX)>.05'))
 page.mouse.move(x,y);page.mouse.wheel(0,-3500);page.wait_for_timeout(400);ck('zoom-to-six',ev('camera.zoom>2.8 && camera.zoom<=6'),ev('camera.zoom'));page.keyboard.press('Home');page.wait_for_timeout(200);ck('home-restores-camera',ev('camera.zoom===1 && Luna.studio.state.panX===0'))
 old=ev('camera.yaw');page.keyboard.press('Alt+ArrowRight');ck('keyboard-camera-orbit',ev('camera.yaw')>old)
 ev('Luna.debug.setSelected(Luna.store.state.cabinets.find(c=>c.wall==="I").id)');page.keyboard.press('f');page.keyboard.press('o');page.wait_for_timeout(250);ck('keyboard-open-front',ev('Luna.store.state.cabinets.find(c=>c.id===Luna.debug.selected).open===true'));shot('10-open-drawer-detail.png')
 ev('camera.home();Luna.gpu.invalidate(true)');page.keyboard.press('p');page.wait_for_timeout(300);ck('presentation-full-width',page.locator('#stage').bounding_box()['width']>1700);shot('11-presentation.png');page.keyboard.press('Escape')
 ev('Luna.debug.loadScene("studio");Luna.debug.setView("plan")');shot('03-plan.png');ev('Luna.debug.setView("A")');shot('04-elevation.png')
 ev('Luna.apps.open("takeoff")');shot('05-aufmass.png');ev('Luna.apps.open("catalog")');page.select_option('#placeWall','B');page.fill('#catalogSearch','Unterschrank 600');shot('06-catalog.png')
 ev('Luna.debug.loadScene("empty");Luna.apps.open("room");Luna.debug.setView("plan")');shot('07-empty-room.png');ev('Luna.apps.open("settings")');shot('08-settings.png');ev('Luna.wm.minimize()');shot('01-desktop.png')
 ev('Luna.debug.loadScene("studio");Luna.apps.open("room");Luna.store.state.forceCanvas=true;Luna.debug.refresh()');shot('09-canvas-fallback.png');ck('truthful-fallback',ev('Luna.debug.effectiveView==="plan"'))
 ck('no-javascript-errors',not errors,errors);report={'url':url,'browser':b.version,'softwareGPU':True,'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'checks':checks};(out/'release-results.json').write_text(json.dumps(report,indent=2));b.close();assert report['failed']==0,report
