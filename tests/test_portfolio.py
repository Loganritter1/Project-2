"""Regression tests for the portfolio decision engine."""

from copy import deepcopy
from pathlib import Path
import sys
import unittest

SOURCE_DIR = Path(__file__).resolve().parents[1] / "lab13 files"
sys.path.insert(0, str(SOURCE_DIR))

from portfolio import (  # noqa: E402
    CORRELATIONS,
    SLEEVES,
    estimate_from_prices,
    expected_return,
    lowest_risk_mix,
    reserve_eligible_weight,
    validate_correlations,
)


class PortfolioEngineTests(unittest.TestCase):
    def test_equal_grid_weights_sum_to_one(self):
        weights = lowest_risk_mix(SLEEVES, CORRELATIONS, 0.065, 0.03)
        self.assertAlmostEqual(sum(weights.values()), 1.0)
        self.assertTrue(all(weight >= 0 for weight in weights.values()))

    def test_training_answer_meets_objective_and_reserve(self):
        weights = lowest_risk_mix(SLEEVES, CORRELATIONS, 0.065, 0.03)
        self.assertGreaterEqual(expected_return(weights, SLEEVES), 0.065)
        self.assertGreaterEqual(reserve_eligible_weight(weights, SLEEVES), 0.03)

    def test_invalid_asymmetric_correlation_is_rejected(self):
        invalid = deepcopy(CORRELATIONS)
        invalid["Treasury bills"]["Global equity index fund"] = 0.40
        with self.assertRaises(ValueError):
            validate_correlations(invalid, SLEEVES)

    def test_full_history_price_data_reproduces_base_mix(self):
        path = SOURCE_DIR / "prices.csv"
        sleeves, correlations = estimate_from_prices(str(path))
        sleeves["SGOV"]["reserve_eligible"] = True
        sleeves["VGIT"]["reserve_eligible"] = True
        weights = lowest_risk_mix(sleeves, correlations, 0.065, 0.03)
        self.assertAlmostEqual(weights["SGOV"], 0.60)
        self.assertAlmostEqual(weights["VGIT"], 0.00)
        self.assertAlmostEqual(weights["VCIT"], 0.00)
        self.assertAlmostEqual(weights["ACWI"], 0.40)

    def test_higher_reserve_constraint_stops_process(self):
        sleeves, correlations = estimate_from_prices(str(SOURCE_DIR / "prices.csv"))
        sleeves["SGOV"]["reserve_eligible"] = True
        sleeves["VGIT"]["reserve_eligible"] = True
        self.assertIsNone(lowest_risk_mix(sleeves, correlations, 0.065, 0.70))

    def test_lowered_acwi_return_requires_more_acwi(self):
        sleeves, correlations = estimate_from_prices(str(SOURCE_DIR / "prices.csv"))
        sleeves["SGOV"]["reserve_eligible"] = True
        sleeves["VGIT"]["reserve_eligible"] = True
        before = lowest_risk_mix(sleeves, correlations, 0.065, 0.03)
        changed = deepcopy(sleeves)
        changed["ACWI"]["return"] = 0.08
        after = lowest_risk_mix(changed, correlations, 0.065, 0.03)
        self.assertGreater(after["ACWI"], before["ACWI"])


if __name__ == "__main__":
    unittest.main()
