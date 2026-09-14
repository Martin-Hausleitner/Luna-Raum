# LUNA RAUM

**Aufmaß · Küche · 3D-Gespräch** — EDV Hausleitner theme.

[Open the browser demo](https://martin-hausleitner.github.io/Luna-Raum/) · [Single runtime file](Luna-Raum.html) · [Local test evidence](qa/test-results.json)

## Deutsch

Eine **inoffizielle, lokale 3D-Aufmaß- und Küchengespräch-Demo** für Tischlereien. Kein BIM-Modell, kein Roomle, kein Vectorworks, keine lizenzierte WAWI und kein fertigungstauglicher Küchenplaner. Sie öffnen `Luna-Raum.html` direkt im Browser. Es gibt keine Installation, kein Konto, keinen Anwendungsserver und keine npm-, CDN-, Framework- oder Schrift-Abhängigkeiten.

Der Windows-11-inspirierte Arbeitsplatz umfasst **Raum, Katalog, Aufmaß, Grundriss, Gespräch und Einstellungen**. Native WebGPU-Geometrie zeigt den möblierten Raum; ohne nutzbaren Adapter bleibt der vollständig bedienbare Canvas-2D-Grundriss. Der Rendererstatus zeigt den tatsächlich aktiven Pfad. Die App lädt keine anderen Anwendungen in Iframes.

### Das funktioniert

- Rechteckiger Raum, standardmäßig **4 200 × 3 600 × 2 600 mm**, editierbare Wandpaare A/C und B/D und Raumhöhe; Türen und Fenster mit Brüstungshöhe. Öffnungen werden geometrisch aus den 3D-Wänden ausgespart.
- 3D-Orbit, Grundriss und vier Wandansichten A/B/C/D, sichtbare Millimetermaße, Raster 100 mm, Auswahl, Verschieben, Rückgängig/Wiederholen.
- Zwölf Module: Unterschränke 300/400/500/600/800/1000 mm, Spülenunterschrank 600, Geschirrspülerlücke 600, Oberschränke 600/800/1000 und Hochschrank 600. Eiche natur oder Alpinweiß. Automatische Arbeitsplatte 600 mm tief und 40 mm stark, 20 mm Überstand an freien Enden und vorn.
- Wandgebundene Platzierung, Suche nach dem nächsten freien Rasterplatz, dreidimensionale AABB-Kollisionen, Fenster-/Türbereichswarnungen. Manuell erzeugte Überschneidungen werden rot markiert, nicht verschwiegen.
- Synchrones Aufmaß mit Boden- und Netto-/Bruttowandflächen, Schrankanzahlen, Zeilenlängen, Wangen, Arbeitsplatte, Sockel, Wandabschluss und offen ausgewiesenen **fiktiven Demopreisen in EUR**. CSV-Export, Projekt-JSON-Import/-Export und Druckansicht.
- Drei Demoprojekte: Familie Berger, leerer Aufmaßraum und L-Küche 3 000 + 2 400 mm. Szenenwechsel mit einem Klick und Rückgängig-Möglichkeit.
- Lokale Gesprächsnotizen, bearbeitbar/abhakbar/löschbar, etwa „Steckdose 350 mm“ und „Wasser 600 mm“. **not Teams**: kein Chatserver, keine Videokonferenz, keine Netzwerk-Synchronisation.

### Bedienung

Im Katalog wählen Sie eine Zielwand und klicken ein Modul. Im Grundriss ziehen Sie Schränke direkt; in 3D drehen Sie durch Ziehen und verschieben im Werkzeug **Verschieben**. Mausrad = Zoom, **Home** = einpassen, **G** = Grundriss, **3** = 3D, Pfeiltasten = ausgewählten Schrank um 100 mm verschieben, **Entf** = entfernen, **Strg/⌘ Z** = rückgängig. Fensterknöpfe minimieren, maximieren und schließen nur das lokale Arbeitsfenster; Desktop und Startmenü öffnen es wieder.

Die Anwendung speichert ausschließlich unter `localStorage["luna.raum.v1"]`. Datei- und HTTPS-Adresse haben getrennte Speicher. Exportieren/importieren Sie JSON für einen Wechsel. Ist lokaler Speicher gesperrt oder voll, meldet die Oberfläche ungesicherte Daten; sichern Sie dann ausdrücklich die JSON-Datei. Importgrenzen: 2 MB, 200 Schränke, 40 Öffnungen und 100 Notizen. Unbekannte Typen, doppelte IDs und überlappende Öffnungen werden abgewiesen.

### Rechenmodell und Grenzen

Boden = Breite × Tiefe. Bruttowände = 2 × (Breite + Tiefe) × Höhe. Netto = Bruttowände minus rechteckige Tür-/Fensteröffnungen. Zusammenhängende Bodenmodule bilden Zeilen; Hochschränke tragen keine Arbeitsplatte, Geräte-Lücken schon. Arbeitsplatten erhalten 20 mm Zugabe nur an tatsächlich freien Enden; an der L-Ecke wird keine doppelte Endzugabe gerechnet. Sockel und Wandabschluss folgen nominellen Zeilenlängen. Wangen sind die freien Enden, nicht eine Material-/Beschlagbestellung.

**Berger-Prüfwerte:** Boden 15,12 m²; Bruttowand 40,56 m²; Öffnungen 3,57 m²; Nettowand 36,99 m²; 4 Unter-, 2 Ober- und 1 Hochschrank plus 1 Geräte-Lücke; Zeile 4 200 mm; Arbeitsplatte 3,60 lm; Sockel 4,20 lm; Eiche-Demobetrag 3 981,80 EUR. Geräte, Montage und Umsatzsteuer sind nicht enthalten. Dies ist kein Angebot. Die L-Szene hat 5,44 lm Arbeitsplatte einschließlich zweier freier Endzugaben.

Nur rechteckige Räume und vereinfachte Kästen: keine Aufmaß-Hardware, schiefen Wände, Installations-/Ergonomieprüfung, Beschläge, Türanschläge, Eckbeschläge, Fertigungsdetails, belastbaren Kalkulationen, IFC/BIM-, CNC- oder Bestelldaten. Die Türbereichsprüfung ist konservative Quaderprüfung, keine zertifizierte Öffnungs-/Sicherheitsberechnung. Prüfen Sie alle Maße und Mengen vor jeder echten Planung oder Bestellung unabhängig.

## English

LUNA RAUM is an **unofficial 3D measure-up and kitchen discussion demo**, browser-only and local-first, with an EDV Hausleitner / Luna theme. It is **not BIM, not Roomle, not Vectorworks, not licensed WAWI and not a production kitchen planner**. The complete runtime is the single `Luna-Raum.html` file: inline HTML/CSS/JavaScript/WGSL and vector icons, no runtime packages, CDN, external fonts, network calls or embedded remote apps.

A native WebGPU pipeline renders room wall openings and warm-oak or white cabinet boxes. A Canvas2D top-plan fallback remains functional without WebGPU. Twelve catalog modules, wall snapping, three-dimensional AABB conflicts, adjustable rectangular room dimensions/openings, orbit/plan/four elevations, three example scenes, local notes, undo/redo, validated JSON project transfer and a live quantity/illustrative-price CSV are implemented. Quantities and unit-price assumptions are exposed; this is not a fabrication bill of materials or a commercial quotation.

### Run and deploy

Open `Luna-Raum.html` directly in a compatible browser, or serve this directory with any static HTTP server on localhost. For example:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
# http://127.0.0.1:8765/Luna-Raum.html
```

The public Pages root is deployed from **`gh-pages:/`**, where `index.html` is a **byte-identical, renamed deployment copy** of `main:Luna-Raum.html`. It is not a second implementation, wrapper or iframe. Main keeps exactly one runtime HTML file. README, LICENSE, tests and QA evidence are development/documentation assets, not runtime dependencies.

### Verification

`tests/qa.py` uses Python Playwright **for tests only**. It performs assertions and captures real browser screens at 1600 × 1000, plus responsive overflow checks at 1440 × 900, 834 × 1112 and 390 × 844. No npm command is required. With Python Playwright and an existing Chrome binary:

```sh
python3 tests/qa.py --browser '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' --url "file://$PWD/Luna-Raum.html" --out qa
python3 tests/qa.py --browser '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' --url https://martin-hausleitner.github.io/Luna-Raum/ --out qa/live
```

The test report records the actual URL, browser, platform, adapter, first-view time, runtime errors, screenshot SHA-256 values, export files and every assertion. `qa/orbit-performance.json` records a 180-frame real rendered orbit, not a hard-coded FPS badge. Boot is the first interactive rendered view; WebGPU initializes asynchronously while the usable plan is already shown. Performance measurements apply to the tested browser/hardware, not every machine. The test harness enables WebGPU explicitly; the product does not alter browser settings or bypass adapter availability.

Required captures: `qa/01-desktop.png`, `02-room-3d.png`, `03-plan.png`, `04-elevation.png`, `05-aufmass.png`, `06-catalog.png`, `07-empty-room.png`, `08-settings.png`. Additional evidence includes `09-canvas-fallback.png`, `10-mobile.png`, exported CSV/JSON, local and live reports.

## Reference projects, provenance and MIT credits

The eleven supplied repositories were actually cloned and inspected during the build. This is a **bounded in-process implementation of the requested room/kitchen subset**, not eleven complete embedded products. Matrix/vector projection routines are adapted from **StratumBIM `src/core/math.js`** under MIT; their notice is retained inside the runtime HTML and LICENSE. Other repositories inform the shell/workflow/drawing/review/notes/list design; their complete application implementations and servers are **not** included. No Aster branding is displayed in the product.

| Reference | Role | Inspected commit |
|---|---|---|
| [Aster](https://github.com/wieslawsoltes/Aster) · [demo](https://wieslawsoltes.github.io/Aster/) | Desktop/window-shell reference | `a7cca00c03837f8f94e2f6b1cccc2f82830e32fc` |
| [StratumBIM](https://github.com/wieslawsoltes/StratumBIM) · [demo](https://wieslawsoltes.github.io/StratumBIM/) | Room/openings, adapted matrix/vector math | `675178103f2d35b6fa5d131543c9433a8d6013d8` |
| [ConvergeStudio](https://github.com/wieslawsoltes/ConvergeStudio) · [demo](https://wieslawsoltes.github.io/ConvergeStudio/) | Coordination/conflict workflow | `473ba24141efe067c92d6756757a3a9fa2c582c7` |
| [PlanforgeReview](https://github.com/wieslawsoltes/PlanforgeReview) · [demo](https://wieslawsoltes.github.io/PlanforgeReview/) | Quantity takeoff workflow | `f6b4978c65ef8a8f3ff35687d154fcc40687101f` |
| [AureonStudio](https://github.com/wieslawsoltes/AureonStudio) · [demo](https://wieslawsoltes.github.io/AureonStudio/) | 3D viewport reference | `b7a4d48e5cfa2253c4ad1cd388e8ff63ac0532b3` |
| [Formalyth](https://github.com/wieslawsoltes/Formalyth) · [demo](https://wieslawsoltes.github.io/Formalyth/) | Workbench reference | `14f32d9fa468a158cafc60707d6f3593220576b8` |
| [Draftline](https://github.com/wieslawsoltes/Draftline) · [demo](https://wieslawsoltes.github.io/Draftline/) | Dimensioning reference | `cdb4f81a832b89bbb5f278a8c08adccf0cb61dc0` |
| [KestrelCAD](https://github.com/wieslawsoltes/KestrelCAD) · [demo](https://wieslawsoltes.github.io/KestrelCAD/) | Plan/elevation/undo workflow | `7a1e84c67fd24410c22f0d1a45b2e54120b32d0e` |
| [Orivane](https://github.com/wieslawsoltes/Orivane) · [demo](https://wieslawsoltes.github.io/Orivane/) | Local note-board reference | `af71000f3b44aab5bc7638b21cfee3e1733df233` |
| [VeyraWorkspace](https://github.com/wieslawsoltes/VeyraWorkspace) · [demo](https://wieslawsoltes.github.io/VeyraWorkspace/) | Conversation-workspace reference only; no server | `328dbc75cb754ab809ece30c4c79913619245267` |
| [Gridline](https://github.com/wieslawsoltes/Gridline) · [demo](https://wieslawsoltes.github.io/Gridline/) | Tabular schedule reference | `dab377510f5e3600b228e0fb1baba2e131e0ec47` |

MIT License. Copyright © 2026 LUNA RAUM contributors. Adapted math: copyright © 2026 Stratum BIM contributors. No endorsement by the reference-project authors or any named commercial vendor is implied.
