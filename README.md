# LUNA RAUM 3 · Atelier

**Aufmaß · Küche · 3D-Gespräch — EDV Hausleitner.** Unofficial, browser-only kitchen measure-up and discussion demo. Not BIM, not Roomle, not Vectorworks, not licensed WAWI, and not a production kitchen planner. MIT. One self-contained `Luna-Raum.html`: no runtime npm, CDN, external fonts, framework, iframe, account or application server.

[Open the application](https://martin-hausleitner.github.io/Luna-Raum/) · [All 82 additions](FEATURES.md) · [Source](https://github.com/Martin-Hausleitner/Luna-Raum)

## Deutsch · Mehr Detail, mehr Planungswerkzeuge

Version 3 erweitert die ursprünglich ausgelieferte Version 1 um **82 Funktionen und Detailfähigkeiten**. Die zuvor nicht fertig ausgelieferte Detailversion 2 ist darin enthalten. Es sind nicht 82 zusätzliche Funktionen gegenüber einem bereits veröffentlichten Version-2-Produkt. Das vollständige nummerierte Verzeichnis steht in `FEATURES.md` und direkt in der Anwendung unter **Hilfe · Funktionen**.

| Bereich | Jetzt vorhanden |
|---|---|
| Küche und Katalog | 30 Module: ursprüngliche Standards plus Auszüge, Kochfeld-, Spülen-, Backofen-, Kühlschrank-, Vorrats-, Vitrinen-, Regal- und Abzugsmodule. Volltextsuche, Gerätefilter, Platzieren per Klick oder Ziehen in den Grundriss. |
| Korpusse und Innenleben | Maße und Montagehöhe je Möbel, eigenes Material, Frontbild, Griffe, Anschlag, Böden und Auszüge. Sichtbare Einzelplatten, aufklappbare Türen, herausgezogene Schubladen, Rahmen- und Rillenfronten. |
| Material und Licht | Eiche, Weiß, Salbei, Graphit, Nussbaum, vier Griff- und vier Plattenvarianten, variable Plattenstärke und Überstände, drei Bodenoberflächen, Tageslichtregler, Unterbauleuchten, Schlagschatten und umschaltbare Detailstufe. |
| Raum und Aufmaß | Insel anlegen, bestücken, verschieben und drehen; fünf Szenen; frei gesetzte Messlinien; 10/50/100-mm-Raster; bearbeitbare Anschlusspositionen für Wasser, Abfluss, Strom und Licht. |
| Varianten und Prüfung | Sechs lokale Entwurfsstände mit Preisvergleich, Wiederherstellung und Export; AABB-Überschneidungen, grobe Abstands- und Installationshinweise; Hinweise als Gesprächsnotiz. |
| Kamera und Gespräch | Bis 600 % Zoom, Auswahlfokus, seitliches Verschieben, Parallel- oder echte Perspektivprojektion, automatischer Orbit, Präsentationsmodus, acht lokale Blickpunkte, drei abgestimmte Stilpakete. |
| Listen und Übergabe | Synchrones Aufmaß, schematische Bauteilvorschau, CSV für Mengen/Bauteile/Anschlüsse, bemaßter SVG-Grundriss, PNG der echten Ansicht, Projekt-JSON und Gesprächsblatt als Text. |

### Direkt ausprobieren

Öffnen Sie **Berger Atelier · mit Insel** im Projektwähler. Ein vorhandenes lokales Projekt wird nicht beim Start überschrieben. Klicken Sie einen Inselschrank an: **F** fokussiert ihn, **O** öffnet die Front. Mit Mausrad und **Shift + Ziehen** können Sie Details vergrößern und die Kamera verschieben. **P** startet die Präsentation, **Esc** beendet sie. **Home** passt die Gesamtansicht ein; **Alt + Pfeiltasten** dreht die Kamera. **Blickpunkte** speichert Kamerapositionen lokal.

**Materialien** ändert einzelne Oberflächen; **Stilpakete** ändert mehrere Oberflächen gemeinsam und setzt individuelle Materialübersteuerungen zurück. Das bleibt rückgängig machbar. **Anschlüsse**, **Varianten**, **Planprüfung** und **Bauteile** sind eigenständige Arbeitsbereiche. **Messen** beginnt eine Zweipunktmessung im Grundriss.

### Daten und Sicherheit

Projekte bleiben unter `luna.raum.v1` (Schema-Revision 2), Varianten unter `luna.raum.variants.v2`, Kamerablickpunkte unter `luna.raum.views.v3`. HTTPS und lokal geöffnete Dateien haben getrennte Speicherbereiche. Projekt-JSON ist der Übertragungs- und Sicherungsweg; Kamerablickpunkte sind gerätebezogen und nicht Teil des Projekt-JSON. Bei gesperrtem Speicher meldet die Anwendung den fehlenden Speicherzugriff. Gesprächsnotizen sind lokal — **not Teams**, kein Server und keine Mehrbenutzer-Synchronisation.

## English · Engineering and verification

This extends the existing shared engine rather than replacing the original application. Native WebGPU renders the same parametric model used by placement bounds, quantities and exports. Canvas2D provides an honest top-plan fallback. The runtime has no external network dependencies. The extended code preserves the original Berger arithmetic as a regression fixture and validates imported data before changing the project.

The numbered feature register describes implemented additions, not a count of test assertions. Browser tests independently exercise model updates, invalid input, persistence, exports, the shell, mobile layout, camera behavior and rendered pixels. Screenshots are captured from the running application; they are not concept images.

**New-version GPU verification uses Google Chrome on a Linux CI runner with software WebGPU. This proves working shader/geometry/presentation paths, not 60-fps hardware performance. The original version-1 Apple-GPU benchmark is not a version-3 benchmark.** Browser boot measurements are recorded per run. Hardware speed and device compatibility must be measured on the target machine. See the included QA reports for exact observations, failures and skips.

Build from the checked repository source, without downloading a temporary CI artifact:

```sh
python3 tools/v3/build_all.py candidate
python3 -m http.server 8765 --bind 127.0.0.1 --directory candidate
# Open http://127.0.0.1:8765/Luna-Raum.html
```

Python/Playwright/Chrome are test tools only, never application runtime dependencies. The Actions workflow records the exact tested revision. `gh-pages:/index.html` is a byte-identical renamed copy of `main:Luna-Raum.html`, not a wrapper or second implementation.

## Demo, nicht Fertigungsfreigabe

Die Raumgrundform bleibt rechteckig; gegenüberliegende Wände sind gekoppelt. Geräte und Glas sind stilisierte Geometrie, keine Herstellerprodukte. Preise sind frei gewählte Demowerte ohne Geräte, Montage und Umsatzsteuer. Die Bauteilvorschau ist eine vereinfachte Modellzerlegung, kein geprüfter Zuschnitt: Beschläge, Nuten, Kanten, Toleranzen und Installationsanforderungen fehlen. Geöffnete Fronten sind sichtbar, ihre Bewegungsräume werden aber nicht als zertifizierte Kollisionsvolumen geprüft. Der Inselabstand-Hinweis ist eine Demoannahme, keine Norm. Keine IFC/BIM-, CNC-, Bestell- oder freigegebenen Fertigungsdaten. Maße, Anschlusslagen, Bewegungsräume und Mengen müssen vor Angebot, Bestellung oder Montage unabhängig geprüft werden.

## Credits

Windows/workspace reference: [Aster](https://github.com/wieslawsoltes/Aster), [live reference](https://wieslawsoltes.github.io/Aster/). Projection math is adapted from MIT-licensed [StratumBIM](https://github.com/wieslawsoltes/StratumBIM); its copyright/license notice is retained in the HTML. The original project's complete reference/provenance table is retained below when this document is assembled into the release README. No endorsement or complete embedding of those applications is claimed.
