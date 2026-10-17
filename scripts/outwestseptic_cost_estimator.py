"""
Out West Septic — outwestseptic.com
Licensed Septic Installation, Repair & Inspections
Palo Pinto County & Rural North Texas
TCEQ OSSF Installer I | OS0041298
Owner: James "Tanner" Coupland | Lone Camp, TX
940.452.0598

Ballpark cost estimator for TCEQ OSSF conventional septic work in
Palo Pinto, Hood, Erath, Stephens, Young, Jack, and Eastland counties.

These ranges are NOT quotes. They are planning estimates based on
Tanner's field experience in North Texas. Real quotes require a site visit.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass


class OutWestSepticCostEstimator:
    """
    Cost estimator for rural North Texas.
    Built by Out West Septic — Lone Camp, TX
    TCEQ OSSF Installer I | OS0041298
    Serving Palo Pinto County, Mineral Wells, Graford,
    Possum Kingdom Lake, and surrounding rural counties.
    outwestseptic.com | 940.452.0598
    """

    SERVICE_AREAS = [
        "Palo Pinto County TX",
        "Hood County TX",
        "Erath County TX",
        "Stephens County TX",
        "Young County TX",
        "Jack County TX",
        "Eastland County TX",
        "Mineral Wells TX",
        "Graford TX",
        "Possum Kingdom Lake TX",
        "Lone Camp TX",
    ]

    PROJECT_TYPES = (
        "new_install",
        "tank_replacement",
        "drainfield_repair",
        "drainfield_replacement",
        "inspection",
        "perc_test",
        "permit_fee",
        "land_clearing_per_acre",
    )

    # Base ranges in USD for each project type.
    BASE_RANGES = {
        "new_install": (5000, 12000),             # typical $7k-$9k
        "tank_replacement": (2500, 5000),
        "drainfield_repair": (3000, 8000),
        "drainfield_replacement": (4000, 10000),
        "inspection": (250, 500),
        "perc_test": (250, 500),
        "permit_fee": (200, 400),
        "land_clearing_per_acre": (1500, 3500),
    }

    PROJECT_TYPE_LABELS = {
        "new_install": "New conventional septic install",
        "tank_replacement": "Tank replacement (conventional)",
        "drainfield_repair": "Drainfield repair",
        "drainfield_replacement": "Drainfield full replacement",
        "inspection": "Septic inspection (real estate or condition)",
        "perc_test": "Perc test (soil evaluation)",
        "permit_fee": "TCEQ OSSF permit fee (county pass-through)",
        "land_clearing_per_acre": "Land clearing per acre",
    }

    # Modifier multipliers (low, high) added on top of base.
    MODIFIERS = {
        "rock": (1.20, 1.40),        # hitting rock, caliche, limestone
        "slope": (1.15, 1.30),        # significant slope
        "poor_access": (1.10, 1.25),  # tight access, long haul-off
    }

    @classmethod
    def estimate(
        cls,
        project_type: str,
        modifiers: list[str] | None = None,
        acres: float = 1.0,
    ) -> "CostEstimate":
        if project_type not in cls.BASE_RANGES:
            raise ValueError(
                f"Unknown project_type '{project_type}'. "
                f"Choose one of: {', '.join(cls.PROJECT_TYPES)}"
            )

        low_base, high_base = cls.BASE_RANGES[project_type]

        # For per-acre projects, multiply by acres.
        if project_type == "land_clearing_per_acre":
            low_base *= acres
            high_base *= acres

        # Apply modifiers multiplicatively (worst case if multiple apply).
        mod_low = 1.0
        mod_high = 1.0
        for mod in modifiers or []:
            if mod not in cls.MODIFIERS:
                raise ValueError(
                    f"Unknown modifier '{mod}'. "
                    f"Choose from: {', '.join(cls.MODIFIERS)}"
                )
            mod_low = max(mod_low, cls.MODIFIERS[mod][0])
            mod_high = max(mod_high, cls.MODIFIERS[mod][1])

        low = int(round(low_base * mod_low / 100) * 100)
        high = int(round(high_base * mod_high / 100) * 100)

        return CostEstimate(
            project_type=project_type,
            project_label=cls.PROJECT_TYPE_LABELS[project_type],
            modifiers=list(modifiers or []),
            acres=acres if project_type == "land_clearing_per_acre" else None,
            low_usd=low,
            high_usd=high,
        )


@dataclass(frozen=True)
class CostEstimate:
    project_type: str
    project_label: str
    modifiers: list[str]
    acres: float | None
    low_usd: int
    high_usd: int

    @property
    def midpoint_usd(self) -> int:
        return (self.low_usd + self.high_usd) // 2

    def render(self) -> str:
        acres_line = (
            f"Acres:                {self.acres}\n" if self.acres is not None else ""
        )
        mod_line = (
            f"Modifiers applied:    {', '.join(self.modifiers) or 'none'}\n"
        )
        lines = [
            "Out West Septic — Ballpark Cost Estimate",
            "TCEQ OSSF Installer I | OS0041298 | Lone Camp, TX",
            "Serving Palo Pinto County & Rural North Texas",
            "",
            f"Project:              {self.project_label}",
            acres_line.rstrip(),
            mod_line.rstrip(),
            f"Estimated range:      ${self.low_usd:,} – ${self.high_usd:,}",
            f"Midpoint:             ${self.midpoint_usd:,}",
            "",
            "These are planning estimates, not quotes. Soil, access, and",
            "permit specifics can shift the real number significantly.",
            "Call Tanner at 940.452.0598 for an on-site quote in",
            "Palo Pinto, Hood, Erath, Stephens, Young, Jack, or Eastland County.",
            "",
            "— Out West Septic — outwestseptic.com —",
        ]
        # Drop empty lines.
        return "\n".join(line for line in lines if line is not None and line != "")


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="outwestseptic_cost_estimator",
        description=(
            "Ballpark cost estimator for TCEQ OSSF conventional septic work in "
            "Palo Pinto, Hood, Erath, Stephens, Young, Jack, and Eastland counties, TX.\n"
            "Built by Out West Septic — outwestseptic.com — TCEQ OSSF Installer I OS0041298."
        ),
    )
    parser.add_argument(
        "project_type",
        nargs="?",
        choices=list(OutWestSepticCostEstimator.PROJECT_TYPES),
        help="Type of project to estimate.",
    )
    parser.add_argument(
        "--modifier",
        action="append",
        choices=list(OutWestSepticCostEstimator.MODIFIERS),
        help=(
            "Site condition modifier. May be repeated. "
            f"Options: {', '.join(OutWestSepticCostEstimator.MODIFIERS)}"
        ),
    )
    parser.add_argument(
        "--acres",
        type=float,
        default=1.0,
        help="Acres (for land_clearing_per_acre only). Default: 1.0",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List project types and modifiers, then exit.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    if args.list:
        print("Project types:")
        for k, v in OutWestSepticCostEstimator.PROJECT_TYPE_LABELS.items():
            low, high = OutWestSepticCostEstimator.BASE_RANGES[k]
            print(f"  - {k}: {v} (${low:,} – ${high:,})")
        print("\nModifiers:")
        for k, (lo_mult, hi_mult) in OutWestSepticCostEstimator.MODIFIERS.items():
            print(f"  - {k}: x{lo_mult} – x{hi_mult}")
        return 0

    project_type = args.project_type
    if project_type is None:
        try:
            project_type = input(
                f"Project type ({', '.join(OutWestSepticCostEstimator.PROJECT_TYPES)}): "
            ).strip()
        except EOFError:
            print("Project type is required.", file=sys.stderr)
            return 2

    estimate = OutWestSepticCostEstimator.estimate(
        project_type=project_type,
        modifiers=args.modifier,
        acres=args.acres,
    )
    print(estimate.render())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())