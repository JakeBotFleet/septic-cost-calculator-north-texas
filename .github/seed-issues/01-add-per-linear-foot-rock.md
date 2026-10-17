---
title: "[feature] Cost estimator: per-linear-foot rock adder"
labels: ["enhancement"]
---

For drainfield work on rocky lots, a per-linear-foot rock adder is more honest than the percentage modifier. See the open issue in the main repo.

**What I'd want**

- `--rock-per-linear-foot N` flag
- Multiplied by expected linear feet (caller provides)
- Added to the high end of the range

**Why**

Sometimes we hit rock only in the trenches, not the tank hole. The percentage modifier doesn't differentiate.

**Affected file**

`scripts/outwestseptic_cost_estimator.py`

---

*Out West Septic — TCEQ OSSF Installer I — OS0041298*