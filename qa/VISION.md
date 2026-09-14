# LUNA RAUM — visual acceptance

Status: **PASS local / PASS public GitHub Pages**. Inspected real browser PNGs at **1600 × 1000**, not generated mockups. Source file and live root share SHA-256 `94904a6cf5f4e9935ebac0686a5ed100a546ff865591e7431aa8d483190603db`.

The local set `01-desktop.png` through `08-settings.png` and `09-canvas-fallback.png` was visually opened and inspected. The live set was captured by navigating to `https://martin-hausleitner.github.io/Luna-Raum/`; `live/02-room-3d.png`, `live/05-aufmass.png` and `live/09-canvas-fallback.png` were independently opened and inspected after download from the GitHub Pages build artifact. PNG hashes match the browser test reports.

| Required visual criterion | Local | Pages | Evidence |
|---|---|---|---|
| Windows 11-inspired chrome, taskbar, right caption controls | PASS | PASS | 02, 05 |
| Blue title bar; LUNA RAUM and Hausleitner legible | PASS | PASS | 02, 05 |
| Furnished scene visibly reads as a room and kitchen | PASS | PASS | 02 |
| Dimensions shown in millimetres | PASS | PASS | 02, 03; live 02, 09 |
| Synchronized non-zero demo takeoff visible | PASS | PASS | 02, 05 |
| German product interface | PASS | PASS | 02, 05 |
| Required demo / not-BIM / local-data disclaimer visible | PASS | PASS | 02, 05, 09 |
| Canvas badge corresponds to a visible usable floor plan | PASS | PASS | 09 |
| No Aster branding and no empty black viewport | PASS | PASS | 02, 05, 09 |

Local 01 also shows four working desktop launchers; 04 shows the cabinet wall elevation; 06 shows an actually placed 600 mm base on wall B with updated counts; 07 is the empty measure-up scene; 08 shows usable settings. The full local and live assertion reports each record **85 passes and zero failures**. Native WebGPU was also checked in default Chrome without special GPU flags.

These checks establish the specified bounded demo on the tested Mac/Chrome configuration, not professional kitchen-planning suitability, all-browser certification, or a universal frame-rate guarantee. See README for geometry, quantity and price limitations.

## Verified inspected-image hashes

`qa/01-desktop.png` — `86b9b7ae7577d65d932e4428550662c9ba2c4ffef97134670251f86bc5ee52e0`

`qa/02-room-3d.png` — `933979322a50631e28ec60e8b87109702cbbc5b890cad9390e2757de9ec38794`

`qa/03-plan.png` — `fea10664eca3ea1678eed5ddc914deaff0be5111d541b7c44652093d9d23b54e`

`qa/04-elevation.png` — `a6adf35751923037089cc2c202ca76ea43cebb5d4c2fe85fb5a947e41ff68ea2`

`qa/05-aufmass.png` — `66ad61885475963faa7f364d97630bc724b7584530c92651e16864c41ad9d5e6`

`qa/06-catalog.png` — `20ed867bce6860ce6184823271bffdf0655406b1204bc44d0bb2e42942c5071a`

`qa/07-empty-room.png` — `6f8e095a466f635c2c5a682e2bf4a735e94f4fefba3e5fda60f6bba1deb3e14a`

`qa/08-settings.png` — `68d6a37150a84ccd3ca20abbb73e581eeaa91df46f10c93388966305e387490c`

`qa/09-canvas-fallback.png` — `e796029c5e3a79485e7360c4151d6abc9f15d0ac46a28f609aa52511ed968167`

`qa/live/02-room-3d.png` — `c2d1fab48efd05791a5767bbcb547026d13c12d14a8724d5d536a75ecda2f5e3`

`qa/live/05-aufmass.png` — `8d8b8e1930200293a6141098ad12bc979fbd6345b651bd747eebe67927595e4e`

`qa/live/09-canvas-fallback.png` — `b0ef763a654803af8cd82eefff3bef01dc14a99edc02a8c62cfca0bc1b2bf74b`

