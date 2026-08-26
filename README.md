# V2X-assets

Public image assets for issue reports in `purcell-lab/V2X`.

`purcell-lab/V2X` is a private repository. GitHub routes every externally referenced
image through its **camo** proxy, which fetches the URL unauthenticated. For a private
repo that returns 404, so no chart embedded from `raw.githubusercontent.com` will ever
render in a private-repo issue, in any format. This repository exists solely to host
those images publicly so they render inline for everyone reading the issue thread.

Images only. No telemetry exports, no configuration, no credentials, no site identifiers.

## Contents

### `charts/issue-26/` — DCEV charging fault lockout

Sigenergy SigenStor DC EV charger stops completing its insulation-resistance test
from 22 August 2026. Alarm `5105_4`.

| File | Description |
|---|---|
| `issue-26-timeline` | EVDC power, vehicle DC-link voltage, EMS command mode, 21 to 26 Aug |
| `issue-26-voltage-collapse` | Vehicle DC-link voltage collapse. No contactor closure from 24 Aug |
| `issue-26-throughput` | Daily charge and discharge throughput against alarm entry counts |
| `issue-26-flap-burst` | 21 Aug 10:37 to 11:07 AEST Charging and Discharging reversal burst |
| `issue-26-vehicle-iso` | Vehicle isolation resistance against fault onsets, with vehicle-on-pile bands |

Each chart is provided as PNG for inline rendering and SVG for zooming or re-styling.

Full analysis, source data and discussion: `purcell-lab/V2X` issue #26 (private).
Public research workup: https://gist.github.com/purcell-lab/766a6ccb0ee54ee16121d03ed1ccf606

## Licence

CC BY 4.0. Attribution: Mark Purcell, purcell.id.au.
