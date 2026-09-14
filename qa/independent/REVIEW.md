# LUNA RAUM — independent release verification

**PASS: local file and public GitHub Pages.**

During this build, a complete canonical implementation was published to the requested repository by another concurrent run. That runtime and all repository history were preserved rather than overwritten with a competing build. The published file was independently retrieved, inspected and tested again in real Chrome. Only the test harness and additional evidence were changed in this verification pass.

## Identity

- Public repository: https://github.com/Martin-Hausleitner/Luna-Raum
- Live root: https://martin-hausleitner.github.io/Luna-Raum/
- Source runtime: `Luna-Raum.html`, 112281 bytes.
- Pages runtime: identical bytes, renamed `index.html` on `gh-pages`.
- Runtime SHA-256: `94904a6cf5f4e9935ebac0686a5ed100a546ff865591e7431aa8d483190603db`.
- HTTP 200 and source/live hash equality independently observed.

## Re-run results

Chrome 152.0.7977.83, macOS, native Apple WebGPU, screenshots at **1600 × 1000**. These are observed results on this machine, not universal performance guarantees.

| Gate | Local file | Live Pages |
|---|---:|---:|
| Browser assertions | 85/85 PASS | 85/85 PASS |
| First interactive rendered view | 106.4 ms | 318.1 ms |
| Real orbit benchmark, 180 frames | 60.0027 fps | 60.0027 fps |
| JavaScript errors | 0 | 0 |
| Native GPU pipeline | PASS | PASS |
| Canvas plan fallback | PASS | PASS |
| CSV download and local JSON persistence | PASS | PASS |

The harness now waits for the ready HTML attribute without evaluating a function string under CSP, uses a 59 fps lower bound for the approximately-60 fps check, and returns a non-zero process exit code whenever an assertion fails. No product CSP was weakened. The actual measured frame rate was 60.0027 fps, not merely the lower threshold.

## Visual inspection

Full-resolution local screenshots 01–08 and the live 02/05/09 screenshots in the deployed artifact were opened and inspected. Windows-style dark taskbar, blue title bar with right-aligned caption controls, readable EDV Hausleitner / LUNA RAUM branding, German labels, millimetre dimensions, non-zero takeoff and the required disclaimer are visible. The native scene reads as a furnished kitchen: tall/base/wall cabinets, oak fronts, worktop, sink, hob, window and navy grid. The fallback shows a populated dimensioned plan rather than a black rectangle. No Aster branding or embedded remote app appears on the product surface.

| Screenshot | Inspected state | Result |
|---|---|---|
| `01-desktop.png` | Desktop, four app shortcuts and dark taskbar | PASS |
| `02-room-3d.png` | Furnished Berger room, native WebGPU | PASS |
| `03-plan.png` | Top plan with 4200 / 3600 mm dimensions | PASS |
| `04-elevation.png` | Wall A, window, cabinets and height dimension | PASS |
| `05-aufmass.png` | Actual non-zero quantities and demo EUR value | PASS |
| `06-catalog.png` | 600 mm base placed on wall B and quantity update | PASS |
| `07-empty-room.png` | Empty cabinet layout for live measure-up | PASS |
| `08-settings.png` | Grid, snap, material, room dimensions and fallback | PASS |
| `live/02-room-3d.png` | Published native kitchen scene | PASS |
| `live/05-aufmass.png` | Published quantity table | PASS |
| `live/09-canvas-fallback.png` | Published functional Canvas plan | PASS |

Berger reference: 15.12 m² floor; 36.99 m² net walls; 4 base, 2 wall and 1 tall cabinet plus 1 appliance gap; 4.20 m run, 3.60 lm worktop and 4.20 lm plinth; **EUR 3981.80 fictional oak demo value**. See README for pricing assumptions and manufacturing exclusions.

This is a room/placement and measure-up conversation demo, not a certified kitchen planner, BIM model or licensed WAWI. AABB collisions, quantities and local notes are functional; fabrication details, supplier pricing, irregular-room modelling, installation validation, CNC and ordering are outside its scope.
