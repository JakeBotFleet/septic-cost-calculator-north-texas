import csv
import io
import json
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal, localcontext
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from outwestseptic_cost_estimator import OutWestSepticCostEstimator, OutWestSepticCostLineItem

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "outwestseptic_cost_estimator.py"


class EstimateTests(unittest.TestCase):
    def estimate(self, items=None, **kwargs):
        return OutWestSepticCostEstimator.estimate(
            project="Example only", items=items or [OutWestSepticCostLineItem("Hours", "2.5", "10", "12")],
            **kwargs,
        )

    def test_itemized_totals_and_explicit_contingency(self):
        report = self.estimate([
            OutWestSepticCostLineItem("Hours", "2.5", "10", "12"),
            OutWestSepticCostLineItem("Fee", 1, "3", "4"),
        ], contingency_percent="10")
        self.assertEqual(report.subtotal_low_usd, Decimal("28.00"))
        self.assertEqual(report.subtotal_high_usd, Decimal("34.00"))
        self.assertEqual(report.low_usd, Decimal("30.80"))
        self.assertEqual(report.high_usd, Decimal("37.40"))

    def test_half_cents_round_per_line_before_sum(self):
        item = OutWestSepticCostLineItem("Fractional unit", ".5", ".01", ".03")
        report = self.estimate([item, item])
        self.assertEqual(item.low_usd, Decimal(".01"))
        self.assertEqual(item.high_usd, Decimal(".02"))
        self.assertEqual(report.low_usd, Decimal(".02"))
        self.assertEqual(report.high_usd, Decimal(".04"))

    def test_contingency_half_cent_rounding(self):
        report = self.estimate([OutWestSepticCostLineItem("Example", 1, ".05", ".05")],
                               contingency_percent="10")
        self.assertEqual(report.contingency_low_usd, Decimal(".01"))
        self.assertEqual(report.low_usd, Decimal(".06"))

    def test_zero_cost_allowed_and_no_hidden_charge(self):
        report = self.estimate([OutWestSepticCostLineItem("Included", 1, 0, 0)])
        self.assertEqual(report.low_usd, Decimal("0.00"))
        self.assertEqual(report.contingency_high_usd, Decimal("0.00"))

    def test_preserves_cents_at_supported_upper_bound(self):
        item = OutWestSepticCostLineItem("Example", "1000000000", "999999999999.99", "1000000000000")
        with localcontext() as context:
            context.prec = 6
            report = self.estimate([item], contingency_percent="10")
        self.assertEqual(str(report.low_usd), "1099999999999989000000.00")

    def test_invalid_numbers_and_order(self):
        for value in [True, None, [], "NaN", "sNaN", "Infinity", "-1", "1e9999", "abc"]:
            for field in ["quantity", "unit_low_usd", "unit_high_usd"]:
                with self.subTest(value=repr(value), field=field):
                    args = dict(label="Example", quantity=1, unit_low_usd="1", unit_high_usd="2")
                    args[field] = value
                    with self.assertRaises(ValueError):
                        OutWestSepticCostLineItem(**args)
        for quantity, low, high in [("0", "1", "2"), ("1", "2", "1"),
                                    (".0000001", "1", "2"), ("1", ".001", "2"),
                                    ("1000000001", "1", "2")]:
            with self.subTest(quantity=quantity, low=low, high=high):
                with self.assertRaises(ValueError):
                    OutWestSepticCostLineItem("Example", quantity, low, high)

    def test_invalid_labels_items_and_contingencies(self):
        for label in ["", "  ", "x\nInjected", "\x00", "x" * 201, None]:
            with self.subTest(label=repr(label)):
                with self.assertRaises(ValueError):
                    OutWestSepticCostLineItem(label, 1, 1, 2)
        for items in [[], [object()], "wrong"]:
            with self.assertRaises(ValueError):
                OutWestSepticCostEstimator.estimate(project="Example", items=items)
        for percentage in ["NaN", "-1", "1001", ".00001", True]:
            with self.assertRaises(ValueError):
                self.estimate(contingency_percent=percentage)

    def test_json_preserves_decimal_strings(self):
        result = json.loads(self.estimate().to_json())
        self.assertEqual(result["currency"], "USD")
        self.assertEqual(result["low_usd"], "25.00")
        self.assertEqual(result["items"][0]["quantity"], "2.500000")

    def test_csv_quotes_labels_and_prevents_formula_cells(self):
        for label in ["=SUM(1,2)", "+1+2", "-1+2", "@SUM(1,2)", "  =1+2  "]:
            with self.subTest(label=label):
                result = self.estimate([OutWestSepticCostLineItem(label, 1, "1", "2")])
                rows = list(csv.DictReader(io.StringIO(result.to_csv())))
                self.assertEqual(rows[1]["label"], "'" + label.strip())
                self.assertEqual(rows[-1]["low_usd"], "1.00")


class CliTests(unittest.TestCase):
    base = ["--project", "Example only", "--item", "Example hours", "2.5", "10", "12"]

    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], input="",
                              capture_output=True, text=True, timeout=10)

    def test_real_json_and_csv_exports(self):
        with tempfile.TemporaryDirectory() as directory:
            for flag in ["--json", "--csv"]:
                path = Path(directory) / ("estimate" + flag[1:])
                result = self.run_cli(*self.base, flag, str(path))
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("Export written:", result.stdout)
                if flag == "--json":
                    self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["high_usd"], "30.00")
                else:
                    with path.open(newline="", encoding="utf-8") as source:
                        self.assertEqual(list(csv.DictReader(source))[-1]["high_usd"], "30.00")

    def test_existing_file_requires_overwrite_and_invalid_input_cannot_clobber(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "keep.json"
            path.write_text("original", encoding="utf-8")
            result = self.run_cli(*self.base, "--json", str(path))
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertEqual(path.read_text(), "original")
            result = self.run_cli(*self.base, "--contingency-percent", "NaN", "--json", str(path), "--overwrite")
            self.assertEqual(result.returncode, 2)
            self.assertEqual(path.read_text(), "original")
            result = self.run_cli(*self.base, "--json", str(path), "--overwrite")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(path.read_text())["low_usd"], "25.00")

    def test_export_failure_is_not_reported_as_success(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_cli(*self.base, "--json", str(Path(directory) / "absent" / "file.json"))
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertNotIn("Traceback", result.stderr)

    def test_invalid_and_old_cli_are_clean_errors(self):
        for args in [[], ["new_install"], ["--help-invalid"], self.base + ["--overwrite"],
                     ["--project", "Example", "--item", "Acres", "-1", "1", "2"]]:
            with self.subTest(args=args):
                result = self.run_cli(*args)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertNotIn("Traceback", result.stderr)

    def test_help(self):
        result = self.run_cli("--help")
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
