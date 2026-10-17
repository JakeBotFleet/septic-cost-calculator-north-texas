---
title: "feat(cost-estimator): add --pdf export"
labels: ["enhancement"]
---

Adds a `--pdf PATH` flag to `outwestseptic_cost_estimator.py`. The script exports a branded one-page PDF when the flag is set.

**Why**

When I'm running the cost estimator on-site and the customer asks for a paper copy, having the PDF ready saves me a step.

**Verified**

```bash
python scripts/outwestseptic_cost_estimator.py new_install --pdf estimate.pdf
```

---

*Out West Septic — TCEQ OSSF Installer I — OS0041298*