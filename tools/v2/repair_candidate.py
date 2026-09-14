"""Version-controlled candidate corrections applied after the verified transport bundle."""
from pathlib import Path
import sys
p=Path(sys.argv[1])/'qa_v2.py'
s=p.read_text()
s=s.replace("P.add_argument('--quick',action='store_true');", "P.add_argument('--quick',action='store_true');P.add_argument('--software-gpu',action='store_true');")
old="args=['--no-sandbox','--enable-unsafe-webgpu','--use-angle=swiftshader','--disable-dev-shm-usage']"
new="args=['--no-sandbox','--disable-dev-shm-usage']+(['--enable-unsafe-webgpu','--use-angle=swiftshader','--enable-features=Vulkan','--use-vulkan=swiftshader','--disable-vulkan-surface'] if a.software_gpu else[])"
assert old in s
s=s.replace(old,new)
old="  page.wait_for_timeout(1800)\n  gpu=ev"
new="  page.wait_for_timeout(1800)\n  if a.require_gpu:\n   try:page.wait_for_function('Luna.gpu.ready || !Luna.gpu.initializing',timeout=60000)\n   except Exception:print('GPU_INIT_TIMEOUT',ev('({reason:Luna.gpu.reason,initializing:Luna.gpu.initializing,stats:Luna.gpu.stats})'),flush=True)\n  gpu=ev"
assert old in s
s=s.replace(old,new)
s=s.replace("No GPU exposed by opaque inline origin. No 3D PASS claimed for this run.", "WebGPU was not ready in this browser run. No 3D PASS claimed.")
s=s.replace("'environment':platform.platform(),", "'environment':platform.platform(),'softwareGPURequested':a.software_gpu,")
p.write_text(s)
print('Applied explicit CI WebGPU configuration and asynchronous initialization gate')
