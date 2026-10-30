# Build scripts

Run from the repo root. Order matters for the diagrams, because later scripts overwrite some files.

1. `python3 _build/diagrams_select_cutfill.py`, then `diagrams_elections_traffic.py`, `diagrams_traffic_animation.py`, `diagrams_cutfill_plan_solar_ped.py`, `diagrams_select_modes.py`, `diagrams_ic_ped_fine.py`, `diagrams_cutfill_combined.py`
2. `python3 _build/thin_lines.py images/fig-*.svg` (makes line weights fine; skips files already thinned)
3. `python3 _build/build.py` (writes index.html and every project page)

`archive.json` lists Wayback Machine snapshots for every external link.
