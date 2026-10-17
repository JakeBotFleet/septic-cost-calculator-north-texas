# Texas Septic Cost Estimator

> **Ballpark cost estimator for TCEQ OSSF conventional septic work in rural North Texas.**
> Forked from the [texas-septic-toolkit](https://github.com/TexasSepticEnthusiast/texas-septic-toolkit).
> Built by [Out West Septic](https://outwestseptic.com) — Lone Camp, TX.
> **TCEQ OSSF Installer I | License OS0041298** — Owner: James "Tanner" Coupland — 940.452.0598

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![TCEQ OSSF](https://img.shields.io/badge/TCEQ-OSSF_Installer_I-007787)](https://www.tceq.texas.gov/permitting/ossf)

## What this fork is

A focused fork of the [texas-septic-toolkit](https://github.com/TexasSepticEnthusiast/texas-septic-toolkit), containing only the cost estimator. Use this if you want planning estimates for North Texas septic work without the rest of the toolkit.

## Quick start

```bash
git clone https://github.com/TexasSepticEnthusiast/texas-septic-cost-estimator.git
cd texas-septic-cost-estimator
python scripts/outwestseptic_cost_estimator.py new_install
```

The script outputs planning estimates for:

- New conventional install
- Tank replacement
- Drainfield repair
- Drainfield replacement
- Inspection
- Perc test
- Permit fee
- Land clearing per acre

## What the estimates are (and aren't)

**These are planning ranges**, not quotes. The script encodes Out West Septic's field experience in Palo Pinto County, Hood County, Erath County, Stephens County, Young County, Jack County, and Eastland County. Real quotes require a site visit.

The script does NOT:

- Subtract for permits already on file
- Add for unusual site access
- Account for homeowner association restrictions
- Apply financing or discount programs

For real quotes, call Tanner at 940.452.0598.

## Service area

Out West Septic installs in Palo Pinto, Hood, Erath, Stephens, Young, Jack, and Eastland counties. Mineral Wells, Graford, Possum Kingdom Lake.

## License

MIT — see [LICENSE](./LICENSE).

---

*Out West Septic — outwestseptic.com — 940.452.0598 — TCEQ OSSF Installer I OS0041298 — Lone Camp, TX*
*Serving Palo Pinto County, Mineral Wells, Graford, Possum Kingdom Lake, and rural North Texas.*